# NGS2 — статическая карта вызовов EBOOT

> Сформировано по результатам IDA 7.0 / IDAPython из `result/eboot.elf.ngs2_static.json`, файл `eboot.elf`, image base `0`. Анализ статический: код не исполнялся. Дата исходного сканирования: 2026-11-01 11:05:04.  
> Цель: инвентаризация ABI NGS2, call site, параметров и точек для сопоставления с HLE.

## 1. Итоговая сводка

| Метрика | Значение |
|---|---:|
| Импортируемые NGS2 API | 10 |
| Обнаруженные прямые call site | 238 |
| Сгруппированные сигнатуры вызовов | 42 |
| Функции-производители NGS2-вызовов | 20 |
| Статические вхождения известных NGS2-констант | 193,289 |
| Разрешённые NGS2-символы в импортах | 10 |
| Строки с NID, найденные в бинарнике | 0 |

**Главный вывод:** импортируемая поверхность EBOOT ограничена десятью NGS2-функциями. Большая часть логики сосредоточена в `sceNgs2VoiceControl` и `sceNgs2RackGetVoiceHandle`: вместе они дают 197 из 238 прямых вызовов (82.8%).

### Важная оговорка о достоверности

Счётчик `confidence=high` в выгрузке означает уверенное сопоставление xref/call target с импортом, но **не** гарантирует, что параметры и объекты полностью восстановлены. Все 238 call site распознаны как прямые вызовы; при этом у 107 из 111 вызовов `VoiceControl` цепочка параметров не восстановлена до полноценного списка структур. Для динамических цепочек отчёт IDA сохраняет лишь часть локальных записей и function-wide константы. Последние ниже помечаются как кандидаты, а не как безусловно переданные параметры.

## 2. Карта API и число вызовов

| API | Вызовы | Функций-производителей | Роль |
|---|---:|---:|---|
| `sceNgs2RackCreate` | 11 | 1 | создание rack с контекстным буфером |
| `sceNgs2RackCreateWithAllocator` | 4 | 1 | создание rack через allocator |
| `sceNgs2RackDestroy` | 9 | 3 | уничтожение rack |
| `sceNgs2RackGetVoiceHandle` | 86 | 17 | получение voice handle |
| `sceNgs2RackQueryBufferSize` | 11 | 1 | запрос буферов rack |
| `sceNgs2SystemCreateWithAllocator` | 1 | 1 | создание системы |
| `sceNgs2SystemDestroy` | 2 | 2 | уничтожение системы |
| `sceNgs2SystemRender` | 1 | 1 | рендер аудио |
| `sceNgs2VoiceControl` | 111 | 15 | параметры/события/маршрутизация voice |
| `sceNgs2VoiceGetState` | 2 | 1 | чтение состояния voice |

### Роли основных функций-производителей

| Функция | Всего вызовов NGS2 | Состав |
|---|---:|---|
| `sub_1AC510` | 49 | RackCreate: 11<br>RackGetVoiceHandle: 15<br>RackQueryBufferSize: 11<br>VoiceControl: 12 |
| `sub_1ADC10` | 48 | RackGetVoiceHandle: 23<br>VoiceControl: 25 |
| `sub_1A9690` | 40 | RackGetVoiceHandle: 11<br>VoiceControl: 29 |
| `sub_1A69C0` | 33 | RackCreateWithAllocator: 4<br>RackDestroy: 4<br>RackGetVoiceHandle: 6<br>SystemCreateWithAllocator: 1<br>SystemDestroy: 1<br>VoiceControl: 17 |
| `sub_1AEFD0` | 13 | RackGetVoiceHandle: 7<br>VoiceControl: 6 |
| `sub_1A8E90` | 12 | RackGetVoiceHandle: 6<br>VoiceControl: 6 |
| `sub_1B08E0` | 6 | RackGetVoiceHandle: 3<br>VoiceControl: 3 |
| `sub_1A83A0` | 5 | RackDestroy: 4<br>SystemDestroy: 1 |
| `sub_1B0300` | 5 | RackGetVoiceHandle: 3<br>VoiceControl: 2 |
| `sub_1A85B0` | 4 | RackGetVoiceHandle: 2<br>VoiceGetState: 2 |
| `sub_1AB920` | 4 | RackGetVoiceHandle: 2<br>VoiceControl: 2 |
| `sub_1B11E0` | 4 | RackGetVoiceHandle: 2<br>VoiceControl: 2 |
| `sub_1ABD70` | 3 | RackGetVoiceHandle: 1<br>VoiceControl: 2 |
| `sub_1ABEF0` | 3 | RackGetVoiceHandle: 1<br>VoiceControl: 2 |
| `sub_1A8160` | 2 | RackGetVoiceHandle: 1<br>VoiceControl: 1 |
| `sub_1A82B0` | 2 | RackGetVoiceHandle: 1<br>VoiceControl: 1 |
| `sub_1ABB70` | 2 | RackGetVoiceHandle: 1<br>VoiceControl: 1 |
| `sub_1ADB70` | 1 | RackDestroy: 1 |
| `sub_1B0050` | 1 | RackGetVoiceHandle: 1 |
| `sub_1B04F0` | 1 | SystemRender: 1 |

Интерпретация:
- `sub_1A69C0` — создание системы, первоначальное создание базовых rack, их первичная настройка, уничтожение при неудачном/завершающем пути.
- `sub_1AC510` — построение набора bus/submixer/reverb/custom rack: по 11 запросов размера и созданий rack, затем настройка связей и обработчиков.
- `sub_1A9690` — основной путь sampler voice: получение voice и передача параметров источника/волны.
- `sub_1ADC10` — настройки mastering, его портов и маршрутизации.
- `sub_1AEFD0` — конфигурирование FX/custom bus; содержит сигнатуры компрессора, фильтра, reverb и custom-модулей.
- `sub_1B04F0` — render thread: единственный статически найденный вызов `SystemRender`.
- `sub_1A85B0` — запрос состояния voice, два разных размера state.

## 3. Жизненный цикл и граф вызовов

### 3.1 Инициализация системы и базовых rack

Функция `sub_1A69C0` содержит:
1. `SystemCreateWithAllocator` — 1 вызов (`0x1A7656`).
2. `RackCreateWithAllocator` — 4 вызова:
   - MASTERING `0x3000` — `0x1A76F1`;
   - SUBMIXER `0x2000` — `0x1A7773` и `0x1A78E6`;
   - SAMPLER `0x1000` — `0x1A7828`.
3. Получение voice handles и `VoiceControl` для setup, output, patch, событий и матриц.
4. Ветви cleanup: до 4 вызовов `RackDestroy` и один `SystemDestroy` на пути очистки.

### 3.2 Построение bus-графа

`sub_1AC510` вызывает `RackQueryBufferSize` и `RackCreate` для каждой конфигурации. Восстановленные значения rack ID:

| Rack ID | Тип | RackQueryBufferSize | RackCreate |
|---:|---|---:|---:|
| `0x1000` | SAMPLER | 0 | 0 |
| `0x2000` | SUBMIXER | 7 | 7 |
| `0x2001` | REVERB | 1 | 1 |
| `0x3000` | MASTERING | 0 | 0 |
| `0x4002` | CUSTOM_SUBMIXER | 3 | 3 |

MASTERING и SAMPLER создаются отдельно через `RackCreateWithAllocator`. Итого в статически восстановленных call site: 11 запросов размера + 11 `RackCreate` + 4 `RackCreateWithAllocator`.

**Критическое следствие для текущего HLE:** `sub_1AC510` трижды создаёт `CUSTOM_SUBMIXER (0x4002)` и трижды запрашивает для него размер буфера. В текущем `Ngs2Exports.cpp` функция `RackTailWords()` содержит только SAMPLER, SUBMIXER, MASTERING и REVERB; ветви `0x4002` нет. Поэтому передача реальной опции этого rack в PS4→PS5 адаптер приводит к `ngs2_stop(... "rack id ... is not translated")`. Это не гипотетическое использование: rack ID зафиксирован в аргументе `RSI/EDI` непосредственно перед вызовами:
- Query: `0x1AC710`, `0x1AD427`, `0x1AD5DE`;
- Create: `0x1AC762`, `0x1AD479`, `0x1AD630`.

### 3.3 Render

Единственный статический вызов `sceNgs2SystemRender`:
- call site: `0x1B064C`;
- caller: `sub_1B04F0`;
- аргументы: system — из объекта/поля памяти; render buffer array — адрес локальной структуры на стеке; число буферов — регистровое значение (`RDX=R12D` в последнем определении).

Из одного статического call site нельзя гарантированно восстановить runtime-число буферов и их размеры. Отдельные динамические заметки в `docs/NGS2_LEVANTAMENTO.md` сообщают для TLG основной выход float32, 8 каналов, 256 кадров, 48 кГц. Это нужно проверять именно по native trace, а не выводить только из статического call site.

### 3.4 Cleanup и состояние voice

- `RackDestroy`: 9 вызовов, в `sub_1A69C0`, `sub_1A83A0`, `sub_1ADB70`.
- `SystemDestroy`: 2 вызова, в `sub_1A69C0`, `sub_1A83A0`.
- `VoiceGetState`: два вызова из `sub_1A85B0`: размер `0x30` (`0x1A862D`) и `0x10` (`0x1A8800`). Следовательно, нельзя ограничивать совместимость только sampler state 0x30: существует и 16-байтовый вариант (с высокой вероятностью submixer state, что соответствует текущему PS4 adapter layout).

## 4. Точная карта rack create/query

| API | Call site | Caller | Rack type | Инструкция, задающая ID |
|---|---|---|---|---|
| `sceNgs2RackCreateWithAllocator` | 0x1A76F1 | `sub_1A69C0` | `MASTERING` (0x3000) | `mov     esi, 3000h` |
| `sceNgs2RackCreateWithAllocator` | 0x1A7773 | `sub_1A69C0` | `SUBMIXER` (0x2000) | `mov     esi, 2000h` |
| `sceNgs2RackCreateWithAllocator` | 0x1A7828 | `sub_1A69C0` | `SAMPLER` (0x1000) | `mov     esi, 1000h` |
| `sceNgs2RackCreateWithAllocator` | 0x1A78E6 | `sub_1A69C0` | `SUBMIXER` (0x2000) | `mov     esi, 2000h` |
| `sceNgs2RackQueryBufferSize` | 0x1AC710 | `sub_1AC510` | `CUSTOM_SUBMIXER` (0x4002) | `mov     edi, 4002h` |
| `sceNgs2RackCreate` | 0x1AC762 | `sub_1AC510` | `CUSTOM_SUBMIXER` (0x4002) | `mov     esi, 4002h` |
| `sceNgs2RackQueryBufferSize` | 0x1AC9AC | `sub_1AC510` | `SUBMIXER` (0x2000) | `mov     edi, 2000h` |
| `sceNgs2RackCreate` | 0x1AC9FE | `sub_1AC510` | `SUBMIXER` (0x2000) | `mov     esi, 2000h` |
| `sceNgs2RackQueryBufferSize` | 0x1ACB1D | `sub_1AC510` | `SUBMIXER` (0x2000) | `mov     edi, 2000h` |
| `sceNgs2RackCreate` | 0x1ACB6F | `sub_1AC510` | `SUBMIXER` (0x2000) | `mov     esi, 2000h` |
| `sceNgs2RackQueryBufferSize` | 0x1ACC7D | `sub_1AC510` | `SUBMIXER` (0x2000) | `mov     edi, 2000h` |
| `sceNgs2RackCreate` | 0x1ACCCF | `sub_1AC510` | `SUBMIXER` (0x2000) | `mov     esi, 2000h` |
| `sceNgs2RackQueryBufferSize` | 0x1ACE05 | `sub_1AC510` | `SUBMIXER` (0x2000) | `mov     edi, 2000h` |
| `sceNgs2RackCreate` | 0x1ACE57 | `sub_1AC510` | `SUBMIXER` (0x2000) | `mov     esi, 2000h` |
| `sceNgs2RackQueryBufferSize` | 0x1ACF74 | `sub_1AC510` | `REVERB` (0x2001) | `mov     edi, 2001h` |
| `sceNgs2RackCreate` | 0x1ACFC6 | `sub_1AC510` | `REVERB` (0x2001) | `mov     esi, 2001h` |
| `sceNgs2RackQueryBufferSize` | 0x1AD0DE | `sub_1AC510` | `SUBMIXER` (0x2000) | `mov     edi, 2000h` |
| `sceNgs2RackCreate` | 0x1AD130 | `sub_1AC510` | `SUBMIXER` (0x2000) | `mov     esi, 2000h` |
| `sceNgs2RackQueryBufferSize` | 0x1AD249 | `sub_1AC510` | `SUBMIXER` (0x2000) | `mov     edi, 2000h` |
| `sceNgs2RackCreate` | 0x1AD29B | `sub_1AC510` | `SUBMIXER` (0x2000) | `mov     esi, 2000h` |
| `sceNgs2RackQueryBufferSize` | 0x1AD427 | `sub_1AC510` | `CUSTOM_SUBMIXER` (0x4002) | `mov     edi, 4002h` |
| `sceNgs2RackCreate` | 0x1AD479 | `sub_1AC510` | `CUSTOM_SUBMIXER` (0x4002) | `mov     esi, 4002h` |
| `sceNgs2RackQueryBufferSize` | 0x1AD5DE | `sub_1AC510` | `CUSTOM_SUBMIXER` (0x4002) | `mov     edi, 4002h` |
| `sceNgs2RackCreate` | 0x1AD630 | `sub_1AC510` | `CUSTOM_SUBMIXER` (0x4002) | `mov     esi, 4002h` |
| `sceNgs2RackQueryBufferSize` | 0x1AD765 | `sub_1AC510` | `SUBMIXER` (0x2000) | `mov     edi, 2000h` |
| `sceNgs2RackCreate` | 0x1AD7B7 | `sub_1AC510` | `SUBMIXER` (0x2000) | `mov     esi, 2000h` |

## 5. VoiceControl: карта семейств параметров

### 5.1 Полностью/частично восстановленные заголовки в локальных структурах

IDA нашла 46 вызовов, где рядом с call site удалось восстановить прямую запись в поле `id` заголовка `VoiceControl`. Заголовок PS4 имеет вид:

```c
struct ParamHeader {
    uint16_t size;
    int16_t  next;   // byte offset to next parameter; 0 terminates chain
    uint32_t id;
};
```

Для этих случаев размер и `next` берутся из записей в стек; неизвестные payload-поля оставлены неизвестными. Суммарно:

| Param ID | Имя | Восстановленных call site |
|---:|---|---:|
| `0x00000006` | KICK_EVENT | 12 |
| `0x20000000` | SUBMIXER_SETUP | 9 |
| `0x00000005` | PATCH | 5 |
| `0x30000000` | MASTERING_SETUP | 3 |
| `0x30000005` | MASTERING_OUTPUT | 2 |
| `0x10000001` | SAMPLER_ADD_WAVEFORM_BLOCKS | 2 |
| `0x00000002` | PORT_VOLUME | 2 |
| `0x1000000A` | SAMPLER_FILTER | 1 |
| `0x10000000` | SAMPLER_SETUP | 1 |
| `0x10000005` | SAMPLER_PITCH | 1 |
| `0x10000008` | SAMPLER_USER_FX | 1 |
| `0x10000006` | SAMPLER_ENVELOPE | 1 |
| `0x20000005` | UNKNOWN_20000005 | 1 |
| `0x00000001` | MATRIX_LEVELS | 1 |
| `0x20000006` | SUBMIXER_FILTER | 1 |
| `0x20000004` | SUBMIXER_USER_FX | 1 |
| `0x30000004` | MASTERING_GAIN | 1 |
| `0x30000003` | MASTERING_LIMITER | 1 |

Полный список восстановленных локальных header writes:

| VoiceControl call | Caller | ID | size | next | Статически восстановленные поля payload |
|---|---|---|---:|---:|---|
| 0x1A794C | `sub_1A69C0` | `0x30000000` MASTERING_SETUP | 0x10 | 0 | +12: mov     [rbp+var_3C], 0 = 0 |
| 0x1A7970 | `sub_1A69C0` | `0x00000006` KICK_EVENT | 0xc | 0 | — |
| 0x1A79B2 | `sub_1A69C0` | `0x20000000` SUBMIXER_SETUP | 0x10 | 0 | +12: mov     [rbp+var_3C], 0 = 0 |
| 0x1A79D6 | `sub_1A69C0` | `0x00000006` KICK_EVENT | 0xc | 0 | — |
| 0x1A7A12 | `sub_1A69C0` | `0x00000005` PATCH | 0x18 | 0 | +8: mov     dword ptr [rbp+var_44+4], 0 = 0<br>+16: mov     [rbp+var_38], rax<br>+12: mov     [rbp+var_3C], 0 = 0 |
| 0x1A7C03 | `sub_1A69C0` | `0x30000000` MASTERING_SETUP | 0x10 | 0 | +12: mov     [rbp+var_3C], 0 = 0 |
| 0x1A7C30 | `sub_1A69C0` | `0x30000005` MASTERING_OUTPUT | 0x10 | 0 | +8: mov     dword ptr [rbp+var_44+4], ebx<br>+12: mov     [rbp+var_3C], 0 = 0 |
| 0x1A7C54 | `sub_1A69C0` | `0x00000006` KICK_EVENT | 0xc | 0 | — |
| 0x1A7CC7 | `sub_1A69C0` | `0x30000000` MASTERING_SETUP | 0x10 | 0 | +12: mov     [rbp+var_3C], 0 = 0 |
| 0x1A7CF4 | `sub_1A69C0` | `0x30000005` MASTERING_OUTPUT | 0x10 | 0 | +8: mov     dword ptr [rbp+var_44+4], ebx<br>+12: mov     [rbp+var_3C], 0 = 0 |
| 0x1A7D18 | `sub_1A69C0` | `0x00000006` KICK_EVENT | 0xc | 0 | — |
| 0x1A81D9 | `sub_1A8160` | `0x00000006` KICK_EVENT | 0xc | 0 | — |
| 0x1A8314 | `sub_1A82B0` | `0x00000006` KICK_EVENT | 0xc | 0 | +8: mov     [rbp+var_20], eax |
| 0x1A9ADC | `sub_1A9690` | `0x1000000A` SAMPLER_FILTER | 0x30 | 0 | +8: mov     dword ptr [rbp+var_148], eax<br>+12: mov     dword ptr [rbp+var_148+4], r12d<br>+16: mov     dword ptr [rbp+var_148+8], ebx<br>+20: mov     dword ptr [rbp+var_148+0Ch], 0 = 0<br>+24: mov     dword ptr [rbp+var_138], edx<br>+28: vmovss  dword ptr [rbp+var_138+4], xmm0<br>+32: mov     dword ptr [rbp+var_138+8], ecx<br>+36: mov     dword ptr [rbp+var_138+0Ch], 0 = 0<br>+40: mov     [rbp+var_128], 0 = 0<br>+44: mov     [rbp+var_124], 0 = 0 |
| 0x1A9F5B | `sub_1A9690` | `0x10000000` SAMPLER_SETUP | 0x28 | 0 | +8: mov     dword ptr [rbp+var_148], r15d<br>+12: mov     dword ptr [rbp+var_148+4], r12d<br>+16: mov     dword ptr [rbp+var_148+8], ebx<br>+20: mov     dword ptr [rbp+var_148+0Ch], eax<br>+24: mov     dword ptr [rbp+var_138], r13d<br>+28: mov     dword ptr [rbp+var_138+4], r14d<br>+32: mov     dword ptr [rbp+var_138+8], 0 = 0<br>+36: mov     dword ptr [rbp+var_138+0Ch], 0 = 0 |
| 0x1A9FF4 | `sub_1A9690` | `0x10000005` SAMPLER_PITCH | 0x10 | 0 | +8: vmovss  dword ptr [rbp+var_148], xmm0<br>+12: mov     dword ptr [rbp+var_148+4], 0 = 0 |
| 0x1AA0A5 | `sub_1A9690` | `0x10000008` SAMPLER_USER_FX | 0x28 | 0 | +8: mov     qword ptr [rbp+var_148], rax<br>+16: mov     qword ptr [rbp+var_148+8], r13<br>+24: vmovups [rbp+var_138], xmm0 |
| 0x1AB135 | `sub_1A9690` | `0x10000001` SAMPLER_ADD_WAVEFORM_BLOCKS | 0x20 | 0 | +16: mov     dword ptr [rbp+var_148+8], 1 = 1<br>+8: mov     qword ptr [rbp+var_148], rax<br>+20: mov     dword ptr [rbp+var_148+0Ch], 1 = 1<br>+24: mov     qword ptr [rbp+var_138], rax |
| 0x1AB33F | `sub_1A9690` | `0x10000001` SAMPLER_ADD_WAVEFORM_BLOCKS | 0x20 | 0 | — |
| 0x1AB489 | `sub_1A9690` | `0x10000006` SAMPLER_ENVELOPE | 0x18 | 0 | +8: mov     dword ptr [rbp+var_50+8], r15d<br>+12: mov     dword ptr [rbp+var_50+0Ch], r12d<br>+16: mov     [rbp+var_40], rax |
| 0x1ABB20 | `sub_1AB920` | `0x00000005` PATCH | 0x18 | 0 | +8: mov     [rbp+var_30], ebx<br>+16: mov     [rbp+var_28], rax<br>+12: mov     [rbp+var_2C], 0 = 0 |
| 0x1ABB4C | `sub_1AB920` | `0x00000002` PORT_VOLUME | 0x10 | 0 | +8: mov     [rbp+var_30], ebx<br>+12: vmovss  [rbp+var_2C], xmm0 |
| 0x1ABC7B | `sub_1ABB70` | `0x20000000` SUBMIXER_SETUP | 0x10 | 0 | +8: mov     [rbp+var_140], eax<br>+12: mov     [rbp+var_13C], 0 = 0 |
| 0x1ABDF8 | `sub_1ABD70` | `0x00000006` KICK_EVENT | 0xc | 0 | — |
| 0x1ABEC9 | `sub_1ABD70` | `0x20000005` UNKNOWN_20000005 | 0x10 | 0 | — |
| 0x1AC1E4 | `sub_1ABEF0` | `0x00000001` MATRIX_LEVELS | 0x18 | 0 | +8: mov     [rbp+var_240], 0 = 0<br>+12: mov     [rbp+var_23C], r12d<br>+16: mov     [rbp+var_238], rax |
| 0x1AC4C7 | `sub_1ABEF0` | `0x20000006` SUBMIXER_FILTER | 0x30 | 0 | +8: mov     [rbp+var_128], r12d<br>+12: mov     [rbp+var_124], eax<br>+16: mov     dword ptr [rbp+var_120], esi<br>+20: mov     dword ptr [rbp+var_120+4], 0 = 0<br>+24: mov     [rbp+var_118], ecx<br>+28: vmovss  [rbp+var_114], xmm0<br>+32: mov     [rbp+var_110], edx<br>+36: mov     [rbp+var_10C], 0 = 0<br>+40: mov     [rbp+var_108], 0 = 0 |
| 0x1ACA5B | `sub_1AC510` | `0x20000000` SUBMIXER_SETUP | 0x10 | 0 | +12: mov     dword ptr [rbp+var_674+8], 0 = 0 |
| 0x1ACBCC | `sub_1AC510` | `0x20000000` SUBMIXER_SETUP | 0x10 | 0 | +12: mov     dword ptr [rbp+var_674+8], 0 = 0 |
| 0x1ACD2C | `sub_1AC510` | `0x20000000` SUBMIXER_SETUP | 0x10 | 0 | +12: mov     dword ptr [rbp+var_674+8], 0 = 0 |
| 0x1ACEB4 | `sub_1AC510` | `0x20000000` SUBMIXER_SETUP | 0x10 | 0 | +12: mov     dword ptr [rbp+var_674+8], 0 = 0 |
| 0x1AD18D | `sub_1AC510` | `0x20000000` SUBMIXER_SETUP | 0x10 | 0 | +12: mov     dword ptr [rbp+var_674+8], 0 = 0 |
| 0x1AD2F8 | `sub_1AC510` | `0x20000000` SUBMIXER_SETUP | 0x10 | 0 | +12: mov     dword ptr [rbp+var_674+8], 0 = 0 |
| 0x1AD814 | `sub_1AC510` | `0x20000000` SUBMIXER_SETUP | 0x10 | 0 | +12: mov     dword ptr [rbp+var_674+8], 0 = 0 |
| 0x1ADA84 | `sub_1AC510` | `0x20000004` SUBMIXER_USER_FX | 0x28 | 0 | +8: mov     qword ptr [rbp+var_674+4], rcx<br>+16: mov     qword ptr [rbp+var_674+0Ch], rax |
| 0x1ADE41 | `sub_1ADC10` | `0x30000004` MASTERING_GAIN | 0x10 | 0 | +8: vmovss  [rbp+var_B8], xmm0<br>+12: vmovss  [rbp+var_B4], xmm0 |
| 0x1ADE9F | `sub_1ADC10` | `0x30000003` MASTERING_LIMITER | 0x10 | 0 | +8: mov     [rbp+var_B8], eax<br>+12: mov     [rbp+var_B4], 3F800000h = 1065353216 |
| 0x1ADF3F | `sub_1ADC10` | `0x00000005` PATCH | 0x18 | 0 | +8: mov     dword ptr [rbp+var_6C+4], 0 = 0<br>+16: mov     [rbp+var_60], rax<br>+12: mov     [rbp+var_64], 0 = 0 |
| 0x1AE576 | `sub_1ADC10` | `0x00000005` PATCH | 0x18 | 0 | +8: mov     dword ptr [rbp+var_6C+4], 0 = 0<br>+16: mov     [rbp+var_60], rax<br>+12: mov     [rbp+var_64], 0 = 0 |
| 0x1AE5E3 | `sub_1ADC10` | `0x00000002` PORT_VOLUME | 0x10 | 0 | +8: mov     dword ptr [rbp+var_6C+4], 0 = 0<br>+12: vmovss  [rbp+var_64], xmm0 |
| 0x1AEDA4 | `sub_1ADC10` | `0x00000006` KICK_EVENT | 0xc | 0 | — |
| 0x1AEF3B | `sub_1ADC10` | `0x00000006` KICK_EVENT | 0xc | 0 | — |
| 0x1B0408 | `sub_1B0300` | `0x00000005` PATCH | 0x18 | 0 | +8: mov     dword ptr [rbp+var_44+4], 0 = 0<br>+16: mov     [rbp+var_38], rax<br>+12: mov     [rbp+var_3C], 0 = 0 |
| 0x1B0A64 | `sub_1B08E0` | `0x00000006` KICK_EVENT | 0xc | 0 | — |
| 0x1B0B24 | `sub_1B08E0` | `0x00000006` KICK_EVENT | 0xc | 0 | — |
| 0x1B134B | `sub_1B11E0` | `0x00000006` KICK_EVENT | 0xc | 0 | — |

**Особенно важные непосредственные доказательства:**
- `0x1ABEC9`, caller `sub_1ABD70`: заголовок size `0x10`, next `0`, ID `0x20000005`. Низшие 32 бита значения регистра/записи дают ID `0x20000005`, следующий dword — `1`. Семантика параметра по этому дампу не установлена; его нельзя переименовывать по догадке.
- `0x1ADE9F`, caller `sub_1ADC10`: size `0x10`, ID `0x30000003` (MASTERING_LIMITER); запись payload включает значение из регистра и `0x3F800000` (float 1.0).
- `0x1ADE41`, caller `sub_1ADC10`: size `0x10`, ID `0x30000004` (MASTERING_GAIN), два float-поля берутся из XMM0.
- `0x1AA0A5`, caller `sub_1A9690`: ID `0x10000008` (SAMPLER_USER_FX) физически записывается в локальный header. Это означает, что данный путь есть в бинарнике; это не доказывает, что он выполняется в каждом игровом сеансе.
- `0x1A9ADC`: ID `0x1000000A` SAMPLER_FILTER, размер 0x30.
- `0x1A9F5B`: ID `0x10000000` SAMPLER_SETUP, размер 0x28.
- `0x1AB135` и `0x1AB33F`: ID `0x10000001` ADD_WAVEFORM_BLOCKS, размер 0x20.
- `0x1AB489`: ID `0x10000006` ENVELOPE, размер 0x18.

### 5.2 Сгруппированные сигнатуры VoiceControl

Сигнатуры, автоматически сформированные сканером, полезны для поиска похожих call site. Они используют function/call-site контекст; **список candidate IDs в сигнатуре не равен доказанному набору параметров каждого вызова**.

| Вызовы | Сигнатура аргументов / candidate IDs | Caller | Все call site |
|---:|---|---|---|
| 22 | `voice=memory_expr / parameter_chain=reg_copy / params=00000001,00000002,00000003,00000005,00000006,10000000,10000001,10000005,10000006,10000008,1000000a` | `sub_1A9690` | 0x1AA545, 0x1AA57B, 0x1AA5B7, 0x1AA5F3, 0x1AA62F, 0x1AA66B, 0x1AA6A7, 0x1AA6E3, 0x1AA71F, 0x1AA7CC, 0x1AABA1, 0x1AABDA, 0x1AAC13, 0x1AAC4C, 0x1AAC85, 0x1AACBE, 0x1AACF7, 0x1AAD26, 0x1AAD74, 0x1AAE95, 0x1AAF4D, 0x1AAFE9 |
| 18 | `voice=memory_expr / parameter_chain=reg_copy / params=00000001,00000002,00000003,00000005,00000006,30000003,30000004` | `sub_1ADC10` | 0x1AE09D, 0x1AE0CD, 0x1AE0FD, 0x1AE12D, 0x1AE15D, 0x1AE18D, 0x1AE1BD, 0x1AE1ED, 0x1AE28C, 0x1AE381, 0x1AE3FC, 0x1AE4AB, 0x1AE685, 0x1AE6DF, 0x1AEA50, 0x1AEAA0, 0x1AEB49, 0x1AEB99 |
| 12 | `voice=memory_expr / parameter_chain=memory_expr / params=00000001,00000003,20000000,20000004` | `sub_1AC510` | 0x1AC7BE, 0x1ACA5B, 0x1ACBCC, 0x1ACD2C, 0x1ACEB4, 0x1AD022, 0x1AD18D, 0x1AD2F8, 0x1AD4D5, 0x1AD68C, 0x1AD814, 0x1ADA84 |
| 11 | `voice=memory_expr / parameter_chain=memory_expr / params=00000001,00000002,00000005,00000006,20000000,30000000,30000005` | `sub_1A69C0` | 0x1A794C, 0x1A7970, 0x1A79B2, 0x1A79D6, 0x1A7A12, 0x1A7C03, 0x1A7C30, 0x1A7C54, 0x1A7CC7, 0x1A7CF4, 0x1A7D18 |
| 7 | `voice=memory_expr / parameter_chain=memory_expr / params=00000001,00000002,00000003,00000005,00000006,30000003,30000004` | `sub_1ADC10` | 0x1ADE41, 0x1ADE9F, 0x1ADF3F, 0x1AE576, 0x1AE5E3, 0x1AEDA4, 0x1AEF3B |
| 6 | `voice=memory_expr / parameter_chain=reg_copy / params=00000001,00000002,00000005,00000006,20000000,30000000,30000005` | `sub_1A69C0` | 0x1A7A72, 0x1A7A9E, 0x1A7AC1, 0x1A7B42, 0x1A7B6F, 0x1A7B92 |
| 6 | `voice=memory_expr / parameter_chain=reg_copy / params=00000002,00000006,10000009` | `sub_1A8E90` | 0x1A900A, 0x1A9156, 0x1A9296, 0x1A93D6, 0x1A9516, 0x1A964D |
| 5 | `voice=memory_expr / parameter_chain=memory_expr / params=00000001,00000002,00000003,00000005,00000006,10000000,10000001,10000005,10000006,10000008,1000000a` | `sub_1A9690` | 0x1A9FF4, 0x1AA0A5, 0x1AB135, 0x1AB33F, 0x1AB489 |
| 3 | `voice=memory_expr / parameter_chain=memory_expr / params=00000001,00000002,00000006` | `sub_1B08E0`, `sub_1B11E0` | 0x1B0A64, 0x1B0B24, 0x1B134B |
| 3 | `voice=memory_expr / parameter_chain=memory_expr / params=00000002,00000006` | `sub_1A82B0`, `sub_1ABD70` | 0x1A8314, 0x1ABDF8, 0x1ABEC9 |
| 2 | `voice=memory_expr / parameter_chain=memory_expr / params=2e666666` | `sub_1AEFD0` | 0x1AFF71, 0x1B0015 |
| 2 | `voice=memory_expr / parameter_chain=reg_copy / params=00000001,00000002,00000003,00000005,20000002,20000006,20010001,40001c00,40001d00,40020000` | `sub_1AEFD0` | 0x1AF86A, 0x1AFA88 |
| 2 | `voice=memory_expr / parameter_chain=reg_copy / params=00000001,00000002,00000006` | `sub_1B08E0`, `sub_1B11E0` | 0x1B0C04, 0x1B141D |
| 2 | `voice=reg_copy / parameter_chain=memory_expr / params=00000002,00000005` | `sub_1AB920` | 0x1ABB20, 0x1ABB4C |
| 2 | `voice=reg_copy / parameter_chain=memory_expr / params=2e666666` | `sub_1AEFD0` | 0x1AFA04, 0x1AFC14 |
| 2 | `voice=unresolved / parameter_chain=memory_expr / params=00000001,00000002,00000003,00000005,00000006,10000000,10000001,10000005,10000006,10000008,1000000a` | `sub_1A9690` | 0x1A9ADC, 0x1A9F5B |
| 1 | `voice=memory_expr / parameter_chain=memory_expr / params=00000001,00000002,00000003,00000005,00000006,20000006` | `sub_1ABEF0` | 0x1AC1E4 |
| 1 | `voice=memory_expr / parameter_chain=memory_expr / params=00000001,00000005,00000006` | `sub_1B0300` | 0x1B0408 |
| 1 | `voice=memory_expr / parameter_chain=memory_expr / params=00000001,20000000` | `sub_1ABB70` | 0x1ABC7B |
| 1 | `voice=memory_expr / parameter_chain=reg_copy / params=00000001,00000005,00000006` | `sub_1B0300` | 0x1B039A |
| 1 | `voice=unresolved / parameter_chain=memory_expr / params=00000001,00000002,00000003,00000005,00000006,20000006` | `sub_1ABEF0` | 0x1AC4C7 |
| 1 | `voice=unresolved / parameter_chain=memory_expr / params=00000001,00000002,00000006` | `sub_1A8160` | 0x1A81D9 |

### 5.3 Результаты частотного поиска констант (не вызовы API)

Глобальный поиск обнаружил много NGS2-констант. Это количество статических вхождений в инструкциях всего EBOOT, а не количество реально переданных параметров и не runtime frequency.

| Класс | Значение | Символ | Вхождений |
|---|---:|---|---:|
| param_id | `0x00000001` | MATRIX_LEVELS | 109,334 |
| param_id | `0x00000005` | PATCH | 64,214 |
| param_id | `0x00000002` | PORT_VOLUME | 9,461 |
| param_id | `0x00000003` | PORT_MATRIX | 6,548 |
| param_id | `0x00000006` | KICK_EVENT | 3,374 |
| rack_id | `0x00001000` | SAMPLER | 133 |
| rack_id | `0x00002000` | SUBMIXER | 63 |
| param_id | `0x20000000` | SUBMIXER_SETUP | 62 |
| param_id | `0x10000000` | SAMPLER_SETUP | 50 |
| param_id | `0x30000000` | MASTERING_SETUP | 7 |
| rack_id | `0x00004002` | CUSTOM_SUBMIXER | 6 |
| rack_id | `0x00003000` | MASTERING | 5 |
| param_id | `0x30000005` | MASTERING_OUTPUT | 4 |
| rack_id | `0x00002001` | REVERB | 4 |
| param_id | `0x20000004` | SUBMIXER_USER_FX | 4 |
| param_id | `0x10000005` | SAMPLER_PITCH | 3 |
| param_id | `0x20000006` | SUBMIXER_FILTER | 3 |
| param_id | `0x1000000A` | SAMPLER_FILTER | 2 |
| param_id | `0x10000001` | SAMPLER_ADD_WAVEFORM_BLOCKS | 2 |
| param_id | `0x10000009` | SAMPLER_PEAK_METER | 1 |
| param_id | `0x10000008` | SAMPLER_USER_FX | 1 |
| param_id | `0x10000006` | SAMPLER_ENVELOPE | 1 |
| param_id | `0x30000004` | MASTERING_GAIN | 1 |
| param_id | `0x30000003` | MASTERING_LIMITER | 1 |
| param_id | `0x20000002` | SUBMIXER_COMPRESSOR | 1 |
| param_id | `0x20010001` | REVERB_I3DL2 | 1 |
| param_id | `0x40001C00` | CUSTOM_CHORUS_1C | 1 |
| param_id | `0x40001D00` | CUSTOM_DELAY_1D | 1 |
| param_id | `0x40020000` | CUSTOM_RACK_SETUP | 1 |

Большое число для `MATRIX_LEVELS`, `PATCH`, `PORT_VOLUME` и `PORT_MATRIX` объясняется использованием констант в статически слинкованном sndx-коде, таблицах и ветвлениях. Нельзя трактовать эти числа как объём вызовов `VoiceControl`.

## 6. RackGetVoiceHandle и жизненный цикл voice

Всего `RackGetVoiceHandle` вызывается 86 раз из 17 функций. В сигнатурах:
- 50/86 вариантов явно передают индекс `0`;
- 33/86 вариантов передают индекс через регистр/память;
- 3/86 имеют неразрешённый rack-аргумент.

Полная группировка:

| Вызовы | Сигнатура | Caller | Все call site |
|---:|---|---|---|
| 36 | `rack=memory_expr / voice_index=zero / out_voice=memory_expr` | `sub_1AC510`, `sub_1ADC10`, `sub_1AEFD0`, `sub_1B0300`, `sub_1B08E0`, `sub_1B11E0` | 0x1AC77F, 0x1ACA1B, 0x1ACB8C, 0x1ACCEC, 0x1ACE74, 0x1ACFE3, 0x1AD14D, 0x1AD2B8, 0x1AD496, 0x1AD64D, 0x1AD7D4, 0x1AD94B, 0x1AD99C, 0x1AD9E4, 0x1ADA29, 0x1ADD6C, 0x1ADEF2, 0x1AE240, 0x1AEA03, 0x1AEA65, 0x1AEAFC, 0x1AEB5E, 0x1AED80, 0x1AEF11, 0x1AF828, 0x1AF8FC, 0x1AFB08, 0x1AFC57, 0x1AFCEA, 0x1AFE09, 0x1AFF12, 0x1B0374, 0x1B03C4, 0x1B0A3D, 0x1B0AFD, 0x1B132A |
| 15 | `rack=memory_expr / voice_index=memory_expr / out_voice=memory_expr` | `sub_1A8160`, `sub_1A9690`, `sub_1AB920`, `sub_1ABB70`, `sub_1ABD70`, `sub_1ABEF0` | 0x1A8194, 0x1A9882, 0x1A99B3, 0x1A9E7B, 0x1AA4FB, 0x1AA790, 0x1AAF0C, 0x1AB083, 0x1AB2FF, 0x1AB453, 0x1ABA4E, 0x1ABAEF, 0x1ABC39, 0x1ABDBD, 0x1ABF53 |
| 11 | `rack=memory_expr / voice_index=memory_expr / out_voice=reg_copy` | `sub_1A85B0`, `sub_1A8E90`, `sub_1A9690`, `sub_1B0050` | 0x1A861B, 0x1A87EF, 0x1A8FEA, 0x1A913A, 0x1A927A, 0x1A93BA, 0x1A94FA, 0x1A962A, 0x1AAB6E, 0x1AAE08, 0x1B015F |
| 10 | `rack=reg_copy / voice_index=zero / out_voice=memory_expr` | `sub_1ADC10`, `sub_1B0300` | 0x1ADF03, 0x1AE06F, 0x1AE251, 0x1AE347, 0x1AE3B0, 0x1AE3C1, 0x1AE46C, 0x1AEA14, 0x1AEB0D, 0x1B03D2 |
| 6 | `rack=memory_expr / voice_index=reg_copy / out_voice=memory_expr` | `sub_1A69C0`, `sub_1ADC10` | 0x1A7A42, 0x1A7B12, 0x1A7BD2, 0x1A7C96, 0x1AE53A, 0x1AE646 |
| 4 | `rack=memory_expr / voice_index=zero / out_voice=reg_copy` | `sub_1A69C0`, `sub_1B08E0`, `sub_1B11E0` | 0x1A791B, 0x1A7981, 0x1B0BD7, 0x1B13DD |
| 3 | `rack=unresolved / voice_index=zero / out_voice=memory_expr` | `sub_1ADC10` | 0x1AE45B, 0x1AE520, 0x1AE62C |
| 1 | `rack=reg_copy / voice_index=memory_expr / out_voice=memory_expr` | `sub_1A82B0` | 0x1A82E4 |

## 7. Все 238 call site по API

Ниже — полный индекс адресов из выгрузки. Адреса указаны как EA в IDB при image base 0. Сгруппированы по API и функции-производителю; повторные вызовы намеренно не удалены.

### `sceNgs2RackCreate` — 11 call site(s)

- `sub_1AC510` (11): 0x1AC762, 0x1AC9FE, 0x1ACB6F, 0x1ACCCF, 0x1ACE57, 0x1ACFC6, 0x1AD130, 0x1AD29B, 0x1AD479, 0x1AD630, 0x1AD7B7

### `sceNgs2RackCreateWithAllocator` — 4 call site(s)

- `sub_1A69C0` (4): 0x1A76F1, 0x1A7773, 0x1A7828, 0x1A78E6

### `sceNgs2RackDestroy` — 9 call site(s)

- `sub_1A69C0` (4): 0x1A7E8D, 0x1A7EA0, 0x1A7EB3, 0x1A7EC6

- `sub_1A83A0` (4): 0x1A83BB, 0x1A83CD, 0x1A83DF, 0x1A83F1

- `sub_1ADB70` (1): 0x1ADBC4

### `sceNgs2RackGetVoiceHandle` — 86 call site(s)

- `sub_1A69C0` (6): 0x1A791B, 0x1A7981, 0x1A7A42, 0x1A7B12, 0x1A7BD2, 0x1A7C96

- `sub_1A8160` (1): 0x1A8194

- `sub_1A82B0` (1): 0x1A82E4

- `sub_1A85B0` (2): 0x1A861B, 0x1A87EF

- `sub_1A8E90` (6): 0x1A8FEA, 0x1A913A, 0x1A927A, 0x1A93BA, 0x1A94FA, 0x1A962A

- `sub_1A9690` (11): 0x1A9882, 0x1A99B3, 0x1A9E7B, 0x1AA4FB, 0x1AA790, 0x1AAB6E, 0x1AAE08, 0x1AAF0C, 0x1AB083, 0x1AB2FF, 0x1AB453

- `sub_1AB920` (2): 0x1ABA4E, 0x1ABAEF

- `sub_1ABB70` (1): 0x1ABC39

- `sub_1ABD70` (1): 0x1ABDBD

- `sub_1ABEF0` (1): 0x1ABF53

- `sub_1AC510` (15): 0x1AC77F, 0x1ACA1B, 0x1ACB8C, 0x1ACCEC, 0x1ACE74, 0x1ACFE3, 0x1AD14D, 0x1AD2B8, 0x1AD496, 0x1AD64D, 0x1AD7D4, 0x1AD94B, 0x1AD99C, 0x1AD9E4, 0x1ADA29

- `sub_1ADC10` (23): 0x1ADD6C, 0x1ADEF2, 0x1ADF03, 0x1AE06F, 0x1AE240, 0x1AE251, 0x1AE347, 0x1AE3B0, 0x1AE3C1, 0x1AE45B, 0x1AE46C, 0x1AE520, 0x1AE53A, 0x1AE62C, 0x1AE646, 0x1AEA03, 0x1AEA14, 0x1AEA65, 0x1AEAFC, 0x1AEB0D, 0x1AEB5E, 0x1AED80, 0x1AEF11

- `sub_1AEFD0` (7): 0x1AF828, 0x1AF8FC, 0x1AFB08, 0x1AFC57, 0x1AFCEA, 0x1AFE09, 0x1AFF12

- `sub_1B0050` (1): 0x1B015F

- `sub_1B0300` (3): 0x1B0374, 0x1B03C4, 0x1B03D2

- `sub_1B08E0` (3): 0x1B0A3D, 0x1B0AFD, 0x1B0BD7

- `sub_1B11E0` (2): 0x1B132A, 0x1B13DD

### `sceNgs2RackQueryBufferSize` — 11 call site(s)

- `sub_1AC510` (11): 0x1AC710, 0x1AC9AC, 0x1ACB1D, 0x1ACC7D, 0x1ACE05, 0x1ACF74, 0x1AD0DE, 0x1AD249, 0x1AD427, 0x1AD5DE, 0x1AD765

### `sceNgs2SystemCreateWithAllocator` — 1 call site(s)

- `sub_1A69C0` (1): 0x1A7656

### `sceNgs2SystemDestroy` — 2 call site(s)

- `sub_1A69C0` (1): 0x1A7ED9

- `sub_1A83A0` (1): 0x1A8403

### `sceNgs2SystemRender` — 1 call site(s)

- `sub_1B04F0` (1): 0x1B064C

### `sceNgs2VoiceControl` — 111 call site(s)

- `sub_1A69C0` (17): 0x1A794C, 0x1A7970, 0x1A79B2, 0x1A79D6, 0x1A7A12, 0x1A7A72, 0x1A7A9E, 0x1A7AC1, 0x1A7B42, 0x1A7B6F, 0x1A7B92, 0x1A7C03, 0x1A7C30, 0x1A7C54, 0x1A7CC7, 0x1A7CF4, 0x1A7D18

- `sub_1A8160` (1): 0x1A81D9

- `sub_1A82B0` (1): 0x1A8314

- `sub_1A8E90` (6): 0x1A900A, 0x1A9156, 0x1A9296, 0x1A93D6, 0x1A9516, 0x1A964D

- `sub_1A9690` (29): 0x1A9ADC, 0x1A9F5B, 0x1A9FF4, 0x1AA0A5, 0x1AA545, 0x1AA57B, 0x1AA5B7, 0x1AA5F3, 0x1AA62F, 0x1AA66B, 0x1AA6A7, 0x1AA6E3, 0x1AA71F, 0x1AA7CC, 0x1AABA1, 0x1AABDA, 0x1AAC13, 0x1AAC4C, 0x1AAC85, 0x1AACBE, 0x1AACF7, 0x1AAD26, 0x1AAD74, 0x1AAE95, 0x1AAF4D, 0x1AAFE9, 0x1AB135, 0x1AB33F, 0x1AB489

- `sub_1AB920` (2): 0x1ABB20, 0x1ABB4C

- `sub_1ABB70` (1): 0x1ABC7B

- `sub_1ABD70` (2): 0x1ABDF8, 0x1ABEC9

- `sub_1ABEF0` (2): 0x1AC1E4, 0x1AC4C7

- `sub_1AC510` (12): 0x1AC7BE, 0x1ACA5B, 0x1ACBCC, 0x1ACD2C, 0x1ACEB4, 0x1AD022, 0x1AD18D, 0x1AD2F8, 0x1AD4D5, 0x1AD68C, 0x1AD814, 0x1ADA84

- `sub_1ADC10` (25): 0x1ADE41, 0x1ADE9F, 0x1ADF3F, 0x1AE09D, 0x1AE0CD, 0x1AE0FD, 0x1AE12D, 0x1AE15D, 0x1AE18D, 0x1AE1BD, 0x1AE1ED, 0x1AE28C, 0x1AE381, 0x1AE3FC, 0x1AE4AB, 0x1AE576, 0x1AE5E3, 0x1AE685, 0x1AE6DF, 0x1AEA50, 0x1AEAA0, 0x1AEB49, 0x1AEB99, 0x1AEDA4, 0x1AEF3B

- `sub_1AEFD0` (6): 0x1AF86A, 0x1AFA04, 0x1AFA88, 0x1AFC14, 0x1AFF71, 0x1B0015

- `sub_1B0300` (2): 0x1B039A, 0x1B0408

- `sub_1B08E0` (3): 0x1B0A64, 0x1B0B24, 0x1B0C04

- `sub_1B11E0` (2): 0x1B134B, 0x1B141D

### `sceNgs2VoiceGetState` — 2 call site(s)

- `sub_1A85B0` (2): 0x1A862D, 0x1A8800

## 8. ABI и структура аргументов

Сканер использовал x86-64 System V:
- integer/pointer args: `RDI, RSI, RDX, RCX, R8, R9`;
- float/vector args: `XMM0–XMM7`.

Для импортов доступны следующие формальные аргументы (по прототипам из сканера и подтверждённым местам вызова):

| API | Аргументы |
|---|---|
| `SystemCreateWithAllocator` | option, allocator, out_system |
| `SystemDestroy` | system_handle |
| `SystemRender` | system, render_buffers, num_buffers |
| `RackQueryBufferSize` | rack_id, rack_option, out_buffer_info |
| `RackCreate` | system, rack_id, rack_option, context_buffer, out_rack |
| `RackCreateWithAllocator` | system, rack_id, rack_option, allocator, out_rack |
| `RackDestroy` | rack_handle |
| `RackGetVoiceHandle` | rack, voice_index, out_voice |
| `VoiceControl` | voice, parameter_chain |
| `VoiceGetState` | voice, out_state, state_size |

У `RackDestroy` и `SystemDestroy` прототип в сканере представлен только первым аргументом. Сами raw snapshots дополнительных integer- и XMM-регистров полезны, но их нельзя автоматически объявлять формальными параметрами ABI без SDK/trace подтверждения.

## 9. Сверка с текущей HLE на ветке `GFOXSH/tlg_pc:ngs2`

Проверенная база: HEAD `685e4e1d5d69c64357dd364c17de0202a89a41ed`. Основные файлы:
- [Ngs2Exports.cpp](https://github.com/GFOXSH/tlg_pc/blob/ngs2/port/src/ngs2/Ngs2Exports.cpp) — PS4→PS5 ABI-адаптер.
- [Voice.cpp](https://github.com/GFOXSH/tlg_pc/blob/ngs2/port/src/ngs2/Voice.cpp) — диспетчер параметров voice.
- [Custom.cpp](https://github.com/GFOXSH/tlg_pc/blob/ngs2/port/src/ngs2/Custom.cpp) — custom rack/modules.
- [Rack.cpp](https://github.com/GFOXSH/tlg_pc/blob/ngs2/port/src/ngs2/Rack.cpp) — rack layouts.
- [NGS2_LEVANTAMENTO.md](https://github.com/GFOXSH/tlg_pc/blob/ngs2/docs/NGS2_LEVANTAMENTO.md) — прежние динамические наблюдения.

### 9.1 Расхождения с прямыми доказательствами в EBOOT

| Приоритет | Доказательство EBOOT | Текущая HLE/адаптер | Оценка |
|---|---|---|---|
| **P0** | RackQuery/RackCreate для `0x4002 CUSTOM_SUBMIXER`: по 3 прямых вызова каждого | `Ngs2Exports.cpp::RackTailWords()` не имеет `0x4002`; адаптер останавливается на неизвестном rack ID | Блокирующая несовместимость создания custom rack |
| **P1** | `VoiceControl 0x1ABEC9`: прямой param ID `0x20000005`, size 0x10 | Нет в `Implemented()` и нет ветви в `Voice.cpp` | Нужны назначение/структура/обработчик |
| **P1** | `VoiceControl 0x1ADE9F`: прямой param ID `0x30000003` | Нет в `Implemented()` и нет ветви mastering dispatcher | Параметр limiter отсутствует в текущем пути |
| **P1** | `VoiceControl 0x1AA0A5`: прямой param ID `0x10000008` | Нет в `Implemented()` и нет sampler handler | Sampler USER_FX путь скомпилирован в EBOOT; требуется проверить runtime и callback ABI |
| **P1** | В `sub_1AEFD0` найдены candidate IDs `0x40001C00`, `0x40001D00`, `0x40020000` | `Custom.cpp` распознаёт текущие filter/USER_FX/USER_FX2 семейства; `0x40001C00` прямо не обрабатывает | Проверить старые PS4 custom modules 0x1C/0x1D и соответствие layouts, не считать ID 0x1D эквивалентом автоматически |
| **P2** | `sub_1A8E90` даёт candidate ID `0x10000009` в шести `VoiceControl` сигнатурах | Нет в `Implemented()` и sampler dispatcher | Проверить ветви производителя и runtime trace; пока candidate, не прямой header proof |
| **P2** | `VoiceGetState` size 0x30 и 0x10 | Adapter поддерживает PS4 sampler 48-byte и submixer 16-byte layouts | Размеры согласованы; проверить оба runtime результата |
| **OK / проверить значения** | Common IDs 1,2,3,5,6; sampler setup/blocks/pitch/filter/envelope; submixer setup/userFX/filter/compressor; reverb I3DL2; mastering setup/gain/output | Основные обработчики присутствуют в `Voice.cpp` / adapter | Наличие handler не гарантирует корректность payload и звуковой семантики |

**Пояснение по `0x40001C00/0x40001D00`:** старые заметки native NGS2 описывают эти значения как custom CHORUS/DELAY; текущая C++ реализация AnyPS5 именует близкие module families как FILTER/USER_FX/USER_FX2. Пока не сравнили размеры и точные layouts PS4 module option/voice param с текущими типами, небезопасно просто переиспользовать текущий `USER_FX` обработчик для старого DELAY. Сам факт появления ID в function-wide candidate list не подтверждает передачу каждого ID на каждом из двух вызовов — требуется проследить builder из `sub_1AEFD0`.

### 9.2 Приоритетная последовательность доработки

1. Реализовать PS4 `CUSTOM_SUBMIXER (0x4002)` в `RackOption()`: восстановить весь PS4 tail/layout размера 0x4D8 и перевести его в актуальную структуру PS5, включая список модулей и их option/state.
2. Разобрать producer `sub_1ABD70` вокруг `0x1ABEC9`, выяснить семантику `0x20000005`, структуру 16 байт и значение payload `1`; добавить адаптер и handler лишь после подтверждения значения.
3. Добавить/адаптировать `MASTERING_LIMITER 0x30000003`: payload size 16, поле enable из регистра и float 1.0; сопоставить с native traces.
4. Проследить `SAMPLER_USER_FX 0x10000008`: изучить callback, контекст, частоту вызова и вызываемый sndx callback; проверить, почему статический путь есть, но прежние динамические заметки выделяли его для GR2.
5. В `sub_1A8E90` проследить candidate `SAMPLER_PEAK_METER 0x10000009`; если он действительно попадает в цепочку — реализовать state/update semantics или безопасно документировать, что игра его не использует.
6. Разобрать `sub_1AEFD0` от построения custom rack option до двух регистровых `VoiceControl` вызовов; восстановить IDs `0x40001C00/0x40001D00/0x40020000` на уровне конкретного param block, lengths и указателей.
7. Дополнить runtime trace для проверки реальных частот и содержимого параметров, включая оба размера `VoiceGetState`, custom FX и outputs.

## 10. Строки и module-loading evidence

В EBOOT найдены:
- `noLoadNgs2`;
- путь исходного sndx: `C:\\sound\\sndx\\20160930_trico_lto\\runtime\\source\\sndx\\sndx_engine_ngs2_orbis.c`;
- `Failed to load NGS2 module (%X)`;
- `Loaded NGS2 module`;
- `Unload NGS2 module`.

Внутри EBOOT отдельные строки NID не найдены (`nid_strings=[])); имена импортов сопоставлены по import-table/xref данным и таблице NID из `tlg_pc/ngs2` metadata.

## 11. Ограничения и дальнейшая проверка

1. Статический анализ не сообщает runtime call frequency и не доказывает достижимость каждой ветви.
2. Function-wide candidate constants могут относиться к разным ветвям, построителям или сравнениям; это не точный список переданных ID на конкретный call.
3. 4 попытки декодировать якобы статический `VoiceControl` pointer дали некорректную структуру с ID `0x2E666666` и implausible `next=-4095`; эти записи — ложные декодирования/ошибочно разрешённый адрес кода, исключены из списка реальных param IDs.
4. Статическая запись в заголовок доказывает наличие пути в бинарнике, но не то, что этот путь исполнялся в уже выполненном native trace.
5. Значения из float-регистров и косвенных указателей не восстановлены там, где сканер не смог связать reaching definition; неизвестные байты не следует заменять догадками.
6. Скрипт использует IDA 7.0 и image base 0. Для другой версии/сборки EBOOT адреса и сигнатуры могут измениться.

### Источники внутри репозитория

- Исходная выгрузка: `result/eboot.elf.ngs2_static.json`, `result/eboot.elf.ngs2_static.csv`, `result/eboot.elf.ngs2_static.md`.
- Анализатор: `tools/ngs2_ida7_static.py`.
- Ранее выполненные динамические наблюдения и layouts: [tlg_pc/docs/NGS2_LEVANTAMENTO.md](https://github.com/GFOXSH/tlg_pc/blob/ngs2/docs/NGS2_LEVANTAMENTO.md).
