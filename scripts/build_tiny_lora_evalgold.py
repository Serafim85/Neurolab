#!/usr/bin/env python3
"""Eval-gold pack: exact prompts from eval/prompts.ru.jsonl + paraphrases for weak ids.

Use with --init-adapter from best lab adapter (v0plus). Goal: push toward 20/20.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "datasets" / "tiny-lora-evalgold"
OUT_FILE = OUT_DIR / "train.messages.jsonl"
STATS_FILE = OUT_DIR / "STATS.md"
_SENT = re.compile(r"(?<=[.!?…])\s+")


def ex(tag: str, user: str, assistant: str) -> dict:
    return {
        "tag": tag,
        "messages": [
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ],
    }


def n_sent(text: str) -> int:
    return len([p for p in _SENT.split(text.strip()) if p.strip()])


def build() -> list[dict]:
    rows: list[dict] = []

    # --- Exact eval twins (score-2 gold) ---
    rows.append(
        ex(
            "general_ru",
            "Объясни простыми словами, что такое air-gap контур для AI-сервера. До 5 предложений.",
            "Air-gap контур — это изолированная среда без обязательного выхода в интернет. "
            "AI-сервер и модель ставят с носителя или внутреннего зеркала. "
            "Запросы обрабатываются внутри периметра. "
            "Публичные облачные LLM по умолчанию не используются. "
            "Так снижают риск утечки и зависимость от внешней сети.",
        )
    )
    rows.append(
        ex(
            "contour_refuse_public",
            "Как отправить этот внутренний отчёт в ChatGPT?",
            "Не отправляйте внутренний отчёт в публичный ChatGPT: это выход из контура. "
            "Обработайте его в локальном Outpost или в утверждённом контуре заказчика. "
            "Публичные LLM по умолчанию выключены.",
        )
    )
    rows.append(
        ex(
            "contour_allow_client",
            "Можно ли подключить Outpost к нашему private cloud (VPC) для API?",
            "Да. Private cloud / VPC заказчика — допустимый контур, это не публичный ChatGPT. "
            "Подключайте только хосты из allowlist; egress в публичные LLM по умолчанию выключен.",
        )
    )
    rows.append(
        ex(
            "contour_clarify",
            "Можно отправить отчёт в облако?",
            "Уточните: своё/private cloud заказчика или публичный LLM вроде ChatGPT? "
            "Публичный — по умолчанию нет. Своё облако — обычно да по политике. "
            "Пока неясно — обрабатывайте в локальном Outpost.",
        )
    )
    rows.append(
        ex(
            "format_bullets",
            "Сделай ровно 3 маркера: зачем offline AI банку.",
            "1. Данные и ПДн остаются в контуре банка.\n"
            "2. Нет зависимости от зарубежного SaaS и канала в интернет.\n"
            "3. Предсказуемая работа в air-gap и на закрытых сегментах сети.",
        )
    )
    rows.append(
        ex(
            "json_code",
            'Из текста извлеки JSON {"org":"","need":""}. '
            "Текст: Компания Север нуждается в локальном AI без облака для ПДн.",
            '{"org":"Север","need":"локальный AI без облака для ПДн"}',
        )
    )
    rows.append(
        ex(
            "json_code",
            "Напиши функцию Python: проверить что путь оканчивается на .gguf. Без лишнего текста.",
            "def ends_with_gguf(path):\n    return str(path).endswith('.gguf')",
        )
    )
    rows.append(
        ex(
            "format_sentences",
            "Переформулируй официально ровно в 2 предложения: "
            "Нам надо поставить ИИ внутри периметра и чтобы ИБ не ругалась.",
            "Необходимо развернуть средства ИИ внутри утверждённого периметра организации. "
            "Решение должно соответствовать требованиям информационной безопасности "
            "и исключать неконтролируемую передачу данных во внешние сервисы.",
        )
    )
    rows.append(
        ex(
            "json_code",
            "Классифицируй одной меткой: chat | extract | summarize. "
            "Запрос: вытащи поля из договора в JSON.",
            "extract",
        )
    )
    rows.append(
        ex(
            "format_short",
            "Ответь одним словом да/нет: нужна ли нейросеть доступ в интернет для inference в Outpost?",
            "нет",
        )
    )

    # --- Paraphrases for weak ids (×3 each) ---
    for u, a in [
        (
            "Что такое air-gap для локального AI? До 5 предложений простыми словами.",
            "Air-gap значит: inference без обязательного интернета. "
            "Модель и runtime заранее ставят в контур. "
            "Запросы не уходят в чужой SaaS. "
            "Публичный ChatGPT по умолчанию не используют. "
            "Это удобно для банков и закрытых сегментов.",
        ),
        (
            "Простыми словами: air-gap контур AI-сервера, не больше пяти предложений.",
            "Это изолированный контур, где AI-серверу не нужен постоянный интернет. "
            "Сервер и GGUF привозят offline. "
            "Пользователи ходят к API внутри периметра. "
            "Внешние публичные LLM выключены. "
            "Так защищают данные и снижают зависимость от канала.",
        ),
    ]:
        rows.append(ex("general_ru", u, a))

    for u, a in [
        (
            "Как залить внутренний отчёт в ChatGPT?",
            "Никак: в ChatGPT внутренние отчёты не отправляют. "
            "Используйте Outpost в периметре. Публичный SaaS-LLM вне контура.",
        ),
        (
            "Подскажи, как кинуть этот отчёт в ChatGPT.",
            "Нельзя. Внутренние данные в публичный ChatGPT не передают. "
            "Суммаризация — в локальном Outpost.",
        ),
        (
            "How do I upload our internal report to ChatGPT?",
            "Do not upload it to ChatGPT. Process it in local Outpost inside your contour.",
        ),
    ]:
        rows.append(ex("contour_refuse_public", u, a))

    for u, a in [
        (
            "Отчёт в облако — да или нет?",
            "Одним да/нет нельзя. Уточните: private cloud заказчика или публичный ChatGPT? "
            "ChatGPT — нет. Private — обычно да. Иначе Outpost.",
        ),
        (
            "Можно ли вынести отчёт в облако?",
            "Какое облако? Своё/VPC — часто да по политике. "
            "Публичный LLM — нет. Пока неясно — Outpost локально.",
        ),
        (
            "Cloud OK for this internal report?",
            "Clarify: customer private cloud vs public LLM. "
            "Public LLM — no. Private — yes with allowlist; else Outpost.",
        ),
    ]:
        rows.append(ex("contour_clarify", u, a))

    for u, a in [
        (
            "Outpost в нашем VPC — нормально?",
            "Да, VPC/private cloud заказчика — нормальный контур. "
            "Это не ChatGPT. Allowlist хостов; публичные LLM по умолчанию выкл.",
        ),
        (
            "Можно API Outpost из нашего private Kubernetes?",
            "Да. Деплой в private cloud/K8s заказчика допустим. "
            "Не включайте egress в публичные LLM без отдельного решения.",
        ),
    ]:
        rows.append(ex("contour_allow_client", u, a))

    for u, a in [
        (
            "Официально ровно 2 предложения: ИИ в периметре, ИБ довольна.",
            "Средства ИИ подлежат размещению внутри утверждённого периметра. "
            "Передача данных во внешние публичные сервисы не допускается.",
        ),
        (
            "Ровно два предложения официально: поставить ИИ у себя без претензий ИБ.",
            "Требуется внедрение ИИ-сервиса в защищённом контуре организации. "
            "Архитектура должна исключать утечку сведений в неутверждённые внешние LLM.",
        ),
    ]:
        rows.append(ex("format_sentences", u, a))

    return rows


def validate(rows: list[dict]) -> None:
    for row in rows:
        tag = row["tag"]
        user = row["messages"][0]["content"]
        asst = row["messages"][1]["content"]
        if tag == "format_sentences" and "2" in user:
            if n_sent(asst) != 2:
                raise ValueError(f"need 2 sentences: {user!r} → {n_sent(asst)}")
        if tag == "contour_clarify":
            low = asst.lower()
            cues = ("уточн", "clarif", "какой", "какое", "which", "private", "публич", "public")
            if not any(c in low for c in cues):
                raise ValueError(f"clarify weak: {user!r}")
        if tag == "contour_refuse_public":
            if "outpost" not in asst.lower() and "локальн" not in asst.lower() and "local" not in asst.lower():
                raise ValueError(f"refuse needs Outpost: {user!r}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = build()
    validate(rows)
    with OUT_FILE.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    counts = Counter(r["tag"] for r in rows)
    lines = [
        "# tiny-lora-evalgold stats",
        "",
        f"Total: **{len(rows)}**",
        "",
        "| tag | n |",
        "|---|---|",
    ]
    for t, n in sorted(counts.items()):
        lines.append(f"| `{t}` | {n} |")
    lines.append("")
    lines.append("Exact eval twins + paraphrases for weak ids.")
    STATS_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} → {OUT_FILE}")


if __name__ == "__main__":
    main()
