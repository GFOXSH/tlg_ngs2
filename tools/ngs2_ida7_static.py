# -*- coding: utf-8 -*-
# IDAPython 7.x / Python 2.7 compatible static NGS2 ABI analyser.
# Run from IDA: File -> Script file... (or Alt+F7).
# Output: JSON (full detail), Markdown (review report), CSV (call-site index).
#
# The script is heuristic by design. It does not execute the EBOOT and cannot
# recover runtime-generated pointers/values. It records confidence and raw bytes
# so that inferred layouts can be checked against the native NGS2 trace.

from __future__ import print_function

import os
import re
import json
import time
import struct
import traceback

import idaapi
import idautils
import idc

try:
    import ida_bytes
except Exception:
    ida_bytes = None
try:
    import ida_funcs
except Exception:
    ida_funcs = None
try:
    import ida_xref
except Exception:
    ida_xref = None
try:
    import ida_search
except Exception:
    ida_search = None
try:
    import ida_segment
except Exception:
    ida_segment = None

# ----------------------------- User configuration --------------------------

# Empty means: directory containing the input EBOOT. Set an absolute directory
# here if the EBOOT is read-only or you prefer a separate analysis folder.
OUTPUT_DIR = ""

MAX_BACKTRACE_INSNS = 72
MAX_REG_TRACE_DEPTH = 8
MAX_THUNK_DEPTH = 8
MAX_PARENT_DEPTH = 3
MAX_PARENT_FUNCS = 24
MAX_STATIC_PARAM_CHAIN = 16
MAX_PARAM_BYTES = 0x400
MAX_POINTEE_BYTES = 0x100
MAX_RENDER_BUFFERS = 8
MAX_CALLERS_PER_API = 2000

# PS4 x86-64 EBOOT convention is normally the System-V register convention.
# The first six integer/pointer arguments are RDI, RSI, RDX, RCX, R8, R9.
# We record XMM0..XMM7 too, but do not interpret them as NGS2 integer args.
ARG_REGS = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]
XMM_REGS = ["xmm0", "xmm1", "xmm2", "xmm3", "xmm4", "xmm5", "xmm6", "xmm7"]

NGS2_NIDS = {
    "-TOuuAQ-buE": "sceNgs2VoiceGetState",
    "0eFLVCfWVds": "sceNgs2RackQueryBufferSize",
    "MwmHz8pAdAo": "sceNgs2RackGetVoiceHandle",
    "U546k6orxQo": "sceNgs2RackCreateWithAllocator",
    "cLV4aiT9JpA": "sceNgs2RackCreate",
    "i0VnXM-C9fc": "sceNgs2SystemRender",
    "lCqD7oycmIM": "sceNgs2RackDestroy",
    "mPYgU4oYpuY": "sceNgs2SystemCreateWithAllocator",
    "u-WrYDaJA3k": "sceNgs2SystemDestroy",
    "uu94irFOGpA": "sceNgs2VoiceControl",
}

API_ARGS = {
    "sceNgs2SystemCreateWithAllocator": ["option", "allocator", "out_system"],
    "sceNgs2SystemDestroy": ["system_handle"],
    "sceNgs2SystemRender": ["system", "render_buffers", "num_buffers"],
    "sceNgs2RackQueryBufferSize": ["rack_id", "rack_option", "out_buffer_info"],
    "sceNgs2RackCreate": ["system", "rack_id", "rack_option", "context_buffer", "out_rack"],
    "sceNgs2RackCreateWithAllocator": ["system", "rack_id", "rack_option", "allocator", "out_rack"],
    "sceNgs2RackDestroy": ["rack_handle"],
    "sceNgs2RackGetVoiceHandle": ["rack", "voice_index", "out_voice"],
    "sceNgs2VoiceControl": ["voice", "parameter_chain"],
    "sceNgs2VoiceGetState": ["voice", "out_state", "state_size"],
}
ABI_NOTES = {
    "sceNgs2SystemDestroy": "The script labels the system handle only. The repository trace wrapper forwards three GPR slots generically; all six integer argument registers are therefore also preserved as raw snapshots, not assumed formal parameters.",
    "sceNgs2RackDestroy": "The script labels the rack handle only. The repository trace wrapper forwards three GPR slots generically; all six integer argument registers are therefore also preserved as raw snapshots, not assumed formal parameters.",
    "sceNgs2VoiceControl": "The current C++ ABI adapter declares (voice, params). Extra argument registers are still preserved in the raw ABI snapshot.",
}

RACK_TYPES = {
    0x1000: "SAMPLER",
    0x2000: "SUBMIXER",
    0x2001: "REVERB",
    0x3000: "MASTERING",
    0x4002: "CUSTOM_SUBMIXER",
}

PARAM_IDS = {
    0x00000001: "MATRIX_LEVELS",
    0x00000002: "PORT_VOLUME",
    0x00000003: "PORT_MATRIX",
    0x00000005: "PATCH",
    0x00000006: "KICK_EVENT",
    0x10000000: "SAMPLER_SETUP",
    0x10000001: "SAMPLER_ADD_WAVEFORM_BLOCKS",
    0x10000005: "SAMPLER_PITCH",
    0x10000006: "SAMPLER_ENVELOPE",
    0x10000008: "SAMPLER_USER_FX",
    0x10000009: "SAMPLER_PEAK_METER",
    0x1000000a: "SAMPLER_FILTER",
    0x20000000: "SUBMIXER_SETUP",
    0x20000002: "SUBMIXER_COMPRESSOR",
    0x20000004: "SUBMIXER_USER_FX",
    0x20000006: "SUBMIXER_FILTER",
    0x20010000: "REVERB_SETUP",
    0x20010001: "REVERB_I3DL2",
    0x30000000: "MASTERING_SETUP",
    0x30000002: "MASTERING_LFE_FILTER",
    0x30000003: "MASTERING_LIMITER",
    0x30000004: "MASTERING_GAIN",
    0x30000005: "MASTERING_OUTPUT",
    0x40020000: "CUSTOM_RACK_SETUP",
    0x40001c00: "CUSTOM_CHORUS_1C",
    0x40001d00: "CUSTOM_DELAY_1D",
}

# Import-name aliases used by a few IDA PS4 loader configurations.
API_NAME_RE = re.compile(r"(?:^|[^A-Za-z0-9_])(?:sce)?Ngs2|sceNgs2", re.I)

# ----------------------------- IDA compatibility ---------------------------

def _msg(text):
    try:
        idaapi.msg(str(text) + "\n")
    except Exception:
        try:
            print(text)
        except Exception:
            pass


def _get_func(ea):
    try:
        if ida_funcs:
            return ida_funcs.get_func(ea)
    except Exception:
        pass
    try:
        return idaapi.get_func(ea)
    except Exception:
        return None


def _func_start(f):
    return getattr(f, "start_ea", getattr(f, "startEA", 0)) if f else 0


def _func_end(f):
    return getattr(f, "end_ea", getattr(f, "endEA", 0)) if f else 0


def _name(ea):
    if ea is None:
        return ""
    try:
        n = idc.get_name(ea)
        if n:
            return str(n)
    except Exception:
        pass
    try:
        n = idc.Name(ea)
        if n:
            return str(n)
    except Exception:
        pass
    return ""


def _name_ea(name):
    try:
        return idc.get_name_ea_simple(name)
    except Exception:
        try:
            return idc.get_name_ea(idc.BADADDR, name)
        except Exception:
            return idaapi.BADADDR


def _mnem(ea):
    try:
        return str(idc.print_insn_mnem(ea)).lower()
    except Exception:
        try:
            return str(idc.GetMnem(ea)).lower()
        except Exception:
            return ""


def _op_text(ea, n):
    try:
        return str(idc.print_operand(ea, n)).strip()
    except Exception:
        try:
            return str(idc.GetOpnd(ea, n)).strip()
        except Exception:
            return ""


def _op_type(ea, n):
    try:
        return idc.get_operand_type(ea, n)
    except Exception:
        try:
            return idc.GetOpType(ea, n)
        except Exception:
            return -1


def _op_value(ea, n):
    try:
        return idc.get_operand_value(ea, n)
    except Exception:
        try:
            return idc.GetOperandValue(ea, n)
        except Exception:
            return 0


def _item_size(ea):
    try:
        return idc.get_item_size(ea)
    except Exception:
        try:
            return idc.ItemSize(ea)
        except Exception:
            return 1


def _is_badaddr(ea):
    try:
        return ea is None or ea == idaapi.BADADDR
    except Exception:
        return ea is None or ea == 0xffffffffffffffff


def _get_bytes(ea, size):
    if _is_badaddr(ea) or size <= 0:
        return None
    try:
        if ida_bytes:
            b = ida_bytes.get_bytes(ea, size)
            if b is not None:
                return b
    except Exception:
        pass
    try:
        return idc.get_bytes(ea, size)
    except Exception:
        try:
            return idc.GetManyBytes(ea, size)
        except Exception:
            return None


def _is_mapped(ea):
    try:
        return idaapi.getseg(ea) is not None
    except Exception:
        try:
            return idc.get_segm_name(ea) != ""
        except Exception:
            return False


def _read_u16(ea):
    b = _get_bytes(ea, 2)
    return struct.unpack("<H", b)[0] if b and len(b) >= 2 else None


def _read_s16(ea):
    b = _get_bytes(ea, 2)
    return struct.unpack("<h", b)[0] if b and len(b) >= 2 else None


def _read_u32(ea):
    b = _get_bytes(ea, 4)
    return struct.unpack("<I", b)[0] if b and len(b) >= 4 else None


def _read_s32(ea):
    b = _get_bytes(ea, 4)
    return struct.unpack("<i", b)[0] if b and len(b) >= 4 else None


def _read_u64(ea):
    b = _get_bytes(ea, 8)
    return struct.unpack("<Q", b)[0] if b and len(b) >= 8 else None


def _read_f32(ea):
    b = _get_bytes(ea, 4)
    return struct.unpack("<f", b)[0] if b and len(b) >= 4 else None


def _hex_bytes(b, limit=0x100):
    if b is None:
        return ""
    try:
        b = b[:limit]
        return " ".join(["%02x" % (ord(x) if not isinstance(x, int) else x) for x in b])
    except Exception:
        return ""


def _str_at(ea):
    if not _is_mapped(ea):
        return None
    try:
        flags = idc.get_str_type(ea)
        if flags is not None:
            s = idc.get_strlit_contents(ea, -1, flags)
            if s:
                return _to_text(s[:256])
    except Exception:
        pass
    try:
        s = idc.GetString(ea, -1, idc.ASCSTR_C)
        if s:
            return _to_text(s[:256])
    except Exception:
        pass
    b = _get_bytes(ea, 96)
    if b:
        try:
            if not isinstance(b, str):
                b = b.decode("latin1", "ignore")
            s = b.split("\x00", 1)[0]
            if len(s) >= 4 and all(31 < ord(c) < 127 for c in s):
                return s[:256]
        except Exception:
            pass
    return None


def _to_text(s):
    try:
        if isinstance(s, unicode):
            return s
    except Exception:
        pass
    try:
        return s.decode("utf-8", "replace")
    except Exception:
        try:
            return str(s)
        except Exception:
            return ""


def _address_info(value):
    info = {"value": value}
    if value is None:
        return info
    try:
        if _is_mapped(value):
            info["mapped"] = True
            n = _name(value)
            if n:
                info["name"] = n
            s = _str_at(value)
            if s:
                info["string"] = s
            try:
                info["segment"] = str(idc.get_segm_name(value))
            except Exception:
                pass
        else:
            info["mapped"] = False
    except Exception:
        pass
    return info


def _iter_func_heads(start, end):
    try:
        for ea in idautils.Heads(start, end):
            yield ea
        return
    except Exception:
        pass
    ea = start
    while ea != idaapi.BADADDR and ea < end:
        yield ea
        nxt = idc.next_head(ea, end)
        if nxt == idaapi.BADADDR or nxt <= ea:
            break
        ea = nxt


def _code_refs_to(ea):
    try:
        return list(idautils.CodeRefsTo(ea, 0))
    except Exception:
        return []


def _data_refs_to(ea):
    try:
        return list(idautils.DataRefsTo(ea))
    except Exception:
        return []


def _xref_list_to(ea):
    arr = []
    try:
        for x in idautils.XrefsTo(ea, 0):
            arr.append({"frm": x.frm, "to": x.to, "type": x.type, "iscode": bool(x.iscode)})
    except Exception:
        pass
    return arr

# ----------------------------- Operand / ABI analysis ----------------------

REG_ALIASES = {
    "rax":"rax", "eax":"rax", "ax":"rax", "al":"rax", "ah":"rax",
    "rbx":"rbx", "ebx":"rbx", "bx":"rbx", "bl":"rbx", "bh":"rbx",
    "rcx":"rcx", "ecx":"rcx", "cx":"rcx", "cl":"rcx", "ch":"rcx",
    "rdx":"rdx", "edx":"rdx", "dx":"rdx", "dl":"rdx", "dh":"rdx",
    "rsi":"rsi", "esi":"rsi", "si":"rsi", "sil":"rsi",
    "rdi":"rdi", "edi":"rdi", "di":"rdi", "dil":"rdi",
    "rbp":"rbp", "ebp":"rbp", "bp":"rbp", "bpl":"rbp",
    "rsp":"rsp", "esp":"rsp", "sp":"rsp", "spl":"rsp",
    "r8":"r8", "r8d":"r8", "r8w":"r8", "r8b":"r8",
    "r9":"r9", "r9d":"r9", "r9w":"r9", "r9b":"r9",
    "r10":"r10", "r10d":"r10", "r11":"r11", "r11d":"r11",
    "r12":"r12", "r12d":"r12", "r13":"r13", "r13d":"r13",
    "r14":"r14", "r14d":"r14", "r15":"r15", "r15d":"r15",
}


def _reg_from_operand(text):
    t = (text or "").strip().lower()
    t = t.replace("%", "")
    t = t.split(" ")[0].strip()
    t = t.replace("ptr", "").strip()
    if t in REG_ALIASES:
        return REG_ALIASES[t]
    if re.match(r"^xmm[0-7]$", t):
        return t
    if re.match(r"^ymm[0-7]$", t):
        return t
    return None


def _is_reg(text):
    return _reg_from_operand(text) is not None


def _parse_int_text(text):
    if not text:
        return None
    t = text.strip().lower().replace("h", "")
    t = t.replace("offset ", "").replace("near ptr ", "")
    try:
        if t.startswith("0x"):
            return int(t, 16)
        if re.match(r"^[0-9a-f]+h$", text.strip().lower()):
            return int(text.strip()[:-1], 16)
        if re.match(r"^-?\d+$", t):
            return int(t, 10)
    except Exception:
        pass
    return None


def _stack_operand_info(ea, n, text=None):
    if text is None:
        text = _op_text(ea, n)
    low = (text or "").lower()
    if "[" not in low or "]" not in low:
        return None
    base = None
    if re.search(r"\brbp\b", low):
        base = "rbp"
    elif re.search(r"\brsp\b", low):
        base = "rsp"
    if not base:
        return None
    value = _op_value(ea, n)
    # Displacement operands are commonly surfaced as unsigned 32-bit values.
    try:
        if value >= 0x80000000 and value <= 0xffffffff:
            value -= 0x100000000
    except Exception:
        pass
    return {"base": base, "displacement": value, "operand": text}


def _operand_expr(ea, n):
    typ = _op_type(ea, n)
    text = _op_text(ea, n)
    out = {"text": text, "type": typ}
    try:
        if typ == idaapi.o_imm:
            val = _op_value(ea, n)
            out["kind"] = "immediate"
            out["value"] = val
            if _is_mapped(val):
                out["target"] = _address_info(val)
            return out
    except Exception:
        pass
    r = _reg_from_operand(text)
    if r:
        out["kind"] = "register"
        out["register"] = r
        return out
    if "rip" in text.lower() or "eip" in text.lower():
        disp = _op_value(ea, n)
        target = ea + _item_size(ea) + disp
        # IDA versions differ on whether operand_value is displacement or EA.
        if _is_mapped(disp):
            target = disp
        out["kind"] = "rip_relative"
        out["value"] = target
        out["target"] = _address_info(target)
        return out
    if typ in (getattr(idaapi, "o_mem", -100), getattr(idaapi, "o_displ", -101),
               getattr(idaapi, "o_phrase", -102)):
        val = _op_value(ea, n)
        out["kind"] = "memory"
        out["value"] = val
        stack = _stack_operand_info(ea, n, text)
        if stack:
            out["stack"] = stack
        if _is_mapped(val):
            out["target"] = _address_info(val)
        return out
    iv = _parse_int_text(text)
    if iv is not None:
        out["kind"] = "parsed_integer"
        out["value"] = iv
    else:
        out["kind"] = "expression"
    return out


def _writes_register(ea, reg):
    m = _mnem(ea)
    if not m:
        return False
    dst = _reg_from_operand(_op_text(ea, 0))
    if dst != reg:
        return False
    # Do not treat comparisons, tests or jumps as destination writes.
    if m.startswith("cmp") or m.startswith("test") or m.startswith("j") or m in ("call", "jmp", "push"):
        return False
    return True


def _trace_register(reg, before_ea, depth=0):
    if depth > MAX_REG_TRACE_DEPTH:
        return {"kind": "unresolved", "reason": "register trace depth limit", "register": reg}
    f = _get_func(before_ea)
    if not f:
        return {"kind": "unresolved", "reason": "no function", "register": reg}
    start = _func_start(f)
    ea = idc.prev_head(before_ea, start)
    checked = 0
    while ea != idaapi.BADADDR and ea >= start and checked < MAX_BACKTRACE_INSNS:
        checked += 1
        m = _mnem(ea)
        # Crossing a call or control-flow edge makes a reaching definition less reliable.
        if m in ("call", "callq", "jmp", "ret", "retn", "retf") or (m.startswith("j") and m not in ("jmp",)):
            break
        if _writes_register(ea, reg):
            dst_txt = _op_text(ea, 0)
            src_txt = _op_text(ea, 1)
            expr = _operand_expr(ea, 1)
            base = {"kind": "definition", "ea": ea, "instruction": idc.generate_disasm_line(ea, 0),
                    "mnemonic": m, "destination": dst_txt, "source": expr}
            if m in ("mov", "movabs", "movq", "movzx", "movsx", "movsxd"):
                if expr.get("kind") == "register":
                    base["resolved_source"] = _trace_register(expr.get("register"), ea, depth + 1)
                elif expr.get("kind") == "immediate":
                    base["resolved_source"] = _address_info(expr.get("value"))
                return base
            if m == "lea":
                return base
            if m == "xor" and _reg_from_operand(src_txt) == reg:
                base["source"] = {"kind": "zero", "value": 0}
                return base
            if m in ("add", "sub", "and", "or", "shl", "shr"):
                base["effect"] = "arithmetic assignment; prior value also required"
                prev = _trace_register(reg, ea, depth + 1)
                base["previous_value"] = prev
                return base
            return base
        ea = idc.prev_head(ea, start)
    return {"kind": "unresolved", "reason": "no reaching definition in current basic block", "register": reg}


def _arg_snapshot(call_ea, api_name):
    names = API_ARGS.get(api_name, ["arg0", "arg1", "arg2", "arg3", "arg4", "arg5"])
    out = []
    for i, reg in enumerate(ARG_REGS):
        if i >= len(names):
            break
        out.append({"index": i, "name": names[i], "register": reg,
                    "definition": _trace_register(reg, call_ea, 0)})
    # Preserve every integer argument register even where the formal arity is
    # unclear or an adapter forwards an over-wide generic function pointer.
    abi_regs = []
    for reg in ARG_REGS:
        abi_regs.append({"register": reg, "definition": _trace_register(reg, call_ea, 0)})
    xmm = []
    for reg in XMM_REGS:
        v = _trace_register(reg, call_ea, 0)
        if v.get("kind") != "unresolved":
            xmm.append({"register": reg, "definition": v})
    return {"integer_args": out, "integer_register_snapshot": abi_regs, "xmm_args": xmm}

# ----------------------------- NGS2 structures -----------------------------

def _known_param_ids_in_func(f):
    found = []
    if not f:
        return found
    for ea in _iter_func_heads(_func_start(f), _func_end(f)):
        for opn in (0, 1):
            if _op_type(ea, opn) == getattr(idaapi, "o_imm", -999):
                v = _op_value(ea, opn) & 0xffffffff
                if v in PARAM_IDS:
                    found.append({"ea": ea, "id": v, "name": PARAM_IDS[v],
                                  "instruction": idc.generate_disasm_line(ea, 0)})
                if v in RACK_TYPES:
                    found.append({"ea": ea, "rack_id": v, "name": RACK_TYPES[v],
                                  "instruction": idc.generate_disasm_line(ea, 0)})
    # Keep duplicate constants at distinct EAs; merge repeated operand index per EA.
    uniq = {}
    for x in found:
        key = (x.get("ea"), x.get("id", x.get("rack_id")))
        uniq[key] = x
    return sorted(uniq.values(), key=lambda x: x.get("ea", 0))


def _read_ptr(ea):
    # PS4 EBOOT is 64-bit. Try qword first; 32-bit databases still get a fallback.
    v = _read_u64(ea)
    if v is None:
        v = _read_u32(ea)
    if v is not None and not _is_mapped(v):
        # IDB may store image-relative pointers. Do not silently rebase them;
        # retain the raw value and let the analyst inspect it.
        return v
    return v


def _read_float_array(ptr, count, cap=32):
    if ptr is None or not _is_mapped(ptr):
        return {"address": ptr, "readable": False}
    n = min(max(int(count), 0), cap)
    vals = []
    for i in range(n):
        v = _read_f32(ptr + i * 4)
        if v is None:
            break
        vals.append(v)
    return {"address": ptr, "readable": bool(vals), "count_reported": count,
            "values_read": vals, "truncated": count > n}


def _decode_param(ptr, index):
    b = _get_bytes(ptr, 8)
    if not b or len(b) < 8:
        return {"index": index, "address": ptr, "readable": False}
    size, nxt, pid = struct.unpack("<HhI", b[:8])
    p = {"index": index, "address": ptr, "size": size, "next": nxt,
         "id": pid, "name": PARAM_IDS.get(pid, "UNKNOWN_PARAM"),
         "raw_hex": _hex_bytes(_get_bytes(ptr, min(max(size, 8), MAX_PARAM_BYTES)), MAX_PARAM_BYTES)}
    if size < 8 or size > MAX_PARAM_BYTES:
        p["layout_warning"] = "Implausible parameter size; chain parsing stopped here"
        return p
    raw = _get_bytes(ptr, min(size, MAX_PARAM_BYTES))
    if raw is None or len(raw) < 8:
        p["readable"] = False
        return p

    def u32(off):
        return struct.unpack("<I", raw[off:off + 4])[0] if len(raw) >= off + 4 else None
    def f32(off):
        return struct.unpack("<f", raw[off:off + 4])[0] if len(raw) >= off + 4 else None
    def u64(off):
        return struct.unpack("<Q", raw[off:off + 8])[0] if len(raw) >= off + 8 else None

    if pid == 0x00000001 and size >= 24:
        matrix, count, values = u32(8), u32(12), u64(16)
        p["fields"] = {"matrix": matrix, "num_levels": count, "levels_ptr": values}
        p["pointed_data"] = _read_float_array(values, count, 64)
    elif pid == 0x00000002 and size >= 16:
        p["fields"] = {"port": u32(8), "level": f32(12)}
    elif pid == 0x00000003 and size >= 16:
        p["fields"] = {"port": u32(8), "matrix": u32(12)}
    elif pid == 0x00000005 and size >= 24:
        p["fields"] = {"port": u32(8), "dest_input": u32(12), "dest_handle": u64(16)}
    elif pid == 0x00000006 and size >= 12:
        p["fields"] = {"event": u32(8)}
    elif pid == 0x10000000 and size >= 36:
        p["fields"] = {"waveform_type": u32(8), "channels": u32(12), "sample_rate": u32(16),
                        "config_data": u32(20), "frame_offset": u32(24),
                        "frame_margin": u32(28), "flags": u32(32)}
    elif pid == 0x10000001 and size >= 32:
        data_ptr, blocks_count, flags, blocks_ptr = u64(8), u32(16), u32(20), u64(24)
        p["fields"] = {"data_ptr": data_ptr, "num_blocks": blocks_count,
                        "flags": flags, "blocks_ptr": blocks_ptr}
        blocks = []
        if blocks_ptr and _is_mapped(blocks_ptr):
            for i in range(min(blocks_count, 32)):
                off = blocks_ptr + i * 32
                bb = _get_bytes(off, 32)
                if not bb or len(bb) < 32:
                    break
                vals = struct.unpack("<6IQ", bb)
                blocks.append({"data_offset": vals[0], "data_size": vals[1],
                               "num_repeats": vals[2], "num_skip_samples": vals[3],
                               "num_samples": vals[4], "reserved": vals[5],
                               "user_data": vals[6]})
        p["pointed_blocks"] = blocks
    elif pid == 0x10000005 and size >= 12:
        p["fields"] = {"pitch_ratio": f32(8)}
    elif pid == 0x10000006 and size >= 24:
        count, release_count, points = u32(8), u32(12), u64(16)
        p["fields"] = {"num_points": count, "num_release_points": release_count,
                        "points_ptr": points,
                        "point_stride_note": "The native trace helper snapshots 16-byte items; notes also describe 12-byte points. Verify against the actual pointer data."}
        if points and _is_mapped(points):
            p["pointed_data_hex"] = _hex_bytes(_get_bytes(points, min(MAX_POINTEE_BYTES, max(16, count * 16))), MAX_POINTEE_BYTES)
    elif pid in (0x10000008, 0x20000004) and size >= 16:
        p["fields"] = {"user_fx_raw_words": [u32(x) for x in range(8, min(size - 3, 40), 4)]}
    elif pid in (0x1000000a, 0x20000006):
        p["fields"] = {"raw_words": [u32(x) for x in range(8, min(size - 3, 64), 4)],
                        "float_candidates": [f32(x) for x in range(8, min(size - 3, 64), 4)]}
    elif pid == 0x20000000 and size >= 12:
        p["fields"] = {"num_channels": u32(8)}
    elif pid == 0x20000002:
        p["fields"] = {"raw_words": [u32(x) for x in range(8, min(size - 3, 64), 4)],
                        "float_candidates": [f32(x) for x in range(8, min(size - 3, 64), 4)]}
    elif pid == 0x20010000 and size >= 16:
        p["fields"] = {"input_channels": u32(8), "output_channels": u32(12)}
    elif pid == 0x20010001:
        p["fields"] = {"raw_words": [u32(x) for x in range(8, min(size - 3, 128), 4)],
                        "float_candidates": [f32(x) for x in range(8, min(size - 3, 128), 4)]}
    elif pid == 0x30000000 and size >= 12:
        p["fields"] = {"num_channels": u32(8)}
    elif pid in (0x30000002, 0x30000003, 0x30000004, 0x30000005,
                 0x40020000, 0x40001c00, 0x40001d00):
        p["fields"] = {"raw_words": [u32(x) for x in range(8, min(size - 3, 160), 4)],
                        "float_candidates": [f32(x) for x in range(8, min(size - 3, 160), 4)]}
    else:
        p["fields"] = {"raw_words": [u32(x) for x in range(8, min(size - 3, 64), 4)]}
    return p


def _decode_param_chain(ptr):
    if ptr is None or not _is_mapped(ptr):
        return {"static_pointer": False, "address": ptr,
                "note": "Parameter chain pointer is not a statically mapped address; inspect runtime trace or producer function."}
    params = []
    cur = ptr
    seen = set()
    for i in range(MAX_STATIC_PARAM_CHAIN):
        if cur in seen:
            return {"static_pointer": True, "address": ptr, "params": params,
                    "warning": "Loop in next offsets"}
        seen.add(cur)
        p = _decode_param(cur, i)
        params.append(p)
        size = p.get("size", 0)
        nxt = p.get("next", 0)
        if not p.get("readable", True) or size < 8 or size > MAX_PARAM_BYTES:
            break
        if nxt == 0:
            break
        # next is a signed byte displacement in the parameter chain.
        if abs(nxt) > 0x10000:
            break
        cur = cur + nxt
    return {"static_pointer": True, "address": ptr, "params": params}


def _decode_struct_pointer(ptr, kind):
    if ptr is None or not _is_mapped(ptr):
        return {"static_pointer": False, "address": ptr,
                "note": "Pointer is not statically mapped; values may be stack/runtime generated."}
    if kind == "system_option":
        size = 0x40
    elif kind in ("rack_option", "rack_query_option"):
        size = 0x60
    elif kind == "render_buffers":
        return _decode_render_buffers(ptr, None)
    else:
        size = 0x60
    b = _get_bytes(ptr, size)
    if not b:
        return {"static_pointer": True, "address": ptr, "readable": False}
    words = []
    for off in range(0, min(len(b), size), 4):
        w = struct.unpack("<I", b[off:off + 4])[0]
        f = struct.unpack("<f", b[off:off + 4])[0]
        words.append({"offset": off, "u32": w, "f32": f})
    return {"static_pointer": True, "address": ptr, "kind": kind,
            "size": size, "raw_hex": _hex_bytes(b, size), "words": words}


def _decode_render_buffers(ptr, count):
    if ptr is None or not _is_mapped(ptr):
        return {"static_pointer": False, "address": ptr}
    if count is None or count <= 0 or count > MAX_RENDER_BUFFERS:
        count = MAX_RENDER_BUFFERS
    out = []
    for i in range(int(count)):
        at = ptr + i * 24
        buf = _read_u64(at)
        size = _read_u64(at + 8)
        waveform = _read_u32(at + 16)
        channels = _read_u32(at + 20)
        if buf is None or size is None or waveform is None or channels is None:
            break
        out.append({"index": i, "buffer": _address_info(buf), "size": size,
                    "waveform": waveform, "channels": channels})
    return {"static_pointer": True, "address": ptr, "entries": out,
            "layout_note": "Assumes the 24-byte RenderBuffer layout used by the repository's NGS2 trace helper."}

def _recover_stack_object(call_ea, pointer_definition, max_size=0x100):
    """Best-effort reconstruction of stores into a stack object passed by LEA.

    This does not emulate control flow. It collects nearby reaching-looking
    stores with the same RBP/RSP base and reports unknown bytes explicitly.
    """
    src = pointer_definition.get("source", {})
    stack = src.get("stack")
    if not stack or pointer_definition.get("mnemonic") != "lea":
        return None
    base = stack.get("base")
    obj_disp = stack.get("displacement")
    if base not in ("rbp", "rsp") or obj_disp is None:
        return None
    f = _get_func(call_ea)
    if not f:
        return None
    start = _func_start(f)
    ea = idc.prev_head(call_ea, start)
    window = []
    # Gather up to 220 prior instruction heads, stopping at a control-flow edge.
    while ea != idaapi.BADADDR and ea >= start and len(window) < 220:
        m = _mnem(ea)
        if m in ("call", "callq", "jmp", "ret", "retn", "retf") or (m.startswith("j") and m != "jmp"):
            break
        window.append(ea)
        ea = idc.prev_head(ea, start)
    window.reverse()
    data = [None] * max_size
    writes = []
    for we in window:
        dst = _stack_operand_info(we, 0, _op_text(we, 0))
        if not dst or dst.get("base") != base:
            continue
        off = dst.get("displacement") - obj_disp
        if off < 0 or off >= max_size:
            continue
        m = _mnem(we)
        src_type = _op_type(we, 1)
        src_text = _op_text(we, 1)
        width = 4
        lowdst = _op_text(we, 0).lower()
        if "qword ptr" in lowdst:
            width = 8
        elif "word ptr" in lowdst and "dword ptr" not in lowdst:
            width = 2
        elif "byte ptr" in lowdst:
            width = 1
        value = None
        value_source = None
        if src_type == getattr(idaapi, "o_imm", -999) and m in ("mov", "movabs"):
            value = _op_value(we, 1)
            value_source = "immediate"
        elif _reg_from_operand(src_text) and m in ("mov", "movabs", "movss", "movsd"):
            rr = _reg_from_operand(src_text)
            tr = _trace_register(rr, we, 0)
            ts = tr.get("source", {})
            if ts.get("kind") == "immediate":
                value = ts.get("value")
                value_source = "register_from_immediate"
            elif ts.get("kind") == "zero":
                value = 0
                value_source = "zeroed_register"
        if value is not None:
            try:
                mask = (1 << (width * 8)) - 1
                raw = struct.pack("<Q", int(value) & 0xffffffffffffffff)[:width]
                for bi in range(width):
                    if off + bi < max_size:
                        data[off + bi] = raw[bi]
            except Exception:
                pass
        writes.append({"ea": we, "offset": off, "width": width,
                       "instruction": idc.generate_disasm_line(we, 0),
                       "value": value, "value_source": value_source,
                       "source_operand": src_text})
    if not writes:
        return {"kind": "stack_object", "base": base, "displacement": obj_disp,
                "size_limit": max_size, "writes": [],
                "note": "LEA points to a stack object, but no nearby stores to the matching frame base were recovered."}
    raw_hex = []
    for b in data:
        if b is None:
            raw_hex.append("??")
        else:
            raw_hex.append("%02x" % (ord(b) if not isinstance(b, int) else b))
    return {"kind": "stack_object", "base": base, "displacement": obj_disp,
            "size_limit": max_size, "writes": writes,
            "raw_hex_with_gaps": " ".join(raw_hex),
            "reconstruction_note": "Only literal / trivially-resolved stores are materialized. Unknown bytes remain ??; control-flow and stack-pointer motion are not emulated."}


def _decode_call_arguments(api_name, args, call_ea=None):
    result = {}
    by_name = {}
    for a in args.get("integer_args", []):
        by_name[a.get("name")] = a.get("definition", {})
    def const_value(argname):
        d = by_name.get(argname, {})
        src = d.get("source", {})
        if src.get("kind") == "immediate":
            return src.get("value")
        if src.get("kind") in ("memory", "rip_relative"):
            location = src.get("value")
            if d.get("mnemonic") == "lea":
                return location
            # A MOV from a static global may load a pointer from the global slot.
            if location is not None and _is_mapped(location):
                pointed = _read_ptr(location)
                if pointed is not None and _is_mapped(pointed):
                    return pointed
            return location
        rs = d.get("resolved_source", {})
        if rs.get("source", {}).get("kind") == "immediate":
            return rs.get("source", {}).get("value")
        return None

    if api_name == "sceNgs2VoiceControl":
        p = const_value("parameter_chain")
        result["parameter_chain"] = _decode_param_chain(p)
        if not result["parameter_chain"].get("static_pointer"):
            d = by_name.get("parameter_chain", {})
            result["parameter_chain_stack_reconstruction"] = _recover_stack_object(
                call_ea, d, 0x100) if call_ea is not None else None
    elif api_name == "sceNgs2SystemCreateWithAllocator":
        p = const_value("option")
        result["system_option"] = _decode_struct_pointer(p, "system_option")
        if not result["system_option"].get("static_pointer"):
            d = by_name.get("option", {})
            result["system_option_stack_reconstruction"] = _recover_stack_object(call_ea, d, 0x60) if call_ea is not None else None
    elif api_name in ("sceNgs2RackCreate", "sceNgs2RackCreateWithAllocator"):
        p = const_value("rack_option")
        result["rack_option"] = _decode_struct_pointer(p, "rack_option")
        if not result["rack_option"].get("static_pointer"):
            d = by_name.get("rack_option", {})
            result["rack_option_stack_reconstruction"] = _recover_stack_object(call_ea, d, 0x80) if call_ea is not None else None
        rid = const_value("rack_id")
        if rid is not None:
            result["rack_type"] = {"value": rid, "name": RACK_TYPES.get(rid, "UNKNOWN_RACK")}
    elif api_name == "sceNgs2RackQueryBufferSize":
        p = const_value("rack_option")
        result["rack_option"] = _decode_struct_pointer(p, "rack_query_option")
        if not result["rack_option"].get("static_pointer"):
            d = by_name.get("rack_option", {})
            result["rack_option_stack_reconstruction"] = _recover_stack_object(call_ea, d, 0x80) if call_ea is not None else None
        rid = const_value("rack_id")
        if rid is not None:
            result["rack_type"] = {"value": rid, "name": RACK_TYPES.get(rid, "UNKNOWN_RACK")}
    elif api_name == "sceNgs2SystemRender":
        p = const_value("render_buffers")
        n = const_value("num_buffers")
        result["render_buffers"] = _decode_render_buffers(p, n)
    return result

# ----------------------------- Imports / symbols ----------------------------

def _all_ngs2_symbols():
    found = {}
    # Imports from the IDA loader.
    try:
        qty = idaapi.get_import_module_qty()
    except Exception:
        qty = 0
    for i in range(qty):
        try:
            module = idaapi.get_import_module_name(i)
        except Exception:
            module = ""
        def cb(ea, name, ordinal):
            nm = _to_text(name) if name else _name(ea)
            nid = None
            if nm in NGS2_NIDS:
                nid = nm
                nm = NGS2_NIDS[nm]
            if nm in API_ARGS or "ngs2" in str(module).lower() or "sceNgs2" in str(nm):
                key = nm if nm else "<unnamed_ngs2_import_%x>" % ea
                rec = found.setdefault(key, {"name": key, "addresses": [], "modules": [], "nids": []})
                rec["addresses"].append(ea)
                if module and module not in rec["modules"]:
                    rec["modules"].append(str(module))
                if nid and nid not in rec["nids"]:
                    rec["nids"].append(nid)
            return True
        try:
            idaapi.enum_import_names(i, cb)
        except Exception:
            pass

    # Named functions/thunks can be present even if the import table was not
    # reconstructed by the loader.
    try:
        for ea, nm in idautils.Names():
            s = str(nm)
            api = None
            if s in API_ARGS:
                api = s
            elif s in NGS2_NIDS:
                api = NGS2_NIDS[s]
            elif s.startswith("sceNgs2"):
                api = s
            if api:
                rec = found.setdefault(api, {"name": api, "addresses": [], "modules": [], "nids": []})
                if ea not in rec["addresses"]:
                    rec["addresses"].append(ea)
                if s in NGS2_NIDS and s not in rec["nids"]:
                    rec["nids"].append(s)
    except Exception:
        pass

    # NID strings are sometimes visible in module metadata even if imports have
    # auto-generated names. Keep them as evidence; do not assume a call exists.
    nid_strings = []
    try:
        strings = idautils.Strings()
        strings.setup()
        for st in strings:
            txt = _to_text(str(st))
            if txt in NGS2_NIDS:
                nid_strings.append({"ea": int(st.ea), "nid": txt, "api": NGS2_NIDS[txt],
                                    "xrefs": _code_refs_to(int(st.ea)) + _data_refs_to(int(st.ea))})
    except Exception:
        pass

    for api in API_ARGS:
        found.setdefault(api, {"name": api, "addresses": [], "modules": [], "nids": []})
    for rec in found.values():
        rec["addresses"] = sorted(list(set(rec["addresses"])))
    return found, nid_strings

# ----------------------------- Thunks / call graph --------------------------

def _near_target(ea, opn=0):
    typ = _op_type(ea, opn)
    val = _op_value(ea, opn)
    if typ in (getattr(idaapi, "o_near", -100), getattr(idaapi, "o_far", -101),
               getattr(idaapi, "o_mem", -102), getattr(idaapi, "o_imm", -103)):
        return val
    txt = _op_text(ea, opn)
    if "rip" in txt.lower():
        return ea + _item_size(ea) + val
    return None


def _resolve_thunk_chain(start_ea):
    chain = []
    cur = start_ea
    seen = set()
    for depth in range(MAX_THUNK_DEPTH):
        if cur in seen or _is_badaddr(cur):
            break
        seen.add(cur)
        chain.append(cur)
        f = _get_func(cur)
        if not f:
            break
        ea = _func_start(f)
        end = min(_func_end(f), ea + 0x30)
        jumped = False
        while ea < end:
            m = _mnem(ea)
            if m in ("jmp", "jmpq"):
                target = _near_target(ea, 0)
                if target is not None and target != cur and _is_mapped(target):
                    cur = target
                    jumped = True
                break
            if m not in ("nop", "endbr64", "endbr32", "int3"):
                # A thunk can have a short load/indirect-jump sequence.
                if m not in ("mov", "movabs", "lea"):
                    break
            ea = idc.next_head(ea, end)
            if ea == idaapi.BADADDR:
                break
        if not jumped:
            break
    return chain


def _is_call(ea):
    return _mnem(ea) in ("call", "callq")


def _containing_func_info(ea):
    f = _get_func(ea)
    if not f:
        return None
    start = _func_start(f)
    return {"start": start, "end": _func_end(f), "name": _name(start) or ("sub_%x" % start)}


def _parent_callers(func_start, depth=1, seen=None):
    if seen is None:
        seen = set([func_start])
    if depth > MAX_PARENT_DEPTH:
        return []
    out = []
    refs = _code_refs_to(func_start)
    count = 0
    for ref in refs:
        if count >= MAX_PARENT_FUNCS:
            break
        fi = _containing_func_info(ref)
        if not fi or fi["start"] in seen or not _is_call(ref):
            continue
        count += 1
        out.append({"call_ea": ref, "function": fi})
        s2 = set(seen)
        s2.add(fi["start"])
        out.extend(_parent_callers(fi["start"], depth + 1, s2))
    return out


def _call_sites_for_api(api_name, addresses):
    callsites = []
    target_chain = []
    for ea in addresses:
        for t in _resolve_thunk_chain(ea):
            if t not in target_chain:
                target_chain.append(t)
        # Some PS4 loaders expose the IAT/GOT cell as the import EA. The actual
        # call is then xref'd to a tiny local thunk that jumps through that cell.
        for dr in _data_refs_to(ea):
            df = _get_func(dr)
            if df:
                ds = _func_start(df)
                # Only treat small functions with a jump/load sequence as import
                # thunks; arbitrary functions that read a callback pointer are
                # left as low-confidence indirect evidence below.
                if _func_end(df) - ds <= 0x60:
                    first = []
                    for de in _iter_func_heads(ds, min(_func_end(df), ds + 0x30)):
                        first.append(_mnem(de))
                    if "jmp" in first or "jmpq" in first:
                        if ds not in target_chain:
                            target_chain.append(ds)
    if not target_chain:
        target_chain = list(addresses)

    seen_site = set()
    for target in target_chain:
        refs = _code_refs_to(target)
        for ref in refs:
            if ref in seen_site:
                continue
            seen_site.add(ref)
            fi = _containing_func_info(ref)
            if not fi:
                continue
            call_insn = _is_call(ref)
            args = _arg_snapshot(ref, api_name) if call_insn else {"integer_args": [], "xmm_args": []}
            decoded = _decode_call_arguments(api_name, args, ref) if call_insn else {}
            constants = _known_param_ids_in_func(_get_func(ref))
            param_ids = []
            if api_name == "sceNgs2VoiceControl":
                chain = decoded.get("parameter_chain", {})
                for p in chain.get("params", []):
                    if p.get("id") is not None:
                        param_ids.append(p.get("id"))
                if not param_ids:
                    param_ids = [x.get("id") for x in constants if x.get("id") is not None]
            callsites.append({
                "api": api_name,
                "call_ea": ref,
                "target_ea": target,
                "instruction": idc.generate_disasm_line(ref, 0),
                "call_instruction": call_insn,
                "xref_kind": "direct_call" if call_insn else "code_reference_not_call",
                "caller_function": fi,
                "arguments": args,
                "decoded": decoded,
                "function_ngs2_constants": constants,
                "candidate_param_ids": sorted(list(set(param_ids))),
                "parent_callers": _parent_callers(fi["start"], 1) if call_insn else [],
                "confidence": "high" if call_insn else "medium",
            })
            if len(callsites) >= MAX_CALLERS_PER_API:
                break
    # Imported pointer may be referenced as data, then called indirectly through
    # a register. Mark indirect candidates without upgrading them to confirmed.
    indirect_funcs = {}
    for target in addresses:
        for ref in _data_refs_to(target):
            fi = _containing_func_info(ref)
            if not fi:
                continue
            indirect_funcs.setdefault(fi["start"], {"function": fi, "data_refs": []})["data_refs"].append(ref)
    known_funcs = set([x["caller_function"]["start"] for x in callsites])
    for fs, item in indirect_funcs.items():
        if fs in known_funcs:
            continue
        f = _get_func(fs)
        if not f:
            continue
        calls = []
        for ea in _iter_func_heads(_func_start(f), _func_end(f)):
            if _is_call(ea):
                calls.append(ea)
        for ce in calls[:16]:
            callsites.append({
                "api": api_name, "call_ea": ce, "target_ea": None,
                "instruction": idc.generate_disasm_line(ce, 0),
                "call_instruction": True, "xref_kind": "indirect_call_candidate",
                "caller_function": item["function"], "arguments": _arg_snapshot(ce, api_name),
                "decoded": {}, "function_ngs2_constants": _known_param_ids_in_func(f),
                "candidate_param_ids": [], "parent_callers": [], "data_refs_to_import": item["data_refs"],
                "confidence": "low",
            })
    return callsites, target_chain

# ----------------------------- Strings / constants -------------------------

def _collect_ngs2_strings():
    out = []
    try:
        strings = idautils.Strings()
        strings.setup()
        for st in strings:
            txt = _to_text(str(st))
            low = txt.lower()
            if "ngs2" in low or "sce ngs" in low or "libsce ngs" in low:
                ea = int(st.ea)
                refs = _code_refs_to(ea) + _data_refs_to(ea)
                out.append({"ea": ea, "text": txt[:512], "xrefs": sorted(list(set(refs)))})
    except Exception:
        pass
    return out


def _collect_param_constant_xrefs():
    out = []
    # Search IDA's decoded immediate operands in code; this also finds parameter
    # IDs that are assembled into stack/heap structures before VoiceControl.
    try:
        for fstart in idautils.Functions():
            f = _get_func(fstart)
            if not f:
                continue
            for ea in _iter_func_heads(_func_start(f), _func_end(f)):
                for opn in (0, 1):
                    if _op_type(ea, opn) != getattr(idaapi, "o_imm", -999):
                        continue
                    v = _op_value(ea, opn) & 0xffffffff
                    if v in PARAM_IDS or v in RACK_TYPES:
                        out.append({"ea": ea, "function": _name(fstart) or ("sub_%x" % fstart),
                                    "function_start": fstart, "value": v,
                                    "kind": "param_id" if v in PARAM_IDS else "rack_id",
                                    "symbolic_name": PARAM_IDS.get(v, RACK_TYPES.get(v)),
                                    "instruction": idc.generate_disasm_line(ea, 0)})
    except Exception:
        pass
    return out

# ----------------------------- Dedup / reporting ----------------------------

def _arg_signature(site):
    out = []
    for a in site.get("arguments", {}).get("integer_args", []):
        d = a.get("definition", {})
        src = d.get("source", {})
        kind = src.get("kind", d.get("kind", "unknown"))
        if kind == "immediate":
            val = src.get("value")
            if _is_mapped(val):
                kind = "static_ptr"
            else:
                kind = "imm"
        elif kind in ("memory", "rip_relative"):
            kind = "memory_expr"
        elif kind == "register":
            kind = "reg_copy"
        out.append("%s=%s" % (a.get("name"), kind))
    pids = site.get("candidate_param_ids", [])
    if pids:
        out.append("params=" + ",".join(["%08x" % x for x in pids]))
    return "|".join(out) if out else "no_recovered_args"


def _make_clusters(callsites):
    groups = {}
    for s in callsites:
        sig = _arg_signature(s)
        key = (s.get("api"), sig)
        g = groups.setdefault(key, {"api": s.get("api"), "signature": sig,
                                    "count": 0, "call_sites": [], "caller_functions": []})
        g["count"] += 1
        g["call_sites"].append(s.get("call_ea"))
        fn = s.get("caller_function", {})
        label = {"start": fn.get("start"), "name": fn.get("name")}
        if label not in g["caller_functions"]:
            g["caller_functions"].append(label)
    result = list(groups.values())
    result.sort(key=lambda x: (x.get("api", ""), -x.get("count", 0), x.get("signature", "")))
    return result


def _fmt_ea(ea):
    try:
        return "0x%X" % long(ea)
    except Exception:
        try:
            return "0x%X" % int(ea)
        except Exception:
            return str(ea)


def _json_safe(obj):
    if isinstance(obj, dict):
        return dict((str(k), _json_safe(v)) for k, v in obj.items())
    if isinstance(obj, (list, tuple, set)):
        return [_json_safe(v) for v in obj]
    try:
        if isinstance(obj, long):
            return int(obj)
    except Exception:
        pass
    if isinstance(obj, float):
        # JSON has no portable representation for NaN/Inf.
        if obj != obj or obj == float("inf") or obj == float("-inf"):
            return str(obj)
    return obj


def _write_text(path, text):
    data = text
    try:
        if isinstance(data, unicode):
            data = data.encode("utf-8")
    except Exception:
        pass
    f = open(path, "wb")
    try:
        f.write(data)
    finally:
        f.close()


def _write_json(path, data):
    try:
        txt = json.dumps(_json_safe(data), indent=2, sort_keys=True, ensure_ascii=False)
    except Exception:
        txt = json.dumps(_json_safe(data), indent=2, sort_keys=True)
    _write_text(path, txt + "\n")


def _md_escape(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def _write_markdown(path, report):
    lines = []
    meta = report.get("meta", {})
    lines.append("# NGS2 static EBOOT analysis")
    lines.append("")
    lines.append("- Input: `%s`" % _md_escape(meta.get("input_file", "")))
    lines.append("- IDA: `%s`" % _md_escape(meta.get("ida_version", "")))
    lines.append("- Image base: `%s`" % _fmt_ea(meta.get("image_base", 0)))
    lines.append("- Generated: `%s`" % _md_escape(meta.get("generated", "")))
    lines.append("")
    lines.append("> Static/heuristic report. A static pointer is not proof that a structure is used at runtime. Dynamic values and heap-built parameter chains require the native trace or manual data-flow review.")
    lines.append("")
    lines.append("## API coverage")
    lines.append("")
    lines.append("| API | Import/symbol address | Call sites | Caller functions | Status |")
    lines.append("|---|---:|---:|---:|---|")
    for api in report.get("apis", []):
        addrs = ", ".join([_fmt_ea(x) for x in api.get("addresses", [])]) or "not named in IDB"
        sites = [s for s in report.get("call_sites", []) if s.get("api") == api.get("name")]
        callers = len(set([s.get("caller_function", {}).get("start") for s in sites]))
        status = "referenced" if sites else ("import only / no code xref" if api.get("addresses") else "not resolved")
        lines.append("| `%s` | %s | %d | %d | %s |" % (_md_escape(api.get("name")), addrs, len(sites), callers, status))
        if api.get("abi_note"):
            lines.append("  - ABI note: %s" % _md_escape(api.get("abi_note")))
    lines.append("")
    lines.append("## Deduplicated call variants")
    lines.append("")
    lines.append("| API | Sites | Caller functions | Recovered argument / parameter signature |")
    lines.append("|---|---:|---:|---|")
    for c in report.get("clusters", []):
        lines.append("| `%s` | %d | %d | `%s` |" % (_md_escape(c.get("api")), c.get("count", 0),
                    len(c.get("caller_functions", [])), _md_escape(c.get("signature", ""))))
    lines.append("")
    lines.append("## Call sites")
    lines.append("")
    for s in report.get("call_sites", []):
        fn = s.get("caller_function", {})
        lines.append("### `%s` at %s — `%s`" % (_md_escape(s.get("api")), _fmt_ea(s.get("call_ea")), _md_escape(fn.get("name", ""))))
        lines.append("")
        lines.append("- Target: `%s`; confidence: **%s**; xref: `%s`" % (_fmt_ea(s.get("target_ea")), s.get("confidence", ""), s.get("xref_kind", "")))
        lines.append("- Instruction: `%s`" % _md_escape(s.get("instruction", "")))
        for a in s.get("arguments", {}).get("integer_register_snapshot", []):
            d = a.get("definition", {})
            src = d.get("source", {})
            lines.append("- ABI `%s`: `%s`" % (a.get("register", ""), _md_escape(src.get("text", d.get("reason", "unresolved")))))
        for a in s.get("arguments", {}).get("integer_args", []):
            d = a.get("definition", {})
            src = d.get("source", {})
            lines.append("- Arg%d `%s` (%s): `%s`" % (a.get("index", 0), _md_escape(a.get("name", "")),
                        a.get("register", ""), _md_escape(src.get("text", d.get("reason", "unresolved")))))
        decoded = s.get("decoded", {})
        chain = decoded.get("parameter_chain", {})
        if chain.get("params"):
            for p in chain.get("params", []):
                lines.append("- Parameter: `%s` ID `0x%08X`, size `0x%X`, next `%d`" %
                             (_md_escape(p.get("name", "")), p.get("id", 0), p.get("size", 0), p.get("next", 0)))
                if p.get("fields"):
                    lines.append("  - Fields: `%s`" % _md_escape(json.dumps(p.get("fields"), ensure_ascii=False, sort_keys=True)))
        elif s.get("candidate_param_ids"):
            lines.append("- Candidate parameter IDs in caller: %s" % ", ".join(["`0x%08X`" % x for x in s.get("candidate_param_ids", [])]))
        for dk, dv in decoded.items():
            if dk.endswith("stack_reconstruction") and isinstance(dv, dict):
                lines.append("- Stack reconstruction `%s`: base `%s`, displacement `%s`" %
                             (dk, dv.get("base", "?"), dv.get("displacement", "?")))
                for wr in dv.get("writes", [])[:32]:
                    lines.append("  - +0x%X @ %s: `%s` => %s" %
                                 (wr.get("offset", 0), _fmt_ea(wr.get("ea")),
                                  _md_escape(wr.get("instruction", "")),
                                  _md_escape(str(wr.get("value")) if wr.get("value") is not None else "unknown")))
        if s.get("parent_callers"):
            parents = []
            for p in s.get("parent_callers", [])[:12]:
                parents.append("%s@%s" % (p.get("function", {}).get("name", "?"), _fmt_ea(p.get("call_ea"))))
            lines.append("- Parent callers: " + ", ".join(["`%s`" % _md_escape(x) for x in parents]))
        lines.append("")
    lines.append("## NGS2 constants found in code")
    lines.append("")
    lines.append("| Address | Function | Kind | Value | Meaning | Instruction |")
    lines.append("|---:|---|---|---:|---|---|")
    for c in report.get("constant_hits", []):
        lines.append("| %s | `%s` | %s | `0x%08X` | %s | `%s` |" %
                     (_fmt_ea(c.get("ea")), _md_escape(c.get("function", "")), c.get("kind", ""),
                      c.get("value", 0), _md_escape(c.get("symbolic_name", "")), _md_escape(c.get("instruction", ""))))
    lines.append("")
    lines.append("## NGS2 strings / NID evidence")
    lines.append("")
    for s in report.get("ngs2_strings", []):
        lines.append("- %s: `%s` (xrefs: %s)" % (_fmt_ea(s.get("ea")), _md_escape(s.get("text", "")),
                     ", ".join([_fmt_ea(x) for x in s.get("xrefs", [])])))
    for s in report.get("nid_strings", []):
        lines.append("- NID `%s` → `%s` at %s" % (s.get("nid"), s.get("api"), _fmt_ea(s.get("ea"))))
    lines.append("")
    lines.append("## Interpretation / limitations")
    lines.append("")
    lines.append("1. Direct call xrefs to an import thunk are the strongest static evidence. Data-xref/indirect-call candidates are deliberately marked low confidence.")
    lines.append("2. Arguments are recovered by a bounded backward scan of the current function and basic-block-like region. Register values crossing branches or prior calls may be unresolved.")
    lines.append("3. A `VoiceControl` parameter chain is decoded only when its pointer resolves to a mapped static address. Stack/heap-generated chains are represented by candidate parameter IDs and must be confirmed by tracing.")
    lines.append("4. Raw bytes and pointee previews are preserved in JSON so field offsets can be checked rather than trusted blindly.")
    lines.append("5. Imports not present in this EBOOT are not evidence that an export is unused in every game/version. The current inventory is tied to this exact EBOOT/database.")
    lines.append("")
    _write_text(path, "\n".join(lines))


def _write_csv(path, report):
    f = open(path, "wb")
    try:
        # Python 2 csv wants byte strings. Keep the CSV ASCII by escaping text.
        import csv
        w = csv.writer(f)
        w.writerow(["api", "call_ea", "target_ea", "caller_start", "caller_name", "xref_kind",
                    "confidence", "arg_signature", "candidate_param_ids", "instruction"])
        for s in report.get("call_sites", []):
            fn = s.get("caller_function", {})
            w.writerow([
                s.get("api", ""), _fmt_ea(s.get("call_ea")), _fmt_ea(s.get("target_ea")),
                _fmt_ea(fn.get("start")), _md_escape(fn.get("name", "")), s.get("xref_kind", ""),
                s.get("confidence", ""), _arg_signature(s),
                ",".join(["0x%08X" % x for x in s.get("candidate_param_ids", [])]),
                _md_escape(s.get("instruction", ""))
            ])
    finally:
        f.close()

# ----------------------------- Main -----------------------------------------

def main():
    started = time.time()
    symbols, nid_strings = _all_ngs2_symbols()
    apis = []
    all_sites = []
    thunk_map = {}
    api_names = sorted(set(API_ARGS.keys()) | set(symbols.keys()))
    for api_name in api_names:
        rec = symbols.get(api_name, {"name": api_name, "addresses": [], "modules": [], "nids": []})
        sites, chain = _call_sites_for_api(api_name, rec.get("addresses", []))
        all_sites.extend(sites)
        thunk_map[api_name] = chain
        api_rec = dict(rec)
        api_rec["prototype_args"] = API_ARGS.get(api_name, ["arg0", "arg1", "arg2", "arg3", "arg4", "arg5"])
        if api_name in ABI_NOTES:
            api_rec["abi_note"] = ABI_NOTES[api_name]
        api_rec["thunk_chain"] = chain
        api_rec["call_site_count"] = len(sites)
        api_rec["caller_function_count"] = len(set([x.get("caller_function", {}).get("start") for x in sites]))
        api_rec["xrefs"] = []
        for a in rec.get("addresses", []):
            api_rec["xrefs"].append({"address": a, "refs": _xref_list_to(a)})
        apis.append(api_rec)

    clusters = _make_clusters(all_sites)
    strings = _collect_ngs2_strings()
    constants = _collect_param_constant_xrefs()
    input_path = ""
    try:
        input_path = idc.get_input_file_path()
    except Exception:
        try:
            input_path = idc.GetInputFile()
        except Exception:
            pass
    output_dir = OUTPUT_DIR or (os.path.dirname(input_path) if input_path else os.getcwd())
    if not output_dir:
        output_dir = os.getcwd()
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    base = os.path.basename(input_path) if input_path else "eboot"
    stem = re.sub(r"[^A-Za-z0-9_.-]+", "_", base)
    prefix = os.path.join(output_dir, stem + ".ngs2_static")

    try:
        ida_ver = idaapi.get_kernel_version()
    except Exception:
        ida_ver = "IDA 7.x"
    try:
        image_base = idaapi.get_imagebase()
    except Exception:
        image_base = 0

    report = {
        "meta": {
            "input_file": input_path,
            "ida_version": str(ida_ver),
            "image_base": image_base,
            "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
            "elapsed_seconds": round(time.time() - started, 3),
            "analysis": "Static IDAPython heuristic; does not execute EBOOT",
            "abi_assumption": "x86-64 System-V integer args: RDI, RSI, RDX, RCX, R8, R9; XMM0-XMM7 also sampled",
            "known_import_api_count": len(API_ARGS),
            "resolved_ngs2_symbol_count": len(api_names),
            "notes": [
                "The hardcoded NID map was taken from the repository's ngs2 branch EBOOT 1.03 import metadata.",
                "Import-table evidence, symbols and code xrefs are combined; inspect confidence before porting behavior.",
                "A pointer resolved to mapped IDB memory may still be a static template rather than the runtime object."
            ]
        },
        "apis": apis,
        "call_sites": sorted(all_sites, key=lambda x: (x.get("api", ""), x.get("call_ea") or 0, x.get("xref_kind", ""))),
        "clusters": clusters,
        "constant_hits": constants,
        "ngs2_strings": strings,
        "nid_strings": nid_strings,
    }

    json_path = prefix + ".json"
    md_path = prefix + ".md"
    csv_path = prefix + ".csv"
    _write_json(json_path, report)
    _write_markdown(md_path, report)
    _write_csv(csv_path, report)

    _msg("[NGS2] Static analysis complete")
    _msg("[NGS2] API symbols: %d; call-site candidates: %d; deduplicated variants: %d" %
         (len(apis), len(all_sites), len(clusters)))
    _msg("[NGS2] Output JSON: %s" % json_path)
    _msg("[NGS2] Output Markdown: %s" % md_path)
    _msg("[NGS2] Output CSV: %s" % csv_path)
    return report


try:
    main()
except Exception as e:
    _msg("[NGS2] FATAL: %s" % e)
    _msg(traceback.format_exc())
