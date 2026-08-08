# Intellectual Canon — база линейки нейронок Outpost

> **Статус:** living canon (NL-ADR-007) · обновлять при крупных сдвигах поля  
> **Для кого:** агенты и human перед train/arch решениями  
> **Фильтр:** не «всё про DL», а то, что усиливает **offline / contour / Construct / min→max**  
> **Соседний канон:** мозгоподобные / SNN студия → [`CLOSED-SANDBOX-CANON.md`](CLOSED-SANDBOX-CANON.md) (не смешивать с dense Tiny)

---

## 1. Зачем канон

Линейка Outpost (Tiny → suite → Mid → Large) должна опираться не на хайп, а на:

1. **Проверенные основы** (математика, оптимизация, transformers).  
2. **Scaling & post-training** (как реально растут модели).  
3. **Инженерные практики** frontier-лаб (Anthropic, OpenAI и open-weights лидеры).  
4. **Карту будущего** — куда идут архитектуры, чтобы Construct оставался живым.

Канон **не заменяет** eval и CARD. Он задаёт *на чём думаем*, когда выбираем рычаг.

---

## 2. Столпы линейки (что закладываем в ДНК)

| Столп | Откуда в науке/инженерии | Как в Outpost / Neurolab |
|---|---|---|
| **Dense Transformer first** | Vaswani et al.; практика Qwen/Llama | Tiny/Mid = dense GGUF |
| **Compute–data–size laws** | Kaplan; Hoffmann (Chinchilla) | не раздувать params без данных; LoRA до full FT |
| **Post-training > raw size** | InstructGPT; Qwen2.5 SFT/RL notes | поведение контура = SFT/LoRA на gaps |
| **Specialization / sparsity** | MoE scaling (Mixtral, DeepSeek, 2025 EL laws) | **сначала product Construct** (слоты); arch-MoE на Large |
| **Test-time compute** | o-series / LRM; Anthropic inverse scaling | осторожно: больше thinking ≠ всегда лучше; eval на длинных цепочках |
| **Interpretability & auditability** | Anthropic SAE / circuits | для госа: паспорт, eval, отказ от «чёрного ящика» в поставке |
| **Local inference stack** | llama.cpp / GGUF ecosystem | единственный prod path Phase 1–2 |
| **Systems reliability** | OpenAI train infra essays | воспроизводимость, governor, degrade profiles |
| **System ≠ monolith LLM** | Synapse bridge + Construct + contour | decide/escalate отдельно от language; NL-ADR-019 |
| **Resource economy as moat** | SNN / event-driven / energy proxies | измерять джоуль/ватт/active FLOPs — не только «умнее chat» |

**Девиз канона:** мощная будущая база = **измеримое качество + гибкий Construct + честный scaling + экономия ресурсов**, не копирование GPT/Kimi/Grok.  
North star: [`STRATEGY.md`](STRATEGY.md) · NL-ADR-019.

---

## 3. Карта будущего (куда могут пойти нейросети)

Агенты учитывают эти векторы при эволюции Construct (не обязаны реализовывать сразу).

| Вектор | Суть | Наша ставка |
|---|---|---|
| **A. Bigger pretrain** | больше данных/параметров | Mid/Large позже; не блокер Tiny |
| **B. Better post-train** | SFT, preference, tool-use | **основной рычаг Neurolab сейчас** |
| **C. Test-time reasoning** | длинный CoT / search | опционально; следить за inverse scaling |
| **D. Sparse / MoE** | capacity ≠ active FLOPs | product MoE → arch MoE на dc |
| **E. Long context + memory** | 100k–1M+, RAG, external memory | Outpost RAG/embed + context_size; не свой 1M с нуля |
| **F. Multimodal** | vision/audio | BYOM vision уже в runtime; свой vision pack позже |
| **G. Agents / tools** | tool loop, verify | Commercial LAM; модели учить format/JSON |
| **H. On-device / edge** | tiny + quant | Tiny + profile `lite` |
| **I. Interpretability / eval** | SAE, circuits, safety evals | CARD, rubric, audit; deep SAE — research track |
| **J. Sovereignty / supply chain** | лицензии, provenance | **наш GTM-дифференциатор** |

Construct (`CONSTRUCT.md`) спроектирован так, чтобы A–J добавлялись **слотами и профилями**, без смены протокола.

---

## 4. Книги (ядро)

### Tier A — must (основы мышления)

| Книга | Зачем нам |
|---|---|
| **Goodfellow, Bengio, Courville — *Deep Learning* (2016)** · [deeplearningbook.org](https://www.deeplearningbook.org/) | линал, вероятность, оптимизация, регуляризация — «почему градиенты работают» |
| **Bishop & Bishop — *Deep Learning: Foundations and Concepts* (2023/24)** | современный фундамент: transformers, generative models, идеи которые переживают хайп |
| **Simon J.D. Prince — *Understanding Deep Learning*** · [udlbook.github.io](https://udlbook.github.io/udlbook/) | мост к современным архитектурам; бесплатный online |

### Tier B — systems & product ML

| Книга / курс | Зачем |
|---|---|
| **Chip Huyen — *Designing Machine Learning Systems*** | данные, eval, мониторинг, итерации — ближе к ENGINEERING.md |
| **Andrej Karpathy — *Neural Nets: Zero to Hero*** · [playlist](https://karpathy.ai/zero-to-hero) | от backprop до GPT руками; общий язык с инженерами |
| **Karpathy — *Deep Dive into LLMs like ChatGPT*** (talk) | mental model стека LLM для non-research |

### Tier C — по необходимости

| | |
|---|---|
| Géron — *Hands-On Machine Learning* | практика sklearn/torch, не канон архитектуры |
| Jurafsky & Martin — *Speech and Language Processing* | NLP classic, если углубляем язык |
| Nielsen — *Neural Networks and Deep Learning* (online) | мягкий вход в backprop |

**Не делаем:** читать всё подряд перед первым LoRA. Tier A главы по оптимизации + Karpathy GPT lecture + papers §5 — достаточно старта.

---

## 5. Статьи и tech reports (ядро)

### 5.1 Архитектура и язык

| Работа | Ссылка | Берём |
|---|---|---|
| Vaswani et al. — **Attention Is All You Need** (2017) | [arXiv:1706.03762](https://arxiv.org/abs/1706.03762) | transformer = default backbone |
| Radford et al. — GPT-2 / GPT-3 reports | OpenAI | autoregressive LM paradigm |
| **Qwen2.5 Technical Report** | [arXiv:2412.15115](https://arxiv.org/abs/2412.15115) | **наш locked base lineage**; SFT/RL post-train, size ladder |
| Qwen2 Technical Report | [arXiv:2407.10671](https://arxiv.org/abs/2407.10671) | контекст семейства + early MoE notes |
| Llama 2 / 3 reports (Meta) | arXiv / Meta | open-weights ops, лицензии сравнивать |

### 5.2 Scaling

| Работа | Ссылка | Берём |
|---|---|---|
| Kaplan et al. — Scaling Laws for Neural LM (2020) | [arXiv:2001.08361](https://arxiv.org/abs/2001.08361) | loss ~ compute power law |
| Hoffmann et al. — **Chinchilla** (2022) | [arXiv:2203.15556](https://arxiv.org/abs/2203.15556) | data ∝ params; не «модель ради модели» |
| MoE EL scaling (2025) | [arXiv:2507.17702](https://arxiv.org/abs/2507.17702) | когда arch-MoE даёт leverage; **не для Tiny v0** |

### 5.3 Адаптация (наш основной craft)

| Работа | Ссылка | Берём |
|---|---|---|
| Hu et al. — **LoRA** (2021) | [arXiv:2106.09685](https://arxiv.org/abs/2106.09685) | default adapt path Neurolab |
| Ouyang et al. — **InstructGPT** (2022) | [arXiv:2203.02155](https://arxiv.org/abs/2203.02155) | instruction / preference post-train |
| Rafailov et al. — DPO (2023) | [arXiv:2305.18290](https://arxiv.org/abs/2305.18290) | позже, если RLHF слишком тяжёл |
| Wei et al. — Chain-of-Thought (2022) | [arXiv:2201.11903](https://arxiv.org/abs/2201.11903) | prompting; не путать с обязательным long-CoT |

### 5.4 Специализация / MoE (будущее Large)

| Работа | Зачем |
|---|---|
| Shazeer et al. — Outrageously Large Neural Networks (MoE, 2017) | корни |
| Mixtral / DeepSeek-MoE reports | практика sparse LLM |
| Raschka FAQ — MoE vs dense | ясная инженерная картинка |

**Наш вывод:** arch-MoE — инструмент **L6/dc**; до этого Construct slots ≈ «MoE продукта».

---

## 6. Лаборатории: блоги, доклады, инженерия

### 6.1 Anthropic (качество, механика, риски)

| Материал | URL | Что взять |
|---|---|---|
| Scaling Monosemanticity | [transformer-circuits.pub/2024/scaling-monosemanticity](https://transformer-circuits.pub/2024/scaling-monosemanticity/) | features/SAE; scaling даже interpretability tooling |
| Engineering challenges of scaling interpretability | [anthropic.com/research/…](https://www.anthropic.com/research/engineering-challenges-interpretability) | наука ↔ engineering loop |
| Tracing thoughts / circuit tracing (2025) | [anthropic.com/news/tracing-thoughts…](https://www.anthropic.com/news/tracing-thoughts-language-model) | модели как «биология»; скромность претензий «понимаем всё» |
| Inverse scaling in test-time compute | [alignment.anthropic.com/2025/inverse-scaling](https://alignment.anthropic.com/2025/inverse-scaling/) | **не** наивно крутить reasoning length; eval на failure modes |
| Constitutional AI / HHH essays | anthropic.com | тон отказов и полезности — ближе к нашим refuse gaps |

**Для контура/госа:** интерпретируемость и отказные сценарии — часть *качества поставки*, не academic hobby.

### 6.2 OpenAI (scale systems + training craft)

| Материал | URL | Что взять |
|---|---|---|
| Techniques for training large neural networks | [openai.com/index/techniques-for-training-large-neural-networks](https://openai.com/index/techniques-for-training-large-neural-networks/) | data/pipeline/tensor parallel — карта, когда вырастем |
| Infrastructure for deep learning | [openai.com/index/infrastructure-for-deep-learning](https://openai.com/index/infrastructure-for-deep-learning/) | infra как множитель research |
| Scaling Kubernetes to 7,500 nodes | [openai.com/…](https://openai.com/index/scaling-kubernetes-to-7500-nodes/) | gang scheduling mindset (нам — в миниатюре: reproducible jobs) |
| MRC supercomputer networking (2025/26) | [openai.com/index/mrc…](https://openai.com/index/mrc-supercomputer-networking/) | только для будущего Large/cluster; не Tiny |
| GPT-4 System Card / eval culture | openai.com | культура eval и risk categories |

**Фильтр:** 99% OpenAI infra **не копируем**. Берём *дисциплину*: measure, parallelize only when needed, reliability of the job.

### 6.3 Практический open stack (наш runtime)

| Источник | Зачем |
|---|---|
| **llama.cpp** / GGUF docs & issues | quant, memory, MoE support realities |
| Hugging Face PEFT / Unsloth guides | LoRA recipes (сверять с LICENSE) |
| Sebastian Raschka — LLMs from Scratch / blog | современный engineering pedagogy |

### 6.4 Выступления (короткий список)

| | |
|---|---|
| Karpathy — Deep Dive into LLMs / Zero to Hero GPT lecture | общий стек |
| Anthropic research roundtables (interpretability engineering) | science+eng |
| Stanford CS25 / talks on transformers (обновлять по году) | обзор поля |

---

## 7. Что канон **запрещает** как «основание»

| Анти-паттерн | Почему |
|---|---|
| «Сделаем как GPT-4 архитектуру втайне» | нет весов/данных/compute; ломает min→max |
| Arch-MoE на 3B «потому что тренд» | EL laws + наш Construct уже дают specialization |
| Безeval «улучшили модель» | против ENGINEERING.md |
| Игнорировать LICENSE upstream | убивает гос/КИИ путь |
| Слепо scale test-time compute | inverse scaling (Anthropic) |

---

## 8. Как агентам пользоваться каноном

### Перед решением

1. Найти столп в §2 и вектор в §3.  
2. Есть ли paper/book в Tier A/§5, который поддерживает рычаг?  
3. Записать в ADR или Session log: *«опираемся на X; не делаем Y»*.  
4. Прогнать через фильтр: Contour? Measure? Construct slot?

### Reading order (основатель / агент onboarding)

| Шаг | Материал | Время |
|---|---|---|
| 1 | Этот файл §2–3 + `CONSTRUCT.md` | 1 h |
| 2 | Karpathy GPT lecture + Attention paper (skim) | 3–4 h |
| 3 | LoRA + InstructGPT abstracts + Qwen2.5 report §post-train | 2 h |
| 4 | Chinchilla abstract + our `SCALE-PLAN.md` | 1 h |
| 5 | Anthropic inverse scaling + one interpretability overview | 1–2 h |
| 6 | Goodfellow ch.6–8 / Bishop transformers chapter — фоном | ongoing |

### Обновление канона

- Раз в квартал или при смене locked base / переходе на Mid.  
- Новые ссылки — только с **одной фразой «берём / не берём»**.  
- NL-ADR при смене столпа (например, «default становится arch-MoE»).

---

## 9. Связь с артефактами Lab

| Артефакт | Канон питает |
|---|---|
| `outpost-tiny` | Qwen2.5 + LoRA + Instruct post-train |
| Construct slots | specialization without early arch-MoE |
| Profiles lite→dc | Chinchilla economics + local RAM reality |
| Eval / refuse gaps | Anthropic-style failure modes + InstructGPT alignment craft |
| Future Mid/Large | scaling laws + OpenAI systems literacy |
| Gov narrative | provenance + interpretability humility + offline |

---

## 10. Быстрый «cheat sheet» для Session log

При спорном выборе копируй:

```text
Canon check:
- Pillar: …
- Paper/book: …
- Future vector: …
- Adopt / defer: …
- Construct impact: new slot? profile? weights only?
```
