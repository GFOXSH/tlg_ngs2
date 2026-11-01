# NGS2: глубокий разбор второй выгрузки IDA

> Дата выгрузки: 2026-11-01 12:24:10 (из metadata JSON). Image base: `0`. IDA 7.x / IDAPython.  
> Входные артефакты: [Markdown](ngs2_deep_followup.md), [JSON](ngs2_deep_followup.json), [CSV](ngs2_deep_followup.csv).  
> Проверенная HLE: [GFOXSH/tlg_pc, branch ngs2](https://github.com/GFOXSH/tlg_pc/tree/ngs2), HEAD на момент предыдущей проверки: `685e4e1d5d69c64357dd364c17de0202a89a41ed`.

## 1. Результат второго прохода

Скрипт нашёл все шесть целевых функций и собрал:

| Функция | Инструкций | NGS2-вызовов | Indirect calls | Data refs |
|---|---:|---:|---:|---:|
| `sub_1AC510` — создание bus/custom racks | 959 | 49 | 0 | 31 |
| `sub_1AEFD0` — custom effects | 763 | 13 | 0 | 30 |
| `sub_1A9690` — sampler voice | 1495 | 40 | 0 | 39 |
| `sub_1ADC10` — mastering voice | 966 | 48 | 0 | 12 |
| `sub_1ABD70` — submixer event/param | 86 | 3 | 0 | 4 |
| `sub_1A8E90` — sampler voice lifecycle | 449 | 12 | 0 | 13 |

Все шесть адресов функций совпали с ожидаемыми. В выгрузке есть прямые call-site context и локальные срезы регистров для интересующих вызовов. Ограничение: скрипт делает локальный backward slice, не полноценный path-sensitive dataflow. Если регистр упирается в call barrier, его значение нельзя считать восстановленным. Отсутствие indirect call в этих шести функциях не доказывает отсутствие callback-механизма в runtime.

## 2. Подтверждённые факты и изменения статуса гипотез

### 2.1. CUSTOM_SUBMIXER rack `0x4002`: три пары Query/Create

В `sub_1AC510` непосредственно подтверждены три вызова `sceNgs2RackQueryBufferSize` и соответствующие `sceNgs2RackCreate` для rack ID `0x4002`:

| Rack option | Query | Create | Фрагмент конфигурации |
|---|---:|---:|---|
| базовая конфигурация | `0x1AC710` | `0x1AC762` | option pointer = `rbp+var_678` |
| module `0x1C` | `0x1AD427` | `0x1AD479` | поле `var_5E0 = 0x1C` |
| module `0x1D` | `0x1AD5DE` | `0x1AD630` | поле `var_5E0 = 0x1D` |

Для всех трёх конфигураций:
- rack ID в первом аргументе Query и втором аргументе Create — именно `0x4002`;
- перед Query option создаётся в локальной области `var_678`;
- в `memcpy` копируется ровно `0x4D8` байт из `off_14DCAC8`;
- перед Create передаются option pointer, context buffer и адрес выходного rack handle.

Следовательно, `0x4D8` — фактический размер PS4 custom-submixer rack-option, а не размер, выведенный только из старого runtime trace. Сам шаблон `off_14DCAC8` начинается с dword `0x4D8`; в следующих полях присутствуют значения `0x200`, `1`, `1`, `1`, `8`. Полную семантику каждого поля без описания PS4-структуры пока не присваиваем.

Два дополнительных блока descriptor перед Query:
- module `0x1C`: `var_5E0 = 0x1C`, `var_5E8 = 0` (инициализация видна около `0x1AD408–0x1AD412`);
- module `0x1D`: передаётся пара qword-констант `0x0000000100000014` и `0x447A000000000008`, затем `var_5E0 = 0x1D`; эти значения попадают в локальный descriptor до копирования его содержимого в rack option.

Важное ограничение: мы доказали размер, rack ID, источник шаблона и включение module ID в конфигурацию. Но полное преобразование PS4 custom-rack layout в текущую PS5 `Ngs2CustomSubmixerRackOption` ещё не восстановлено. В HLE PS5 `Ngs2CustomRackOption` имеет размер 1280 (`0x500`), `Ngs2CustomSubmixerRackOption` — 1288 (`0x508`), тогда как EBOOT передаёт PS4 blob размером `0x4D8`. Нельзя исправлять это простым увеличением `RackTailWords(0x4002)` и копированием сырых байтов: требуется по-полевое преобразование.

### 2.2. Custom module IDs `0x1C` и `0x1D` — прямые VoiceControl parameter IDs

В `sub_1AEFD0` теперь есть точное доказательство, что значения `0x40001C00` и `0x40001D00` записываются непосредственно в поле ID заголовка VoiceControl, а не просто встречаются рядом с кодом:

**Chorus / module `0x1C`**
- Заголовок формируется с `size = 0x30`, `next = 0`, `id = 0x40001C00` (код около `0x1AFD48–0x1AFD5C`).
- Payload занимает `0x28` байт.
- В payload записываются несколько скалярных полей (включая значения из `r13+0x1B0`, `r13+0x1B4`, `r13+0x1C0`) и SIMD-данные, умноженные на константный вектор `xmmword_14DADC0`.
- Это согласуется с названием `CHORUS` в строковой таблице, но сами смещения полей пока не следует переименовывать в параметры Chorus без анализа исходной PS4 option-структуры.

**Delay / module `0x1D`**
- Заголовок формируется с `size = 0x88`, `next = 0`, `id = 0x40001D00` (около `0x1AFE51–0x1AFE65`).
- Payload занимает `0x80` байт.
- Видны SIMD-поля, несколько scalar-полей и цикл копирования пар dword из области `r13+0x1D8` в payload начиная с `+0x1C`; количество элементов берётся из `[r13+0x1D0]`.
- В строковой таблице присутствует `DELAY`, ссылающаяся на тот же блок настроек.

Таким образом, прежнее сопоставление PS4 module ID `0x1D` с PS5 USER_FX только по числу было бы ошибкой. Это конкретный PS4 Delay module с собственным 0x88-byte payload. Module ID `0x1C` также имеет отдельный формат 0x30-byte Chorus param.

В этой же функции напрямую подтверждён custom-submixer setup:
- ID `0x40020000`, размер `0x18`, `next = 0` (около `0x1AFF38–0x1AFF4C`);
- два первых dword payload повторяют значение из `eax`, следующие qword — ноль;
- после этого записывается служебный флаг в `[r13+0x23C]`.

Это отдельный VoiceControl param setup, а не сам заголовок RackOption.

### 2.3. SAMPLER_USER_FX `0x10000008`: точный callback и user-data

В `sub_1A9690`, вызов VoiceControl `0x1AA0A5`, восстановлен полностью:

| Offset | Значение |
|---:|---|
| `+0x00` | `u16 size = 0x28` |
| `+0x02` | `s16 next = 0` |
| `+0x04` | `u32 id = 0x10000008` |
| `+0x08` | callback pointer = `sub_1AB580` |
| `+0x10` | user data = `r13` |
| `+0x18..+0x27` | 16 нулевых байт |

Перед вызовом:
- callback pointer загружается через `lea rax, sub_1AB580` на `0x1AA068`;
- `r13` записывается в user-data slot;
- нулевой SIMD-регистр очищает последние 16 байт структуры.

Это снимает неопределённость о payload layout самого запроса: это callback + user-data + 16-byte reserved/zero tail. Но пока не известно, как `sub_1AB580` вызывается и обрабатывает данные: тело callback и его ABI нужно разобрать отдельно. В целевой HLE этот parameter ID не входит в `Implemented()`, а sampler handler в `Voice.cpp` отсутствует.

### 2.4. MASTERING_GAIN и MASTERING_LIMITER

**Mastering gain — ID `0x30000004`, call `0x1ADE41`:**
- `size = 0x10`, `next = 0`;
- два float32 payload-поля берутся из XMM0 и записываются по смещениям `+8` и `+0xC`.
- Это ровно два float-поля в 16-byte param.

**Mastering limiter — ID `0x30000003`, call `0x1ADE9F`:**
- `size = 0x10`, `next = 0`;
- первый payload dword берётся из EAX после вызова `sub_1B2010`;
- второй payload dword жёстко равен `0x3F800000` (float32 `1.0`).
- Перед ветвью проверяется конфигурация `isLimiterEnable`; при ненулевом результате limiter param пропускается, при нулевом — формируется и отправляется.

Размер и поля параметра доказаны. Семантика первого payload dword не доказана без разбора `sub_1B2010`; называть его enable/threshold сейчас преждевременно. В HLE параметр отсутствует в `Implemented()` и mastering dispatcher `Voice.cpp`.

### 2.5. SAMPLER_PEAK_METER — теперь прямое подтверждение

В `sub_1A8E90`, на call site `0x1A964D`:
- в `r13` загружается qword `0x0000000110000009`;
- `size = 0x10`, `next = 0`;
- qword записывается в заголовок с offset `+4`, поэтому младший dword ID равен `0x10000009`, следующий payload dword — `1`;
- dword по offset `+0xC` равен нулю.

Таким образом, прямой параметр VoiceControl имеет ID `0x10000009`, size `0x10`, payload `{1, 0}`. Предыдущая классификация Peak Meter как только function-wide candidate теперь снята: ID подтверждён на конкретном call site. Строка `VOICE_PEAK` также присутствует в event-string table этой функции. В HLE ID отсутствует в `Implemented()` и нет sampler dispatcher branch для него.

### 2.6. Неизвестный SUBMIXER param `0x20000005`

В `sub_1ABD70`, case 7 switch, VoiceControl call `0x1ABEC9`:
- `size = 0x10`, `next = 0`;
- qword immediate `0x0000000120000005` записывается с offset `+4`;
- следовательно, ID = `0x20000005`, первый payload dword = `1`;
- последние 4 байта структуры в данном локальном окне не инициализируются явной инструкцией. Их значение нельзя объявлять нулём без проверки предшествующей инициализации stack slot.

Параметр используется на отдельной ветви dispatch (case 7). Название/семантика остаются неизвестными. Это не стандартный `SUBMIXER_SETUP` или `SUBMIXER_USER_FX`; не следует добавлять guessed handler.

## 3. Что это означает для текущей HLE

Исходники на проверенной ветке `tlg_pc:ngs2` повторно сопоставлены с результатами:

| Область | Текущее состояние | Вывод после выгрузки |
|---|---|---|
| Rack adapter, `0x4002` | `Ngs2Exports.cpp::RackTailWords()` знает только sampler/submixer/mastering/reverb; default вызывает `ngs2_stop` | Подтверждён P0: любой PS4 custom-submixer rack через этот adapter не переводится |
| Custom rack storage | `Rack.cpp` и `Ngs2Types.hpp` содержат PS5 `Ngs2CustomSubmixerRackOption` (0x508), custom module arrays | Тип destination уже есть, но PS4 0x4D8 source layout не переведён; требуется field-by-field adapter |
| Chorus / Delay | `Custom.cpp` разбирает custom IDs, но PS4 IDs/format не переводятся | Нужны отдельные PS4-to-PS5 converters; не путать 0x1D Delay с PS5 USER_FX |
| `0x10000008` | отсутствует в `Implemented()` / sampler dispatcher | Подтверждён P1; callback pointer и user-data layout восстановлены, callback semantics — нет |
| `0x30000003` | отсутствует в `Implemented()` / mastering dispatcher | Подтверждён P1; формат известен, семантика первого payload dword требует helper analysis |
| `0x10000009` | отсутствует в `Implemented()` / sampler dispatcher | Новый P1/P2: конкретный Peak Meter param доказан |
| `0x20000005` | отсутствует в `Implemented()` | Неизвестное поведение; оставить diagnostic/skip policy до отдельного анализа |

Отдельная проверка кодовой базы: в `Ngs2Exports.cpp::Implemented()` перечислены стандартные параметры и несколько extensions, но нет `0x10000008`, `0x10000009`, `0x20000005`, `0x30000003`. В `Voice.cpp` mastering dispatcher обрабатывает setup/gain/output, но не limiter. `Custom.cpp` уже содержит destination типы custom module / custom rack в PS5 ABI, однако это не заменяет адаптер PS4-структур.

## 4. Ранжирование продолжения

1. **P0 — закончить PS4 `0x4002` adapter.** Извлечь полный layout `off_14DCAC8`, разобрать `sub_1B1C70`, сравнить PS4 custom module/port arrays с PS5 `Ngs2CustomRackOption`; построить явное преобразование полей, counts, IDs, buffers, offsets и module payload options. Не делать raw memcpy между версиями ABI.
2. **P1 — разобрать callback `sub_1AB580`.** Восстановить аргументы, поведение, владение/срок жизни `r13`, обращения к sampler state и error paths. После этого можно реализовать адаптацию `0x10000008` осознанно.
3. **P1 — разобрать `sub_1B2010`.** Это определит семантику первого dword `MASTERING_LIMITER`; затем добавить handler с проверками и сопоставлением к PS5 DSP model.
4. **P1/P2 — реализовать `0x10000009` Peak Meter.** Структура запроса известна, но нужно проверить соответствующий PS5 peak-meter API / внутренний state representation и ожидаемый ответ.
5. **Оставить `0x20000005` неопознанным.** Следующий проход должен проследить case-7 caller, аргументный enum и стековую инициализацию; не подменять параметр guessed flag.

## 5. Нужна дополнительная IDA-выгрузка

Вторая выгрузка решила структуру параметров, но не включала тела некоторых вызываемых helper/callback функций. Следующий узкий pass должен дампить disassembly, callers, xrefs, stack/register arguments и data refs для:
- `sub_1B1C70` — формирование/подготовка rack option descriptors;
- `sub_1AB580` — sampler user-FX callback;
- `sub_1B2010` — подготовка limiter payload;
- `sub_1B2130` — helper, вызываемый перед mastering gain, возможно config/value conversion;
- `sub_1ABD70` callers — чтобы определить, откуда приходит event case 7;
- глобальную область `off_14DCAC8` целиком, 0x4D8 байт (включая точные relocations/xrefs), а также module option source ranges вокруг `r13+0x1B0..0x240`.

## 6. Правило интерпретации

Адреса инструкций, размеры структур, значения ID, указатели и явно записанные значения в отчёте — прямые статические доказательства. Названия функций и модулей, основанные на строках (`CHORUS`, `DELAY`, `VOICE_PEAK`), являются сильными семантическими подсказками. Поля с register-derived значениями, helper return values и неинициализированные в локальном окне байты не получают семантического имени до отдельного dataflow/ABI анализа. Результаты статического анализа не устанавливают runtime-частоту выполнения ветвей.


## 7. Дополнительная сверка custom Chorus/Delay с конкретным кодом C++ HLE

После восстановления конкретных PS4 VoiceControl IDs `0x40001C00` и `0x40001D00` выполнена дополнительная проверка текущих `Custom.cpp` и `Ngs2Types.hpp` на том же HEAD `685e4e1d5d69c64357dd364c17de0202a89a41ed`.

### 7.1. Chorus module `0x1C`: отсутствует в текущей модели

IDA доказывает, что EBOOT строит для Chorus отдельный параметр:
- ID `0x40001C00`;
- size `0x30`;
- payload size `0x28`;
- scalar/SIMD значения заполняются из области `r13+0x1B0..0x1C0` и масштабируются константным вектором.

В [Ngs2Types.hpp](https://github.com/GFOXSH/tlg_pc/blob/685e4e1d5d69c64357dd364c17de0202a89a41ed/port/src/ngs2/Ngs2Types.hpp) нет custom module ID `0x1C`. В [Custom.cpp](https://github.com/GFOXSH/tlg_pc/blob/685e4e1d5d69c64357dd364c17de0202a89a41ed/port/src/ngs2/Custom.cpp) `Ngs2CheckCustomRack()` принимает FILTER `0x13`, USER_FX `0x1D`, USER_FX2 `0x1F`; прочий module ID завершает проверку через `ngs2_stop`. Для voice parameter `0x40001C00` не предусмотрен handler: при custom-submixer rack он дойдёт до финального `ngs2_stop("... is not implemented")`.

**Вывод:** перенос custom rack option без поддержки module ID `0x1C` всё равно не сделает Chorus рабочим. Нужны отдельная модель Chorus module и translation его PS4 0x30-byte voice parameter.

### 7.2. Delay module `0x1D`: числовая коллизия с PS5 USER_FX, а не совместимость

IDA напрямую подтверждает:
- EBOOT VoiceControl ID = `0x40001D00`;
- parameter size = `0x88` (136 bytes);
- payload = `0x80` bytes;
- структура содержит несколько SIMD/scalar полей и массив пар dword, число элементов определяется значением из `[r13+0x1D0]`; исходные пары расположены от `r13+0x1D8`.

Текущий PS5 HLE в `Ngs2Types.hpp` также объявляет `SCE_NGS2_CUSTOM_VOICE_PARAM_USER_FX = 0x40001d00`. Это совпадение числового ID **не означает**, что payload совместим. В `Custom.cpp::Ngs2ApplyCustomParam()` значение с этим base ID направляется в `SetCustomUserFxParam()`, где оно интерпретируется как `Ngs2CustomVoiceUserFxParam`: header + callback pointer + три user-data pointer (40 bytes / `0x28`). При этом PS4 Delay parameter — другой объект размером `0x88`, а не callback descriptor.

Путь C++ далее сохраняет прочитанный из payload handler и вызывает его в `Ngs2ProcessUserFx()`, если handler не равен null. Следовательно, при прямой передаче PS4 Delay параметра в этот dispatcher его поля будут ошибочно интерпретированы как function pointer/user data. Это не просто отсутствие DSP-эффекта: это потенциально небезопасная интерпретация данных и попытка вызвать значение из Delay payload как callback. До перевода параметра нельзя пропускать его через существующий USER_FX handler.

**Вывод:** требуется разнести PS4 Delay и PS5 USER_FX в адаптере. Возможные варианты — перевести Delay в отдельный внутренний module/parameter ID с собственным DSP handler либо сопоставить его с эквивалентным PS5 effect API после восстановления полной семантики. Нельзя оставлять ID `0x40001D00` как сырой проходящий идентификатор.

### 7.3. Влияние на порядок работ

Custom-rack support нужно рассматривать как единый пакет, а не как только включение rack ID:
1. Перевод PS4 rack option `0x4D8` в текущую PS5 custom-rack структуру.
2. Перевод module table и назначение отдельного внутреннего ID для TLG Chorus `0x1C` и Delay `0x1D`, без конфликта с PS5 USER_FX `0x1D`.
3. Перевод voice parameter payload для Chorus `0x30` и Delay `0x88`.
4. Подключение реального DSP/module processing и проверка source/destination buffer/port wiring.
5. Runtime-тест custom-rack creation, VoiceControl, process callbacks и destruction/cleanup.

Пока пункты 1–3 не реализованы, нельзя считать `0x4002` адаптированным даже при успешном `RackQueryBufferSize`/ `RackCreate`.

## 8. Уточнённый итоговый gap list по актуальному HLE HEAD

| Путь | Точный конфликт/пробел | Риск |
|---|---|---|
| PS4 rack `0x4002` | `RackTailWords()` не переводит PS4 option; fatal до вызова PS5 rack implementation | Блокирует создание TLG custom racks |
| PS4 Chorus `0x40001C00` / `0x30` | Module ID `0x1C` отсутствует в `Ngs2CheckCustomRack()` и custom voice dispatcher | Rack validation/VoiceControl завершается ошибкой |
| PS4 Delay `0x40001D00` / `0x88` | Тот же числовой ID в PS5 HLE занят USER_FX; payload layout отличается от `Ngs2CustomVoiceUserFxParam` (`0x28`) | Неверная трактовка payload как callback pointer и user data |
| Sampler USER_FX `0x10000008` | Нет sampler param handler; callback `sub_1AB580` ABI ещё не разобран | Unknown-param fatal или пропуск при diagnostic skip |
| Sampler Peak Meter `0x10000009` | Нет sampler param handler / explicit no-op | Unknown-param fatal или потеря peak state |
| Mastering limiter `0x30000003` | Нет mastering param handler; первый payload dword требует разбора helper `sub_1B2010` | Unknown-param fatal или отключение limiter |
| Submixer `0x20000005` | Format и payload dword известны, семантика неизвестна | Не реализовывать наугад; исследовать caller/event context |

Повторная проверка refs ветки `tlg_pc:ngs2` на 2026-11-01 подтвердила HEAD `685e4e1d5d69c64357dd364c17de0202a89a41ed`. Сверены `Ngs2Exports.cpp`, `Voice.cpp`, `Rack.cpp`, `Custom.cpp` и `Ngs2Types.hpp`. В рамках этого отчёта код `tlg_pc` не менялся; в `tlg_ngs2` сохранены результаты реверса и аудит совместимости.


## 9. Формат сырой JSON-выгрузки

Файл `ngs2_deep_followup.json` содержит нестрогие числовые токены `NaN` в float-полях. Такие токены допускаются некоторыми permissive JSON-парсерами, но не соответствуют стандартному JSON и приводят к ошибке строгого `JSON.parse`. Для этого аудита значения `NaN` были нормализованы в `null` при чтении; они не использовались как доказательство содержимого NGS2-параметров. Следующую версию IDA-скрипта следует сериализовать с обработкой non-finite float (например, `allow_nan=False` с предварительным преобразованием в `None`), чтобы JSON был переносимым между стандартными парсерами.
