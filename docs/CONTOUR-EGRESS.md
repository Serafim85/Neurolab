# Contour & egress policy — свои облака vs чужие LLM

> **Status:** policy foundation (NL-ADR-009)  
> **Model behavior** (Tiny LoRA) + **runtime connectors** (Commercial, later)  
> Связано: `GOALS.md` · Commercial `SECURITY-PHASES.md` (B8 offline-first)

---

## 1. One-liner

**Outpost живёт в контуре заказчика.**  
Своё / утверждённое облако клиента — **подключаем**.  
Публичные облачные LLM и неутверждённый egress — **можно заложить, по умолчанию выключены**.

---

## 2. Три зоны

| Зона | Примеры | Политика |
|---|---|---|
| **A. Local / air-gap** | `sovereignd` на сервере, нет исходящего | default Phase 1 |
| **B. Client cloud / private contour** | VPC, private k8s, «своё облако», внутренний API заказчика | **целевой коннект** — когда пилот просит; явный allowlist |
| **C. Public cloud LLM / open internet** | ChatGPT, Claude API, произвольный HF inference | **opt-in, default OFF** |

«Облако клиента» ≠ ChatGPT. Это их периметр (часто всё ещё называется cloud).

---

## 3. Поведение модели (Neurolab / Tiny LoRA)

Учим **contour-safe**, не anti-cloud:

| Пользователь просит | Ответ |
|---|---|
| Залить внутренний отчёт в ChatGPT / публичный SaaS | Отказ + предложить Outpost / контур |
| Использовать **своё** облако / внутренний endpoint заказчика | Ок, если политика контура позволяет; не пугать «облако = зло» |
| Неясно куда | Уточнить / предложить только approved contour |

Eval gap переименовываем в духе: `contour_refuse_public_llm` (не `refuse_any_cloud`).

---

## 4. Runtime connectors (Commercial — design)

| Connector | Default | Когда включать |
|---|---|---|
| Inference outbound to public LLM | **off** | только явный config + WARN + audit |
| Client-private API / object store / IdP в их cloud | **off** until configured | pilot contract: allowlist URL/CIDR |
| Model pull from internet | lab/staging only | prod air-gap: USB / mirror |
| Telemetry / phone-home | **off** (B8) | never without opt-in |

Правила (совместимы с baseline):

1. Нет конфига → **нет исходящего** к C.  
2. B включается списком разрешённых целей, не «открыть интернет».  
3. Любой egress → audit event (metadata: host/purpose; не тело промпта по умолчанию).  
4. Смена default offline → ADR + human.

*Реализация коннекторов — не блокер Tiny LoRA; сначала поведение модели + docs.*

---

## 5. Config sketch (будущее Commercial)

```toml
# НЕ Phase 1 default — иллюстрация политики
[egress]
enabled = false                    # master switch

[egress.public_llm]
enabled = false                    # ChatGPT-class — default OFF
# providers = []

[egress.client_cloud]
enabled = false                    # turn on per pilot
# allow_hosts = ["api.internal.example.ru", "s3.contour.local"]
# allow_cidrs = ["10.0.0.0/8"]
```

Advisor (NL-ADR-008) позже может читать эти флаги при propose.

---

## 6. GTM / ИБ формулировки

| Можно говорить | Нельзя |
|---|---|
| Offline-first; контур заказчика | «Мы никогда не работаем с облаком» (ложно, если своё cloud) |
| Подключение к **вашему** private cloud по allowlist | Молчаливый egress в публичные LLM |
| Публичные LLM — опция, выкл. по умолчанию | Обещать hybrid GPT без контракта и audit |

---

## 7. Связь с девизами

| | |
|---|---|
| Надёжность | default deny egress |
| Качество | модель различает свой контур vs публичный SaaS |
| Min→max | сначала local; client cloud — когда платят за интеграцию |
