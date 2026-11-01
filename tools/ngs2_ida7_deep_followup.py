# -*- coding: utf-8 -*-
# IDAPython 7.x / Python 2.7 compatible focused NGS2 follow-up analyser.
#
# Purpose:
#   Deeply inspect the EBOOT functions that build NGS2 rack options and voice
#   parameter blocks, with special attention to:
#     - CUSTOM_SUBMIXER rack 0x4002 and its module option descriptors;
#     - legacy custom modules / Chorus 0x1C / Delay 0x1D;
#     - SAMPLER_USER_FX 0x10000008 callback and user-data ABI;
#     - MASTERING_LIMITER 0x30000003;
#     - unknown SUBMIXER parameter 0x20000005;
#     - possible SAMPLER_PEAK_METER 0x10000009.
#
# Run after autoanalysis: IDA -> File -> Script file...
# No database mutation is performed. Output is written next to the IDB/input
# file (or OUTPUT_DIR): JSON + Markdown + a focused call-site CSV.
#
# Important: the analyser reports evidence, not guessed prototypes. A constant
# appearing anywhere in a function is labelled function-wide candidate unless
# it is tied to a direct header write / exact call argument.

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
    import ida_segment
except Exception:
    ida_segment = None

# ------------------------------- Configuration ------------------------------

OUTPUT_DIR = ""               # Empty = IDB/input file directory.
IMAGE_BASE_OVERRIDE = None     # None = idaapi.get_imagebase().

# All addresses below are EBOOT offsets/EA with image base 0 in the previous
# report. The script applies the current IDA image base.
TARGET_FUNCTIONS = [
    {"rva": 0x1AC510, "label": "bus_graph_and_custom_rack_builder"},
    {"rva": 0x1AEFD0, "label": "custom_effect_rack_builder"},
    {"rva": 0x1A9690, "label": "sampler_voice_builder"},
    {"rva": 0x1ADC10, "label": "mastering_voice_builder"},
    {"rva": 0x1ABD70, "label": "unknown_submixer_parameter_builder"},
    {"rva": 0x1A8E90, "label": "voice_lifecycle_peak_meter_candidate"},
]

# Addresses worth expanding even if IDA does not identify them as API calls.
ANCHORS = {
    0x1AC510: [0x1AC710, 0x1AC762, 0x1AD427, 0x1AD479, 0x1AD5DE, 0x1AD630],
    0x1AEFD0: [0x1AF86A, 0x1AFA04, 0x1AFA88, 0x1AFC14, 0x1AFF71, 0x1B0015],
    0x1A9690: [0x1A9ADC, 0x1A9F5B, 0x1AA0A5, 0x1AB135, 0x1AB33F, 0x1AB489],
    0x1ADC10: [0x1ADE41, 0x1ADE9F, 0x1ADF3F, 0x1AE576, 0x1AE5E3],
    0x1ABD70: [0x1ABDF8, 0x1ABEC9],
    0x1A8E90: [0x1A900A, 0x1A9156, 0x1A9296, 0x1A93D6, 0x1A9516, 0x1A964D],
}

API_NAMES = [
    "sceNgs2SystemCreateWithAllocator", "sceNgs2SystemDestroy",
    "sceNgs2SystemRender", "sceNgs2RackQueryBufferSize",
    "sceNgs2RackCreate", "sceNgs2RackCreateWithAllocator",
    "sceNgs2RackDestroy", "sceNgs2RackGetVoiceHandle",
    "sceNgs2VoiceControl", "sceNgs2VoiceGetState",
]

API_ARGUMENTS = {
    "sceNgs2SystemCreateWithAllocator": ["option", "allocator", "out_system"],
    "sceNgs2SystemDestroy": ["system"],
    "sceNgs2SystemRender": ["system", "render_buffers", "num_buffers"],
    "sceNgs2RackQueryBufferSize": ["rack_id", "rack_option", "out_buffer_info"],
    "sceNgs2RackCreate": ["system", "rack_id", "rack_option", "context_buffer", "out_rack"],
    "sceNgs2RackCreateWithAllocator": ["system", "rack_id", "rack_option", "allocator", "out_rack"],
    "sceNgs2RackDestroy": ["rack"],
    "sceNgs2RackGetVoiceHandle": ["rack", "voice_index", "out_voice"],
    "sceNgs2VoiceControl": ["voice", "parameter_chain"],
    "sceNgs2VoiceGetState": ["voice", "out_state", "state_size"],
}

PARAM_IDS = {
    0x00000001: "MATRIX_LEVELS",
    0x00000002: "PORT_VOLUME",
    0x00000003: "PORT_MATRIX",
    0x00000004: "PORT_DELAY",
    0x00000005: "PATCH",
    0x00000006: "KICK_EVENT",
    0x00000007: "CALLBACK",
    0x10000000: "SAMPLER_SETUP",
    0x10000001: "SAMPLER_ADD_WAVEFORM_BLOCKS",
    0x10000004: "SAMPLER_EXIT_LOOP",
    0x10000005: "SAMPLER_PITCH",
    0x10000006: "SAMPLER_ENVELOPE",
    0x10000008: "SAMPLER_USER_FX",
    0x10000009: "SAMPLER_PEAK_METER",
    0x1000000A: "SAMPLER_FILTER",
    0x20000000: "SUBMIXER_SETUP",
    0x20000002: "SUBMIXER_COMPRESSOR",
    0x20000004: "SUBMIXER_USER_FX",
    0x20000005: "UNKNOWN_SUBMIXER_PARAM_20000005",
    0x20000006: "SUBMIXER_FILTER",
    0x20010000: "REVERB_SETUP",
    0x20010001: "REVERB_I3DL2",
    0x30000000: "MASTERING_SETUP",
    0x30000002: "MASTERING_LFE_FILTER",
    0x30000003: "MASTERING_LIMITER",
    0x30000004: "MASTERING_GAIN",
    0x30000005: "MASTERING_OUTPUT",
    0x40020000: "CUSTOM_SUBMIXER_SETUP",
    0x40001C00: "CUSTOM_MODULE_1C_CANDIDATE",
    0x40001D00: "CUSTOM_MODULE_1D_CANDIDATE",
}

RACK_IDS = {
    0x1000: "SAMPLER",
    0x2000: "SUBMIXER",
    0x2001: "REVERB",
    0x3000: "MASTERING",
    0x4001: "CUSTOM_SAMPLER",
    0x4002: "CUSTOM_SUBMIXER",
}

# Candidate raw custom module identifiers. Their meanings/layouts must be
# confirmed from the producer, not inferred from their numerical resemblance.
CUSTOM_MODULE_IDS = {
    0x13: "AnyPS5_FILTER_module_id",
    0x1C: "legacy_TLG_CHORUS_candidate",
    0x1D: "legacy_TLG_DELAY_or_USER_FX_candidate",
    0x1F: "AnyPS5_USER_FX2_module_id",
}

GPR_ARGS = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]
XMM_ARGS = ["xmm0", "xmm1", "xmm2", "xmm3", "xmm4", "xmm5", "xmm6", "xmm7"]
MAX_BACKTRACE = 96
MAX_TRACE_DEPTH = 3
MAX_CALL_WINDOW = 22
MAX_ANCHOR_WINDOW = 28
MAX_FUNC_INSNS = 6000
MAX_DATA_PREVIEW = 0x100
MAX_STACK_EVENTS = 1200

# ------------------------------- IDA wrappers -------------------------------

def msg(s):
    try:
        idaapi.msg(str(s) + "\n")
    except Exception:
        try:
            print(s)
        except Exception:
            pass


def imagebase():
    if IMAGE_BASE_OVERRIDE is not None:
        return int(IMAGE_BASE_OVERRIDE)
    try:
        return int(idaapi.get_imagebase())
    except Exception:
        try:
            return int(getattr(idaapi, "get_imagebase", lambda: 0)())
        except Exception:
            return 0


def badaddr(ea):
    try:
        return ea is None or ea == idaapi.BADADDR
    except Exception:
        return ea is None or ea == 0xFFFFFFFFFFFFFFFF


def get_func(ea):
    try:
        if ida_funcs:
            return ida_funcs.get_func(ea)
    except Exception:
        pass
    try:
        return idaapi.get_func(ea)
    except Exception:
        return None


def fstart(f):
    if not f:
        return 0
    return getattr(f, "start_ea", getattr(f, "startEA", 0))


def fend(f):
    if not f:
        return 0
    return getattr(f, "end_ea", getattr(f, "endEA", 0))


def name(ea):
    if badaddr(ea):
        return ""
    for fn in [getattr(idc, "get_name", None), getattr(idc, "Name", None)]:
        if fn:
            try:
                v = fn(ea)
                if v:
                    return str(v)
            except Exception:
                pass
    return ""


def name_ea(n):
    try:
        return idc.get_name_ea_simple(n)
    except Exception:
        try:
            return idc.get_name_ea(idc.BADADDR, n)
        except Exception:
            return idaapi.BADADDR


def disasm(ea):
    for fn in [getattr(idc, "generate_disasm_line", None), getattr(idc, "GetDisasm", None)]:
        if fn:
            try:
                v = fn(ea, 0) if fn == getattr(idc, "generate_disasm_line", None) else fn(ea)
                if v:
                    return str(v)
            except Exception:
                try:
                    v = fn(ea)
                    if v:
                        return str(v)
                except Exception:
                    pass
    return ""


def mnem(ea):
    for fn in [getattr(idc, "print_insn_mnem", None), getattr(idc, "GetMnem", None)]:
        if fn:
            try:
                v = fn(ea)
                if v:
                    return str(v).lower()
            except Exception:
                pass
    return ""


def optext(ea, n):
    for fn in [getattr(idc, "print_operand", None), getattr(idc, "GetOpnd", None)]:
        if fn:
            try:
                v = fn(ea, n)
                if v:
                    return str(v).strip()
            except Exception:
                pass
    return ""


def optype(ea, n):
    for fn in [getattr(idc, "get_operand_type", None), getattr(idc, "GetOpType", None)]:
        if fn:
            try:
                return fn(ea, n)
            except Exception:
                pass
    return -1


def opvalue(ea, n):
    for fn in [getattr(idc, "get_operand_value", None), getattr(idc, "GetOperandValue", None)]:
        if fn:
            try:
                return int(fn(ea, n))
            except Exception:
                pass
    return 0


def item_size(ea):
    for fn in [getattr(idc, "get_item_size", None), getattr(idc, "ItemSize", None)]:
        if fn:
            try:
                v = int(fn(ea))
                if v > 0:
                    return v
            except Exception:
                pass
    return 1


def getbytes(ea, size):
    if badaddr(ea) or size <= 0:
        return None
    try:
        if ida_bytes:
            b = ida_bytes.get_bytes(ea, size)
            if b is not None:
                return b
    except Exception:
        pass
    for fn in [getattr(idc, "get_bytes", None), getattr(idc, "GetManyBytes", None)]:
        if fn:
            try:
                return fn(ea, size)
            except Exception:
                pass
    return None


def mapped(ea):
    if badaddr(ea):
        return False
    try:
        return idaapi.getseg(ea) is not None
    except Exception:
        try:
            return bool(idc.get_segm_name(ea))
        except Exception:
            return False


def read_u64(ea):
    b = getbytes(ea, 8)
    if not b or len(b) < 8:
        return None
    try:
        return struct.unpack("<Q", b)[0]
    except Exception:
        return None


def read_u32(ea):
    b = getbytes(ea, 4)
    if not b or len(b) < 4:
        return None
    try:
        return struct.unpack("<I", b)[0]
    except Exception:
        return None


def read_f32(ea):
    b = getbytes(ea, 4)
    if not b or len(b) < 4:
        return None
    try:
        return struct.unpack("<f", b)[0]
    except Exception:
        return None


def hx(v):
    if v is None:
        return None
    try:
        return "0x%X" % (int(v) & 0xFFFFFFFFFFFFFFFF)
    except Exception:
        return str(v)


def bytes_hex(b, limit=MAX_DATA_PREVIEW):
    if not b:
        return ""
    try:
        b = b[:limit]
        vals = []
        for x in b:
            vals.append("%02X" % (x if isinstance(x, int) else ord(x)))
        return " ".join(vals)
    except Exception:
        return ""


def comment(ea):
    for fn in [getattr(idc, "get_cmt", None), getattr(idc, "Comment", None)]:
        if fn:
            try:
                v = fn(ea, 0) if fn == getattr(idc, "get_cmt", None) else fn(ea)
                if v:
                    return str(v)
            except Exception:
                pass
    return ""


def operand_count(ea):
    n = 0
    for i in range(8):
        t = optype(ea, i)
        if t in (-1, 0):
            break
        n += 1
    return n


def func_items(f):
    result = []
    if not f:
        return result
    try:
        for ea in idautils.FuncItems(fstart(f)):
            if ea >= fend(f):
                continue
            if len(result) >= MAX_FUNC_INSNS:
                break
            result.append(ea)
    except Exception:
        ea = fstart(f)
        end = fend(f)
        while ea < end and len(result) < MAX_FUNC_INSNS:
            if mnem(ea):
                result.append(ea)
            ea += item_size(ea)
    return result


def func_name(ea):
    try:
        n = idc.get_func_name(ea)
        if n:
            return str(n)
    except Exception:
        pass
    f = get_func(ea)
    return name(fstart(f)) if f else name(ea)


def xrefs_to(ea, code_only=False):
    out = []
    try:
        for x in idautils.XrefsTo(ea, 0):
            if code_only and not getattr(x, "iscode", False):
                continue
            out.append({"from": int(x.frm), "from_hex": hx(x.frm), "type": int(x.type),
                        "is_code": bool(getattr(x, "iscode", False)),
                        "function": func_name(x.frm)})
    except Exception:
        pass
    return out


def refs_from(ea):
    out = []
    try:
        for x in idautils.XrefsFrom(ea, 0):
            out.append({"to": int(x.to), "to_hex": hx(x.to), "type": int(x.type),
                        "is_code": bool(getattr(x, "iscode", False)), "name": name(x.to)})
    except Exception:
        pass
    return out


def strings_at(ea):
    if not mapped(ea):
        return None
    for fn in [getattr(idc, "get_strlit_contents", None), getattr(idc, "GetString", None)]:
        if fn:
            try:
                if fn == getattr(idc, "get_strlit_contents", None):
                    st = fn(ea, -1, idc.get_str_type(ea))
                else:
                    st = fn(ea, -1, idc.ASCSTR_C)
                if st:
                    if not isinstance(st, str):
                        st = st.decode("latin1", "ignore")
                    return st[:256]
            except Exception:
                pass
    return None


def data_preview(ea, size=MAX_DATA_PREVIEW):
    b = getbytes(ea, size)
    if not b:
        return None
    qwords = []
    dwords = []
    for off in range(0, min(len(b), 0x40), 8):
        if off + 8 <= len(b):
            q = read_u64(ea + off)
            qwords.append({"offset": off, "value": hx(q), "mapped": mapped(q) if q is not None else False,
                           "name": name(q) if q is not None and mapped(q) else ""})
    for off in range(0, min(len(b), 0x40), 4):
        if off + 4 <= len(b):
            d = read_u32(ea + off)
            dwords.append({"offset": off, "value": hx(d), "float": read_f32(ea + off)})
    return {"address": int(ea), "address_hex": hx(ea), "name": name(ea), "string": strings_at(ea),
            "bytes": bytes_hex(b, size), "qwords": qwords, "dwords": dwords}

# ------------------------- Instruction interpretation -----------------------

REG_ALIASES = {
    "rax": ["rax", "eax", "ax", "al", "ah"],
    "rbx": ["rbx", "ebx", "bx", "bl", "bh"],
    "rcx": ["rcx", "ecx", "cx", "cl", "ch"],
    "rdx": ["rdx", "edx", "dx", "dl", "dh"],
    "rsi": ["rsi", "esi", "si", "sil"],
    "rdi": ["rdi", "edi", "di", "dil"],
    "rbp": ["rbp", "ebp", "bp", "bpl"],
    "rsp": ["rsp", "esp", "sp", "spl"],
    "r8": ["r8", "r8d", "r8w", "r8b"],
    "r9": ["r9", "r9d", "r9w", "r9b"],
    "r10": ["r10", "r10d", "r10w", "r10b"],
    "r11": ["r11", "r11d", "r11w", "r11b"],
    "r12": ["r12", "r12d", "r12w", "r12b"],
    "r13": ["r13", "r13d", "r13w", "r13b"],
    "r14": ["r14", "r14d", "r14w", "r14b"],
    "r15": ["r15", "r15d", "r15w", "r15b"],
}


def canon_reg(s):
    s = (s or "").strip().lower()
    s = s.split(" ")[0].strip(" ,[]")
    if s.startswith("xmm") or s.startswith("ymm") or s.startswith("zmm"):
        return s
    for root, aliases in REG_ALIASES.items():
        if s in aliases:
            return root
    if re.match(r"^r(1[6-9]|2[0-9]|3[01])", s):
        return s
    return ""


def dst_reg(ea):
    t = optext(ea, 0)
    if not t:
        return ""
    m = re.match(r"^([A-Za-z][A-Za-z0-9]*)", t)
    return canon_reg(m.group(1)) if m else ""


def registers_in_text(t):
    out = []
    # Do not treat segment/size keywords as register names.
    for token in re.findall(r"(?i)\b(?:r(?:ax|bx|cx|dx|si|di|bp|sp|[89]|1[0-5])(?:d|w|b)?|e(?:ax|bx|cx|dx|si|di|bp|sp)|xmm[0-9]+)\b", t or ""):
        r = canon_reg(token)
        if r and r not in out:
            out.append(r)
    return out


def source_regs(ea):
    out = []
    for i in range(1, operand_count(ea)):
        for r in registers_in_text(optext(ea, i)):
            if r not in out:
                out.append(r)
    return out


def immediate_operands(ea):
    out = []
    for i in range(operand_count(ea)):
        t = optype(ea, i)
        try:
            imm_type = idc.o_imm
        except Exception:
            imm_type = 5
        if t == imm_type:
            v = opvalue(ea, i)
            out.append({"operand": i, "value": int(v), "hex": hx(v), "text": optext(ea, i),
                        "float32": _as_float32(v)})
    return out


def _as_float32(v):
    try:
        return struct.unpack("<f", struct.pack("<I", int(v) & 0xFFFFFFFF))[0]
    except Exception:
        return None


def stack_operands(ea):
    out = []
    for i in range(operand_count(ea)):
        t = optext(ea, i)
        if "[" in t and ("rbp" in t.lower() or "rsp" in t.lower() or "var_" in t.lower() or "arg_" in t.lower()):
            out.append({"operand": i, "text": t})
    return out


def instruction_record(ea):
    b = getbytes(ea, item_size(ea))
    return {"ea": int(ea), "ea_hex": hx(ea), "bytes": bytes_hex(b, 16),
            "mnem": mnem(ea), "disasm": disasm(ea), "comment": comment(ea),
            "immediates": immediate_operands(ea), "stack_operands": stack_operands(ea),
            "refs": refs_from(ea)}


def is_call(ea):
    return mnem(ea).startswith("call")


def call_target(ea):
    t = optext(ea, 0)
    v = opvalue(ea, 0)
    out = {"operand": t, "target": int(v) if v else None, "target_hex": hx(v) if v else None,
           "name": name(v) if v else "", "indirect": "[" in t or canon_reg(t) != ""}
    if v and mapped(v):
        # For FF /2 call [mem], the operand value may be the IAT cell address.
        ptr = read_u64(v)
        if ptr and mapped(ptr):
            out["pointer_value"] = int(ptr)
            out["pointer_value_hex"] = hx(ptr)
            out["pointer_value_name"] = name(ptr)
            if not out["name"]:
                out["name"] = name(ptr)
    return out


def reg_def_before(items, call_index, reg, max_back=MAX_BACKTRACE):
    want = canon_reg(reg)
    start = max(0, call_index - max_back)
    for j in range(call_index - 1, start - 1, -1):
        ea = items[j]
        if dst_reg(ea) == want:
            return {"ea": int(ea), "ea_hex": hx(ea), "disasm": disasm(ea),
                    "mnem": mnem(ea), "sources": source_regs(ea),
                    "immediates": immediate_operands(ea), "stack_operands": stack_operands(ea),
                    "refs": refs_from(ea), "index": j}
        # A previous call may clobber caller-saved registers. Do not walk across
        # it and falsely attribute an older value to this call's argument.
        if is_call(ea) and want in ["rax", "rcx", "rdx", "rsi", "rdi", "r8", "r9", "r10", "r11"]:
            return {"clobbered_by_call": True, "barrier_ea": int(ea), "barrier_hex": hx(ea),
                    "barrier_disasm": disasm(ea)}
    return {"not_found_within_backtrace": True}


def trace_reg_before(items, call_index, reg, depth=0, seen=None):
    if seen is None:
        seen = []
    r = canon_reg(reg)
    if not r or r in seen or depth > MAX_TRACE_DEPTH:
        return {"register": r, "stop": "depth_or_cycle"}
    seen = seen + [r]
    d = reg_def_before(items, call_index, r)
    result = {"register": r}
    result.update(dict((k, v) for k, v in d.items() if k != "index"))
    if "index" in d:
        idx = d["index"]
        src = d.get("sources", [])
        # MOV register, register and simple arithmetic sources are followed as
        # independent evidence; no symbolic execution is attempted.
        if src:
            prev = []
            for sr in src[:2]:
                if sr == r:
                    continue
                prev.append(trace_reg_before(items, idx, sr, depth + 1, seen))
            if prev:
                result["source_register_history"] = prev
    return result


def function_stack_events(items):
    out = []
    for idx, ea in enumerate(items):
        mems = stack_operands(ea)
        if not mems:
            continue
        out.append({"index": idx, "ea": int(ea), "ea_hex": hx(ea), "disasm": disasm(ea),
                    "mnem": mnem(ea), "operands": mems, "immediates": immediate_operands(ea)})
        if len(out) >= MAX_STACK_EVENTS:
            break
    return out


def function_constants(items):
    hits = {}
    interesting = set(PARAM_IDS.keys()) | set(RACK_IDS.keys()) | set(CUSTOM_MODULE_IDS.keys()) | set([0x4D8, 0x4D0, 0x4E0, 0x13C, 0x1C, 0x1D, 0x1F])
    for ea in items:
        for imm in immediate_operands(ea):
            v = imm["value"] & 0xFFFFFFFF
            if v in interesting:
                key = hx(v)
                hits.setdefault(key, []).append({"ea": int(ea), "ea_hex": hx(ea), "disasm": disasm(ea),
                                                 "operand": imm["operand"], "float32": imm.get("float32")})
    return hits


def candidate_label(v):
    v = int(v) & 0xFFFFFFFF
    if v in PARAM_IDS:
        return "PARAM:" + PARAM_IDS[v]
    if v in RACK_IDS:
        return "RACK:" + RACK_IDS[v]
    if v in CUSTOM_MODULE_IDS:
        return "MODULE:" + CUSTOM_MODULE_IDS[v]
    if v == 0x4D8:
        return "SIZE_CANDIDATE:0x4D8"
    return ""


def resolve_call_name(ea):
    c = call_target(ea)
    n = c.get("name", "")
    if n.startswith("sceNgs2"):
        return n
    target = c.get("pointer_value") or c.get("target")
    if target and mapped(target):
        nm = name(target)
        if nm.startswith("sceNgs2"):
            return nm
        f = get_func(target)
        if f:
            # Follow a short thunk: jmp imported_api / jmp [IAT].
            for it in func_items(f)[:4]:
                if mnem(it).startswith("jmp"):
                    jt = call_target(it)
                    jn = jt.get("name", "")
                    if jn.startswith("sceNgs2"):
                        return jn
                    pv = jt.get("pointer_value")
                    if pv and name(pv).startswith("sceNgs2"):
                        return name(pv)
    return n


def call_sites_in_function(items):
    out = []
    for idx, ea in enumerate(items):
        if not is_call(ea):
            continue
        target = call_target(ea)
        api = resolve_call_name(ea)
        if api in API_NAMES or "ngs2" in api.lower():
            out.append({"index": idx, "ea": int(ea), "ea_hex": hx(ea), "api": api,
                        "target": target, "disasm": disasm(ea)})
    return out


def call_argument_snapshot(items, idx, api):
    args = API_ARGUMENTS.get(api, [])
    gprs = []
    for i, r in enumerate(GPR_ARGS):
        if i < len(args):
            label = args[i]
        else:
            label = "gpr_slot_%d_extra" % i
        gprs.append({"slot": i, "argument_name": label,
                     "register": r, "definition": trace_reg_before(items, idx, r)})
    xmms = []
    for r in XMM_ARGS:
        xmms.append({"register": r, "definition": trace_reg_before(items, idx, r)})
    return {"gpr_arguments": gprs, "xmm_registers": xmms,
            "note": "Register definitions are local backward slices, not full path-sensitive dataflow."}


def local_window(items, center_index, radius):
    a = max(0, center_index - radius)
    b = min(len(items), center_index + radius + 1)
    out = []
    for j in range(a, b):
        out.append(instruction_record(items[j]))
    return out


def nearest_stack_events(stack_events, center_index, radius=90):
    out = []
    for ev in stack_events:
        if abs(ev["index"] - center_index) <= radius:
            out.append(ev)
    return out


def data_targets_in_function(items):
    found = {}
    for ea in items:
        for r in refs_from(ea):
            to = r.get("to")
            if to and mapped(to) and not r.get("is_code"):
                key = int(to)
                if key not in found:
                    found[key] = {"address": key, "address_hex": hx(key), "name": name(key),
                                  "string": strings_at(key), "from": []}
                found[key]["from"].append({"ea": int(ea), "ea_hex": hx(ea), "disasm": disasm(ea)})
    for key in list(found.keys()):
        found[key]["preview"] = data_preview(key)
        if len(found[key]["from"]) > 40:
            found[key]["from"] = found[key]["from"][:40]
    return list(found.values())


def indirect_calls_in_function(items):
    out = []
    for idx, ea in enumerate(items):
        if not is_call(ea):
            continue
        t = call_target(ea)
        # Only genuine register/memory-indirect calls are callback candidates.
        # Unnamed direct calls are intentionally not mixed into this category.
        if t.get("indirect"):
            target_regs = registers_in_text(t.get("operand", ""))
            target_defs = []
            for target_reg in target_regs:
                target_defs.append({"register": target_reg, "definition": trace_reg_before(items, idx, target_reg)})
            out.append({"index": idx, "ea": int(ea), "ea_hex": hx(ea), "disasm": disasm(ea),
                        "target": t, "target_register_definitions": target_defs,
                        "arg_register_defs": call_argument_snapshot(items, idx, "")})
    return out


def all_register_snapshot(items, idx):
    regs = ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"]
    out = []
    for r in regs:
        out.append({"register": r, "definition": trace_reg_before(items, idx, r)})
    for r in XMM_ARGS:
        out.append({"register": r, "definition": trace_reg_before(items, idx, r)})
    return out


def caller_functions(func_ea):
    refs = xrefs_to(func_ea, True)
    seen = set()
    out = []
    for r in refs:
        fs = get_func(r["from"])
        if fs:
            st = fstart(fs)
            if st not in seen:
                seen.add(st)
                out.append({"start": int(st), "start_hex": hx(st), "name": name(st) or func_name(st),
                            "xref_from": r["from_hex"]})
    return out

# ------------------------------ Deep analysis -------------------------------

def analyse_function(spec, base):
    rva = int(spec["rva"])
    ea = base + rva
    f = get_func(ea)
    if not f:
        # Try a name-based fallback if the original database retained the IDA name.
        alt = name_ea("sub_%X" % rva)
        if not badaddr(alt):
            f = get_func(alt)
            if f:
                ea = alt
    if not f:
        return {"rva": hx(rva), "label": spec["label"], "found": False,
                "message": "IDA has no function at the expected EBOOT RVA. Check image base / EBOOT revision."}

    start = fstart(f)
    end = fend(f)
    items = func_items(f)
    idx_by_ea = dict((v, i) for i, v in enumerate(items))
    stack_events = function_stack_events(items)
    constants = function_constants(items)
    calls = call_sites_in_function(items)
    indirect = indirect_calls_in_function(items)
    targets = data_targets_in_function(items)

    # Exact anchors are expanded separately from NGS2 call sites. An anchor may
    # be a header write, callback assignment or another instruction of interest.
    anchor_eas = []
    for off in ANCHORS.get(rva, []):
        ae = base + int(off)
        if start <= ae < end:
            anchor_eas.append(ae)

    contexts = []
    marked = set()
    for c in calls:
        ce = c["ea"]
        if ce in marked:
            continue
        marked.add(ce)
        idx = c["index"]
        contexts.append({"kind": "NGS2_API_CALL", "ea": int(ce), "ea_hex": hx(ce), "api": c["api"],
                         "target": c["target"], "call_instruction": c["disasm"],
                         "arguments": call_argument_snapshot(items, idx, c["api"]),
                         "instruction_window": local_window(items, idx, MAX_CALL_WINDOW),
                         "nearby_stack_events": nearest_stack_events(stack_events, idx, 110)})
    for ae in anchor_eas:
        if ae in marked:
            continue
        marked.add(ae)
        idx = idx_by_ea.get(ae)
        if idx is None:
            # Resolve to closest instruction at or before the address.
            candidates = [i for i, it in enumerate(items) if it <= ae]
            if not candidates:
                continue
            idx = candidates[-1]
        contexts.append({"kind": "MANUAL_ANCHOR", "ea": int(items[idx]), "ea_hex": hx(items[idx]),
                         "requested_anchor": hx(ae), "instruction": disasm(items[idx]),
                         "instruction_window": local_window(items, idx, MAX_ANCHOR_WINDOW),
                         "nearby_stack_events": nearest_stack_events(stack_events, idx, 120),
                         "reg_snapshot": call_argument_snapshot(items, idx, ""),
                         "all_register_definitions": all_register_snapshot(items, idx)})

    # Highlight constants at exact instructions; candidate inventory remains
    # distinct from decoded parameter headers.
    candidate_hits = []
    for key, hits in constants.items():
        val = int(key, 16)
        candidate_hits.append({"value": key, "label": candidate_label(val), "count": len(hits), "sites": hits})
    candidate_hits.sort(key=lambda x: (-x["count"], x["value"]))

    full_asm = []
    for it in items:
        full_asm.append(instruction_record(it))

    return {
        "rva": hx(rva), "address": int(start), "address_hex": hx(start),
        "end": int(end), "end_hex": hx(end), "name": name(start) or func_name(start),
        "label": spec["label"], "found": True, "instruction_count": len(items),
        "callers": caller_functions(start), "ngs2_calls": calls,
        "indirect_calls": indirect, "data_targets": targets,
        "candidate_constants": candidate_hits, "stack_events": stack_events,
        "contexts": contexts, "disassembly": full_asm,
    }


def analyse_import_xrefs():
    out = []
    for api in API_NAMES:
        ea = name_ea(api)
        if badaddr(ea):
            out.append({"api": api, "import_ea": None, "found": False, "xrefs": []})
            continue
        out.append({"api": api, "import_ea": int(ea), "import_ea_hex": hx(ea), "found": True,
                    "xrefs": xrefs_to(ea, True)})
    return out


def summarize_constants(functions):
    summary = {}
    for f in functions:
        if not f.get("found"):
            continue
        for entry in f.get("candidate_constants", []):
            key = entry["value"]
            if key not in summary:
                summary[key] = {"value": key, "label": entry.get("label", ""), "functions": []}
            summary[key]["functions"].append({"function": f.get("name"), "rva": f.get("rva"),
                                                "count": entry.get("count"), "sites": entry.get("sites", [])})
    return list(summary.values())

# ------------------------------- Report output ------------------------------

def md_escape(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def make_markdown(report):
    lines = []
    lines.append("# NGS2 focused static reverse-engineering report")
    lines.append("")
    lines.append("> IDA 7.x / IDAPython; static analysis only. A function-wide constant is not proof that a parameter was passed to every call site.")
    lines.append("> Image base: `%s`; generated: `%s`." % (hx(report["image_base"]), report["generated_at"]))
    lines.append("")
    lines.append("## 1. Executive summary")
    lines.append("")
    lines.append("| Target function | Instructions | NGS2 API calls | Indirect calls | Data references |")
    lines.append("|---|---:|---:|---:|---:|")
    for f in report["functions"]:
        if not f.get("found"):
            lines.append("| `%s` | not found | — | — | — |" % f.get("label"))
        else:
            lines.append("| `%s` (`%s`) | %d | %d | %d | %d |" %
                          (md_escape(f.get("label")), md_escape(f.get("name")), f.get("instruction_count", 0),
                           len(f.get("ngs2_calls", [])), len(f.get("indirect_calls", [])), len(f.get("data_targets", []))))
    lines.append("")
    lines.append("## 2. NGS2 import xrefs")
    lines.append("")
    lines.append("| API | Import EA | Xref call sites |")
    lines.append("|---|---:|---:|")
    for api in report["import_xrefs"]:
        lines.append("| `%s` | `%s` | %d |" % (api["api"], api.get("import_ea_hex", "not found"), len(api.get("xrefs", []))))
    lines.append("")
    lines.append("## 3. Candidate constants across focused functions")
    lines.append("")
    lines.append("These are instruction operands observed in a function. They are not automatically parameter IDs passed to a specific `VoiceControl` call.")
    lines.append("")
    lines.append("| Value | Candidate meaning | Functions / hits |")
    lines.append("|---:|---|---|")
    for e in report["constant_summary"]:
        desc = []
        for fn in e.get("functions", []):
            desc.append("%s: %s" % (fn.get("function"), fn.get("count")))
        lines.append("| `%s` | %s | %s |" % (e["value"], md_escape(e.get("label", "")), md_escape(", ".join(desc))))
    lines.append("")

    for f in report["functions"]:
        lines.append("## 4. Function: `%s` — %s" % (f.get("name", f.get("label")), f.get("label")))
        lines.append("")
        if not f.get("found"):
            lines.append("**NOT FOUND:** %s" % f.get("message", ""))
            lines.append("")
            continue
        lines.append("- Range: `%s..%s`" % (f["address_hex"], f["end_hex"]))
        lines.append("- Instructions: %d" % f["instruction_count"])
        lines.append("- Callers: %s" % (", ".join(["`%s` (%s)" % (x["name"], x["xref_from"]) for x in f.get("callers", [])]) or "none identified"))
        lines.append("")
        lines.append("### NGS2 API calls in this function")
        lines.append("")
        if f.get("ngs2_calls"):
            lines.append("| EA | API | Target | Instruction |")
            lines.append("|---:|---|---:|---|")
            for c in f["ngs2_calls"]:
                lines.append("| `%s` | `%s` | `%s` | `%s` |" % (c["ea_hex"], c["api"], c["target"].get("target_hex"), md_escape(c["disasm"])))
        else:
            lines.append("No named NGS2 call was resolved in this function.")
        lines.append("")
        lines.append("### Candidate constants")
        lines.append("")
        if f.get("candidate_constants"):
            for c in f["candidate_constants"]:
                lines.append("- `%s` %s — %d hit(s): %s" % (c["value"], c.get("label", ""), c["count"],
                              ", ".join([x["ea_hex"] for x in c.get("sites", [])[:16]])))
        else:
            lines.append("No configured constants found.")
        lines.append("")
        lines.append("### Detailed call / anchor contexts")
        lines.append("")
        for ctx in f.get("contexts", []):
            lines.append("#### %s at `%s` %s" % (ctx.get("kind"), ctx.get("ea_hex"), ctx.get("api", "")))
            lines.append("")
            if ctx.get("arguments"):
                lines.append("**GPR argument backward slices**")
                lines.append("")
                for a in ctx["arguments"].get("gpr_arguments", []):
                    d = a.get("definition", {})
                    lines.append("- `%s` (%s): `%s` — `%s`" % (a["register"], a["argument_name"],
                                      d.get("ea_hex", "unresolved"), md_escape(d.get("disasm", d.get("barrier_disasm", "")))))
                lines.append("")
                lines.append("**XMM register definitions**")
                lines.append("")
                xmm_hits = []
                for a in ctx["arguments"].get("xmm_registers", []):
                    d = a.get("definition", {})
                    if d.get("ea_hex"):
                        xmm_hits.append("%s `%s` `%s`" % (a["register"], d["ea_hex"], md_escape(d.get("disasm", ""))))
                lines.extend(["- " + x for x in xmm_hits] if xmm_hits else ["- no nearby XMM writes resolved"])
                lines.append("")
            lines.append("**Instruction window**")
            lines.append("")
            lines.append("```asm")
            for ins in ctx.get("instruction_window", []):
                lines.append("%s  %-28s %s" % (ins["ea_hex"], ins.get("bytes", ""), ins.get("disasm", "")))
            lines.append("```")
            lines.append("")
            st = ctx.get("nearby_stack_events", [])
            if st:
                lines.append("**Nearby stack writes/reads**")
                lines.append("")
                lines.append("```asm")
                for ev in st:
                    lines.append("%s  %s" % (ev["ea_hex"], ev["disasm"]))
                lines.append("```")
                lines.append("")
        lines.append("### Indirect calls / callback candidates")
        lines.append("")
        if f.get("indirect_calls"):
            lines.append("| EA | Instruction | Operand / resolved target |")
            lines.append("|---:|---|---|")
            for c in f["indirect_calls"]:
                t = c.get("target", {})
                lines.append("| `%s` | `%s` | `%s / %s` |" % (c["ea_hex"], md_escape(c["disasm"]),
                              md_escape(t.get("operand", "")), md_escape(t.get("name", ""))))
        else:
            lines.append("No indirect calls identified.")
        lines.append("")
        lines.append("### Referenced data / pointer tables")
        lines.append("")
        if f.get("data_targets"):
            for d in f["data_targets"]:
                lines.append("- `%s` `%s` string=%s; referenced from %s" % (d["address_hex"], md_escape(d.get("name", "")),
                              md_escape(d.get("string", "") or ""), ", ".join([x["ea_hex"] for x in d.get("from", [])[:12]])))
                if d.get("preview"):
                    lines.append("  - bytes: `%s`" % d["preview"].get("bytes", "")[:240])
        else:
            lines.append("No mapped data references were resolved.")
        lines.append("")
        lines.append("### Full disassembly")
        lines.append("")
        lines.append("<details>")
        lines.append("<summary>Expand full function listing (%d instructions)</summary>" % f.get("instruction_count", 0))
        lines.append("")
        lines.append("```asm")
        for ins in f.get("disassembly", []):
            cmt = (" ; " + ins["comment"]) if ins.get("comment") else ""
            lines.append("%s  %-28s %s%s" % (ins["ea_hex"], ins.get("bytes", ""), ins.get("disasm", ""), cmt))
        lines.append("```")
        lines.append("")
        lines.append("</details>")
        lines.append("")
    lines.append("## 5. Interpretation rules")
    lines.append("")
    lines.append("1. A direct call/xref to an imported NGS2 symbol is strong evidence of an API call site.")
    lines.append("2. A direct stack write of a parameter ID immediately before `VoiceControl` is evidence of that parameter builder; payload fields still need interpretation.")
    lines.append("3. A function-wide immediate or a constant in a grouped signature is only a candidate until tied to the parameter pointer passed at that call.")
    lines.append("4. A register backtrace is bounded and not path-sensitive. Values crossing branches, calls, or aliases may remain unresolved.")
    lines.append("5. Callback candidates require tracing the assigned function pointer through indirect call sites and validating calling convention / lifetime.")
    lines.append("")
    return "\n".join(lines) + "\n"


def make_csv(report):
    rows = ["function,label,kind,ea,api,argument,register,definition_ea,definition_instruction"]
    for f in report["functions"]:
        if not f.get("found"):
            continue
        for ctx in f.get("contexts", []):
            if ctx.get("arguments"):
                for a in ctx["arguments"].get("gpr_arguments", []):
                    d = a.get("definition", {})
                    vals = [f.get("name", ""), f.get("label", ""), ctx.get("kind", ""), ctx.get("ea_hex", ""),
                            ctx.get("api", ""), a.get("argument_name", ""), a.get("register", ""),
                            d.get("ea_hex", ""), d.get("disasm", "")]
                    rows.append(",".join([csv_quote(x) for x in vals]))
    return "\n".join(rows) + "\n"


def csv_quote(v):
    s = str(v if v is not None else "")
    if '"' in s:
        s = s.replace('"', '""')
    if "," in s or "\n" in s or '"' in s:
        s = '"' + s + '"'
    return s


def output_directory():
    if OUTPUT_DIR:
        return OUTPUT_DIR
    candidates = []
    for fn in [getattr(idc, "get_idb_path", None), getattr(idc, "GetIdbPath", None)]:
        if fn:
            try:
                p = fn()
                if p:
                    candidates.append(os.path.dirname(p))
                    break
            except Exception:
                pass
    if not candidates:
        try:
            p = idaapi.get_input_file_path()
            if p:
                candidates.append(os.path.dirname(p))
        except Exception:
            pass
    return candidates[0] if candidates and candidates[0] else os.getcwd()


def write_text(path, content):
    # JSON/MD are emitted as UTF-8 for Python 2 and Python 3 IDA builds.
    if not isinstance(content, bytes):
        try:
            content = content.encode("utf-8")
        except Exception:
            content = str(content)
    f = open(path, "wb")
    try:
        f.write(content)
    finally:
        f.close()


def main():
    try:
        idaapi.auto_wait()
    except Exception:
        pass
    base = imagebase()
    msg("[NGS2 deep] image base = %s" % hx(base))
    functions = []
    for spec in TARGET_FUNCTIONS:
        msg("[NGS2 deep] analysing %s @ %s" % (spec["label"], hx(base + spec["rva"])))
        functions.append(analyse_function(spec, base))
    report = {
        "tool": "ngs2_ida7_deep_followup.py",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ida_version": getattr(idaapi, "get_kernel_version", lambda: "unknown")(),
        "input_file": "",
        "image_base": int(base),
        "image_base_hex": hx(base),
        "target_functions": TARGET_FUNCTIONS,
        "api_names": API_NAMES,
        "import_xrefs": analyse_import_xrefs(),
        "functions": functions,
        "constant_summary": summarize_constants(functions),
        "notes": [
            "Static analysis only; no EBOOT code execution.",
            "Function-wide constants are candidates, not proof of a VoiceControl payload.",
            "Register backtraces are bounded and not path-sensitive.",
            "All configured EBOOT offsets are based on the earlier image-base-0 IDA report.",
        ],
    }
    try:
        report["input_file"] = idaapi.get_input_file_path()
    except Exception:
        pass
    outdir = output_directory()
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    stem = "ngs2_deep_followup"
    json_path = os.path.join(outdir, stem + ".json")
    md_path = os.path.join(outdir, stem + ".md")
    csv_path = os.path.join(outdir, stem + ".csv")
    write_text(json_path, json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True))
    write_text(md_path, make_markdown(report))
    write_text(csv_path, make_csv(report))
    msg("[NGS2 deep] DONE")
    msg("[NGS2 deep] JSON: %s" % json_path)
    msg("[NGS2 deep] Markdown: %s" % md_path)
    msg("[NGS2 deep] CSV: %s" % csv_path)
    for f in functions:
        if f.get("found"):
            msg("[NGS2 deep] %s: %d instructions, %d API calls, %d indirect calls" %
                (f.get("name"), f.get("instruction_count", 0), len(f.get("ngs2_calls", [])), len(f.get("indirect_calls", []))))
        else:
            msg("[NGS2 deep] WARNING: %s not found" % f.get("label"))


try:
    main()
except Exception:
    msg("[NGS2 deep] FATAL ERROR")
    msg(traceback.format_exc())
