# Closed Sandbox — грантовые программы (карта)

> **Status:** living map (2026-07-26)  
> **Продукт:** [`CLOSED-SANDBOX-MVP.md`](CLOSED-SANDBOX-MVP.md) · канон: [`CLOSED-SANDBOX-CANON.md`](CLOSED-SANDBOX-CANON.md)  
> **Фильтр:** программы под **SNN / edge energy / closed-contour studio**, не под fab и не под «ещё один LLM».  
> Суммы и дедлайны — ориентиры; перед подачей сверять официальные страницы.

---

## 1. Условия входа (общее)

Почти везде нужно:

1. **Юрлицо** в EU Member State или Horizon Europe associated country (в т.ч. CH после ассоциации 2025).  
2. **Демо** sandbox (metrics: F1/accuracy + spike_count / energy proxy) — иначе «idea-only».  
3. Для части программ — **консорциум** (uni / RTO / industry).  
4. Narrative в заявках:

> Closed-contour studio for compact brain-inspired / SNN models with measurable energy proxies, targeting edge industrial sensing — sovereignty-compatible; public LLM only explicit opt-in for lab.

**Не писать:** «Photoshop для всех чипов», «воспроизвели мозг», «tape-out в год 1».

---

## 2. Лестница по стадии

| Стадия | TRL (грубо) | Что есть | Куда бить |
|---|---|---|---|
| **S0** | 1–2 | docs + scaffold | готовить юрлицо; код MVP; гранты не подавать |
| **S1** | 3–4 | sandbox v0.1 + example anomaly | national / Innosuisse / Eurostars / Pathfinder* |
| **S2** | 4–6 | пилот + LoI | Chips JU (консорциум) / Transition* / strong national |
| **S3** | ≥5–6 | пилоты, scale story | **EIC Accelerator Open** |

\*Pathfinder / Transition — см. нюансы ниже.

---

## 3. Программы — shortlist

### 3.1 Ранняя стадия (S1) — приоритет после демо

| ID | Программа | Гео | Формат | Ориентир $$ | Зачем нам | Блокер |
|---|---|---|---|---|---|---|
| **G-INNO** | **Innosuisse Start-up Innovation Projects** | CH | grant SME, equity-free | до ~70% eligible costs (ceiling по правилам Innosuisse, часто до CHF ~2.5M class) | science-based pre-market; AI/NN в теме | нужна **швейцарская** компания |
| **G-NAT** | **National startup / innovation** страны юрлица | LU / DE / NL / … | grant / loan / incubate | десятки–сотни k€ (разнится) | быстрый money на MVP→пилот | выбрать юрисдикцию |
| **G-NAT-LU** | Luxembourg: **Technoport / SNCI** (+ местные instruments) | LU | incubate / soft + иногда capital | case-by-case | дом для семьи + EU access | редко заменяет EIC по размеру |
| **G-NAT-DE** | Germany: **EXIST** / **ZIM** (и аналоги) | DE | grant | case-by-case | сильный deep-tech трек | DE substance |
| **G-NAT-NL** | Netherlands: **RVO** / Innovatiekrediet (и аналоги) | NL | grant/loan | case-by-case | рядом neuromorphic talent (Eindhoven) | NL substance |
| **G-EURO** | **Eurostars** (Eureka) | EU + associated | co-fund, обычно 2+ страны | co-fund national+EU | R&D SME с партнёром edge/SNN | нужен зарубежный партнёр |
| **G-PATH** | **EIC Pathfinder** Open / Challenges | EU / CH | RIA, часто consortium | до ~€4M | research TRL 1–4 с uni | Open: часто **≥3 партнёра / 3 страны**; не чистый SaaS-pitch |

### 3.2 Средняя стадия (S2)

| ID | Программа | Гео | Формат | Ориентир $$ | Зачем нам | Блокер |
|---|---|---|---|---|---|---|
| **G-TRANS** | **EIC Transition** | EU / CH | lump sum RIA | до ~€2.5M | TRL 3/4 → 5/6 | часто нужен **eligible prior project** (Pathfinder/ERC/…) |
| **G-CHIPS-RIA** | **Chips JU — ECS GLOBAL RIA** | консорциум | RIA TRL ~3–4 + national co-fund | EU slice + national | edge AI / ECS; мы как **tools/design SME** | не solo; партнёры RTO |
| **G-CHIPS-IA** | **Chips JU — ECS GLOBAL IA** | консорциум | IA TRL ~5–8 + national co-fund | выше | industrial demo | не solo; выше TRL |
| **G-CASCADE** | **Cascade / Digital Europe** pilots (AI hubs, AI-MATTERS-класс) | через хабы | small grants | часто €50–200k | быстрые пилоты | следить open calls |

**Chips JU 2026 (ориентир на момент фиксации):**  
ECS GLOBAL IA / RIA — окна с closing около **17.09.2026** (проверять [chips-ju.europa.eu](https://www.chips-ju.europa.eu/Open-and-Upcoming-Calls/)).  
Мы — участник консорциума (software/tools), не обязаны делать fab.

### 3.3 Scale (S3)

| ID | Программа | Гео | Формат | Ориентир $$ | Зачем нам | Блокер |
|---|---|---|---|---|---|---|
| **G-EIC-OPEN** | **EIC Accelerator Open** | одна SME EU/CH | grant ≤€2.5M ± equity | главный приз | deep-tech scale после пилотов | TRL ≥5; success rate низкий |
| **G-EIC-CHAL** | **EIC Accelerator Challenges 2026** | одна SME | thematic | €20–50M pot / challenge | — | **2026 темы не про AI** (materials, fusion, soil, CRM, climate) → **не наш primary** |
| **G-STEP** | **EIC STEP Scale-Up** | scale-ups | large equity | later | не год 1 | нужна зрелость |

Швейцария: associated → Swiss SME могут в EIC (в т.ч. equity — сверять актуальный Work Programme).

---

## 4. Юрисдикция × программы

| База | Сильный ход | Слабое место |
|---|---|---|
| **Luxembourg** | G-NAT-LU + G-EIC-OPEN / Eurostars / Chips JU как LU SME | мало «своих» больших AI-грантов; экосистема chips слабее NL/DE |
| **Switzerland** | G-INNO + EIC + uni (ETH/EPFL/CSEM) | SwissChips = academic IC, не наш основной grant |
| **Germany / Netherlands** | national + Chips talent + EIC | медиа/быт — отдельный семейный фильтр |
| **Russia (параллельно)** | РНФ / Сколково / отраслевые — seed R&D | не смешивать IP/dual-use с EU-заявкой без юриста; EU money ≠ RU entity |

Гибрид (обсуждался): **жить/HQ в LU**, R&D/partners в CH/NL/DE — допустим, если substance и eligible applicant ясны аудиторам.

---

## 5. Что **не** считать основным треком

| Программа / миф | Почему не primary |
|---|---|
| SwissChips tape-out budget | academic IC prototyping, не SaaS studio grant |
| «EIC Challenges = AI 2026» | Challenges 2026 — другие темы; нам **Open** |
| Organoid / wetware calls | out of product scope (canon) |
| Подача EIC Accelerator без демо | сжигание месяцев при ~нескольких % success |

---

## 6. Документы, которые готовим до подачи (чеклист)

- [ ] SME зарегистрирован (EU или CH)  
- [ ] `sandbox` v0.1: run + report (F1 + spike_count + budget_ok + quality_per_kspike)  
- [ ] 1–2 page technical annex — start from [`INVESTOR-NORTH-STAR.md`](INVESTOR-NORTH-STAR.md) + economy in reports  
- [ ] LoI / letter from pilot или research partner (S2+)  
- [ ] IP: кто владеет кодом/моделями; нет утечки секретов в public `ask` без политики  
- [ ] Budget + 12–24 мес work plan — [`NORTH-STAR-BUILD.md`](NORTH-STAR-BUILD.md)  
- [ ] Для EIC: video + platform forms (когда дойдём до S3)

---

## 7. Порядок атак (рекомендация Lab)

```text
1. Демо sandbox (S1)
2. Юрлицо (LU или CH/DE/NL — решение семьи + substance)
3. G-NAT или G-INNO  →  деньги на пилот
4. Параллельно искать uni/RTO → G-EURO или G-CHIPS-RIA
5. После пилота → G-EIC-OPEN
```

Гранты **не блокер кодинга**. Код и метрики — блокер грантов.

---

## 8. Официальные точки входа (проверить перед подачей)

| | URL |
|---|---|
| EIC Accelerator | https://eic.ec.europa.eu/eic-funding-opportunities/eic-accelerator_en |
| EIC Pathfinder / Transition | https://eic.ec.europa.eu/ |
| Chips JU calls | https://www.chips-ju.europa.eu/Open-and-Upcoming-Calls/ |
| Innosuisse startup projects | https://www.innosuisse.admin.ch/en/start-up-innovation-projects |
| Funding & Tenders Portal | https://ec.europa.eu/info/funding-tenders/opportunities/portal/ |

---

## 9. История обновлений

| Дата | Что |
|---|---|
| 2026-08-02 | Pointer to investor one-pager + NORTH-STAR-BUILD; economy proxies in sandbox reports |
| 2026-07-26 | Первая фиксация shortlist после продуктового сужения Closed Sandbox |
