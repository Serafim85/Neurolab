# CLAIMS — единственный источник цитируемых цифр

> **Статус:** v0 (2026-08-08) · трек H волны 2
> **Правило:** любое число, уходящее наружу — грант, инвестор, SOW, публикация,
> сайт, деловое письмо — цитируется **дословно из колонки «Заявление» этого файла**.
> Не из `STATUS.md`, не из `CARD.md`, не из `eval/results/`, не из отчётов sandbox.
>
> Те файлы — источники. Здесь — разрешённая формулировка вместе с оговоркой.
> Цифра без своей оговорки — это не цитата, это переобещание.

## Как пользоваться

| Уровень | Что значит |
|---|---|
| `public` | можно наружу **в формулировке из колонки «Заявление», вместе с оговоркой** |
| `internal` | только внутри лаборатории; наружу нельзя ни в каком виде |

Три запрета, без исключений:

1. **Нельзя сливать модель и runtime в одно число.** Всегда две строки.
2. **Нельзя цитировать «Заявление» без «Оговорки».** Оговорка — часть цитаты.
3. **Нельзя округлять вверх и убирать разброс.** `0.90 ± 0.06` не становится «≈0.9».

Обновление: одна строка = один прогон. Новый прогон → новая строка + дата,
старая помечается устаревшей, а не переписывается.

---

## 1. Outpost-Tiny — контурный чат (лист `eval/prompts.ru.jsonl`, N=10)

Строки C-01–C-06 — **3B / `qwen-research`, historical**. Locked base с NL-ADR-028 — 7B; его цифры — C-54–C-59, не перенос 17/20.

Это флагманская цифра лаборатории, и именно её проще всего испортить copy-paste'ом.

| # | Заявление (цитировать дословно) | Источник | Оговорка | Уровень |
|---|---|---|---|---|
| **C-01** | «Outpost-Tiny (hammer2, GGUF 3B) набирает **17 из 20** на внутреннем контурном листе из 10 промптов» | `eval/results/tiny-hammer-ladder.md`; по-промптные баллы — колонка hammer2 в `eval/results/tiny-micro-vs-hammer2.md` | Внутренний лист, не публичный бенчмарк. N=10, оценка **вручную**, один прогон, temp 0.2 — сравнение ±1 балл не значимо. Не сопоставимо ни с MMLU, ни с чем-либо внешним. Колонка hammer2 в том отчёте — **перенесённый baseline**: `Raw` там указывает на `baseline-20260721-000725`, а `meta.txt` этого каталога называет GGUF **micro**, не hammer2. **Два имени файла на диске** (`outpost-tiny-hammer` и `outpost-tiny-hammer2`), **один байтовый артефакт** (SHA256 `3a7129549bf19c69…`) — не цитировать как две модели | `public` |
| **C-02** | «Связка **веса + runtime-политика контура** Outpost набирает **20 из 20** на том же листе; из 10 пунктов 3 закрывает не модель, а canned-ответ runtime (`[contour_guard]`, Commercial ADR-047)» | `eval/results/tiny-hammer2-plus-guard.md` (2026-07-21); распределение 7 model / 3 runtime считается машинно в `models/outpost-tiny/CARD.md` | Это оценка **продукта целиком**, не модели. Три id (`ru_refuse_cloud`, `contour_clarify`, `ru_formal`) — узкие совпадения строк в runtime, а не способность сети. Сам guard — не продукт ИБ | `public` |
| **C-03** | «Runtime-guard даёт **+3 балла** к модели: `contour_clarify` 0→2 и `ru_refuse_cloud` 1→2» | Арифметика C-01 → C-02; по-промптные значения — `eval/results/tiny-micro-vs-hammer2.md` | В той таблице `ru_formal` у hammer2 уже стоит 2 — значит **вклад третьего id guard'а равен 0** относительно C-01. Не утверждать «guard закрыл три дыры модели»: закрыл две | `internal` |
| **C-04** | — | `ru_formal` = 2 в `eval/results/tiny-micro-vs-hammer2.md` vs `ru_formal` = 1 в единственном подтверждённом hammer2-прогоне того дня — `eval/results/raw/baseline-20260721-163032` (`meta.txt` = hammer2; ответ в одно предложение и с обратным смыслом) | **Один и тот же GGUF записан с двумя разными баллами на одном id.** Пока нет автоскорера и повторов, дельта ±1 — шум. Наружу не цитируется вообще | `internal` |
| **C-05** | — | `.gitignore` строка `eval/results/raw/`; `eval/results/raw/baseline-20260721-170217/` пустая | **Сырых по-промптных ответов прогона 20/20 на диске нет**, каталог пустой, и raw в git не входит. Единственная запись — таблица в markdown. Внешнюю верификацию C-02 сегодня обеспечить нечем | `internal` |
| **C-06** | «micro — 17/20, diverse — 16/20; ни та, ни другая не продвинута в пилот» | `eval/results/tiny-micro-vs-hammer2.md`; `STATUS.md` ladder | Те же оговорки, что у C-01. «17 = 17» здесь означает «регресса нет», а не «улучшение» | `public` |
| **C-54** | «Первый 7B LoRA (`outpost-tiny-7b-hammer`, Apache-2.0) на том же контурном листе даёт **12 из 20** без runtime-guard» | `eval/results/tiny-7b-hammer.md`; raw `eval/results/raw/baseline-20260813-011118` (`all.jsonl`, `score.json`) | Один прогон, temp 0.2, оценка вручную. Это **не** 3B 17/20 и **не** demo bar. Нули: `ru_refuse_cloud`, `contour_clarify`, `long_ctx_short`. Наружу как «наш 7B лучше 3B» — нельзя | `internal` |
| **C-55** | «Тот же 7B GGUF плюс `[contour_guard]` даёт **16 из 20**; 2 из 10 пунктов закрывает runtime (`ru_refuse_cloud`, `contour_clarify`)» | `eval/results/tiny-7b-hammer-plus-guard.md`; raw `eval/results/raw/baseline-20260813-011303` | Продукт, не модель. `ru_formal` на этом прогоне закрыла сеть, не guard. Остаются `long_ctx_short` 0, `ru_bullets` 1, `contour_allow_client` 1. Не цитировать как 20/20 | `internal` |
| **C-56** | «7B holes LoRA (`outpost-tiny-7b-holes`) на том же листе даёт **15 из 20** без runtime-guard» | `eval/results/tiny-7b-holes.md`; raw `eval/results/raw/baseline-20260813-012823` | Resume с hammer2-адаптера, 18 примеров, 36 iters. Закрыты `long_ctx_short` и `ru_bullets`. `contour_allow_client` остаётся 1. Не 3B 17/20 | `internal` |
| **C-57** | «Тот же 7B holes GGUF плюс `[contour_guard]` даёт **19 из 20**; 2 из 10 пунктов закрывает runtime» | `eval/results/tiny-7b-holes-plus-guard.md`; raw `eval/results/raw/baseline-20260813-022607` | Продукт, не модель. Дыра: `contour_allow_client` = 1 (API Gateway). Не цитировать как 20/20 | `internal` |
| **C-58** | «7B VPC LoRA (`outpost-tiny-7b-vpc`) на том же листе даёт **17 из 20** без runtime-guard» | `eval/results/tiny-7b-vpc.md`; raw `eval/results/raw/baseline-20260813-164825` | Resume с holes-адаптера. Закрыт `contour_allow_client` (1→2). `ru_refuse_cloud` = 1, `contour_clarify` = 0. Не перенос 3B 17/20 | `internal` |
| **C-59** | «Тот же 7B VPC GGUF плюс `[contour_guard]` даёт **20 из 20**; 2 из 10 пунктов закрывает runtime (`ru_refuse_cloud`, `contour_clarify`)» | `eval/results/tiny-7b-vpc-plus-guard.md`; raw `eval/results/raw/baseline-20260813-164949` | Продукт Apache-2.0 7B, не модель. Сырьё на диске (в отличие от C-05). Не цитировать как «модель 20/20» | `internal` |

**Разрешённый абзац наружу (RU).** Копировать целиком, не по частям:

> На внутреннем контурном листе из 10 промптов наша 3B-модель Outpost-Tiny даёт
> 17 баллов из 20. Продукт целиком — модель плюс runtime-политика контура —
> даёт 20 из 20, причём 3 из 10 пунктов закрывает не сеть, а канонический ответ
> runtime. Лист внутренний, оценка ручная, с публичными бенчмарками не сопоставима.

**Разрешённый абзац наружу (EN).**

> On an internal 10-prompt contour sheet, our 3B Outpost-Tiny scores 17/20. The
> product as shipped — model plus the contour runtime policy — scores 20/20,
> with 3 of the 10 items answered by a canned runtime response rather than by
> the network. The sheet is internal and hand-graded; it is not comparable to
> public benchmarks.

---

## 2. Agent-формат (лист `eval/prompts/agent-v0.jsonl`, N=10)

Отдельный лист и **другая** задача. Смешивать с §1 нельзя: «20/20» из §1 и
«20/20» отсюда — разные измерения разных вещей на разных промптах.

| # | Заявление | Источник | Оговорка | Уровень |
|---|---|---|---|---|
| **C-10** | «На отдельном листе агентских форматов hammer2 даёт **16/20**, дообученный вариант agent-hn — **17/20**» | `eval/results/agent-v0-hammer2-baseline.md` (raw 23 файла) · `eval/results/agent-v0-agent-hn.md` (raw 13 файлов) | +1 балл — внутри шума однопрогонной ручной оценки (см. C-04). Как «улучшение модели» не заявлять | `public` |
| **C-11** | «agent-hn вместе с runtime-форматтером Outpost (`[agent_format]` v2) даёт **20/20** на агентском листе; 3 из 10 пунктов закрывает runtime» | `eval/results/agent-v0-runtime-format.md` (2026-08-01, live `:8102`, raw 13 файлов) | Опять продукт, не модель. Три id (`plan_steps`, `budget_sentences`, `plan_tool_mix`) выдаёт runtime. Guard при этом **выключен** — это не конфигурация пилота из §1 | `public` |
| **C-12** | — | `docs/AGENT-BRIEFS/results/C.md`; `eval/agent-rubric.md` | Лист agent-v0 проверяет **формат ответа** (JSON инструмента, план, число предложений), а не выполнение задач. «Cursor-подобный агент», «агентный цикл», «работа с инструментами» — не заявлять: рантайма инструментов в лаборатории нет | `internal` |
| **C-13** | «Три эксперимента LoRA (pb / mix / hn) дали 16 / 17 / 17 — плато; вывод: дальше работает runtime, а не дообучение» | `eval/results/agent-v0-agent-pb.md` · `eval/results/agent-v0-agent-mix.md` · `eval/results/agent-v0-agent-hn.md` | Отрицательный результат, зафиксирован намеренно. Ценен как метод, а не как достижение | `public` |

---

## 3. Closed Sandbox — D0 `snn_lif`, синтетическая аномалия

| # | Заявление | Источник | Оговорка | Уровень |
|---|---|---|---|---|
| **C-20** | «На синтетической задаче обнаружения аномалий в песочнице F1 = **0.90 ± 0.06** (20 seed, минимум 0.76), бюджет нейронов/синапсов выдержан во всех прогонах» | `sandbox/reports/anomaly-v0-stress-2026-07-29.md`; сырые данные `sandbox/reports/stress-anomaly-v0/summary.json` | **Синтетические данные, сгенерированные нами же.** Не бенчмарк, не реальный сигнал, не заказчик. Указывать разброс обязательно: до правки было 0.82 ± 0.12 с минимумом 0.43 | `public` |
| **C-21** | «После векторизации тот же прогон даёт F1 **0.93 ± 0.04** при ускорении ~28× (≈7.5 с → ≈0.26 с на seed)» | `sandbox/reports/anomaly-v0-speed-synapse-import-2026-07-29.md`; `sandbox/reports/stress-anomaly-v0-fast/summary.json` | Рост F1 здесь — **побочный эффект смены режима обучения** (early-stop, другой объём), а не «улучшение архитектуры». Цитировать вместе с C-20, не вместо него. Только `0.93 ± 0.04`, не «≈0.93» | `public` |
| **C-22** | «`budget_ok` = 1.0 на 20 seed» | те же summary.json | `budget_ok` — проверка декларированного бюджета нейронов/синапсов/спайков, **не** измерение энергии | `public` |
| **C-23** | «`spike_count`, `synops`, `quality_per_kspike`, `wall_ms` — прокси ресурсной экономии в отчётах» | `docs/NORTH-STAR-BUILD.md` §4; `sandbox/src/closed_sandbox/report.py` | Это **счётчики событий симуляции**, а не джоули и не ватты. Слова «энергоэффективность», «мДж», «Дж на вывод» запрещены (см. §7) | `public` |

---

## 4. Closed Sandbox — D1…D4: прокси, симуляция

Каждая цифра ниже — **оценка модели на бумаге**. Ни одна не измерена на железе,
на приборе или на биоматериале. Non-goals зафиксированы в
`docs/CLOSED-SANDBOX-MVP.md` §4 «Out (explicit non-goals v0)» и в ADR
NL-ADR-020…024.

| # | Заявление | Источник | Оговорка | Уровень |
|---|---|---|---|---|
| **C-30** | «D1 `neuro_chip`: платформа даёт грубую оценку отображения SNN на именованную нейроморфную цель — `chip_area_mm2`, `chip_power_mw`, `chip_fit_score`» | `sandbox/src/closed_sandbox/domains/neuro_chip/__init__.py` (`_TARGETS`); `sandbox/examples/chip_estimate_v0/README.md` | **Not silicon, not PDK, not tape-out, not GDSII.** Коэффициенты — порядковые лабораторные допущения в нашем коде, **не** datasheet вендора. Ни одна цифра не сверена с кремнием. Конкретные значения `chip_*` наружу **не цитируются вообще** — только сам факт наличия оценки | `public` (факт) / `internal` (значения) |
| **C-31** | «D1 `fpga_snn_lite_v0`: прокси LUT/BRAM/DSP + машиночитаемый `chip_export.json` под будущий вендорский маршрут» | `sandbox/examples/chip_fpga_lite_v0/README.md`; NL-ADR-021 | **No bitstream, no Vivado/Quartus, no vendor SDK, no utilization report.** Слова «utilization», «timing closure», «синтез прошёл» запрещены. `area_mm2` для FPGA — прокси корпуса/платы, **не** размер кристалла | `public` (факт) / `internal` (значения) |
| **C-32** | «D2 `biocompute`: цифровая булева GRN-модель (toy), метрики размера схемы и `bio_resource_proxy`» | `sandbox/examples/biocompute_grn_v0/README.md`; NL-ADR-022 | **No wet-lab, no cells, no bacteria, no organoids** — ни у нас, ни в продукте. `bio_resource_proxy` — операции симуляции, **не ATP и не джоули** | `public` |
| **C-33** | «D3 `biosignal`: синтетическая ЭКГ/ЭЭГ → спайковое кодирование → малый LIF-классификатор» | `sandbox/examples/biosignal_ecg_v0/README.md`; NL-ADR-023 | **Сигнал синтетический, сгенерированный нами.** Не пациент, не запись прибора, не открытый датасет. **Не медицинское изделие, не диагностика, не clinical** — ни в одной формулировке | `public` |
| **C-34** | «D4 `hybrid`: композиция bio-фронта и кремниевого SNN-бэкенда в одном манифесте» | `sandbox/examples/hybrid_ecg_snn_v0/README.md`; NL-ADR-024 | Цифровая композиция двух симуляций. Не клиника, не wet-lab, не гибридное железо | `public` |
| **C-35** | «Один движок, пять доменных плагинов D0–D4, единый манифест / метрики / отчёт / diff» | `sandbox/src/closed_sandbox/engine.py`; `docs/CLOSED-SANDBOX-MVP.md` §2 | Заявление про **архитектуру**, а не про зрелость доменов. D0 — рабочий; D1–D4 — v0.1-уровня примеры | `public` |

---

## 5. Synapse E5 / Gate

| # | Заявление | Источник | Оговорка | Уровень |
|---|---|---|---|---|
| **C-40** | «На фикстуре E5 класс на escalate чинит Synapse `specialist` с accuracy **0.8636**; oracle-потолок той же фикстуры — **0.8902**» | `sandbox/reports/e5-roles-ask-20260801.md`; фикстура `sandbox/examples/synapse_e5_import/fixtures/e5-official.json`, bench `2026-08-01-e5-brains-v2-skip-llm.json` (репозиторий Synapse) | **Замороженная фикстура одного прогона**, не live-система и не данные заказчика. Oracle 0.8902 — лабораторный потолок, **не KPI продукта**; разрыв ~2.7 pp открыт. Прирост над stub (0.8561) = +0.75 pp — меньше, чем звучит | `public` |
| **C-41** | «Класс на escalate принадлежит Synapse, LLM его не чинит: Outpost объясняет и пишет audit» | `docs/SYNAPSE-GATE-SOW-WORDING.md` §1 (**Approved** человеком 2026-08-03); Commercial ADR-054 | Единственный блок этого файла с человеческим sign-off. Формулировки §3–§5 того документа можно брать как есть; §2 forbidden соблюдать | `public` |
| **C-42** | «Smoke Gate: 3 из 3 ролевых проверок проходят на именованном пилотном контуре» | `STATUS.md` 2026-08-05; `sandbox/reports/e5-roles-ask-20260801.md`; Commercial `scripts/synapse-gate-smoke.sh` | **3 проверки — это smoke, а не eval.** Не «3/3 точность». Флаг `[synapse_bridge]` по умолчанию **выключен**, включается только на именованном пилотном конфиге | `public` |
| **C-43** | «Mid 14B на задаче перевыбора класса дал **Δacc = 0** против заглушки» | `sandbox/reports/e5-mid14-escalate-2026-07-29.md` | Отрицательный результат: размер модели — не рычаг для этой задачи. Цитировать как методологию, не как «мы тестировали 14B» | `public` |

---

## 6. Инженерные счётчики

| # | Заявление | Источник | Оговорка | Уровень |
|---|---|---|---|---|
| **C-50** | «Юнит-набор песочницы: **85 passed** (`pytest -m "not integration"`), плюс шлюз одной командой `scripts/gate.sh` — 6 шагов, GATE: PASS» | Прогон 2026-08-08 на коммите `e030e9e`; CI — `.github/workflows/`; шлюз — `scripts/gate.sh` | Это тесты **нашего кода**, а не валидация научных результатов: golden-файлы фиксируют формат отчёта, а не физику. Было 51 до треков E/F/I — при цитировании брать число из свежего прогона, а не из этой строки | `public` |
| **C-51** | «Интеграционные тесты `ask` ↔ Outpost: 3 passed» | `docs/CLOSED-SANDBOX-VERIFY.md`; `sandbox/tests/test_ask_outpost.py`, `sandbox/tests/test_ask_cli.py` | Требуют Metal/GPU-хоста, GGUF и Commercial-бинарника; в общем прогоне не участвуют | `public` |
| **C-52** | «Demo pack: 6 pass / 0 fail на прогоне доменов» | `docs/DEMO-PACK-SANDBOX.md` §2; `sandbox/scripts/demo_pack.sh` | «6» — число примеров, которые отработали без ошибки, **не** число проверенных научных утверждений | `public` |
| **C-53** | — | `docs/BASE-LICENSE.md`; NL-ADR-028 Accepted 2026-08-13 | **Locked base = Qwen2.5-7B-Instruct, Apache-2.0.** Все 3B GGUF (`hammer` и остальные) остаются производными `qwen-research` — research-only, не в пилотный пак. GGUF 7B на диске; eval — C-54–C-59. Цифры 17/20 и 20/20 с 3B **не переносятся** | `internal` |

---

## 7. Заявлять нельзя вообще

Ни в гранте, ни в SOW, ни в деке, ни на сайте, ни в письме. Список не новый —
это существующие non-goals, сведённые в одно место.

| Запрет | Откуда |
|---|---|
| «Отечественная 70B» и любая линейка без паспорта и eval | `AGENTS.md` §8 |
| Измеренные джоули / ватты / мДж — от sandbox или от Brain | `docs/SYNAPSE-GATE-SOW-WORDING.md` §2; `docs/NORTH-STAR-BUILD.md` §4 («no fake Joules») |
| Vendor utilization, timing closure, bitstream, синтез | `sandbox/examples/chip_fpga_lite_v0/README.md`; NL-ADR-021 |
| Fab / PDK / GDSII / tape-out / measured silicon | `docs/CLOSED-SANDBOX-MVP.md` §4; NL-ADR-020 |
| Clinical / диагностика / медицинское изделие | `docs/CLOSED-SANDBOX-MVP.md` §4; NL-ADR-023; `docs/SYNAPSE-GATE-SOW-WORDING.md` §2 |
| Wet-lab, органоиды, культивация — как наш продукт | `docs/CLOSED-SANDBOX-MVP.md` §2, §4; NL-ADR-022 |
| «LLM чинит class / заменяет Synapse», «Synapse chat» | `docs/SYNAPSE-GATE-SOW-WORDING.md` §2 |
| «Frontier parity» / «лучше GPT / Kimi / Grok» | `docs/SYNAPSE-GATE-SOW-WORDING.md` §2; `docs/INVESTOR-NORTH-STAR.md` («Do not say») |
| «Gate включён по умолчанию в проде» | `docs/SYNAPSE-GATE-SOW-WORDING.md` §2 |
| «Oracle-разрыв закрыт» / 100% точность класса | `docs/SYNAPSE-GATE-SOW-WORDING.md` §2 |
| Обучение на ПДн заказчика | `AGENTS.md` §6, §8 |
| Готовность Mid / 7–14B / arch-MoE | `AGENTS.md` §6; `docs/PILOT-CONTOUR-CHAT.md` §6 |
| Пилотное обещание того, чего нет в `STATUS.md` Done | `AGENTS.md` §4 |
| **Право поставить 3B-веса Outpost-Tiny заказчику коммерчески** — `qwen-research` | `docs/BASE-LICENSE.md`; C-53 |

Отдельно: **«20/20» без указания, что три пункта закрывает runtime** — это тоже
запрещённая формулировка, а не просто неточность (см. C-02).

---

## 8. Чек-лист перед отправкой наружу

1. Каждое число в тексте есть в этом файле? Если нет — не отправлять.
2. Взято **дословно** из «Заявления», не пересказано?
3. Оговорка идёт рядом с цифрой, а не в сноске мелким шрифтом?
4. Ни одна строка `internal` не просочилась?
5. Модель и модель+runtime стоят раздельно?
6. Прогноз или план не подан как измеренный результат?
7. Дата источника ещё актуальна (`STATUS.md` не пересчитал цифру)?

Не проходит хоть один пункт — правится текст, а не эта таблица.
