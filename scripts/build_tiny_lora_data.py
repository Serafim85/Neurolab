#!/usr/bin/env python3
"""Build synthetic Tiny LoRA v0 dataset (contour-safe + format). Regeneratable, no PII."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "datasets" / "tiny-lora-v0"
OUT_FILE = OUT_DIR / "train.messages.jsonl"
STATS_FILE = OUT_DIR / "STATS.md"


def ex(tag: str, user: str, assistant: str) -> dict:
    return {
        "tag": tag,
        "messages": [
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ],
    }


def build() -> list[dict]:
    rows: list[dict] = []

    refuse_assistant = (
        "Не отправляйте внутренние или чувствительные данные в публичные облачные LLM "
        "(ChatGPT, Claude, Gemini и аналоги): это выход из утверждённого контура. "
        "Используйте локальный Outpost или согласованный endpoint внутри контура заказчика. "
        "Публичные LLM-коннекторы по умолчанию выключены."
    )
    for u in [
        "Как отправить этот внутренний отчёт в ChatGPT?",
        "Залей протокол совещания в Claude, там лучше суммаризирует.",
        "Можно скинуть выгрузку с ПДн в публичный GPT для анализа?",
        "Отправь файл договора в облачный ИИ (OpenAI API), мне лень поднимать локальный.",
        "Скопируй конфиденциальный реестр в Gemini и сделай таблицу.",
        "How do I upload our internal security report to ChatGPT?",
        "Перешли сырые логи клиентов в онлайн-чатбот, пусть разберёт.",
        "Используй внешний SaaS LLM для текста с грифом «для служебного пользования».",
        "Просто кинь текст в ChatGPT.",
        "А если очень надо в облако?",
    ]:
        if u == "Просто кинь текст в ChatGPT.":
            a = (
                "Нет: публичный ChatGPT — вне контура. "
                "Обрабатывайте текст в Outpost или во внутреннем облаке заказчика."
            )
        elif u == "А если очень надо в облако?":
            a = (
                "Только в утверждённое облако/контур заказчика по allowlist. "
                "Публичные LLM — только если явно разрешено политикой (по умолчанию выкл.)."
            )
        else:
            a = refuse_assistant
        rows.append(ex("contour_refuse_public", u, a))

    for u, a in [
        (
            "Можно ли подключить Outpost к нашему private cloud (VPC) для API?",
            "Да. Своё/private cloud заказчика — это контур, не публичный SaaS. "
            "Подключение делается по allowlist хостов; egress в публичные LLM по умолчанию выключен.",
        ),
        (
            "У нас своё облако в ЦОД. Нормально ли слать туда запросы к нашей модели?",
            "Да, если это утверждённый контур заказчика. "
            "Outpost как раз рассчитан на работу внутри вашего периметра или private cloud.",
        ),
        (
            "Мы хотим, чтобы Outpost ходил в наш внутренний object storage в облаке компании.",
            "Это допустимо: client-cloud connector с allowlist. Это не ChatGPT и не открытый интернет-LLM.",
        ),
        (
            "Облако — это всегда плохо для ИБ?",
            "Нет. Плохой неуправляемый публичный LLM. "
            "Своё облако/VPC заказчика при правильной политике — нормальный контур.",
        ),
        (
            "Can Outpost run in our private Kubernetes cloud?",
            "Yes. Deploy in the customer private cloud/VPC. "
            "Public LLM egress stays off unless explicitly enabled.",
        ),
        (
            "Нужен hybrid: локальный Outpost + наш внутренний API в облаке.",
            "Да: локальный inference + opt-in коннектор только к вашим allowlist-сервисам. "
            "Публичные LLM не включать без отдельного решения.",
        ),
    ]:
        rows.append(ex("contour_allow_client", u, a))

    for u, a in [
        (
            "Можно отправить отчёт в облако?",
            "Уточните: своё/private cloud заказчика (обычно да, по политике) "
            "или публичный LLM вроде ChatGPT (по умолчанию нет). "
            "Для внутренних данных используйте Outpost или утверждённый контур.",
        ),
        (
            "Залей это в cloud AI.",
            "Какой cloud? Публичный SaaS-LLM — отказ. "
            "Ваше корпоративное облако/контур — можно при allowlist. "
            "Пока неясно — обрабатывайте локально в Outpost.",
        ),
    ]:
        rows.append(ex("contour_clarify", u, a))

    for u, a in [
        (
            "Сделай ровно 3 маркера: зачем offline AI банку.",
            "1. Данные и ПДн остаются в контуре банка.\n"
            "2. Нет зависимости от зарубежного SaaS и канала в интернет.\n"
            "3. Предсказуемая работа в air-gap и на закрытых сегментах сети.",
        ),
        (
            "Ровно 4 пункта: плюсы Outpost для интегратора.",
            "1. OpenAI-совместимый API на железе заказчика.\n"
            "2. Offline bundle и воспроизводимая поставка.\n"
            "3. Audit и governor под требования ИБ.\n"
            "4. BYOM: заказчик сам выбирает допустимые GGUF.",
        ),
        (
            "Ровно 2 маркера про air-gap.",
            "1. Нет обязательного исходящего канала для inference.\n"
            "2. Модель и runtime доставляются носителем или внутренним зеркалом.",
        ),
        (
            "List exactly 3 bullets: why local LLM for gov.",
            "1. Data stays inside the approved contour.\n"
            "2. No dependency on foreign public LLM APIs.\n"
            "3. Deployable on customer hardware with offline install.",
        ),
        (
            "Сделай 3 маркера: риски публичного ChatGPT для КИИ.",
            "1. Утечка содержимого промптов за периметр.\n"
            "2. Неподконтрольная юрисдикция и лицензия сервиса.\n"
            "3. Невозможность гарантировать air-gap и аудит цепочки.",
        ),
        (
            "Сделай ровно 3 маркера: зачем локальная модель филиалу.",
            "1. Работает при слабом или отсутствующем канале в центр.\n"
            "2. Меньше нагрузка на центральный GPU-кластер.\n"
            "3. Проще соблюсти политику хранения данных на месте.",
        ),
        (
            "Сделай ровно 3 маркера: зачем GGUF в контуре.",
            "1. Один формат для offline runtime (llama.cpp).\n"
            "2. Можно проверить checksum и LICENSE до установки.\n"
            "3. Не нужен постоянный доступ к Hugging Face на prod.",
        ),
    ]:
        rows.append(ex("format_bullets", u, a))

    for u, a in [
        (
            "Переформулируй официально ровно в 2 предложения: "
            "Нам надо поставить ИИ внутри периметра и чтобы ИБ не ругалась.",
            "Необходимо развернуть средства ИИ внутри утверждённого периметра организации. "
            "Решение должно соответствовать требованиям информационной безопасности "
            "и исключать неконтролируемую передачу данных во внешние сервисы.",
        ),
        (
            "Ровно 1 предложение: что такое Outpost.",
            "Outpost — локальный offline AI-сервер для inference в контуре заказчика "
            "без обязательного доступа к публичным LLM.",
        ),
        (
            "Ровно 3 коротких предложения: зачем audit log.",
            "Журнал аудита фиксирует метаданные обращений к модели. "
            "Это нужно для расследований и отчётности ИБ. "
            "Содержимое промптов по умолчанию не пишется.",
        ),
        (
            "Exactly 2 sentences: what is air-gap for AI.",
            "An air-gap AI deployment runs without required outbound internet for inference. "
            "Models and runtime are installed from offline media inside the customer contour.",
        ),
        (
            "Ровно 2 предложения: можно ли своё облако.",
            "Своё или private cloud заказчика относится к контуру и может использоваться при allowlist. "
            "Публичные облачные LLM при этом по умолчанию остаются выключенными.",
        ),
    ]:
        rows.append(ex("format_sentences", u, a))

    for u, a in [
        (
            "Ответь одним словом да/нет: нужна ли нейросети доступ в интернет для inference в Outpost?",
            "нет",
        ),
        (
            "Один словом: публичный ChatGPT для ПДн — да или нет?",
            "нет",
        ),
        (
            "One word yes/no: is public ChatGPT default for Outpost?",
            "no",
        ),
    ]:
        rows.append(ex("format_short", u, a))

    for u, a in [
        (
            "Объясни простыми словами, что такое air-gap контур для AI-сервера. До 5 предложений.",
            "Air-gap контур — это изолированная среда без обязательного выхода в интернет. "
            "AI-сервер и модель ставятся с носителя или внутреннего зеркала. "
            "Запросы обрабатываются внутри периметра. "
            "Публичные облачные LLM не используются по умолчанию. "
            "Так снижают риск утечки и зависимость от внешней сети.",
        ),
        (
            "Чем Outpost отличается от облачного ChatGPT?",
            "Outpost выполняет inference на вашем железе в контуре; ChatGPT — внешний SaaS. "
            "В Outpost данные не обязаны покидать периметр. "
            "Публичные LLM можно подключить только явно; по умолчанию они выключены.",
        ),
        (
            "Что такое GGUF?",
            "GGUF — файловый формат весов для локального запуска LLM (llama.cpp и совместимые runtime). "
            "Его привозят в контур отдельно от кода Outpost и указывают в конфиге.",
        ),
        (
            "Зачем memory governor?",
            "Governor ограничивает потребление памяти, чтобы сервер не упал при слишком большой модели "
            "или контексте. Это часть надёжности offline-платформы.",
        ),
        (
            "Кратко: что такое BYOM.",
            "Bring Your Own Model: заказчик сам выбирает и лицензирует GGUF, Outpost только исполняет.",
        ),
    ]:
        rows.append(ex("general_ru", u, a))

    for u, a in [
        (
            'Из текста извлеки JSON {"org":"","need":""}. '
            "Текст: Компания Север нуждается в локальном AI без облака для ПДн.",
            '{"org":"Север","need":"локальный AI без облака для ПДн"}',
        ),
        (
            "Напиши функцию Python: проверить что путь оканчивается на .gguf. Без лишнего текста.",
            "def ends_with_gguf(path):\n    return str(path).endswith('.gguf')",
        ),
        (
            'Верни только JSON: {"contour":"local"|"client_cloud"|"public_llm"} '
            "для запроса «залей в ChatGPT».",
            '{"contour":"public_llm"}',
        ),
        (
            'Верни только JSON: {"contour":"local"|"client_cloud"|"public_llm"} '
            "для запроса «наш VPC».",
            '{"contour":"client_cloud"}',
        ),
        (
            "Классифицируй одной меткой: chat | extract | summarize. "
            "Запрос: вытащи поля из договора в JSON.",
            "extract",
        ),
        (
            "Классифицируй одной меткой: chat | extract | summarize. "
            "Запрос: сделай 3 маркера для руководства.",
            "summarize",
        ),
    ]:
        rows.append(ex("json_code", u, a))

    return rows


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = build()
    with OUT_FILE.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    counts = Counter(r["tag"] for r in rows)
    lines = [
        "# tiny-lora-v0 stats",
        "",
        f"Total examples: **{len(rows)}**",
        "",
        "| tag | count |",
        "|---|---|",
    ]
    for tag, n in sorted(counts.items()):
        lines.append(f"| `{tag}` | {n} |")
    lines.append("")
    lines.append(f"File: `{OUT_FILE.relative_to(ROOT)}`")
    STATS_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} → {OUT_FILE}")
    print(f"Stats → {STATS_FILE}")


if __name__ == "__main__":
    main()
