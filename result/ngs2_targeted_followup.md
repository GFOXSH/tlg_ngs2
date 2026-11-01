# NGS2 targeted follow-up
Input: `C:\Users\Admin\Desktop\11\SKOTOS4\eboot.elf`
Image base: `0x0`
## Full PS4 custom-submixer template
Address: `0x14DCAC8`; expected size: `0x4D8`; bytes read: `1240`.
Raw binary: `off_14DCAC8_0x4D8.bin`.
### Nonzero dwords
| Offset | Value | Decimal |
|---:|---:|---:|
| `0x0` | `0x4D8` | 1240 |
| `0x1C` | `0x200` | 512 |
| `0x20` | `0x1` | 1 |
| `0x24` | `0x1` | 1 |
| `0x28` | `0x1` | 1 |
| `0x2C` | `0x8` | 8 |
| `0x80` | `0xC` | 12 |
| `0x84` | `0x1` | 1 |
| `0x4D0` | `0x8` | 8 |
| `0x4D4` | `0x1` | 1 |

### Printable strings

## sub_1AB580 — sampler_user_fx_callback
Range: `0x1AB580`–`0x1AB91C`; 178 instructions.
### Xrefs to function
- `0x1AA068` `sub_1A9690` (1): `lea     rax, sub_1AB580`
### Disassembly
```asm
0x1AB580  push    rbp
0x1AB581  mov     rbp, rsp
0x1AB584  push    r15
0x1AB586  push    r14
0x1AB588  push    r12
0x1AB58A  push    rbx
0x1AB58B  sub     rsp, 250h
0x1AB592  mov     r15, cs:qword_1700698
0x1AB599  mov     r14, rdi
0x1AB59C  mov     rax, [r15]
0x1AB59F  mov     [rbp+var_28], rax
0x1AB5A3  mov     rax, [r14+8]
0x1AB5A7  mov     rdi, [rax+130h]
0x1AB5AE  test    rdi, rdi
0x1AB5B1  jz      loc_1AB8FC
0x1AB5B7  mov     r12, [rax+80h]
0x1AB5BE  test    r12, r12
0x1AB5C1  jz      loc_1AB8FC
0x1AB5C7  mov     eax, [r14+20h]
0x1AB5CB  and     eax, 0Ch
0x1AB5CE  jnz     loc_1AB8FC
0x1AB5D4  lea     rbx, [rbp+var_230]
0x1AB5DB  mov     rsi, rbx
0x1AB5DE  call    sub_1BFBE0
0x1AB5E3  mov     esi, 4Bh ; 'K'
0x1AB5E8  mov     rdi, rbx
0x1AB5EB  call    sub_1BD310
0x1AB5F0  vcvttss2si eax, xmm0
0x1AB5F4  vxorps  xmm0, xmm0, xmm0
0x1AB5F8  test    eax, eax
0x1AB5FA  jnz     short loc_1AB615
0x1AB5FC  lea     rdi, [rbp+var_230]
0x1AB603  mov     esi, 53h ; 'S'
0x1AB608  call    sub_1BD310
0x1AB60D  vxorps  xmm1, xmm1, xmm1
0x1AB611  vaddss  xmm0, xmm0, xmm1
0x1AB615  lea     rdi, [rbp+var_230]
0x1AB61C  mov     esi, 4Ch ; 'L'
0x1AB621  vmovss  [rbp+var_268], xmm0
0x1AB629  call    sub_1BD310
0x1AB62E  vcvttss2si eax, xmm0
0x1AB632  test    eax, eax
0x1AB634  jnz     short loc_1AB65B
0x1AB636  lea     rdi, [rbp+var_230]
0x1AB63D  mov     esi, 54h ; 'T'
0x1AB642  call    sub_1BD310
0x1AB647  vmovss  xmm1, [rbp+var_268]
0x1AB64F  vaddss  xmm1, xmm1, xmm0
0x1AB653  vmovss  [rbp+var_268], xmm1
0x1AB65B  lea     rdi, [rbp+var_230]
0x1AB662  mov     esi, 4Dh ; 'M'
0x1AB667  call    sub_1BD310
0x1AB66C  vcvttss2si eax, xmm0
0x1AB670  test    eax, eax
0x1AB672  jnz     short loc_1AB699
0x1AB674  lea     rdi, [rbp+var_230]
0x1AB67B  mov     esi, 55h ; 'U'
0x1AB680  call    sub_1BD310
0x1AB685  vmovss  xmm1, [rbp+var_268]
0x1AB68D  vaddss  xmm1, xmm1, xmm0
0x1AB691  vmovss  [rbp+var_268], xmm1
0x1AB699  lea     rdi, [rbp+var_230]
0x1AB6A0  mov     esi, 4Eh ; 'N'
0x1AB6A5  call    sub_1BD310
0x1AB6AA  vcvttss2si eax, xmm0
0x1AB6AE  test    eax, eax
0x1AB6B0  jnz     short loc_1AB6D7
0x1AB6B2  lea     rdi, [rbp+var_230]
0x1AB6B9  mov     esi, 56h ; 'V'
0x1AB6BE  call    sub_1BD310
0x1AB6C3  vmovss  xmm1, [rbp+var_268]
0x1AB6CB  vaddss  xmm1, xmm1, xmm0
0x1AB6CF  vmovss  [rbp+var_268], xmm1
0x1AB6D7  lea     rdi, [rbp+var_230]
0x1AB6DE  mov     esi, 4Fh ; 'O'
0x1AB6E3  call    sub_1BD310
0x1AB6E8  vcvttss2si eax, xmm0
0x1AB6EC  test    eax, eax
0x1AB6EE  jnz     short loc_1AB715
0x1AB6F0  lea     rdi, [rbp+var_230]
0x1AB6F7  mov     esi, 57h ; 'W'
0x1AB6FC  call    sub_1BD310
0x1AB701  vmovss  xmm1, [rbp+var_268]
0x1AB709  vaddss  xmm1, xmm1, xmm0
0x1AB70D  vmovss  [rbp+var_268], xmm1
0x1AB715  lea     rdi, [rbp+var_230]
0x1AB71C  mov     esi, 50h ; 'P'
0x1AB721  call    sub_1BD310
0x1AB726  vcvttss2si eax, xmm0
0x1AB72A  test    eax, eax
0x1AB72C  jnz     short loc_1AB753
0x1AB72E  lea     rdi, [rbp+var_230]
0x1AB735  mov     esi, 58h ; 'X'
0x1AB73A  call    sub_1BD310
0x1AB73F  vmovss  xmm1, [rbp+var_268]
0x1AB747  vaddss  xmm1, xmm1, xmm0
0x1AB74B  vmovss  [rbp+var_268], xmm1
0x1AB753  lea     rdi, [rbp+var_230]
0x1AB75A  mov     esi, 51h ; 'Q'
0x1AB75F  call    sub_1BD310
0x1AB764  vcvttss2si eax, xmm0
0x1AB768  test    eax, eax
0x1AB76A  jnz     short loc_1AB791
0x1AB76C  lea     rdi, [rbp+var_230]
0x1AB773  mov     esi, 59h ; 'Y'
0x1AB778  call    sub_1BD310
0x1AB77D  vmovss  xmm1, [rbp+var_268]
0x1AB785  vaddss  xmm1, xmm1, xmm0
0x1AB789  vmovss  [rbp+var_268], xmm1
0x1AB791  lea     rdi, [rbp+var_230]
0x1AB798  mov     esi, 52h ; 'R'
0x1AB79D  call    sub_1BD310
0x1AB7A2  vcvttss2si eax, xmm0
0x1AB7A6  test    eax, eax
0x1AB7A8  jz      short loc_1AB7B4
0x1AB7AA  vmovss  xmm0, [rbp+var_268]
0x1AB7B2  jmp     short loc_1AB7D5
0x1AB7B4  lea     rdi, [rbp+var_230]
0x1AB7BB  mov     esi, 5Ah ; 'Z'
0x1AB7C0  call    sub_1BD310
0x1AB7C5  vmovss  xmm1, [rbp+var_268]
0x1AB7CD  vaddss  xmm1, xmm1, xmm0
0x1AB7D1  vmovaps xmm0, xmm1
0x1AB7D5  vmulss  xmm0, xmm0, dword ptr [r12+6Ch]
0x1AB7DC  lea     rdx, [rbp+var_240]
0x1AB7E3  lea     rcx, [rbp+var_25C]
0x1AB7EA  mov     edi, cs:dword_1704BD8
0x1AB7F0  vmovss  [rbp+var_25C], xmm0
0x1AB7F8  vmovss  xmm0, dword ptr [r12+84h]
0x1AB802  mov     [rbp+var_264], 0
0x1AB80C  vmulss  xmm0, xmm0, cs:dword_14DAE48
0x1AB814  vmovss  [rbp+var_260], xmm0
0x1AB81C  mov     rax, [r12+88h]
0x1AB824  mov     [rbp+var_240], eax
0x1AB82A  shr     rax, 20h
0x1AB82E  mov     [rbp+var_23C], eax
0x1AB834  mov     eax, [r12+90h]
0x1AB83C  mov     [rbp+var_A0], 3
0x1AB846  mov     [rbp+var_98], rdx
0x1AB84D  mov     [rbp+var_90], 0Ch
0x1AB858  mov     [rbp+var_88], 5
0x1AB862  mov     [rbp+var_80], rcx
0x1AB866  lea     rdx, [rbp+var_260]
0x1AB86D  lea     rcx, [rbp+var_264]
0x1AB874  mov     [rbp+var_78], 4
0x1AB87C  mov     [rbp+var_70], 4
0x1AB883  mov     [rbp+var_258], 1
0x1AB88D  mov     [rbp+var_68], rdx
0x1AB891  mov     [rbp+var_60], 4
0x1AB899  mov     [rbp+var_58], 2
0x1AB8A0  mov     [rbp+var_50], rcx
0x1AB8A4  mov     [rbp+var_48], 4
0x1AB8AC  lea     rcx, [rbp+var_A0]
0x1AB8B3  mov     edx, 5
0x1AB8B8  mov     [rbp+var_238], eax
0x1AB8BE  mov     rax, [r14]
0x1AB8C1  mov     rax, [rax]
0x1AB8C4  mov     [rbp+var_250], rax
0x1AB8CB  mov     eax, [r14+28h]
0x1AB8CF  mov     [rbp+var_40], 1
0x1AB8D6  mov     [rbp+var_248], eax
0x1AB8DC  lea     rax, [rbp+var_258]
0x1AB8E3  mov     [rbp+var_38], rax
0x1AB8E7  mov     [rbp+var_30], 18h
0x1AB8EF  mov     esi, [r12+0A0h]
0x1AB8F7  call    sceAudio3dObjectSetAttributes
0x1AB8FC  mov     rax, [r15]
0x1AB8FF  cmp     rax, [rbp+var_28]
0x1AB903  jnz     short loc_1AB917
0x1AB905  xor     eax, eax
0x1AB907  add     rsp, 250h
0x1AB90E  pop     rbx
0x1AB90F  pop     r12
0x1AB911  pop     r14
0x1AB913  pop     r15
0x1AB915  pop     rbp
0x1AB916  retn
0x1AB917  call    __stack_chk_fail
```

## sub_1B2010 — mastering_limiter_helper
Range: `0x1B2010`–`0x1B2128`; 88 instructions.
### Xrefs to function
- `0x1ADE60` `sub_1ADC10` (17): `call    sub_1B2010`
- `0x1AF4B0` `sub_1AEFD0` (17): `call    sub_1B2010`
- `0x1AF518` `sub_1AEFD0` (17): `call    sub_1B2010`
- `0x1AF576` `sub_1AEFD0` (17): `call    sub_1B2010`
- `0x1AF581` `sub_1AEFD0` (17): `call    sub_1B2010`
### Disassembly
```asm
0x1B2010  mov     r8d, 1
0x1B2016  jmp     short loc_1B2023
0x1B2018  align 20h
0x1B2020  inc     rdi
0x1B2023  movsx   eax, byte ptr [rdi]
0x1B2026  cmp     eax, 1Fh
0x1B2029  jle     short loc_1B2040
0x1B202B  movzx   eax, al
0x1B202E  cmp     eax, 20h ; ' '
0x1B2031  jz      short loc_1B2020
0x1B2033  jmp     short loc_1B204A
0x1B2035  align 20h
0x1B2040  movzx   eax, al
0x1B2043  cmp     eax, 9
0x1B2046  jz      short loc_1B2020
0x1B2048  jmp     short loc_1B2062
0x1B204A  cmp     eax, 2Bh ; '+'
0x1B204D  jz      short loc_1B205F
0x1B204F  cmp     eax, 2Dh ; '-'
0x1B2052  jnz     short loc_1B2062
0x1B2054  inc     rdi
0x1B2057  mov     r8d, 0FFFFFFFFh
0x1B205D  jmp     short loc_1B2062
0x1B205F  inc     rdi
0x1B2062  movzx   edx, byte ptr [rdi]
0x1B2065  cmp     edx, 24h ; '$'
0x1B2068  jnz     short loc_1B20DB
0x1B206A  mov     dl, [rdi+1]
0x1B206D  xor     eax, eax
0x1B206F  test    dl, dl
0x1B2071  jz      loc_1B211C
0x1B2077  add     rdi, 2
0x1B207B  xor     eax, eax
0x1B207D  nop     dword ptr [rax]
0x1B2080  mov     esi, eax
0x1B2082  movsx   eax, dl
0x1B2085  mov     cl, al
0x1B2087  shl     esi, 4
0x1B208A  add     cl, 0D0h
0x1B208D  movzx   ecx, cl
0x1B2090  cmp     ecx, 9
0x1B2093  ja      short loc_1B20A0
0x1B2095  add     eax, 0FFFFFFD0h
0x1B2098  jmp     short loc_1B20CE
0x1B209A  align 20h
0x1B20A0  mov     cl, dl
0x1B20A2  add     cl, 9Fh
0x1B20A5  movzx   ecx, cl
0x1B20A8  cmp     ecx, 5
0x1B20AB  ja      short loc_1B20C0
0x1B20AD  add     eax, 0FFFFFFA9h
0x1B20B0  jmp     short loc_1B20CE
0x1B20B2  align 20h
0x1B20C0  add     dl, 0BFh
0x1B20C3  movzx   ecx, dl
0x1B20C6  cmp     ecx, 5
0x1B20C9  ja      short loc_1B2121
0x1B20CB  add     eax, 0FFFFFFC9h
0x1B20CE  mov     dl, [rdi]
0x1B20D0  add     eax, esi
0x1B20D2  inc     rdi
0x1B20D5  test    dl, dl
0x1B20D7  jnz     short loc_1B2080
0x1B20D9  jmp     short loc_1B211C
0x1B20DB  mov     sil, dl
0x1B20DE  xor     eax, eax
0x1B20E0  add     sil, 0D0h
0x1B20E4  movzx   esi, sil
0x1B20E8  cmp     esi, 9
0x1B20EB  ja      short loc_1B211C
0x1B20ED  inc     rdi
0x1B20F0  xor     eax, eax
0x1B20F2  nop     word ptr [rax+rax+00000000h]
0x1B2100  movsx   ecx, dl
0x1B2103  mov     dl, [rdi]
0x1B2105  lea     eax, [rax+rax*4]
0x1B2108  inc     rdi
0x1B210B  lea     eax, [rcx+rax*2-30h]
0x1B210F  mov     cl, dl
0x1B2111  add     cl, 0D0h
0x1B2114  movzx   ecx, cl
0x1B2117  cmp     ecx, 0Ah
0x1B211A  jb      short loc_1B2100
0x1B211C  imul    eax, r8d
0x1B2120  retn
0x1B2121  mov     eax, esi
0x1B2123  imul    eax, r8d
0x1B2127  retn
```

## sub_1B1C70 — rack_module_option_helper
Range: `0x1B1C70`–`0x1B1CBE`; 31 instructions.
### Xrefs to function
- `0x1A5C92` `sub_1A5B80` (17): `call    sub_1B1C70`
- `0x1A622C` `sub_1A6150` (17): `call    sub_1B1C70`
- `0x1A6923` `sub_1A68F0` (17): `call    sub_1B1C70`
- `0x1A70B0` `sub_1A69C0` (17): `call    sub_1B1C70`
- `0x1A74C7` `sub_1A69C0` (17): `call    sub_1B1C70`
- `0x1A7E5A` `sub_1A69C0` (17): `call    sub_1B1C70`
- `0x1A7E7A` `sub_1A69C0` (17): `call    sub_1B1C70`
- `0x1A849A` `sub_1A83A0` (17): `call    sub_1B1C70`
- `0x1A84BA` `sub_1A83A0` (17): `call    sub_1B1C70`
- `0x1A8502` `sub_1A83A0` (17): `call    sub_1B1C70`
- `0x1A8513` `sub_1A83A0` (17): `call    sub_1B1C70`
- `0x1AC68D` `sub_1AC510` (17): `call    sub_1B1C70`
- `0x1AC7EF` `sub_1AC510` (17): `call    sub_1B1C70`
- `0x1AC818` `sub_1AC510` (17): `call    sub_1B1C70`
- `0x1ACA8C` `sub_1AC510` (17): `call    sub_1B1C70`
- `0x1ACBFD` `sub_1AC510` (17): `call    sub_1B1C70`
- `0x1ACD5D` `sub_1AC510` (17): `call    sub_1B1C70`
- `0x1ACD86` `sub_1AC510` (17): `call    sub_1B1C70`
- `0x1ACEE5` `sub_1AC510` (17): `call    sub_1B1C70`
- `0x1AD053` `sub_1AC510` (17): `call    sub_1B1C70`
- `0x1AD1BE` `sub_1AC510` (17): `call    sub_1B1C70`
- `0x1AD329` `sub_1AC510` (17): `call    sub_1B1C70`
- `0x1AD352` `sub_1AC510` (17): `call    sub_1B1C70`
- `0x1AD3A0` `sub_1AC510` (17): `call    sub_1B1C70`
- `0x1AD506` `sub_1AC510` (17): `call    sub_1B1C70`
- `0x1AD543` `sub_1AC510` (17): `call    sub_1B1C70`
- `0x1AD6BD` `sub_1AC510` (17): `call    sub_1B1C70`
- `0x1AD6E6` `sub_1AC510` (17): `call    sub_1B1C70`
- `0x1AD845` `sub_1AC510` (17): `call    sub_1B1C70`
- `0x1AD86E` `sub_1AC510` (17): `call    sub_1B1C70`
- `0x1ADAEC` `sub_1AC510` (17): `call    sub_1B1C70`
- `0x1ADBD5` `sub_1ADB70` (17): `call    sub_1B1C70`
- `0x1BAFD3` `sub_1BAFA0` (17): `call    sub_1B1C70`
- `0x1BD182` `sub_1BD170` (17): `call    sub_1B1C70`
- `0x1BD1AE` `sub_1BD1A0` (17): `call    sub_1B1C70`
- `0x1BD1C7` `sub_1BD1A0` (17): `call    sub_1B1C70`
- `0x1BDBBD` `` (17): `call    sub_1B1C70`
- `0x1C11DE` `` (17): `call    sub_1B1C70`
- `0x1C22A5` `` (17): `call    sub_1B1C70`
- `0x1C23B7` `` (17): `call    sub_1B1C70`
- `0x1C3889` `sub_1C3850` (17): `call    sub_1B1C70`
- `0x1C53B2` `sub_1C3950` (17): `call    sub_1B1C70`
- `0x1C81D5` `` (17): `call    sub_1B1C70`
- `0x1C81E6` `` (17): `call    sub_1B1C70`
- `0x1C81F7` `` (17): `call    sub_1B1C70`
- `0x1C8208` `` (17): `call    sub_1B1C70`
- `0x1C821D` `` (17): `call    sub_1B1C70`
- `0x1C822E` `` (17): `call    sub_1B1C70`
- `0x1C829E` `` (17): `call    sub_1B1C70`
- `0x1C82AD` `` (17): `call    sub_1B1C70`
- `0x1C830D` `` (17): `call    sub_1B1C70`
- `0x1C835F` `` (17): `call    sub_1B1C70`
- `0x1C83B1` `` (17): `call    sub_1B1C70`
- `0x1C8403` `` (17): `call    sub_1B1C70`
- `0x1CA9DC` `` (17): `call    sub_1B1C70`
- `0x1CA9ED` `` (17): `call    sub_1B1C70`
- `0x1CABC5` `` (17): `call    sub_1B1C70`
- `0x1CAC0B` `` (17): `call    sub_1B1C70`
- `0x1CD610` `sub_1CCDB0` (17): `call    sub_1B1C70`
- `0x1CEB3E` `sub_1CCDB0` (17): `call    sub_1B1C70`
- `0x1D1021` `sub_1CCDB0` (17): `call    sub_1B1C70`
- `0x1D1032` `sub_1CCDB0` (17): `call    sub_1B1C70`
- `0x1D3144` `` (17): `call    sub_1B1C70`
- `0x1D6C05` `sub_1D6BF0` (17): `call    sub_1B1C70`
- `0x1DA8E3` `sub_1DA8B0` (17): `call    sub_1B1C70`
- `0x1DAC42` `sub_1DAC10` (17): `call    sub_1B1C70`
- `0x1DB1F5` `sub_1DB1C0` (17): `call    sub_1B1C70`
- `0x1DB49C` `sub_1DB460` (17): `call    sub_1B1C70`
- `0x1DC9CF` `sub_1DC9B0` (17): `call    sub_1B1C70`
- `0x1DCB01` `sub_1DC9F0` (17): `call    sub_1B1C70`
- `0x1DCB28` `sub_1DC9F0` (17): `call    sub_1B1C70`
- `0x1DCDDE` `sub_1DCB90` (17): `call    sub_1B1C70`
- `0x1DF2B1` `sub_1DF290` (17): `call    sub_1B1C70`
- `0x1E005F` `sub_1DFF40` (17): `call    sub_1B1C70`
- `0x1E00D9` `sub_1DFF40` (17): `call    sub_1B1C70`
- `0x1E02E1` `sub_1DFF40` (17): `call    sub_1B1C70`
- `0x1E035C` `sub_1DFF40` (17): `call    sub_1B1C70`
- `0x1E1009` `sub_1E0FE0` (17): `call    sub_1B1C70`
- `0x1E21AB` `sub_1E1EB0` (17): `call    sub_1B1C70`
- `0x1E26E6` `sub_1E25B0` (17): `call    sub_1B1C70`
- `0x1E2BDA` `sub_1E2AC0` (17): `call    sub_1B1C70`
- `0x1E2BEB` `sub_1E2AC0` (17): `call    sub_1B1C70`
- `0x1E2F16` `sub_1E2EB0` (17): `call    sub_1B1C70`
- `0x1E314A` `` (17): `call    sub_1B1C70`
- `0x1E315B` `` (17): `call    sub_1B1C70`
- `0x1E3273` `` (17): `call    sub_1B1C70`
- `0x1E34BA` `` (17): `call    sub_1B1C70`
- `0x1E34DA` `` (17): `call    sub_1B1C70`
- `0x1E361A` `sub_1E3510` (17): `call    sub_1B1C70`
- `0x1E363A` `sub_1E3510` (17): `call    sub_1B1C70`
- `0x1E3F86` `sub_1E3F60` (17): `call    sub_1B1C70`
- `0x1E3FA2` `sub_1E3F60` (17): `call    sub_1B1C70`
- `0x1E3FC2` `sub_1E3F60` (17): `call    sub_1B1C70`
- `0x1E3FD3` `sub_1E3F60` (17): `call    sub_1B1C70`
- `0x1E4373` `sub_1E4340` (17): `call    sub_1B1C70`
- `0x1E5B1A` `sub_1E5AB0` (17): `call    sub_1B1C70`
- `0x1E5B2E` `sub_1E5AB0` (17): `call    sub_1B1C70`
- `0x1E5B42` `sub_1E5AB0` (17): `call    sub_1B1C70`
- `0x1E5BB1` `sub_1E5AB0` (17): `call    sub_1B1C70`
- `0x1E5BC2` `sub_1E5AB0` (17): `call    sub_1B1C70`
- `0x1E5BD3` `sub_1E5AB0` (17): `call    sub_1B1C70`
- `0x1E5BE4` `sub_1E5AB0` (17): `call    sub_1B1C70`
- `0x1E5BF5` `sub_1E5AB0` (17): `call    sub_1B1C70`
- `0x1E5C06` `sub_1E5AB0` (17): `call    sub_1B1C70`
- `0x1E5C17` `sub_1E5AB0` (17): `call    sub_1B1C70`
- `0x1E5C28` `sub_1E5AB0` (17): `call    sub_1B1C70`
- `0x1E6E78` `sub_1E6BD0` (17): `call    sub_1B1C70`
- `0x1E70D2` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E70E4` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E70F6` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E7108` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E711A` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E712C` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E713E` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E7150` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E7399` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E73B0` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E73C2` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E74C9` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E75C9` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E75DB` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E7B09` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E87C2` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E8D58` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E95F9` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E960B` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E9A38` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E9A4A` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E9B41` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1E9B53` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1EA10A` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1EA11C` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1EA2E9` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1EA2FB` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1EABB3` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1EABC5` `sub_1E70A0` (17): `call    sub_1B1C70`
- `0x1EADA5` `sub_1EAD90` (17): `call    sub_1B1C70`
- `0x1EE4F5` `sub_1EE4E0` (17): `call    sub_1B1C70`
- `0x1EF64C` `` (17): `call    sub_1B1C70`
- `0x1F161A` `sub_1F1090` (17): `call    sub_1B1C70`
- `0x1F16CE` `sub_1F1090` (17): `call    sub_1B1C70`
- `0x1F1A44` `sub_1F1090` (17): `call    sub_1B1C70`
- `0x1F1D6D` `sub_1F1CB0` (17): `call    sub_1B1C70`
- `0x1F1E6A` `sub_1F1CB0` (17): `call    sub_1B1C70`
- `0x1F29C5` `sub_1F29B0` (17): `call    sub_1B1C70`
- `0x1F6DE5` `sub_1F6840` (17): `call    sub_1B1C70`
- `0x1F6F6D` `sub_1F6840` (17): `call    sub_1B1C70`
- `0x1F73DF` `sub_1F7340` (17): `call    sub_1B1C70`
- `0x1F7406` `sub_1F7340` (17): `call    sub_1B1C70`
- `0x1F7417` `sub_1F7340` (17): `call    sub_1B1C70`
- `0x1F7DDA` `sub_1F7D20` (17): `call    sub_1B1C70`
- `0x1F7DEC` `sub_1F7D20` (17): `call    sub_1B1C70`
- `0x1F9D69` `sub_1F9D20` (17): `call    sub_1B1C70`
- `0x1FAC48` `sub_1FABA0` (17): `call    sub_1B1C70`
- `0x1FADF0` `` (17): `call    sub_1B1C70`
- `0x1FC09E` `sub_1FBFA0` (17): `call    sub_1B1C70`
- `0x1FC412` `sub_1FC3D0` (17): `call    sub_1B1C70`
- `0x1FCA70` `sub_1FC3D0` (17): `call    sub_1B1C70`
- `0x1FCCC2` `sub_1FC3D0` (17): `call    sub_1B1C70`
- `0x1FCCE1` `sub_1FC3D0` (17): `call    sub_1B1C70`
- `0x1FCCFB` `sub_1FC3D0` (17): `call    sub_1B1C70`
- `0x1FCD1D` `sub_1FC3D0` (17): `call    sub_1B1C70`
- `0x1FCD3F` `sub_1FC3D0` (17): `call    sub_1B1C70`
- `0x1FCD61` `sub_1FC3D0` (17): `call    sub_1B1C70`
- `0x1FD17B` `sub_1FD0B0` (17): `call    sub_1B1C70`
- `0x1FD19E` `sub_1FD0B0` (17): `call    sub_1B1C70`
- `0x1FD1BF` `sub_1FD0B0` (17): `call    sub_1B1C70`
- `0x1FD1E8` `sub_1FD0B0` (17): `call    sub_1B1C70`
- `0x1FD211` `sub_1FD0B0` (17): `call    sub_1B1C70`
- `0x1FD23A` `sub_1FD0B0` (17): `call    sub_1B1C70`
- `0x1FD25B` `sub_1FD0B0` (17): `call    sub_1B1C70`
### Disassembly
```asm
0x1B1C70  push    rbp
0x1B1C71  mov     rbp, rsp
0x1B1C74  push    rbx
0x1B1C75  push    rax
0x1B1C76  mov     rbx, rdi
0x1B1C79  mov     rax, rsi
0x1B1C7C  mov     rcx, rbx
0x1B1C7F  or      rcx, rax
0x1B1C82  test    cl, 3
0x1B1C85  jz      short loc_1B1C96
0x1B1C87  test    cl, 1
0x1B1C8A  jnz     short loc_1B1CA2
0x1B1C8C  shr     rax, 1
0x1B1C8F  jz      short loc_1B1CB4
0x1B1C91  add     rax, rax
0x1B1C94  jmp     short loc_1B1CA7
0x1B1C96  shr     rax, 2
0x1B1C9A  jz      short loc_1B1CB4
0x1B1C9C  shl     rax, 2
0x1B1CA0  jmp     short loc_1B1CA7
0x1B1CA2  test    rax, rax
0x1B1CA5  jz      short loc_1B1CB4
0x1B1CA7  xor     esi, esi
0x1B1CA9  mov     rdi, rbx
0x1B1CAC  mov     rdx, rax
0x1B1CAF  call    memset
0x1B1CB4  mov     rax, rbx
0x1B1CB7  add     rsp, 8
0x1B1CBB  pop     rbx
0x1B1CBC  pop     rbp
0x1B1CBD  retn
```

## sub_1AC510 — custom_submixer_rack_builder
Range: `0x1AC510`–`0x1ADB61`; 963 instructions.
### Xrefs to function
- `0x1A5EE2` `sub_1A5B80` (17): `call    sub_1AC510`
- `0x1A5F04` `sub_1A5B80` (17): `call    sub_1AC510`
### Disassembly
```asm
0x1AC510  push    rbp
0x1AC511  mov     rbp, rsp
0x1AC514  push    r15
0x1AC516  push    r14
0x1AC518  push    r13
0x1AC51A  push    r12
0x1AC51C  push    rbx
0x1AC51D  sub     rsp, 0D98h
0x1AC524  mov     r14, cs:qword_1700698
0x1AC52B  mov     r15, rdx
0x1AC52E  mov     rbx, rsi
0x1AC531  mov     [rbp+var_DA0], rdi
0x1AC538  test    r15, r15
0x1AC53B  mov     rax, [r14]
0x1AC53E  mov     [rbp+var_30], rax
0x1AC542  jz      short loc_1AC54B
0x1AC544  mov     qword ptr [r15], 0
0x1AC54B  mov     rax, 3030303030303030h
0x1AC555  xor     r8d, r8d
0x1AC558  mov     [rbp+var_688], rax
0x1AC55F  mov     [rbp+var_690], rax
0x1AC566  mov     [rbp+var_698], rax
0x1AC56D  mov     [rbp+var_6A0], rax
0x1AC574  mov     [rbp+var_6A8], rax
0x1AC57B  mov     [rbp+var_6B0], rax
0x1AC582  mov     [rbp+var_6B8], rax
0x1AC589  mov     [rbp+var_6C0], rax
0x1AC590  mov     [rbp+var_6C8], rax
0x1AC597  mov     [rbp+var_6D0], rax
0x1AC59E  mov     [rbp+var_6D8], rax
0x1AC5A5  mov     [rbp+var_6E0], rax
0x1AC5AC  mov     [rbp+var_6E8], rax
0x1AC5B3  mov     [rbp+var_6F0], rax
0x1AC5BA  mov     [rbp+var_6F8], rax
0x1AC5C1  mov     [rbp+var_700], rax
0x1AC5C8  mov     eax, [rbx]
0x1AC5CA  test    rax, rax
0x1AC5CD  jz      short loc_1AC609
0x1AC5CF  mov     rcx, [rbx+8]
0x1AC5D3  xor     edx, edx
0x1AC5D5  xor     r8d, r8d
0x1AC5D8  nop     dword ptr [rax+rax+00000000h]
0x1AC5E0  mov     esi, [rcx+rdx*4]
0x1AC5E3  mov     byte ptr [rbp+rsi+var_700], 31h ; '1'
0x1AC5EB  mov     esi, [rcx+rdx*4]
0x1AC5EE  cmp     r8d, esi
0x1AC5F1  cmovb   r8d, esi
0x1AC5F5  inc     rdx
0x1AC5F8  cmp     rdx, rax
0x1AC5FB  jb      short loc_1AC5E0
0x1AC5FD  movzx   eax, byte ptr [rbp+var_700]
0x1AC604  cmp     eax, 30h ; '0'
0x1AC607  jnz     short loc_1AC610
0x1AC609  mov     byte ptr [rbp+var_700], 31h ; '1'
0x1AC610  mov     rax, cs:qword_57F1C20
0x1AC617  inc     r8d
0x1AC61A  lea     rdx, aNumgrainsDNumb; "numGrains=%d numBusses=%d bussIdMap=%s"
0x1AC621  lea     rdi, [rbp+var_B00]
0x1AC628  lea     r9, [rbp+var_700]
0x1AC62F  mov     esi, 400h
0x1AC634  xor     r12d, r12d
0x1AC637  mov     byte ptr [rbp+r8+var_700], 0
0x1AC640  mov     ecx, [rax+4]
0x1AC643  xor     eax, eax
0x1AC645  call    sub_1B32F0
0x1AC64A  mov     eax, [rbx+10h]
0x1AC64D  mov     rdi, [rbp+var_DA0]
0x1AC654  mov     edx, 1
0x1AC659  imul    rsi, rax, 250h
0x1AC660  call    sub_1B3BD0
0x1AC665  cmp     dword ptr [rbx+10h], 0
0x1AC669  mov     r13, rax
0x1AC66C  jz      loc_1ADABB
0x1AC672  mov     [rbp+var_DB0], r15
0x1AC679  jmp     loc_1AC830
0x1AC67E  lea     rax, [rbp+var_D90]
0x1AC685  mov     esi, 8
0x1AC68A  mov     rdi, rax
0x1AC68D  call    sub_1B1C70
0x1AC692  lea     r15, [rbp+var_678]
0x1AC699  mov     edx, 4D8h
0x1AC69E  lea     rsi, off_14DCAC8
0x1AC6A5  mov     dword ptr [rbp+var_D90], 8
0x1AC6AF  mov     rdi, r15
0x1AC6B2  call    memcpy
0x1AC6B7  lea     rax, [rbp+var_D90]
0x1AC6BE  mov     edi, 4002h
0x1AC6C3  mov     rsi, r15
0x1AC6C6  lea     rdx, [rbp+var_1A0]
0x1AC6CD  mov     [rbp+var_5F0], 1
0x1AC6D7  mov     [rbp+var_5F4], 1
0x1AC6E1  mov     [rbp+var_5DC], 0
0x1AC6EB  mov     [rbp+var_5D4], 0
0x1AC6F5  mov     [rbp+var_5E0], 20h ; ' '
0x1AC6FF  mov     [rbp+var_5E8], rax
0x1AC706  mov     [rbp+var_228], 0
0x1AC710  call    sceNgs2RackQueryBufferSize
0x1AC715  test    eax, eax
0x1AC717  js      loc_1ADB35
0x1AC71D  mov     rsi, [rbp+var_198]
0x1AC724  mov     rdi, [rbp+var_DA0]
0x1AC72B  mov     edx, 1
0x1AC730  call    sub_1B3BD0
0x1AC735  mov     [rbp+var_1A0], rax
0x1AC73C  test    rax, rax
0x1AC73F  jz      loc_1AD873
0x1AC745  mov     esi, 4002h
0x1AC74A  mov     rdi, r14
0x1AC74D  lea     rdx, [rbp+var_678]
0x1AC754  lea     rcx, [rbp+var_1A0]
0x1AC75B  lea     r8, [rbp+var_D78]
0x1AC762  call    sceNgs2RackCreate
0x1AC767  test    eax, eax
0x1AC769  js      loc_1ADB35
0x1AC76F  mov     rdi, [rbp+var_D78]
0x1AC776  xor     esi, esi
0x1AC778  lea     rdx, [rbp+var_D70]
0x1AC77F  call    sceNgs2RackGetVoiceHandle
0x1AC784  mov     rdi, [rbp+var_D70]
0x1AC78B  vmovups xmm0, cs:xmmword_14DAD80
0x1AC793  lea     rsi, [rbp+var_D68]
0x1AC79A  mov     [rbp+var_D68], 18h
0x1AC7A3  mov     [rbp+var_D66], 0
0x1AC7AC  vmovups [rbp+var_D64], xmm0
0x1AC7B4  mov     [rbp+var_D54], 0
0x1AC7BE  call    sceNgs2VoiceControl
0x1AC7C3  mov     rax, [rbp+var_D78]
0x1AC7CA  lea     rdi, aPitch_0; "PITCH"
0x1AC7D1  mov     [rbp+var_D50], rax
0x1AC7D8  call    sub_1B1580
0x1AC7DD  mov     esi, 50h ; 'P'
0x1AC7E2  lea     rdi, [rbp+var_D40]
0x1AC7E9  mov     [rbp+var_D44], eax
0x1AC7EF  call    sub_1B1C70
0x1AC7F4  lea     rax, [rbp+var_D38]
0x1AC7FB  mov     esi, 0Ch
0x1AC800  lea     rdi, [rbp+var_B1C]
0x1AC807  mov     [rbp+var_D40], 8
0x1AC811  mov     [rbp+var_CF8], rax
0x1AC818  call    sub_1B1C70
0x1AC81D  mov     [rbp+var_B1C], 8
0x1AC827  jmp     loc_1AD873
0x1AC82C  align 10h
0x1AC830  mov     rax, cs:qword_57F1C20
0x1AC837  mov     r12d, r12d
0x1AC83A  lea     rsi, aThru; "THRU"
0x1AC841  lea     rcx, [r12+r12*2]
0x1AC845  mov     [rbp+var_D98], rcx
0x1AC84C  mov     r14, [rax+60h]
0x1AC850  mov     rax, [rbx+18h]
0x1AC854  mov     r15, [rax+rcx*8+8]
0x1AC859  mov     rdi, r15
0x1AC85C  call    sub_1B1E90
0x1AC861  test    eax, eax
0x1AC863  jz      loc_1ACAC0
0x1AC869  mov     rdi, r15
0x1AC86C  lea     rsi, aEq_0; "EQ"
0x1AC873  call    sub_1B1E90
0x1AC878  test    eax, eax
0x1AC87A  jz      loc_1ACC20
0x1AC880  mov     rdi, r15
0x1AC883  lea     rsi, aComp; "COMP"
0x1AC88A  call    sub_1B1E90
0x1AC88F  test    eax, eax
0x1AC891  jz      loc_1ACDA8
0x1AC897  mov     rdi, r15
0x1AC89A  lea     rsi, aReverb; "REVERB"
0x1AC8A1  call    sub_1B1E90
0x1AC8A6  test    eax, eax
0x1AC8A8  jz      loc_1ACF13
0x1AC8AE  mov     rdi, r15
0x1AC8B1  lea     rsi, aDisto; "DISTO"
0x1AC8B8  call    sub_1B1E90
0x1AC8BD  test    eax, eax
0x1AC8BF  jz      loc_1AD081
0x1AC8C5  mov     rdi, r15
0x1AC8C8  lea     rsi, aUmix; "UMIX"
0x1AC8CF  call    sub_1B1E90
0x1AC8D4  test    eax, eax
0x1AC8D6  jz      loc_1AD1EC
0x1AC8DC  mov     rdi, r15
0x1AC8DF  lea     rsi, aChorus; "CHORUS"
0x1AC8E6  call    sub_1B1E90
0x1AC8EB  test    eax, eax
0x1AC8ED  jz      loc_1AD394
0x1AC8F3  mov     rdi, r15
0x1AC8F6  lea     rsi, aDelay_0; "DELAY"
0x1AC8FD  call    sub_1B1E90
0x1AC902  test    eax, eax
0x1AC904  jz      loc_1AD534
0x1AC90A  mov     rdi, r15
0x1AC90D  lea     rsi, off_14DB98D
0x1AC914  call    sub_1B1E90
0x1AC919  test    eax, eax
0x1AC91B  jz      loc_1AD708
0x1AC921  mov     rdi, r15
0x1AC924  lea     rsi, aPitch_0; "PITCH"
0x1AC92B  call    sub_1B1E90
0x1AC930  test    eax, eax
0x1AC932  jz      loc_1AC67E
0x1AC938  mov     rdi, r15
0x1AC93B  lea     rsi, aPanner; "PANNER"
0x1AC942  call    sub_1B1E90
0x1AC947  test    eax, eax
0x1AC949  jnz     loc_1AD873
0x1AC94F  vmovups ymm0, cs:ymmword_14DC960+18h
0x1AC957  vmovups ymm2, cs:ymmword_14DC960
0x1AC95F  vmovups ymm1, cs:ymmword_14DC940
0x1AC967  mov     edi, 2000h
0x1AC96C  lea     rsi, [rbp+var_D0]
0x1AC973  lea     rdx, [rbp+var_1A0]
0x1AC97A  vmovups ymmword ptr [rbp+anonymous_0+18h], ymm0
0x1AC97F  vmovups ymmword ptr [rbp-70h], ymm2
0x1AC984  vmovups [rbp+var_90], ymm1
0x1AC98C  vmovups ymm2, cs:ymmword_14DC920
0x1AC994  vmovups ymm1, cs:ymmword_14DC900
0x1AC99C  vmovups [rbp+var_B0], ymm2
0x1AC9A4  vmovups [rbp+var_D0], ymm1
0x1AC9AC  call    sceNgs2RackQueryBufferSize
0x1AC9B1  test    eax, eax
0x1AC9B3  js      loc_1ADB35
0x1AC9B9  mov     rsi, [rbp+var_198]
0x1AC9C0  mov     rdi, [rbp+var_DA0]
0x1AC9C7  mov     edx, 1
0x1AC9CC  call    sub_1B3BD0
0x1AC9D1  mov     [rbp+var_1A0], rax
0x1AC9D8  test    rax, rax
0x1AC9DB  jz      loc_1AD873
0x1AC9E1  mov     esi, 2000h
0x1AC9E6  mov     rdi, r14
0x1AC9E9  lea     rdx, [rbp+var_D0]
0x1AC9F0  lea     rcx, [rbp+var_1A0]
0x1AC9F7  lea     r8, [rbp+var_D78]
0x1AC9FE  call    sceNgs2RackCreate
0x1ACA03  test    eax, eax
0x1ACA05  js      loc_1ADB35
0x1ACA0B  mov     rdi, [rbp+var_D78]
0x1ACA12  xor     esi, esi
0x1ACA14  lea     rdx, [rbp+var_D70]
0x1ACA1B  call    sceNgs2RackGetVoiceHandle
0x1ACA20  mov     rdi, [rbp+var_D70]
0x1ACA27  lea     rsi, [rbp+var_678]
0x1ACA2E  mov     rax, 820000000h
0x1ACA38  mov     [rbp+var_678], 10h
0x1ACA41  mov     [rbp+var_676], 0
0x1ACA4A  mov     qword ptr [rbp+var_674], rax
0x1ACA51  mov     dword ptr [rbp+var_674+8], 0
0x1ACA5B  call    sceNgs2VoiceControl
0x1ACA60  mov     rax, [rbp+var_D78]
0x1ACA67  lea     rdi, aPanner; "PANNER"
0x1ACA6E  mov     [rbp+var_D50], rax
0x1ACA75  call    sub_1B1580
0x1ACA7A  mov     esi, 50h ; 'P'
0x1ACA7F  lea     rdi, [rbp+var_D40]
0x1ACA86  mov     [rbp+var_D44], eax
0x1ACA8C  call    sub_1B1C70
0x1ACA91  lea     rax, [rbp+var_D38]
0x1ACA98  mov     esi, 0Ch
0x1ACA9D  lea     rdi, [rbp+var_B10]
0x1ACAA4  mov     [rbp+var_D40], 8
0x1ACAAE  mov     [rbp+var_CF8], rax
0x1ACAB5  jmp     loc_1AD86E
0x1ACABA  align 20h
0x1ACAC0  vmovups ymm0, cs:ymmword_14DC960+18h
0x1ACAC8  vmovups ymm2, cs:ymmword_14DC960
0x1ACAD0  vmovups ymm1, cs:ymmword_14DC940
0x1ACAD8  mov     edi, 2000h
0x1ACADD  lea     rsi, [rbp+var_D0]
0x1ACAE4  lea     rdx, [rbp+var_1A0]
0x1ACAEB  vmovups ymmword ptr [rbp+anonymous_0+18h], ymm0
0x1ACAF0  vmovups ymmword ptr [rbp-70h], ymm2
0x1ACAF5  vmovups [rbp+var_90], ymm1
0x1ACAFD  vmovups ymm2, cs:ymmword_14DC920
0x1ACB05  vmovups ymm1, cs:ymmword_14DC900
0x1ACB0D  vmovups [rbp+var_B0], ymm2
0x1ACB15  vmovups [rbp+var_D0], ymm1
0x1ACB1D  call    sceNgs2RackQueryBufferSize
0x1ACB22  test    eax, eax
0x1ACB24  js      loc_1ADB35
0x1ACB2A  mov     rsi, [rbp+var_198]
0x1ACB31  mov     rdi, [rbp+var_DA0]
0x1ACB38  mov     edx, 1
0x1ACB3D  call    sub_1B3BD0
0x1ACB42  mov     [rbp+var_1A0], rax
0x1ACB49  test    rax, rax
0x1ACB4C  jz      loc_1AD873
0x1ACB52  mov     esi, 2000h
0x1ACB57  mov     rdi, r14
0x1ACB5A  lea     rdx, [rbp+var_D0]
0x1ACB61  lea     rcx, [rbp+var_1A0]
0x1ACB68  lea     r8, [rbp+var_D78]
0x1ACB6F  call    sceNgs2RackCreate
0x1ACB74  test    eax, eax
0x1ACB76  js      loc_1ADB35
0x1ACB7C  mov     rdi, [rbp+var_D78]
0x1ACB83  xor     esi, esi
0x1ACB85  lea     rdx, [rbp+var_D70]
0x1ACB8C  call    sceNgs2RackGetVoiceHandle
0x1ACB91  mov     rdi, [rbp+var_D70]
0x1ACB98  lea     rsi, [rbp+var_678]
0x1ACB9F  mov     rax, 820000000h
0x1ACBA9  mov     [rbp+var_678], 10h
0x1ACBB2  mov     [rbp+var_676], 0
0x1ACBBB  mov     qword ptr [rbp+var_674], rax
0x1ACBC2  mov     dword ptr [rbp+var_674+8], 0
0x1ACBCC  call    sceNgs2VoiceControl
0x1ACBD1  mov     rax, [rbp+var_D78]
0x1ACBD8  lea     rdi, aThru; "THRU"
0x1ACBDF  mov     [rbp+var_D50], rax
0x1ACBE6  call    sub_1B1580
0x1ACBEB  mov     esi, 50h ; 'P'
0x1ACBF0  lea     rdi, [rbp+var_D40]
0x1ACBF7  mov     [rbp+var_D44], eax
0x1ACBFD  call    sub_1B1C70
0x1ACC02  lea     rax, [rbp+var_D38]
0x1ACC09  mov     [rbp+var_D40], 8
0x1ACC13  mov     [rbp+var_CF8], rax
0x1ACC1A  jmp     loc_1AD873
0x1ACC1F  align 20h
0x1ACC20  vmovups ymm0, cs:ymmword_14DC960+18h
0x1ACC28  vmovups ymm2, cs:ymmword_14DC960
0x1ACC30  vmovups ymm1, cs:ymmword_14DC940
0x1ACC38  mov     edi, 2000h
0x1ACC3D  lea     rsi, [rbp+var_D0]
0x1ACC44  lea     rdx, [rbp+var_1A0]
0x1ACC4B  vmovups ymmword ptr [rbp+anonymous_0+18h], ymm0
0x1ACC50  vmovups ymmword ptr [rbp-70h], ymm2
0x1ACC55  vmovups [rbp+var_90], ymm1
0x1ACC5D  vmovups ymm2, cs:ymmword_14DC920
0x1ACC65  vmovups ymm1, cs:ymmword_14DC900
0x1ACC6D  vmovups [rbp+var_B0], ymm2
0x1ACC75  vmovups [rbp+var_D0], ymm1
0x1ACC7D  call    sceNgs2RackQueryBufferSize
0x1ACC82  test    eax, eax
0x1ACC84  js      loc_1ADB35
0x1ACC8A  mov     rsi, [rbp+var_198]
0x1ACC91  mov     rdi, [rbp+var_DA0]
0x1ACC98  mov     edx, 1
0x1ACC9D  call    sub_1B3BD0
0x1ACCA2  mov     [rbp+var_1A0], rax
0x1ACCA9  test    rax, rax
0x1ACCAC  jz      loc_1AD873
0x1ACCB2  mov     esi, 2000h
0x1ACCB7  mov     rdi, r14
0x1ACCBA  lea     rdx, [rbp+var_D0]
0x1ACCC1  lea     rcx, [rbp+var_1A0]
0x1ACCC8  lea     r8, [rbp+var_D78]
0x1ACCCF  call    sceNgs2RackCreate
0x1ACCD4  test    eax, eax
0x1ACCD6  js      loc_1ADB35
0x1ACCDC  mov     rdi, [rbp+var_D78]
0x1ACCE3  xor     esi, esi
0x1ACCE5  lea     rdx, [rbp+var_D70]
0x1ACCEC  call    sceNgs2RackGetVoiceHandle
0x1ACCF1  mov     rdi, [rbp+var_D70]
0x1ACCF8  lea     rsi, [rbp+var_678]
0x1ACCFF  mov     rax, 820000000h
0x1ACD09  mov     [rbp+var_678], 10h
0x1ACD12  mov     [rbp+var_676], 0
0x1ACD1B  mov     qword ptr [rbp+var_674], rax
0x1ACD22  mov     dword ptr [rbp+var_674+8], 0
0x1ACD2C  call    sceNgs2VoiceControl
0x1ACD31  mov     rax, [rbp+var_D78]
0x1ACD38  lea     rdi, aEq_0; "EQ"
0x1ACD3F  mov     [rbp+var_D50], rax
0x1ACD46  call    sub_1B1580
0x1ACD4B  mov     esi, 50h ; 'P'
0x1ACD50  lea     rdi, [rbp+var_D40]
0x1ACD57  mov     [rbp+var_D44], eax
0x1ACD5D  call    sub_1B1C70
0x1ACD62  lea     rax, [rbp+var_D38]
0x1ACD69  mov     esi, 98h
0x1ACD6E  lea     rdi, [rbp+var_CF0]
0x1ACD75  mov     [rbp+var_D40], 8
0x1ACD7F  mov     [rbp+var_CF8], rax
0x1ACD86  call    sub_1B1C70
0x1ACD8B  lea     rax, [rbp+var_CEC]
0x1ACD92  mov     [rbp+var_CF0], 8
0x1ACD9C  mov     [rbp+var_C68], rax
0x1ACDA3  jmp     loc_1AD873
0x1ACDA8  vmovups ymm0, cs:ymmword_14DC960+18h
0x1ACDB0  vmovups ymm2, cs:ymmword_14DC960
0x1ACDB8  vmovups ymm1, cs:ymmword_14DC940
0x1ACDC0  mov     edi, 2000h
0x1ACDC5  lea     rsi, [rbp+var_D0]
0x1ACDCC  lea     rdx, [rbp+var_1A0]
0x1ACDD3  vmovups ymmword ptr [rbp+anonymous_0+18h], ymm0
0x1ACDD8  vmovups ymmword ptr [rbp-70h], ymm2
0x1ACDDD  vmovups [rbp+var_90], ymm1
0x1ACDE5  vmovups ymm2, cs:ymmword_14DC920
0x1ACDED  vmovups ymm1, cs:ymmword_14DC900
0x1ACDF5  vmovups [rbp+var_B0], ymm2
0x1ACDFD  vmovups [rbp+var_D0], ymm1
0x1ACE05  call    sceNgs2RackQueryBufferSize
0x1ACE0A  test    eax, eax
0x1ACE0C  js      loc_1ADB35
0x1ACE12  mov     rsi, [rbp+var_198]
0x1ACE19  mov     rdi, [rbp+var_DA0]
0x1ACE20  mov     edx, 1
0x1ACE25  call    sub_1B3BD0
0x1ACE2A  mov     [rbp+var_1A0], rax
0x1ACE31  test    rax, rax
0x1ACE34  jz      loc_1AD873
0x1ACE3A  mov     esi, 2000h
0x1ACE3F  mov     rdi, r14
0x1ACE42  lea     rdx, [rbp+var_D0]
0x1ACE49  lea     rcx, [rbp+var_1A0]
0x1ACE50  lea     r8, [rbp+var_D78]
0x1ACE57  call    sceNgs2RackCreate
0x1ACE5C  test    eax, eax
0x1ACE5E  js      loc_1ADB35
0x1ACE64  mov     rdi, [rbp+var_D78]
0x1ACE6B  xor     esi, esi
0x1ACE6D  lea     rdx, [rbp+var_D70]
0x1ACE74  call    sceNgs2RackGetVoiceHandle
0x1ACE79  mov     rdi, [rbp+var_D70]
0x1ACE80  lea     rsi, [rbp+var_678]
0x1ACE87  mov     rax, 820000000h
0x1ACE91  mov     [rbp+var_678], 10h
0x1ACE9A  mov     [rbp+var_676], 0
0x1ACEA3  mov     qword ptr [rbp+var_674], rax
0x1ACEAA  mov     dword ptr [rbp+var_674+8], 0
0x1ACEB4  call    sceNgs2VoiceControl
0x1ACEB9  mov     rax, [rbp+var_D78]
0x1ACEC0  lea     rdi, aComp; "COMP"
0x1ACEC7  mov     [rbp+var_D50], rax
0x1ACECE  call    sub_1B1580
0x1ACED3  mov     esi, 50h ; 'P'
0x1ACED8  lea     rdi, [rbp+var_D40]
0x1ACEDF  mov     [rbp+var_D44], eax
0x1ACEE5  call    sub_1B1C70
0x1ACEEA  lea     rax, [rbp+var_D38]
0x1ACEF1  mov     [rbp+var_D40], 8
0x1ACEFB  mov     esi, 18h
0x1ACF00  lea     rdi, [rbp+var_C58]
0x1ACF07  mov     [rbp+var_CF8], rax
0x1ACF0E  jmp     loc_1AD86E
0x1ACF13  mov     rax, cs:qword_14DCAC0
0x1ACF1A  vmovups ymm0, cs:ymmword_14DCAA0
0x1ACF22  vmovups ymm1, cs:ymmword_14DCA80
0x1ACF2A  vmovups ymm2, cs:ymmword_14DCA60
0x1ACF32  mov     edi, 2001h
0x1ACF37  lea     rsi, [rbp+var_160]
0x1ACF3E  lea     rdx, [rbp+var_1A0]
0x1ACF45  mov     [rbp+var_E0], rax
0x1ACF4C  vmovups [rbp+var_100], ymm0
0x1ACF54  vmovups [rbp+var_120], ymm1
0x1ACF5C  vmovups ymm1, cs:ymmword_14DCA40
0x1ACF64  vmovups [rbp+var_140], ymm2
0x1ACF6C  vmovups [rbp+var_160], ymm1
0x1ACF74  call    sceNgs2RackQueryBufferSize
0x1ACF79  test    eax, eax
0x1ACF7B  js      loc_1ADB35
0x1ACF81  mov     rsi, [rbp+var_198]
0x1ACF88  mov     rdi, [rbp+var_DA0]
0x1ACF8F  mov     edx, 1
0x1ACF94  call    sub_1B3BD0
0x1ACF99  mov     [rbp+var_1A0], rax
0x1ACFA0  test    rax, rax
0x1ACFA3  jz      loc_1AD873
0x1ACFA9  mov     esi, 2001h
0x1ACFAE  mov     rdi, r14
0x1ACFB1  lea     rdx, [rbp+var_160]
0x1ACFB8  lea     rcx, [rbp+var_1A0]
0x1ACFBF  lea     r8, [rbp+var_D78]
0x1ACFC6  call    sceNgs2RackCreate
0x1ACFCB  test    eax, eax
0x1ACFCD  js      loc_1ADB35
0x1ACFD3  mov     rdi, [rbp+var_D78]
0x1ACFDA  xor     esi, esi
0x1ACFDC  lea     rdx, [rbp+var_D70]
0x1ACFE3  call    sceNgs2RackGetVoiceHandle
0x1ACFE8  mov     rdi, [rbp+var_D70]
0x1ACFEF  vmovups xmm0, cs:xmmword_14DAD90
0x1ACFF7  lea     rsi, [rbp+var_678]
0x1ACFFE  mov     [rbp+var_678], 18h
0x1AD007  mov     [rbp+var_676], 0
0x1AD010  vmovups [rbp+var_674], xmm0
0x1AD018  mov     [rbp+var_664], 0
0x1AD022  call    sceNgs2VoiceControl
0x1AD027  mov     rax, [rbp+var_D78]
0x1AD02E  lea     rdi, aReverb; "REVERB"
0x1AD035  mov     [rbp+var_D50], rax
0x1AD03C  call    sub_1B1580
0x1AD041  mov     esi, 50h ; 'P'
0x1AD046  lea     rdi, [rbp+var_D40]
0x1AD04D  mov     [rbp+var_D44], eax
0x1AD053  call    sub_1B1C70
0x1AD058  lea     rax, [rbp+var_D38]
0x1AD05F  mov     [rbp+var_D40], 8
0x1AD069  mov     esi, 38h ; '8'
0x1AD06E  lea     rdi, [rbp+var_C40]
0x1AD075  mov     [rbp+var_CF8], rax
0x1AD07C  jmp     loc_1AD86E
0x1AD081  vmovups ymm0, cs:ymmword_14DC960+18h
0x1AD089  vmovups ymm2, cs:ymmword_14DC960
0x1AD091  vmovups ymm1, cs:ymmword_14DC940
0x1AD099  mov     edi, 2000h
0x1AD09E  lea     rsi, [rbp+var_D0]
0x1AD0A5  lea     rdx, [rbp+var_1A0]
0x1AD0AC  vmovups ymmword ptr [rbp+anonymous_0+18h], ymm0
0x1AD0B1  vmovups ymmword ptr [rbp-70h], ymm2
0x1AD0B6  vmovups [rbp+var_90], ymm1
0x1AD0BE  vmovups ymm2, cs:ymmword_14DC920
0x1AD0C6  vmovups ymm1, cs:ymmword_14DC900
0x1AD0CE  vmovups [rbp+var_B0], ymm2
0x1AD0D6  vmovups [rbp+var_D0], ymm1
0x1AD0DE  call    sceNgs2RackQueryBufferSize
0x1AD0E3  test    eax, eax
0x1AD0E5  js      loc_1ADB35
0x1AD0EB  mov     rsi, [rbp+var_198]
0x1AD0F2  mov     rdi, [rbp+var_DA0]
0x1AD0F9  mov     edx, 1
0x1AD0FE  call    sub_1B3BD0
0x1AD103  mov     [rbp+var_1A0], rax
0x1AD10A  test    rax, rax
0x1AD10D  jz      loc_1AD873
0x1AD113  mov     esi, 2000h
0x1AD118  mov     rdi, r14
0x1AD11B  lea     rdx, [rbp+var_D0]
0x1AD122  lea     rcx, [rbp+var_1A0]
0x1AD129  lea     r8, [rbp+var_D78]
0x1AD130  call    sceNgs2RackCreate
0x1AD135  test    eax, eax
0x1AD137  js      loc_1ADB35
0x1AD13D  mov     rdi, [rbp+var_D78]
0x1AD144  xor     esi, esi
0x1AD146  lea     rdx, [rbp+var_D70]
0x1AD14D  call    sceNgs2RackGetVoiceHandle
0x1AD152  mov     rdi, [rbp+var_D70]
0x1AD159  lea     rsi, [rbp+var_678]
0x1AD160  mov     rax, 820000000h
0x1AD16A  mov     [rbp+var_678], 10h
0x1AD173  mov     [rbp+var_676], 0
0x1AD17C  mov     qword ptr [rbp+var_674], rax
0x1AD183  mov     dword ptr [rbp+var_674+8], 0
0x1AD18D  call    sceNgs2VoiceControl
0x1AD192  mov     rax, [rbp+var_D78]
0x1AD199  lea     rdi, aDisto; "DISTO"
0x1AD1A0  mov     [rbp+var_D50], rax
0x1AD1A7  call    sub_1B1580
0x1AD1AC  mov     esi, 50h ; 'P'
0x1AD1B1  lea     rdi, [rbp+var_D40]
0x1AD1B8  mov     [rbp+var_D44], eax
0x1AD1BE  call    sub_1B1C70
0x1AD1C3  lea     rax, [rbp+var_D38]
0x1AD1CA  mov     [rbp+var_D40], 8
0x1AD1D4  mov     esi, 8
0x1AD1D9  lea     rdi, [rbp+var_C08]
0x1AD1E0  mov     [rbp+var_CF8], rax
0x1AD1E7  jmp     loc_1AD86E
0x1AD1EC  vmovups ymm0, cs:ymmword_14DC960+18h
0x1AD1F4  vmovups ymm2, cs:ymmword_14DC960
0x1AD1FC  vmovups ymm1, cs:ymmword_14DC940
0x1AD204  mov     edi, 2000h
0x1AD209  lea     rsi, [rbp+var_D0]
0x1AD210  lea     rdx, [rbp+var_1A0]
0x1AD217  vmovups ymmword ptr [rbp+anonymous_0+18h], ymm0
0x1AD21C  vmovups ymmword ptr [rbp-70h], ymm2
0x1AD221  vmovups [rbp+var_90], ymm1
0x1AD229  vmovups ymm2, cs:ymmword_14DC920
0x1AD231  vmovups ymm1, cs:ymmword_14DC900
0x1AD239  vmovups [rbp+var_B0], ymm2
0x1AD241  vmovups [rbp+var_D0], ymm1
0x1AD249  call    sceNgs2RackQueryBufferSize
0x1AD24E  test    eax, eax
0x1AD250  js      loc_1ADB35
0x1AD256  mov     rsi, [rbp+var_198]
0x1AD25D  mov     rdi, [rbp+var_DA0]
0x1AD264  mov     edx, 1
0x1AD269  call    sub_1B3BD0
0x1AD26E  mov     [rbp+var_1A0], rax
0x1AD275  test    rax, rax
0x1AD278  jz      loc_1AD357
0x1AD27E  mov     esi, 2000h
0x1AD283  mov     rdi, r14
0x1AD286  lea     rdx, [rbp+var_D0]
0x1AD28D  lea     rcx, [rbp+var_1A0]
0x1AD294  lea     r8, [rbp+var_D78]
0x1AD29B  call    sceNgs2RackCreate
0x1AD2A0  test    eax, eax
0x1AD2A2  js      loc_1ADB35
0x1AD2A8  mov     rdi, [rbp+var_D78]
0x1AD2AF  xor     esi, esi
0x1AD2B1  lea     rdx, [rbp+var_D70]
0x1AD2B8  call    sceNgs2RackGetVoiceHandle
0x1AD2BD  mov     rdi, [rbp+var_D70]
0x1AD2C4  lea     rsi, [rbp+var_678]
0x1AD2CB  mov     rax, 820000000h
0x1AD2D5  mov     [rbp+var_678], 10h
0x1AD2DE  mov     [rbp+var_676], 0
0x1AD2E7  mov     qword ptr [rbp+var_674], rax
0x1AD2EE  mov     dword ptr [rbp+var_674+8], 0
0x1AD2F8  call    sceNgs2VoiceControl
0x1AD2FD  mov     rax, [rbp+var_D78]
0x1AD304  lea     rdi, aUmix; "UMIX"
0x1AD30B  mov     [rbp+var_D50], rax
0x1AD312  call    sub_1B1580
0x1AD317  mov     esi, 50h ; 'P'
0x1AD31C  lea     rdi, [rbp+var_D40]
0x1AD323  mov     [rbp+var_D44], eax
0x1AD329  call    sub_1B1C70
0x1AD32E  lea     rax, [rbp+var_D38]
0x1AD335  mov     esi, 58h ; 'X'
0x1AD33A  lea     rdi, [rbp+var_C00]
0x1AD341  mov     [rbp+var_D40], 8
0x1AD34B  mov     [rbp+var_CF8], rax
0x1AD352  call    sub_1B1C70
0x1AD357  call    sub_1E6B20
0x1AD35C  mov     rdi, [rbp+var_DA0]
0x1AD363  movsxd  rsi, eax
0x1AD366  mov     edx, 1
0x1AD36B  call    sub_1B3BD0
0x1AD370  mov     [rbp+var_BB0], rax
0x1AD377  test    rax, rax
0x1AD37A  jz      loc_1AD873
0x1AD380  lea     rdi, [rbp+var_C00]
0x1AD387  mov     rsi, rax
0x1AD38A  call    sub_1E6B30
0x1AD38F  jmp     loc_1AD873
0x1AD394  mov     esi, 0Ch
0x1AD399  lea     rdi, [rbp+var_D90]
0x1AD3A0  call    sub_1B1C70
0x1AD3A5  lea     r15, [rbp+var_678]
0x1AD3AC  mov     rax, 40000000Ch
0x1AD3B6  mov     edx, 4D8h
0x1AD3BB  lea     rsi, off_14DCAC8
0x1AD3C2  mov     rdi, r15
0x1AD3C5  mov     [rbp+var_D90], rax
0x1AD3CC  call    memcpy
0x1AD3D1  mov     edi, 4002h
0x1AD3D6  mov     rsi, r15
0x1AD3D9  lea     rdx, [rbp+var_1A0]
0x1AD3E0  mov     [rbp+var_5F0], 1
0x1AD3EA  mov     [rbp+var_5F4], 1
0x1AD3F4  mov     [rbp+var_5DC], 0
0x1AD3FE  mov     [rbp+var_5D4], 0
0x1AD408  mov     [rbp+var_5E0], 1Ch
0x1AD412  mov     [rbp+var_5E8], 0
0x1AD41D  mov     [rbp+var_228], 0
0x1AD427  call    sceNgs2RackQueryBufferSize
0x1AD42C  test    eax, eax
0x1AD42E  js      loc_1ADB35
0x1AD434  mov     rsi, [rbp+var_198]
0x1AD43B  mov     rdi, [rbp+var_DA0]
0x1AD442  mov     edx, 1
0x1AD447  call    sub_1B3BD0
0x1AD44C  mov     [rbp+var_1A0], rax
0x1AD453  test    rax, rax
0x1AD456  jz      loc_1AD873
0x1AD45C  mov     esi, 4002h
0x1AD461  mov     rdi, r14
0x1AD464  lea     rdx, [rbp+var_678]
0x1AD46B  lea     rcx, [rbp+var_1A0]
0x1AD472  lea     r8, [rbp+var_D78]
0x1AD479  call    sceNgs2RackCreate
0x1AD47E  test    eax, eax
0x1AD480  js      loc_1ADB35
0x1AD486  mov     rdi, [rbp+var_D78]
0x1AD48D  xor     esi, esi
0x1AD48F  lea     rdx, [rbp+var_D70]
0x1AD496  call    sceNgs2RackGetVoiceHandle
0x1AD49B  mov     rdi, [rbp+var_D70]
0x1AD4A2  vmovups xmm0, cs:xmmword_14DAD80
0x1AD4AA  lea     rsi, [rbp+var_D68]
0x1AD4B1  mov     [rbp+var_D68], 18h
0x1AD4BA  mov     [rbp+var_D66], 0
0x1AD4C3  vmovups [rbp+var_D64], xmm0
0x1AD4CB  mov     [rbp+var_D54], 0
0x1AD4D5  call    sceNgs2VoiceControl
0x1AD4DA  mov     rax, [rbp+var_D78]
0x1AD4E1  lea     rdi, aChorus; "CHORUS"
0x1AD4E8  mov     [rbp+var_D50], rax
0x1AD4EF  call    sub_1B1580
0x1AD4F4  mov     esi, 50h ; 'P'
0x1AD4F9  lea     rdi, [rbp+var_D40]
0x1AD500  mov     [rbp+var_D44], eax
0x1AD506  call    sub_1B1C70
0x1AD50B  lea     rax, [rbp+var_D38]
0x1AD512  mov     [rbp+var_D40], 8
0x1AD51C  mov     esi, 20h ; ' '
0x1AD521  lea     rdi, [rbp+var_BA8]
0x1AD528  mov     [rbp+var_CF8], rax
0x1AD52F  jmp     loc_1AD86E
0x1AD534  lea     rax, [rbp+var_D90]
0x1AD53B  mov     esi, 14h
0x1AD540  mov     rdi, rax
0x1AD543  call    sub_1B1C70
0x1AD548  lea     r15, [rbp+var_678]
0x1AD54F  mov     rax, 100000014h
0x1AD559  mov     rcx, 447A000000000008h
0x1AD563  mov     edx, 4D8h
0x1AD568  lea     rsi, off_14DCAC8
0x1AD56F  mov     rdi, r15
0x1AD572  mov     [rbp+var_D90], rax
0x1AD579  mov     [rbp+var_D88], rcx
0x1AD580  call    memcpy
0x1AD585  lea     rax, [rbp+var_D90]
0x1AD58C  mov     edi, 4002h
0x1AD591  mov     rsi, r15
0x1AD594  lea     rdx, [rbp+var_1A0]
0x1AD59B  mov     [rbp+var_5F0], 1
0x1AD5A5  mov     [rbp+var_5F4], 1
0x1AD5AF  mov     [rbp+var_5DC], 0
0x1AD5B9  mov     [rbp+var_5D4], 0
0x1AD5C3  mov     [rbp+var_5E0], 1Dh
0x1AD5CD  mov     [rbp+var_5E8], rax
0x1AD5D4  mov     [rbp+var_228], 0
0x1AD5DE  call    sceNgs2RackQueryBufferSize
0x1AD5E3  test    eax, eax
0x1AD5E5  js      loc_1ADB35
0x1AD5EB  mov     rsi, [rbp+var_198]
0x1AD5F2  mov     rdi, [rbp+var_DA0]
0x1AD5F9  mov     edx, 1
0x1AD5FE  call    sub_1B3BD0
0x1AD603  mov     [rbp+var_1A0], rax
0x1AD60A  test    rax, rax
0x1AD60D  jz      loc_1AD873
0x1AD613  mov     esi, 4002h
0x1AD618  mov     rdi, r14
0x1AD61B  lea     rdx, [rbp+var_678]
0x1AD622  lea     rcx, [rbp+var_1A0]
0x1AD629  lea     r8, [rbp+var_D78]
0x1AD630  call    sceNgs2RackCreate
0x1AD635  test    eax, eax
0x1AD637  js      loc_1ADB35
0x1AD63D  mov     rdi, [rbp+var_D78]
0x1AD644  xor     esi, esi
0x1AD646  lea     rdx, [rbp+var_D70]
0x1AD64D  call    sceNgs2RackGetVoiceHandle
0x1AD652  mov     rdi, [rbp+var_D70]
0x1AD659  vmovups xmm0, cs:xmmword_14DAD80
0x1AD661  lea     rsi, [rbp+var_D68]
0x1AD668  mov     [rbp+var_D68], 18h
0x1AD671  mov     [rbp+var_D66], 0
0x1AD67A  vmovups [rbp+var_D64], xmm0
0x1AD682  mov     [rbp+var_D54], 0
0x1AD68C  call    sceNgs2VoiceControl
0x1AD691  mov     rax, [rbp+var_D78]
0x1AD698  lea     rdi, aDelay_0; "DELAY"
0x1AD69F  mov     [rbp+var_D50], rax
0x1AD6A6  call    sub_1B1580
0x1AD6AB  mov     esi, 50h ; 'P'
0x1AD6B0  lea     rdi, [rbp+var_D40]
0x1AD6B7  mov     [rbp+var_D44], eax
0x1AD6BD  call    sub_1B1C70
0x1AD6C2  lea     rax, [rbp+var_D38]
0x1AD6C9  mov     esi, 68h ; 'h'
0x1AD6CE  lea     rdi, [rbp+var_B88]
0x1AD6D5  mov     [rbp+var_D40], 8
0x1AD6DF  mov     [rbp+var_CF8], rax
0x1AD6E6  call    sub_1B1C70
0x1AD6EB  lea     rax, [rbp+var_B7C]
0x1AD6F2  mov     [rbp+var_B84], 8
0x1AD6FC  mov     [rbp+var_B38], rax
0x1AD703  jmp     loc_1AD873
0x1AD708  vmovups ymm0, cs:ymmword_14DC960+18h
0x1AD710  vmovups ymm2, cs:ymmword_14DC960
0x1AD718  vmovups ymm1, cs:ymmword_14DC940
0x1AD720  mov     edi, 2000h
0x1AD725  lea     rsi, [rbp+var_D0]
0x1AD72C  lea     rdx, [rbp+var_1A0]
0x1AD733  vmovups ymmword ptr [rbp+anonymous_0+18h], ymm0
0x1AD738  vmovups ymmword ptr [rbp-70h], ymm2
0x1AD73D  vmovups [rbp+var_90], ymm1
0x1AD745  vmovups ymm2, cs:ymmword_14DC920
0x1AD74D  vmovups ymm1, cs:ymmword_14DC900
0x1AD755  vmovups [rbp+var_B0], ymm2
0x1AD75D  vmovups [rbp+var_D0], ymm1
0x1AD765  call    sceNgs2RackQueryBufferSize
0x1AD76A  test    eax, eax
0x1AD76C  js      loc_1ADB35
0x1AD772  mov     rsi, [rbp+var_198]
0x1AD779  mov     rdi, [rbp+var_DA0]
0x1AD780  mov     edx, 1
0x1AD785  call    sub_1B3BD0
0x1AD78A  mov     [rbp+var_1A0], rax
0x1AD791  test    rax, rax
0x1AD794  jz      loc_1AD873
0x1AD79A  mov     esi, 2000h
0x1AD79F  mov     rdi, r14
0x1AD7A2  lea     rdx, [rbp+var_D0]
0x1AD7A9  lea     rcx, [rbp+var_1A0]
0x1AD7B0  lea     r8, [rbp+var_D78]
0x1AD7B7  call    sceNgs2RackCreate
0x1AD7BC  test    eax, eax
0x1AD7BE  js      loc_1ADB35
0x1AD7C4  mov     rdi, [rbp+var_D78]
0x1AD7CB  xor     esi, esi
0x1AD7CD  lea     rdx, [rbp+var_D70]
0x1AD7D4  call    sceNgs2RackGetVoiceHandle
0x1AD7D9  mov     rdi, [rbp+var_D70]
0x1AD7E0  lea     rsi, [rbp+var_678]
0x1AD7E7  mov     rax, 820000000h
0x1AD7F1  mov     [rbp+var_678], 10h
0x1AD7FA  mov     [rbp+var_676], 0
0x1AD803  mov     qword ptr [rbp+var_674], rax
0x1AD80A  mov     dword ptr [rbp+var_674+8], 0
0x1AD814  call    sceNgs2VoiceControl
0x1AD819  mov     rax, [rbp+var_D78]
0x1AD820  lea     rdi, off_14DB98D
0x1AD827  mov     [rbp+var_D50], rax
0x1AD82E  call    sub_1B1580
0x1AD833  mov     esi, 50h ; 'P'
0x1AD838  lea     rdi, [rbp+var_D40]
0x1AD83F  mov     [rbp+var_D44], eax
0x1AD845  call    sub_1B1C70
0x1AD84A  lea     rax, [rbp+var_D38]
0x1AD851  mov     [rbp+var_D40], 8
0x1AD85B  mov     esi, 4
0x1AD860  lea     rdi, [rbp+var_B20]
0x1AD867  mov     [rbp+var_CF8], rax
0x1AD86E  call    sub_1B1C70
0x1AD873  test    r13, r13
0x1AD876  jz      loc_1ADA96
0x1AD87C  mov     r15, rbx
0x1AD87F  imul    rbx, r12, 250h
0x1AD886  mov     edx, 250h
0x1AD88B  lea     rsi, [rbp+var_D50]
0x1AD892  mov     [rbp+var_DA8], r12
0x1AD899  lea     r14, [r13+rbx+0]
0x1AD89E  mov     rdi, r14
0x1AD8A1  call    sub_1B17C0
0x1AD8A6  lea     rax, [r13+rbx+18h]
0x1AD8AB  lea     rdx, [r13+rbx+64h]
0x1AD8B0  lea     rcx, [r13+rbx+1D4h]
0x1AD8B8  mov     r12, r13
0x1AD8BB  lea     rsi, aDisto; "DISTO"
0x1AD8C2  mov     [r13+rbx+58h], rax
0x1AD8C7  mov     [r13+rbx+0E8h], rdx
0x1AD8CF  mov     [r13+rbx+218h], rcx
0x1AD8D7  mov     rcx, [rbp+var_D98]
0x1AD8DE  mov     r13, r15
0x1AD8E1  mov     rax, [r15+18h]
0x1AD8E5  mov     r15, [rax+rcx*8+8]
0x1AD8EA  mov     rdi, r15
0x1AD8ED  call    sub_1B1E90
0x1AD8F2  test    eax, eax
0x1AD8F4  jz      loc_1AD990
0x1AD8FA  mov     rdi, r15
0x1AD8FD  lea     rsi, aUmix; "UMIX"
0x1AD904  call    sub_1B1E90
0x1AD909  test    eax, eax
0x1AD90B  jz      loc_1AD9D8
0x1AD911  mov     rdi, r15
0x1AD914  lea     rsi, off_14DB98D
0x1AD91B  call    sub_1B1E90
0x1AD920  test    eax, eax
0x1AD922  jz      loc_1ADA1D
0x1AD928  mov     rdi, r15
0x1AD92B  lea     rsi, aPanner; "PANNER"
0x1AD932  call    sub_1B1E90
0x1AD937  test    eax, eax
0x1AD939  jnz     loc_1ADA89
0x1AD93F  mov     rdi, [r14]
0x1AD942  xor     esi, esi
0x1AD944  lea     rdx, [rbp+var_D0]
0x1AD94B  call    sceNgs2RackGetVoiceHandle
0x1AD950  mov     rdi, qword ptr [rbp+var_D0]
0x1AD957  lea     rax, [r12+rbx+240h]
0x1AD95F  lea     rcx, sub_1B1780
0x1AD966  mov     [rbp+var_678], 28h ; '('
0x1AD96F  mov     [rbp+var_676], 0
0x1AD978  mov     dword ptr [rbp+var_674], 20000004h
0x1AD982  jmp     loc_1ADA60
0x1AD987  align 10h
0x1AD990  mov     rdi, [r14]
0x1AD993  xor     esi, esi
0x1AD995  lea     rdx, [rbp+var_D0]
0x1AD99C  call    sceNgs2RackGetVoiceHandle
0x1AD9A1  mov     rdi, qword ptr [rbp+var_D0]
0x1AD9A8  mov     [rbp+var_678], 28h ; '('
0x1AD9B1  mov     [rbp+var_676], 0
0x1AD9BA  lea     rax, [r12+rbx+148h]
0x1AD9C2  mov     dword ptr [rbp+var_674], 20000004h
0x1AD9CC  lea     rcx, sub_1B16C0
0x1AD9D3  jmp     loc_1ADA60
0x1AD9D8  mov     rdi, [r14]
0x1AD9DB  xor     esi, esi
0x1AD9DD  lea     rdx, [rbp+var_D0]
0x1AD9E4  call    sceNgs2RackGetVoiceHandle
0x1AD9E9  mov     rdi, qword ptr [rbp+var_D0]
0x1AD9F0  mov     [rbp+var_678], 28h ; '('
0x1AD9F9  mov     [rbp+var_676], 0
0x1ADA02  lea     rax, [r12+rbx+150h]
0x1ADA0A  mov     dword ptr [rbp+var_674], 20000004h
0x1ADA14  lea     rcx, sub_1B1700
0x1ADA1B  jmp     short loc_1ADA60
0x1ADA1D  mov     rdi, [r14]
0x1ADA20  xor     esi, esi
0x1ADA22  lea     rdx, [rbp+var_D0]
0x1ADA29  call    sceNgs2RackGetVoiceHandle
0x1ADA2E  mov     rdi, qword ptr [rbp+var_D0]
0x1ADA35  mov     [rbp+var_678], 28h ; '('
0x1ADA3E  mov     [rbp+var_676], 0
0x1ADA47  lea     rax, [r12+rbx+230h]
0x1ADA4F  mov     dword ptr [rbp+var_674], 20000004h
0x1ADA59  lea     rcx, sub_1B1740
0x1ADA60  mov     qword ptr [rbp+var_674+4], rcx
0x1ADA67  mov     qword ptr [rbp+var_674+0Ch], rax
0x1ADA6E  lea     rsi, [rbp+var_678]
0x1ADA75  lea     rax, [rbp+var_660]
0x1ADA7C  vxorps  xmm0, xmm0, xmm0
0x1ADA80  vmovups xmmword ptr [rax], xmm0
0x1ADA84  call    sceNgs2VoiceControl
0x1ADA89  mov     rbx, r13
0x1ADA8C  mov     r13, r12
0x1ADA8F  mov     r12, [rbp+var_DA8]
0x1ADA96  mov     eax, [rbx+10h]
0x1ADA99  inc     r12d
0x1ADA9C  cmp     r12d, eax
0x1ADA9F  jb      loc_1AC830
0x1ADAA5  mov     r14, cs:qword_1700698
0x1ADAAC  mov     r15, [rbp+var_DB0]
0x1ADAB3  shl     rax, 3
0x1ADAB7  lea     r12, [rax+rax*4]
0x1ADABB  mov     rdi, [rbp+var_DA0]
0x1ADAC2  mov     rsi, r12
0x1ADAC5  mov     edx, 1
0x1ADACA  mov     r12, r13
0x1ADACD  mov     r13, rbx
0x1ADAD0  call    sub_1B3BD0
0x1ADAD5  mov     rbx, rax
0x1ADAD8  test    rbx, rbx
0x1ADADB  jz      short loc_1ADAF1
0x1ADADD  mov     eax, [r13+10h]
0x1ADAE1  mov     rdi, rbx
0x1ADAE4  shl     rax, 3
0x1ADAE8  lea     rsi, [rax+rax*4]
0x1ADAEC  call    sub_1B1C70
0x1ADAF1  mov     rdi, [rbp+var_DA0]
0x1ADAF8  mov     esi, 30h ; '0'
0x1ADAFD  mov     edx, 1
0x1ADB02  call    sub_1B3BD0
0x1ADB07  mov     rcx, rax
0x1ADB0A  test    rcx, rcx
0x1ADB0D  jz      short loc_1ADB29
0x1ADB0F  mov     [rcx], r12
0x1ADB12  vxorps  xmm0, xmm0, xmm0
0x1ADB16  mov     eax, [r13+10h]
0x1ADB1A  mov     [rcx+8], eax
0x1ADB1D  mov     [rcx+10h], rbx
0x1ADB21  mov     [rcx+18h], eax
0x1ADB24  vmovups xmmword ptr [rcx+1Ch], xmm0
0x1ADB29  xor     eax, eax
0x1ADB2B  test    r15, r15
0x1ADB2E  jz      short loc_1ADB41
0x1ADB30  mov     [r15], rcx
0x1ADB33  jmp     short loc_1ADB41
0x1ADB35  mov     r14, cs:qword_1700698
0x1ADB3C  mov     eax, 0FFFFFFFFh
0x1ADB41  mov     rcx, [r14]
0x1ADB44  cmp     rcx, [rbp+var_30]
0x1ADB48  jnz     short loc_1ADB5C
0x1ADB4A  add     rsp, 0D98h
0x1ADB51  pop     rbx
0x1ADB52  pop     r12
0x1ADB54  pop     r13
0x1ADB56  pop     r14
0x1ADB58  pop     r15
0x1ADB5A  pop     rbp
0x1ADB5B  retn
0x1ADB5C  call    __stack_chk_fail
```

## sub_1ADC10 — mastering_builder
Range: `0x1ADC10`–`0x1AEFCD`; 970 instructions.
### Xrefs to function
- `0x1A62A9` `sub_1A6150` (17): `call    sub_1ADC10`
### Disassembly
```asm
0x1ADC10  push    rbp
0x1ADC11  mov     rbp, rsp
0x1ADC14  push    r15
0x1ADC16  push    r14
0x1ADC18  push    r13
0x1ADC1A  push    r12
0x1ADC1C  push    rbx
0x1ADC1D  sub     rsp, 128h
0x1ADC24  mov     rdx, cs:qword_1700698
0x1ADC2B  mov     r9, rdi
0x1ADC2E  mov     rbx, rsi
0x1ADC31  mov     [rbp+var_130], rbx
0x1ADC38  mov     [rbp+var_E8], r9
0x1ADC3F  test    r9, r9
0x1ADC42  mov     rax, [rdx]
0x1ADC45  mov     [rbp+var_30], rax
0x1ADC49  mov     eax, 0FFFFFFF9h
0x1ADC4E  jz      loc_1AEFAD
0x1ADC54  test    rbx, rbx
0x1ADC57  jz      loc_1AEFAD
0x1ADC5D  mov     ecx, [rbx]
0x1ADC5F  cmp     ecx, 1
0x1ADC62  ja      loc_1AEFAD
0x1ADC68  jz      loc_1ADD3E
0x1ADC6E  test    ecx, ecx
0x1ADC70  jnz     loc_1ADED0
0x1ADC76  mov     rax, cs:qword_57F1C20
0x1ADC7D  vmovups xmm1, cs:xmmword_14DADB0
0x1ADC85  xor     ecx, ecx
0x1ADC87  vxorps  xmm0, xmm0, xmm0
0x1ADC8B  nop     dword ptr [rax+rax+00h]
0x1ADC90  mov     dword ptr [rax+rcx+0A8h], 0
0x1ADC9B  vmovups xmmword ptr [rax+rcx+0B0h], xmm0
0x1ADCA4  mov     dword ptr [rax+rcx+0F4h], 0
0x1ADCAF  mov     byte ptr [rax+rcx+0C3h], 0
0x1ADCB7  vmovups xmmword ptr [rax+rcx+0D0h], xmm1
0x1ADCC0  vmovups ymmword ptr [rax+rcx+0F8h], ymm0
0x1ADCC9  mov     dword ptr [rax+rcx+0E0h], 3F800000h
0x1ADCD4  mov     qword ptr [rax+rcx+118h], 0
0x1ADCE0  mov     dword ptr [rax+rcx+0E4h], 3F800000h
0x1ADCEB  mov     qword ptr [rax+rcx+120h], 0
0x1ADCF7  mov     dword ptr [rax+rcx+0E8h], 3F800000h
0x1ADD02  mov     qword ptr [rax+rcx+128h], 0
0x1ADD0E  mov     dword ptr [rax+rcx+0ECh], 3F800000h
0x1ADD19  mov     qword ptr [rax+rcx+130h], 0
0x1ADD25  add     rcx, 98h
0x1ADD2C  cmp     rcx, 4C00h
0x1ADD33  jnz     loc_1ADC90
0x1ADD39  jmp     loc_1ADED0
0x1ADD3E  mov     r15, [rbx+40h]
0x1ADD42  mov     r14, r9
0x1ADD45  test    r15, r15
0x1ADD48  jz      loc_1ADECD
0x1ADD4E  cmp     byte ptr [r15], 0
0x1ADD52  jz      loc_1ADECD
0x1ADD58  mov     rax, cs:qword_57F1C20
0x1ADD5F  lea     rdx, [rbp+var_C8]
0x1ADD66  xor     esi, esi
0x1ADD68  mov     rdi, [rax+68h]
0x1ADD6C  call    sceNgs2RackGetVoiceHandle
0x1ADD71  lea     rcx, asc_14DAC3F; "; \t\n"
0x1ADD78  lea     rsi, [rbp+var_70]
0x1ADD7C  mov     edx, 40h ; '@'
0x1ADD81  xor     r8d, r8d
0x1ADD84  mov     rdi, r15
0x1ADD87  call    sub_1B34E0
0x1ADD8C  mov     cl, byte ptr [rbp+var_70]
0x1ADD8F  mov     r15, rax
0x1ADD92  or      cl, [r15]
0x1ADD95  jz      loc_1ADECD
0x1ADD9B  lea     r13, [rbp+var_70]
0x1ADD9F  lea     r12, [rbp+var_90]
0x1ADDA6  nop     word ptr [rax+rax+00000000h]
0x1ADDB0  mov     edx, 20h ; ' '
0x1ADDB5  xor     r8d, r8d
0x1ADDB8  mov     rdi, r13
0x1ADDBB  mov     rsi, r12
0x1ADDBE  lea     rcx, qword_14DA4A0
0x1ADDC5  call    sub_1B34E0
0x1ADDCA  mov     edx, 20h ; ' '
0x1ADDCF  xor     r8d, r8d
0x1ADDD2  mov     rdi, rax
0x1ADDD5  lea     rsi, [rbp+var_B0]
0x1ADDDC  lea     rcx, byte_14C0CC5
0x1ADDE3  call    sub_1B34E0
0x1ADDE8  mov     rdi, r12
0x1ADDEB  lea     rsi, aOutputlevel; "outputLevel"
0x1ADDF2  call    sub_1B1E90
0x1ADDF7  test    eax, eax
0x1ADDF9  jnz     short loc_1ADE46
0x1ADDFB  lea     rdi, [rbp+var_B0]
0x1ADE02  call    sub_1B2130
0x1ADE07  mov     rdi, [rbp+var_C8]
0x1ADE0E  lea     rsi, [rbp+var_C0]
0x1ADE15  mov     word ptr [rbp+var_C0], 10h
0x1ADE1E  mov     word ptr [rbp+var_C0+2], 0
0x1ADE27  mov     dword ptr [rbp+var_C0+4], 30000004h
0x1ADE31  vmovss  [rbp+var_B8], xmm0
0x1ADE39  vmovss  [rbp+var_B4], xmm0
0x1ADE41  call    sceNgs2VoiceControl
0x1ADE46  mov     rdi, r12
0x1ADE49  lea     rsi, aIslimiterenabl; "isLimiterEnable"
0x1ADE50  call    sub_1B1E90
0x1ADE55  test    eax, eax
0x1ADE57  jnz     short loc_1ADEA4
0x1ADE59  lea     rdi, [rbp+var_B0]
0x1ADE60  call    sub_1B2010
0x1ADE65  mov     rdi, [rbp+var_C8]
0x1ADE6C  lea     rsi, [rbp+var_C0]
0x1ADE73  mov     word ptr [rbp+var_C0], 10h
0x1ADE7C  mov     word ptr [rbp+var_C0+2], 0
0x1ADE85  mov     dword ptr [rbp+var_C0+4], 30000003h
0x1ADE8F  mov     [rbp+var_B8], eax
0x1ADE95  mov     [rbp+var_B4], 3F800000h
0x1ADE9F  call    sceNgs2VoiceControl
0x1ADEA4  mov     edx, 40h ; '@'
0x1ADEA9  xor     r8d, r8d
0x1ADEAC  mov     rdi, r15
0x1ADEAF  mov     rsi, r13
0x1ADEB2  lea     rcx, asc_14DAC3F; "; \t\n"
0x1ADEB9  call    sub_1B34E0
0x1ADEBE  mov     cl, byte ptr [rbp+var_70]
0x1ADEC1  mov     r15, rax
0x1ADEC4  or      cl, [r15]
0x1ADEC7  jnz     loc_1ADDB0
0x1ADECD  mov     r9, r14
0x1ADED0  cmp     dword ptr [r9+28h], 0
0x1ADED5  jnz     short loc_1ADF47
0x1ADED7  mov     rax, cs:qword_57F1C20
0x1ADEDE  lea     rdx, [rbp+var_90]
0x1ADEE5  xor     esi, esi
0x1ADEE7  mov     r14, r9
0x1ADEEA  mov     rdi, [rax+70h]
0x1ADEEE  mov     r15, [rax+68h]
0x1ADEF2  call    sceNgs2RackGetVoiceHandle
0x1ADEF7  lea     rdx, [rbp+var_B0]
0x1ADEFE  xor     esi, esi
0x1ADF00  mov     rdi, r15
0x1ADF03  call    sceNgs2RackGetVoiceHandle
0x1ADF08  mov     rdi, [rbp+var_90]
0x1ADF0F  mov     rax, [rbp+var_B0]
0x1ADF16  lea     rsi, [rbp+var_70]
0x1ADF1A  mov     [rbp+var_70], 18h
0x1ADF20  mov     [rbp+var_6E], 0
0x1ADF26  mov     dword ptr [rbp+var_6C], 5
0x1ADF2D  mov     dword ptr [rbp+var_6C+4], 0
0x1ADF34  mov     [rbp+var_60], rax
0x1ADF38  mov     [rbp+var_64], 0
0x1ADF3F  call    sceNgs2VoiceControl
0x1ADF44  mov     r9, r14
0x1ADF47  xor     eax, eax
0x1ADF49  cmp     dword ptr [rbx+28h], 0
0x1ADF4D  jz      short loc_1ADFC8
0x1ADF4F  xor     r14d, r14d
0x1ADF52  nop     word ptr [rax+rax+00000000h]
0x1ADF60  mov     r8, [rbx+30h]
0x1ADF64  mov     r14d, r14d
0x1ADF67  mov     rsi, [r9]
0x1ADF6A  mov     r15, r9
0x1ADF6D  lea     rcx, [r14+r14*4]
0x1ADF71  mov     eax, [r8+rcx*8+8]
0x1ADF76  imul    rax, 250h
0x1ADF7D  mov     dword ptr [rsi+rax+14h], 0
0x1ADF85  lea     rdi, [rsi+rax]
0x1ADF89  mov     edx, [rsi+rax+10h]
0x1ADF8D  test    rdx, rdx
0x1ADF90  jz      short loc_1ADFB0
0x1ADF92  mov     rsi, [rsi+rax+58h]
0x1ADF97  xor     eax, eax
0x1ADF99  nop     dword ptr [rax+00000000h]
0x1ADFA0  mov     qword ptr [rsi+rax*8], 0
0x1ADFA8  inc     rax
0x1ADFAB  cmp     rax, rdx
0x1ADFAE  jb      short loc_1ADFA0
0x1ADFB0  mov     rsi, [r8+rcx*8+10h]
0x1ADFB5  call    sub_1AEFD0
0x1ADFBA  mov     eax, [rbx+28h]
0x1ADFBD  inc     r14d
0x1ADFC0  mov     r9, r15
0x1ADFC3  cmp     r14d, eax
0x1ADFC6  jb      short loc_1ADF60
0x1ADFC8  cmp     dword ptr [rbx+18h], 0
0x1ADFCC  jz      loc_1AE839
0x1ADFD2  mov     eax, [rbx+28h]
0x1ADFD5  xor     edx, edx
0x1ADFD7  mov     ecx, eax
0x1ADFD9  nop     dword ptr [rax+00000000h]
0x1ADFE0  test    ecx, ecx
0x1ADFE2  jz      loc_1AE820
0x1ADFE8  mov     esi, edx
0x1ADFEA  xor     r12d, r12d
0x1ADFED  mov     dword ptr [rbp+var_110], edx
0x1ADFF3  mov     dword ptr [rbp+var_D0], 1
0x1ADFFD  mov     dword ptr [rbp+var_F8], 1
0x1AE007  mov     [rbp+var_100], rsi
0x1AE00E  xchg    ax, ax
0x1AE010  mov     rcx, [rbx+20h]
0x1AE014  mov     r13, [rbx+30h]
0x1AE018  mov     r14, rsi
0x1AE01B  mov     r12d, r12d
0x1AE01E  shl     r14, 4
0x1AE022  lea     rdx, [r12+r12*4]
0x1AE026  mov     ecx, [rcx+r14+8]
0x1AE02B  cmp     ecx, [r13+rdx*8+0Ch]
0x1AE030  jnz     loc_1AE7FF
0x1AE036  lea     rax, [r13+rdx*8+0Ch]
0x1AE03B  mov     rcx, [r9]
0x1AE03E  mov     [rbp+var_E0], r13
0x1AE045  mov     [rbp+var_F0], rdx
0x1AE04C  xor     esi, esi
0x1AE04E  mov     [rbp+var_D8], rax
0x1AE055  mov     eax, [r13+rdx*8+8]
0x1AE05A  lea     rdx, [rbp+var_C0]
0x1AE061  imul    rax, 250h
0x1AE068  mov     r13, [rcx+rax]
0x1AE06C  mov     rdi, r13
0x1AE06F  call    sceNgs2RackGetVoiceHandle
0x1AE074  mov     rdi, [rbp+var_C0]
0x1AE07B  lea     r15, [rbp+var_70]
0x1AE07F  mov     [rbp+var_70], 10h
0x1AE085  mov     [rbp+var_6E], 0
0x1AE08B  mov     [rbp+var_6C], 2
0x1AE093  mov     [rbp+var_64], 3F800000h
0x1AE09A  mov     rsi, r15
0x1AE09D  call    sceNgs2VoiceControl
0x1AE0A2  mov     rdi, [rbp+var_C0]
0x1AE0A9  mov     rsi, r15
0x1AE0AC  mov     rax, 100000002h
0x1AE0B6  mov     [rbp+var_70], 10h
0x1AE0BC  mov     [rbp+var_6E], 0
0x1AE0C2  mov     [rbp+var_6C], rax
0x1AE0C6  mov     [rbp+var_64], 3F800000h
0x1AE0CD  call    sceNgs2VoiceControl
0x1AE0D2  mov     rdi, [rbp+var_C0]
0x1AE0D9  mov     rsi, r15
0x1AE0DC  mov     rax, 200000002h
0x1AE0E6  mov     [rbp+var_70], 10h
0x1AE0EC  mov     [rbp+var_6E], 0
0x1AE0F2  mov     [rbp+var_6C], rax
0x1AE0F6  mov     [rbp+var_64], 3F800000h
0x1AE0FD  call    sceNgs2VoiceControl
0x1AE102  mov     rdi, [rbp+var_C0]
0x1AE109  mov     rsi, r15
0x1AE10C  mov     rax, 300000002h
0x1AE116  mov     [rbp+var_70], 10h
0x1AE11C  mov     [rbp+var_6E], 0
0x1AE122  mov     [rbp+var_6C], rax
0x1AE126  mov     [rbp+var_64], 3F800000h
0x1AE12D  call    sceNgs2VoiceControl
0x1AE132  mov     rdi, [rbp+var_C0]
0x1AE139  mov     rsi, r15
0x1AE13C  mov     rax, 400000002h
0x1AE146  mov     [rbp+var_70], 10h
0x1AE14C  mov     [rbp+var_6E], 0
0x1AE152  mov     [rbp+var_6C], rax
0x1AE156  mov     [rbp+var_64], 3F800000h
0x1AE15D  call    sceNgs2VoiceControl
0x1AE162  mov     rdi, [rbp+var_C0]
0x1AE169  mov     rsi, r15
0x1AE16C  mov     rax, 500000002h
0x1AE176  mov     [rbp+var_70], 10h
0x1AE17C  mov     [rbp+var_6E], 0
0x1AE182  mov     [rbp+var_6C], rax
0x1AE186  mov     [rbp+var_64], 3F800000h
0x1AE18D  call    sceNgs2VoiceControl
0x1AE192  mov     rdi, [rbp+var_C0]
0x1AE199  mov     rsi, r15
0x1AE19C  mov     rax, 600000002h
0x1AE1A6  mov     [rbp+var_70], 10h
0x1AE1AC  mov     [rbp+var_6E], 0
0x1AE1B2  mov     [rbp+var_6C], rax
0x1AE1B6  mov     [rbp+var_64], 3F800000h
0x1AE1BD  call    sceNgs2VoiceControl
0x1AE1C2  mov     rdi, [rbp+var_C0]
0x1AE1C9  mov     rsi, r15
0x1AE1CC  mov     rax, 700000002h
0x1AE1D6  mov     [rbp+var_70], 10h
0x1AE1DC  mov     [rbp+var_6E], 0
0x1AE1E2  mov     [rbp+var_6C], rax
0x1AE1E6  mov     [rbp+var_64], 3F800000h
0x1AE1ED  call    sceNgs2VoiceControl
0x1AE1F2  cmp     dword ptr [rbp+var_F8], 0
0x1AE1F9  jz      loc_1AE291
0x1AE1FF  mov     rax, [rbx+20h]
0x1AE203  mov     rdx, [rbp+var_D8]
0x1AE20A  mov     ecx, [rax+r14+8]
0x1AE20F  mov     rax, cs:qword_57F1C20
0x1AE216  imul    rcx, 98h
0x1AE21D  mov     [rax+rcx+0B0h], r13
0x1AE225  mov     edx, [rdx]
0x1AE227  mov     [rax+rcx+0A8h], edx
0x1AE22E  cmp     dword ptr [rbx], 1
0x1AE231  jnz     short loc_1AE291
0x1AE233  mov     rdi, [rax+70h]
0x1AE237  xor     esi, esi
0x1AE239  lea     rdx, [rbp+var_90]
0x1AE240  call    sceNgs2RackGetVoiceHandle
0x1AE245  xor     esi, esi
0x1AE247  mov     rdi, r13
0x1AE24A  lea     rdx, [rbp+var_B0]
0x1AE251  call    sceNgs2RackGetVoiceHandle
0x1AE256  mov     rdi, [rbp+var_90]
0x1AE25D  mov     rax, [rbp+var_B0]
0x1AE264  mov     rsi, r15
0x1AE267  mov     [rbp+var_70], 18h
0x1AE26D  mov     [rbp+var_6E], 0
0x1AE273  mov     dword ptr [rbp+var_6C], 5
0x1AE27A  mov     dword ptr [rbp+var_6C+4], 0
0x1AE281  mov     [rbp+var_60], rax
0x1AE285  mov     [rbp+var_64], 0
0x1AE28C  call    sceNgs2VoiceControl
0x1AE291  mov     rcx, [rbp+var_E0]
0x1AE298  mov     rax, [rbp+var_F0]
0x1AE29F  mov     [rbp+var_F8], r13
0x1AE2A6  lea     rdi, [rcx+rax*8+8]
0x1AE2AB  mov     eax, [rbx+28h]
0x1AE2AE  mov     ecx, dword ptr [rbp+var_D0]
0x1AE2B4  nop     word ptr [rax+rax+00000000h]
0x1AE2C0  cmp     ecx, eax
0x1AE2C2  jnb     loc_1AE420
0x1AE2C8  mov     rsi, [rbx+20h]
0x1AE2CC  mov     r13, [rbx+30h]
0x1AE2D0  mov     edx, ecx
0x1AE2D2  inc     ecx
0x1AE2D4  lea     r15, [rdx+rdx*4]
0x1AE2D8  mov     esi, [rsi+r14+8]
0x1AE2DD  cmp     esi, [r13+r15*8+0Ch]
0x1AE2E2  jnz     short loc_1AE2C0
0x1AE2E4  mov     rax, [rbp+var_E8]
0x1AE2EB  mov     ecx, [rdi]
0x1AE2ED  vmovss  xmm0, cs:dword_14DAE60
0x1AE2F5  mov     [rbp+var_108], rdi
0x1AE2FC  mov     rax, [rax]
0x1AE2FF  imul    rcx, 250h
0x1AE306  cmp     dword ptr [rax+rcx+0Ch], 1
0x1AE30B  jnz     short loc_1AE32C
0x1AE30D  vmovss  xmm0, dword ptr [rax+rcx+0F0h]
0x1AE316  vmovss  xmm1, cs:dword_14DAE58
0x1AE31E  vaddss  xmm0, xmm0, dword ptr [rax+rcx+0F4h]
0x1AE327  call    sub_1B55F0
0x1AE32C  mov     r14, [rbp+var_F8]
0x1AE333  xor     esi, esi
0x1AE335  lea     rdx, [rbp+var_C8]
0x1AE33C  vmovss  dword ptr [rbp+var_E0], xmm0
0x1AE344  mov     rdi, r14
0x1AE347  call    sceNgs2RackGetVoiceHandle
0x1AE34C  mov     rdi, [rbp+var_C8]
0x1AE353  vmovss  xmm0, dword ptr [rbp+var_E0]
0x1AE35B  lea     rbx, [rbp+var_70]
0x1AE35F  mov     [rbp+var_70], 10h
0x1AE365  mov     [rbp+var_6E], 0
0x1AE36B  mov     dword ptr [rbp+var_6C], 2
0x1AE372  mov     dword ptr [rbp+var_6C+4], 0
0x1AE379  mov     rsi, rbx
0x1AE37C  vmovss  [rbp+var_64], xmm0
0x1AE381  call    sceNgs2VoiceControl
0x1AE386  mov     eax, [r13+r15*8+8]
0x1AE38B  mov     r13, [rbp+var_E8]
0x1AE392  mov     r15, rbx
0x1AE395  xor     esi, esi
0x1AE397  mov     rdi, r14
0x1AE39A  lea     rdx, [rbp+var_90]
0x1AE3A1  mov     rcx, [r13+0]
0x1AE3A5  imul    rax, 250h
0x1AE3AC  mov     rbx, [rcx+rax]
0x1AE3B0  call    sceNgs2RackGetVoiceHandle
0x1AE3B5  xor     esi, esi
0x1AE3B7  mov     rdi, rbx
0x1AE3BA  lea     rdx, [rbp+var_B0]
0x1AE3C1  call    sceNgs2RackGetVoiceHandle
0x1AE3C6  mov     rdi, [rbp+var_90]
0x1AE3CD  mov     rax, [rbp+var_B0]
0x1AE3D4  mov     rsi, r15
0x1AE3D7  mov     [rbp+var_70], 18h
0x1AE3DD  mov     [rbp+var_6E], 0
0x1AE3E3  mov     dword ptr [rbp+var_6C], 5
0x1AE3EA  mov     dword ptr [rbp+var_6C+4], 0
0x1AE3F1  mov     [rbp+var_60], rax
0x1AE3F5  mov     [rbp+var_64], 0
0x1AE3FC  call    sceNgs2VoiceControl
0x1AE401  mov     r9, r13
0x1AE404  mov     r13, [rbp+var_108]
0x1AE40B  mov     rbx, [rbp+var_130]
0x1AE412  jmp     loc_1AE7D0
0x1AE417  align 20h
0x1AE420  mov     rax, [rbx+20h]
0x1AE424  mov     r13, rdi
0x1AE427  mov     rdi, [rbp+var_F8]
0x1AE42E  mov     ecx, [rax+r14+8]
0x1AE433  mov     rax, cs:qword_57F1C20
0x1AE43A  imul    rcx, 98h
0x1AE441  mov     [rax+rcx+0B8h], rdi
0x1AE449  cmp     dword ptr [rbx], 0
0x1AE44C  jz      short loc_1AE4BF
0x1AE44E  mov     r14, [rax+68h]
0x1AE452  xor     esi, esi
0x1AE454  lea     rdx, [rbp+var_90]
0x1AE45B  call    sceNgs2RackGetVoiceHandle
0x1AE460  xor     esi, esi
0x1AE462  mov     rdi, r14
0x1AE465  lea     rdx, [rbp+var_B0]
0x1AE46C  call    sceNgs2RackGetVoiceHandle
0x1AE471  mov     rdi, [rbp+var_90]
0x1AE478  mov     rax, [rbp+var_B0]
0x1AE47F  lea     r15, [rbp+var_70]
0x1AE483  mov     [rbp+var_70], 18h
0x1AE489  mov     [rbp+var_6E], 0
0x1AE48F  mov     dword ptr [rbp+var_6C], 5
0x1AE496  mov     dword ptr [rbp+var_6C+4], 0
0x1AE49D  mov     rsi, r15
0x1AE4A0  mov     [rbp+var_60], rax
0x1AE4A4  mov     [rbp+var_64], 0
0x1AE4AB  call    sceNgs2VoiceControl
0x1AE4B0  mov     rax, [rbp+var_E8]
0x1AE4B7  mov     r9, rax
0x1AE4BA  jmp     loc_1AE7D0
0x1AE4BF  mov     rcx, [rbp+var_D8]
0x1AE4C6  mov     r15d, [rcx]
0x1AE4C9  lea     ecx, [r15-64h]
0x1AE4CD  cmp     ecx, 15h; switch 22 cases
0x1AE4D0  ja      loc_1AE6EB; jumptable 00000000001AE4E4 default case
0x1AE4D6  lea     rdx, off_14DB0C8
0x1AE4DD  movsxd  rcx, dword ptr [rdx+rcx*4]
0x1AE4E1  add     rcx, rdx
0x1AE4E4  jmp     rcx; switch jump
0x1AE4E6  add     r15d, 0FFFFFF9Dh; jumptable 00000000001AE4E4 cases 0-3
0x1AE4EA  cmp     r15d, [rax+90h]
0x1AE4F1  ja      loc_1AE6EB; jumptable 00000000001AE4E4 default case
0x1AE4F7  jmp     short loc_1AE517
0x1AE4F9  mov     rax, [rax+90h]; jumptable 00000000001AE4E4 cases 10-13
0x1AE500  add     r15d, 0FFFFFF93h
0x1AE504  mov     rcx, rax
0x1AE507  shr     rcx, 20h
0x1AE50B  cmp     r15d, ecx
0x1AE50E  ja      loc_1AE6EB; jumptable 00000000001AE4E4 default case
0x1AE514  add     r15d, eax
0x1AE517  xor     esi, esi
0x1AE519  lea     rdx, [rbp+var_90]
0x1AE520  call    sceNgs2RackGetVoiceHandle
0x1AE525  mov     rax, cs:qword_57F1C20
0x1AE52C  mov     esi, r15d
0x1AE52F  lea     rdx, [rbp+var_B0]
0x1AE536  mov     rdi, [rax+68h]
0x1AE53A  call    sceNgs2RackGetVoiceHandle
0x1AE53F  mov     rdi, [rbp+var_90]
0x1AE546  mov     rax, [rbp+var_B0]
0x1AE54D  lea     rsi, [rbp+var_70]
0x1AE551  mov     [rbp+var_70], 18h
0x1AE557  mov     [rbp+var_6E], 0
0x1AE55D  mov     dword ptr [rbp+var_6C], 5
0x1AE564  mov     dword ptr [rbp+var_6C+4], 0
0x1AE56B  mov     [rbp+var_60], rax
0x1AE56F  mov     [rbp+var_64], 0
0x1AE576  call    sceNgs2VoiceControl
0x1AE57B  mov     rax, [rbp+var_E0]
0x1AE582  mov     rcx, [rbp+var_F0]
0x1AE589  cmp     dword ptr [rax+rcx*8+18h], 0
0x1AE58E  jz      loc_1AE6EB; jumptable 00000000001AE4E4 default case
0x1AE594  mov     rax, [rbp+var_E0]
0x1AE59B  mov     rcx, [rbp+var_F0]
0x1AE5A2  vmovss  xmm1, cs:dword_14DAE58
0x1AE5AA  mov     rax, [rax+rcx*8+20h]
0x1AE5AF  vmovss  xmm0, dword ptr [rax+4]
0x1AE5B4  call    sub_1B55F0
0x1AE5B9  mov     rdi, [rbp+var_90]
0x1AE5C0  lea     rsi, [rbp+var_70]
0x1AE5C4  mov     [rbp+var_70], 10h
0x1AE5CA  mov     [rbp+var_6E], 0
0x1AE5D0  mov     dword ptr [rbp+var_6C], 2
0x1AE5D7  mov     dword ptr [rbp+var_6C+4], 0
0x1AE5DE  vmovss  [rbp+var_64], xmm0
0x1AE5E3  call    sceNgs2VoiceControl
0x1AE5E8  jmp     loc_1AE6EB; jumptable 00000000001AE4E4 default case
0x1AE5ED  mov     rax, [rax+90h]; jumptable 00000000001AE4E4 case 20
0x1AE5F4  mov     [rbp+var_108], r13
0x1AE5FB  mov     rcx, rax
0x1AE5FE  shr     rcx, 20h
0x1AE602  lea     r15d, [rax+rcx+1]
0x1AE607  jmp     short loc_1AE623
0x1AE609  mov     rax, [rax+90h]; jumptable 00000000001AE4E4 case 21
0x1AE610  mov     [rbp+var_108], r13
0x1AE617  mov     rcx, rax
0x1AE61A  shr     rcx, 20h
0x1AE61E  lea     r15d, [rax+rcx+2]
0x1AE623  xor     esi, esi
0x1AE625  lea     rdx, [rbp+var_90]
0x1AE62C  call    sceNgs2RackGetVoiceHandle
0x1AE631  mov     rax, cs:qword_57F1C20
0x1AE638  mov     esi, r15d
0x1AE63B  lea     rdx, [rbp+var_B0]
0x1AE642  mov     rdi, [rax+68h]
0x1AE646  call    sceNgs2RackGetVoiceHandle
0x1AE64B  mov     rdi, [rbp+var_90]
0x1AE652  mov     rax, [rbp+var_B0]
0x1AE659  lea     r15, [rbp+var_70]
0x1AE65D  mov     [rbp+var_70], 18h
0x1AE663  mov     [rbp+var_6E], 0
0x1AE669  mov     dword ptr [rbp+var_6C], 5
0x1AE670  mov     dword ptr [rbp+var_6C+4], 0
0x1AE677  mov     rsi, r15
0x1AE67A  mov     [rbp+var_60], rax
0x1AE67E  mov     [rbp+var_64], 0
0x1AE685  call    sceNgs2VoiceControl
0x1AE68A  mov     rax, [rbp+var_E0]
0x1AE691  mov     rcx, [rbp+var_F0]
0x1AE698  cmp     dword ptr [rax+rcx*8+18h], 0
0x1AE69D  jz      short loc_1AE6E4
0x1AE69F  mov     rax, [rax+rcx*8+20h]
0x1AE6A4  vmovss  xmm1, cs:dword_14DAE58
0x1AE6AC  vmovss  xmm0, dword ptr [rax+4]
0x1AE6B1  call    sub_1B55F0
0x1AE6B6  mov     rdi, [rbp+var_90]
0x1AE6BD  mov     rsi, r15
0x1AE6C0  mov     [rbp+var_70], 10h
0x1AE6C6  mov     [rbp+var_6E], 0
0x1AE6CC  mov     dword ptr [rbp+var_6C], 2
0x1AE6D3  mov     dword ptr [rbp+var_6C+4], 0
0x1AE6DA  vmovss  [rbp+var_64], xmm0
0x1AE6DF  call    sceNgs2VoiceControl
0x1AE6E4  mov     r13, [rbp+var_108]
0x1AE6EB  mov     rax, [rbx+20h]; jumptable 00000000001AE4E4 default case
0x1AE6EF  movzx   ecx, byte ptr [rax+r14+0Ch]
0x1AE6F5  test    ecx, ecx
0x1AE6F7  jz      short loc_1AE729
0x1AE6F9  mov     r9, [rbp+var_E8]
0x1AE700  cmp     ecx, 1
0x1AE703  jz      short loc_1AE74F
0x1AE705  cmp     ecx, 2
0x1AE708  jnz     short loc_1AE76E
0x1AE70A  mov     eax, [rax+r14+8]
0x1AE70F  mov     rcx, cs:qword_57F1C20
0x1AE716  imul    rdx, rax, 98h
0x1AE71D  mov     word ptr [rcx+rdx+0C1h], 101h
0x1AE727  jmp     short loc_1AE77A
0x1AE729  mov     eax, [rax+r14+8]
0x1AE72E  mov     rcx, cs:qword_57F1C20
0x1AE735  mov     r9, [rbp+var_E8]
0x1AE73C  imul    rdx, rax, 98h
0x1AE743  mov     word ptr [rcx+rdx+0C1h], 0
0x1AE74D  jmp     short loc_1AE77A
0x1AE74F  mov     eax, [rax+r14+8]
0x1AE754  mov     rcx, cs:qword_57F1C20
0x1AE75B  imul    rdx, rax, 98h
0x1AE762  mov     word ptr [rcx+rdx+0C1h], 1
0x1AE76C  jmp     short loc_1AE77A
0x1AE76E  mov     eax, [rax+r14+8]
0x1AE773  mov     rcx, cs:qword_57F1C20
0x1AE77A  mov     rdx, [rbx+50h]
0x1AE77E  vmovss  xmm1, cs:dword_14DAE5C
0x1AE786  mov     eax, eax
0x1AE788  imul    rax, 98h
0x1AE78F  mov     esi, edx
0x1AE791  shr     rdx, 20h
0x1AE795  vcvtsi2ss xmm0, xmm0, rsi
0x1AE79A  vdivss  xmm0, xmm0, xmm1
0x1AE79E  vmovss  dword ptr [rcx+rax+0C4h], xmm0
0x1AE7A7  vxorps  xmm0, xmm0, xmm0
0x1AE7AB  vcvtsi2ss xmm0, xmm0, rdx
0x1AE7B0  vdivss  xmm0, xmm0, xmm1
0x1AE7B4  vmovss  dword ptr [rcx+rax+0C8h], xmm0
0x1AE7BD  mov     dword ptr [rcx+rax+0CCh], 0
0x1AE7C8  nop     dword ptr [rax+rax+00000000h]
0x1AE7D0  mov     rax, [rbp+var_D8]
0x1AE7D7  mov     ecx, [r13+0]
0x1AE7DB  mov     rdx, [r9]
0x1AE7DE  mov     rsi, [rbp+var_100]
0x1AE7E5  mov     dword ptr [rbp+var_F8], 0
0x1AE7EF  mov     eax, [rax]
0x1AE7F1  imul    rcx, 250h
0x1AE7F8  mov     [rdx+rcx+8], eax
0x1AE7FC  mov     eax, [rbx+28h]
0x1AE7FF  inc     dword ptr [rbp+var_D0]
0x1AE805  inc     r12d
0x1AE808  mov     ecx, eax
0x1AE80A  cmp     r12d, eax
0x1AE80D  jb      loc_1AE010
0x1AE813  jmp     short loc_1AE828
0x1AE815  align 20h
0x1AE820  mov     dword ptr [rbp+var_110], edx
0x1AE826  xor     ecx, ecx
0x1AE828  mov     edx, dword ptr [rbp+var_110]
0x1AE82E  inc     edx
0x1AE830  cmp     edx, [rbx+18h]
0x1AE833  jb      loc_1ADFE0
0x1AE839  test    eax, eax
0x1AE83B  jz      loc_1AECFC
0x1AE841  xor     edi, edi
0x1AE843  nop     word ptr [rax+rax+00000000h]
0x1AE850  mov     rdx, [rbx+30h]
0x1AE854  mov     edi, edi
0x1AE856  mov     r10, [r9]
0x1AE859  lea     rsi, [rdi+rdi*4]
0x1AE85D  mov     r8d, [rdx+rsi*8+8]
0x1AE862  cmp     dword ptr [rdx+rsi*8+18h], 0
0x1AE867  jz      loc_1AEC60
0x1AE86D  lea     rax, [rdx+rsi*8+8]
0x1AE872  mov     [rbp+var_138], rdi
0x1AE879  lea     rdi, [rdx+rsi*8+18h]
0x1AE87E  lea     rcx, [rdx+rsi*8+20h]
0x1AE883  lea     rdx, [rdx+rsi*8+0Ch]
0x1AE888  mov     r14, rbx
0x1AE88B  xor     r15d, r15d
0x1AE88E  mov     [rbp+var_140], r8
0x1AE895  mov     [rbp+var_148], r10
0x1AE89C  mov     [rbp+var_120], rax
0x1AE8A3  imul    rax, r8, 250h
0x1AE8AA  mov     [rbp+var_F0], rdi
0x1AE8B1  mov     [rbp+var_F8], rcx
0x1AE8B8  mov     [rbp+var_E0], rdx
0x1AE8BF  lea     rcx, [r10+rax+0Ch]
0x1AE8C4  lea     r8, [r10+rax+0F0h]
0x1AE8CC  lea     rdi, [r10+rax+0F4h]
0x1AE8D4  lea     rax, [r10+rax+58h]
0x1AE8D9  mov     [rbp+var_100], rcx
0x1AE8E0  mov     [rbp+var_110], r8
0x1AE8E7  mov     [rbp+var_118], rdi
0x1AE8EE  mov     [rbp+var_108], rax
0x1AE8F5  nop     word ptr [rax+rax+00000000h]
0x1AE900  mov     rax, [rbp+var_F8]
0x1AE907  mov     r13d, r15d
0x1AE90A  vmovss  xmm1, cs:dword_14DAE58
0x1AE912  mov     rax, [rax]
0x1AE915  vmovss  xmm0, dword ptr [rax+r13*8+4]
0x1AE91C  mov     r12d, [rax+r13*8]
0x1AE920  call    sub_1B55F0
0x1AE925  mov     rax, [rbp+var_100]
0x1AE92C  vmovss  dword ptr [rbp+var_D0], xmm0
0x1AE934  vmovss  xmm0, cs:dword_14DAE60
0x1AE93C  cmp     dword ptr [rax], 1
0x1AE93F  jnz     short loc_1AE964
0x1AE941  mov     rax, [rbp+var_110]
0x1AE948  mov     rcx, [rbp+var_118]
0x1AE94F  vmovss  xmm1, cs:dword_14DAE58
0x1AE957  vmovss  xmm0, dword ptr [rax]
0x1AE95B  vaddss  xmm0, xmm0, dword ptr [rcx]
0x1AE95F  call    sub_1B55F0
0x1AE964  test    r12d, r12d
0x1AE967  jz      short loc_1AE9B0
0x1AE969  mov     ecx, [r14+28h]
0x1AE96D  vmovss  dword ptr [rbp+var_D8], xmm0
0x1AE975  test    ecx, ecx
0x1AE977  jz      loc_1AEB9E
0x1AE97D  mov     rax, [r14+30h]
0x1AE981  xor     edx, edx
0x1AE983  lea     rsi, [rax+0Ch]
0x1AE987  nop     word ptr [rax+rax+00000000h]
0x1AE990  cmp     [rsi], r12d
0x1AE993  jz      loc_1AEABB
0x1AE999  inc     rdx
0x1AE99C  add     rsi, 28h
0x1AE9A0  cmp     edx, ecx
0x1AE9A2  jb      short loc_1AE990
0x1AE9A4  jmp     loc_1AEB9E
0x1AE9A9  align 10h
0x1AE9B0  mov     rax, [rbp+var_E0]
0x1AE9B7  mov     eax, [rax]
0x1AE9B9  cmp     eax, 63h ; 'c'
0x1AE9BC  ja      loc_1AEBD9
0x1AE9C2  mov     rcx, [rbp+var_E8]
0x1AE9C9  mov     rax, [rbp+var_120]
0x1AE9D0  mov     eax, [rax]
0x1AE9D2  xor     esi, esi
0x1AE9D4  lea     rdx, [rbp+var_90]
0x1AE9DB  vmovss  dword ptr [rbp+var_D8], xmm0
0x1AE9E3  mov     rcx, [rcx]
0x1AE9E6  imul    rax, 250h
0x1AE9ED  mov     rdi, [rcx+rax]
0x1AE9F1  mov     rax, cs:qword_57F1C20
0x1AE9F8  mov     rbx, [rax+70h]
0x1AE9FC  mov     [rbp+var_128], rdi
0x1AEA03  call    sceNgs2RackGetVoiceHandle
0x1AEA08  xor     esi, esi
0x1AEA0A  mov     rdi, rbx
0x1AEA0D  lea     rdx, [rbp+var_B0]
0x1AEA14  call    sceNgs2RackGetVoiceHandle
0x1AEA19  mov     rdi, [rbp+var_90]
0x1AEA20  mov     rax, [rbp+var_B0]
0x1AEA27  lea     rbx, [rbp+var_70]
0x1AEA2B  mov     [rbp+var_70], 18h
0x1AEA31  mov     [rbp+var_6E], 0
0x1AEA37  mov     dword ptr [rbp+var_6C], 5
0x1AEA3E  mov     dword ptr [rbp+var_6C+4], r15d
0x1AEA42  mov     rsi, rbx
0x1AEA45  mov     [rbp+var_60], rax
0x1AEA49  mov     [rbp+var_64], 0
0x1AEA50  call    sceNgs2VoiceControl
0x1AEA55  mov     rdi, [rbp+var_128]
0x1AEA5C  xor     esi, esi
0x1AEA5E  lea     rdx, [rbp+var_C0]
0x1AEA65  call    sceNgs2RackGetVoiceHandle
0x1AEA6A  vmovss  xmm0, dword ptr [rbp+var_D8]
0x1AEA72  mov     rdi, [rbp+var_C0]
0x1AEA79  mov     rsi, rbx
0x1AEA7C  mov     [rbp+var_70], 10h
0x1AEA82  mov     [rbp+var_6E], 0
0x1AEA88  mov     dword ptr [rbp+var_6C], 2
0x1AEA8F  mov     dword ptr [rbp+var_6C+4], r15d
0x1AEA93  vmulss  xmm0, xmm0, dword ptr [rbp+var_D0]
0x1AEA9B  vmovss  [rbp+var_64], xmm0
0x1AEAA0  call    sceNgs2VoiceControl
0x1AEAA5  mov     rax, [rbp+var_E0]
0x1AEAAC  vmovss  xmm0, dword ptr [rbp+var_D8]
0x1AEAB4  mov     eax, [rax]
0x1AEAB6  jmp     loc_1AEBD9
0x1AEABB  mov     rsi, [rbp+var_E8]
0x1AEAC2  mov     rcx, [rbp+var_120]
0x1AEAC9  mov     ecx, [rcx]
0x1AEACB  mov     rsi, [rsi]
0x1AEACE  imul    rcx, 250h
0x1AEAD5  mov     rdi, [rsi+rcx]
0x1AEAD9  lea     rcx, [rdx+rdx*4]
0x1AEADD  lea     rdx, [rbp+var_90]
0x1AEAE4  mov     eax, [rax+rcx*8+8]
0x1AEAE8  mov     [rbp+var_128], rdi
0x1AEAEF  imul    rax, 250h
0x1AEAF6  mov     rbx, [rsi+rax]
0x1AEAFA  xor     esi, esi
0x1AEAFC  call    sceNgs2RackGetVoiceHandle
0x1AEB01  xor     esi, esi
0x1AEB03  mov     rdi, rbx
0x1AEB06  lea     rdx, [rbp+var_B0]
0x1AEB0D  call    sceNgs2RackGetVoiceHandle
0x1AEB12  mov     rdi, [rbp+var_90]
0x1AEB19  mov     rax, [rbp+var_B0]
0x1AEB20  lea     rbx, [rbp+var_70]
0x1AEB24  mov     [rbp+var_70], 18h
0x1AEB2A  mov     [rbp+var_6E], 0
0x1AEB30  mov     dword ptr [rbp+var_6C], 5
0x1AEB37  mov     dword ptr [rbp+var_6C+4], r15d
0x1AEB3B  mov     rsi, rbx
0x1AEB3E  mov     [rbp+var_60], rax
0x1AEB42  mov     [rbp+var_64], 0
0x1AEB49  call    sceNgs2VoiceControl
0x1AEB4E  mov     rdi, [rbp+var_128]
0x1AEB55  xor     esi, esi
0x1AEB57  lea     rdx, [rbp+var_C0]
0x1AEB5E  call    sceNgs2RackGetVoiceHandle
0x1AEB63  vmovss  xmm0, dword ptr [rbp+var_D8]
0x1AEB6B  mov     rdi, [rbp+var_C0]
0x1AEB72  mov     rsi, rbx
0x1AEB75  mov     [rbp+var_70], 10h
0x1AEB7B  mov     [rbp+var_6E], 0
0x1AEB81  mov     dword ptr [rbp+var_6C], 2
0x1AEB88  mov     dword ptr [rbp+var_6C+4], r15d
0x1AEB8C  vmulss  xmm0, xmm0, dword ptr [rbp+var_D0]
0x1AEB94  vmovss  [rbp+var_64], xmm0
0x1AEB99  call    sceNgs2VoiceControl
0x1AEB9E  mov     rcx, cs:qword_57F1C20
0x1AEBA5  imul    rax, r12, 98h
0x1AEBAC  vmovss  xmm0, dword ptr [rbp+var_D8]
0x1AEBB4  lea     rdx, [rcx+rax+0A8h]
0x1AEBBC  mov     rax, [rbp+var_E0]
0x1AEBC3  mov     eax, [rax]
0x1AEBC5  imul    rsi, rax, 98h
0x1AEBCC  lea     rcx, [rcx+rsi+0A8h]
0x1AEBD4  mov     [rcx+r13*8+50h], rdx
0x1AEBD9  mov     rcx, [rbp+var_108]
0x1AEBE0  vmovss  xmm1, dword ptr [rbp+var_D0]
0x1AEBE8  mov     eax, eax
0x1AEBEA  mov     rsi, [rbp+var_F0]
0x1AEBF1  inc     r15d
0x1AEBF4  imul    rax, 98h
0x1AEBFB  mov     rcx, [rcx]
0x1AEBFE  vmulss  xmm0, xmm1, xmm0
0x1AEC02  mov     [rcx+r13*8], r12d
0x1AEC06  vmovss  dword ptr [rcx+r13*8+4], xmm1
0x1AEC0D  mov     rcx, cs:qword_57F1C20
0x1AEC14  add     rax, rcx
0x1AEC17  vmovss  dword ptr [rax+r13*4+0D0h], xmm0
0x1AEC21  mov     edx, [rsi]
0x1AEC23  cmp     r15d, edx
0x1AEC26  jb      loc_1AE900
0x1AEC2C  mov     rbx, r14
0x1AEC2F  mov     r9, [rbp+var_E8]
0x1AEC36  mov     rdi, [rbp+var_138]
0x1AEC3D  mov     r8, [rbp+var_140]
0x1AEC44  mov     r10, [rbp+var_148]
0x1AEC4B  mov     r11, [rbp+var_E0]
0x1AEC52  mov     eax, [rbx+28h]
0x1AEC55  jmp     short loc_1AEC6E
0x1AEC57  align 20h
0x1AEC60  mov     rcx, cs:qword_57F1C20
0x1AEC67  lea     r11, [rdx+rsi*8+0Ch]
0x1AEC6C  xor     edx, edx
0x1AEC6E  imul    rsi, r8, 250h
0x1AEC75  inc     edi
0x1AEC77  mov     [r10+rsi+14h], edx
0x1AEC7C  mov     esi, [r11]
0x1AEC7F  imul    rsi, 98h
0x1AEC86  cmp     edi, eax
0x1AEC88  mov     [rcx+rsi+0C3h], dl
0x1AEC8F  jb      loc_1AE850
0x1AEC95  mov     ecx, [rbx]
0x1AEC97  xor     r15d, r15d
0x1AEC9A  test    eax, eax
0x1AEC9C  jz      short loc_1AECAB
0x1AEC9E  cmp     ecx, 1
0x1AECA1  jnz     short loc_1AECAB
0x1AECA3  mov     rdx, [rbx+30h]
0x1AECA7  mov     r15d, [rdx+8]
0x1AECAB  test    eax, eax
0x1AECAD  jz      short loc_1AED01
0x1AECAF  xor     r14d, r14d
0x1AECB2  nop     word ptr [rax+rax+00000000h]
0x1AECC0  mov     rcx, [r9+10h]
0x1AECC4  lea     eax, [r15+r14]
0x1AECC8  mov     edx, 28h ; '('
0x1AECCD  mov     r12, r9
0x1AECD0  lea     rax, [rax+rax*4]
0x1AECD4  lea     rdi, [rcx+rax*8]
0x1AECD8  mov     eax, r14d
0x1AECDB  lea     rsi, [rax+rax*4]
0x1AECDF  shl     rsi, 3
0x1AECE3  add     rsi, [rbx+30h]
0x1AECE7  call    sub_1B17C0
0x1AECEC  inc     r14d
0x1AECEF  cmp     r14d, [rbx+28h]
0x1AECF3  mov     r9, r12
0x1AECF6  jb      short loc_1AECC0
0x1AECF8  mov     ecx, [rbx]
0x1AECFA  jmp     short loc_1AED01
0x1AECFC  mov     ecx, [rbx]
0x1AECFE  xor     r15d, r15d
0x1AED01  mov     eax, ecx
0x1AED03  mov     r13, r9
0x1AED06  mov     [r9+rax*4+1Ch], r15d
0x1AED0B  mov     eax, [rbx]
0x1AED0D  mov     ecx, [rbx+28h]
0x1AED10  mov     [r9+rax*4+24h], ecx
0x1AED15  call    sub_1B0050
0x1AED1A  mov     rax, rbx
0x1AED1D  mov     ebx, [rax]
0x1AED1F  cmp     rbx, 2
0x1AED23  jb      short loc_1AED2C
0x1AED25  xor     eax, eax
0x1AED27  jmp     loc_1AEFA6
0x1AED2C  cmp     dword ptr [r13+rbx*4+24h], 0
0x1AED32  mov     r14, rax
0x1AED35  jz      loc_1AEDD6
0x1AED3B  mov     eax, [r13+rbx*4+1Ch]
0x1AED40  xor     r15d, r15d
0x1AED43  mov     [rbp+var_D0], rax
0x1AED4A  mov     rax, [r13+10h]
0x1AED4E  xchg    ax, ax
0x1AED50  mov     rcx, [rbp+var_D0]
0x1AED57  lea     ecx, [rcx+r15]
0x1AED5B  xor     esi, esi
0x1AED5D  lea     rdx, [rbp+var_B0]
0x1AED64  shl     rcx, 3
0x1AED68  lea     r12, [rcx+rcx*4]
0x1AED6C  mov     rcx, [r13+0]
0x1AED70  mov     eax, [rax+r12+8]
0x1AED75  imul    rax, 250h
0x1AED7C  mov     rdi, [rcx+rax]
0x1AED80  call    sceNgs2RackGetVoiceHandle
0x1AED85  mov     rdi, [rbp+var_B0]
0x1AED8C  lea     rsi, [rbp+var_70]
0x1AED90  mov     [rbp+var_70], 0Ch
0x1AED96  mov     [rbp+var_6E], 0
0x1AED9C  mov     [rbp+var_6C], 6
0x1AEDA4  call    sceNgs2VoiceControl
0x1AEDA9  mov     rax, [r13+10h]
0x1AEDAD  mov     rdx, cs:qword_57F1C20
0x1AEDB4  inc     r15d
0x1AEDB7  mov     ecx, [rax+r12+0Ch]
0x1AEDBC  imul    rcx, 98h
0x1AEDC3  mov     byte ptr [rdx+rcx+0C0h], 1
0x1AEDCB  cmp     r15d, [r13+rbx*4+24h]
0x1AEDD0  jb      loc_1AED50
0x1AEDD6  xor     r15d, r15d
0x1AEDD9  mov     [rbp+var_E8], r13
0x1AEDE0  test    ebx, ebx
0x1AEDE2  jnz     short loc_1AEE46
0x1AEDE4  nop     word ptr [rax+rax+00000000h]
0x1AEDF0  mov     rax, cs:qword_57F1C20
0x1AEDF7  imul    r12, r15, 98h
0x1AEDFE  mov     ebx, [rax+r12+0F0h]
0x1AEE06  test    ebx, ebx
0x1AEE08  jz      short loc_1AEE3A
0x1AEE0A  lea     rdi, [rax+r12+0A8h]
0x1AEE12  xor     esi, esi
0x1AEE14  call    sub_1B1470
0x1AEE19  cmp     ebx, 1
0x1AEE1C  jz      short loc_1AEE3A
0x1AEE1E  dec     ebx
0x1AEE20  mov     rax, cs:qword_57F1C20
0x1AEE27  xor     esi, esi
0x1AEE29  lea     rdi, [rax+r12+0A8h]
0x1AEE31  call    sub_1B1470
0x1AEE36  dec     ebx
0x1AEE38  jnz     short loc_1AEE20
0x1AEE3A  inc     r15
0x1AEE3D  cmp     r15, 80h
0x1AEE44  jnz     short loc_1AEDF0
0x1AEE46  mov     r12, [rbp+var_E8]
0x1AEE4D  mov     ebx, 1
0x1AEE52  nop     word ptr [rax+rax+00000000h]
0x1AEE60  mov     rax, cs:qword_57F1C20
0x1AEE67  imul    r13, rbx, 98h
0x1AEE6E  cmp     qword ptr [rax+r13+0B0h], 0
0x1AEE77  jz      loc_1AEF70
0x1AEE7D  cmp     byte ptr [rax+r13+0C1h], 0
0x1AEE86  jz      loc_1AEF70
0x1AEE8C  cmp     byte ptr [rax+r13+0C0h], 0
0x1AEE95  jz      loc_1AEF70
0x1AEE9B  cmp     dword ptr [rax+r13+0F0h], 0
0x1AEEA4  jg      loc_1AEF70
0x1AEEAA  cmp     dword ptr [rax+r13+0F4h], 0
0x1AEEB3  jg      loc_1AEF70
0x1AEEB9  mov     rax, [rbp+var_E8]
0x1AEEC0  xor     r15d, r15d
0x1AEEC3  mov     dword ptr [rbp+var_D0], 0
0x1AEECD  mov     eax, [rax+24h]
0x1AEED0  test    eax, eax
0x1AEED2  jz      loc_1AEF70
0x1AEED8  nop     dword ptr [rax+rax+00000000h]
0x1AEEE0  mov     rcx, [r12+10h]
0x1AEEE5  mov     r15d, r15d
0x1AEEE8  lea     rdx, [r15+r15*4]
0x1AEEEC  mov     esi, [rcx+rdx*8+0Ch]
0x1AEEF0  cmp     rsi, rbx
0x1AEEF3  jnz     short loc_1AEF4B
0x1AEEF5  mov     eax, [rcx+rdx*8+8]
0x1AEEF9  mov     rcx, [r12]
0x1AEEFD  xor     esi, esi
0x1AEEFF  lea     rdx, [rbp+var_90]
0x1AEF06  imul    rax, 250h
0x1AEF0D  mov     rdi, [rcx+rax]
0x1AEF11  call    sceNgs2RackGetVoiceHandle
0x1AEF16  mov     rdi, [rbp+var_90]
0x1AEF1D  lea     rsi, [rbp+var_70]
0x1AEF21  mov     rax, 100000006h
0x1AEF2B  mov     [rbp+var_70], 0Ch
0x1AEF31  mov     [rbp+var_6E], 0
0x1AEF37  mov     [rbp+var_6C], rax
0x1AEF3B  call    sceNgs2VoiceControl
0x1AEF40  mov     eax, [r12+24h]
0x1AEF45  inc     dword ptr [rbp+var_D0]
0x1AEF4B  inc     r15d
0x1AEF4E  cmp     r15d, eax
0x1AEF51  jb      short loc_1AEEE0
0x1AEF53  cmp     dword ptr [rbp+var_D0], 0
0x1AEF5A  jz      short loc_1AEF70
0x1AEF5C  mov     rax, cs:qword_57F1C20
0x1AEF63  mov     byte ptr [rax+r13+0C0h], 0
0x1AEF6C  nop     dword ptr [rax+00h]
0x1AEF70  inc     rbx
0x1AEF73  cmp     rbx, 80h
0x1AEF7A  jnz     loc_1AEE60
0x1AEF80  vxorps  xmm0, xmm0, xmm0
0x1AEF84  call    sub_1B08E0
0x1AEF89  xor     eax, eax
0x1AEF8B  cmp     dword ptr [r14], 0
0x1AEF8F  jnz     short loc_1AEFA6
0x1AEF91  mov     rcx, cs:qword_57F1C20
0x1AEF98  mov     rdx, [rbp+var_E8]
0x1AEF9F  mov     [rcx+4CA8h], rdx
0x1AEFA6  mov     rdx, cs:qword_1700698
0x1AEFAD  mov     rcx, [rdx]
0x1AEFB0  cmp     rcx, [rbp+var_30]
0x1AEFB4  jnz     short loc_1AEFC8
0x1AEFB6  add     rsp, 128h
0x1AEFBD  pop     rbx
0x1AEFBE  pop     r12
0x1AEFC0  pop     r13
0x1AEFC2  pop     r14
0x1AEFC4  pop     r15
0x1AEFC6  pop     rbp
0x1AEFC7  retn
0x1AEFC8  call    __stack_chk_fail
```
