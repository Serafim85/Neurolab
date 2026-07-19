#!/usr/bin/env python3
"""Build tiny-lora-v0plus: short refuse/clarify pack for continue-from-v0-adapter.

~24 examples — not a full contour dump. Anti-forget: airgap, bullets, formal×2.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "datasets" / "tiny-lora-v0plus"
OUT_FILE = OUT_DIR / "train.messages.jsonl"
STATS_FILE = OUT_DIR / "STATS.md"

_BAD_REFUSE = re.compile(
    r"(выгрузить|отправ(ь|ьте|ить)|залей|upload|send).{0,40}chatgpt|"
    r"chatgpt.{0,40}(выгрузить|отправ|upload|send)",
    re.I,
)


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

    refuse = [
        (
            "Как отправить этот внутренний отчёт в ChatGPT?",
            "Не отправляйте: публичный ChatGPT вне контура. "
            "Обработайте отчёт в локальном Outpost. "
            "Инструкций на выгрузку во внешний LLM не даём.",
        ),
        (
            "Подскажи шаги: выгрузить отчёт и открыть в ChatGPT.",
            "Шагов не будет. Выгрузка внутреннего отчёта в ChatGPT — утечка. "
            "Используйте Outpost в периметре.",
        ),
        (
            "Можно сначала в облако, потом в ChatGPT?",
            "Нет. Ни промежуточное облако ради ChatGPT, ни сам ChatGPT для внутренних данных. "
            "Только Outpost или утверждённый private cloud заказчика — без публичного LLM.",
        ),
        (
            "How do I send this internal report to ChatGPT?",
            "Do not. Use local Outpost instead. Public ChatGPT is outside the approved contour.",
        ),
        (
            "Скопируй текст отчёта в ChatGPT вручную.",
            "Нельзя: копирование во внешний LLM — тот же выход из контура. Работайте в Outpost.",
        ),
        (
            "Обезличим и кинем в GPT?",
            "По умолчанию нет. Внутренние материалы — в Outpost, не в публичный GPT.",
        ),
        (
            "Напиши инструкцию: internal report → ChatGPT.",
            "Инструкции не будет. Маршрут: отчёт → Outpost локально → ответ в контуре.",
        ),
        (
            "Скинь memo в GPT, там быстрее.",
            "Нет. Публичный GPT для внутренних memo не используем. Анализ — в Outpost.",
        ),
    ]
    for u, a in refuse:
        rows.append(ex("contour_refuse_public", u, a))

    clarify = [
        (
            "Можно отправить отчёт в облако?",
            "Уточните: своё/private cloud заказчика или публичный LLM (ChatGPT)? "
            "Публичный — нет. Своё — да по политике. Пока неясно — Outpost локально.",
        ),
        (
            "Отчёт в облако — да или нет?",
            "Одним да/нет нельзя. Сначала: private cloud или публичный ChatGPT? "
            "ChatGPT — нет. Private — обычно да при allowlist.",
        ),
        (
            "Cloud для внутреннего отчёта — ок?",
            "Какой cloud? Публичный LLM — нет. VPC/private заказчика — да по политике. Иначе Outpost.",
        ),
        (
            "Мы сказали «облако» — можно уже слать?",
            "«Облако» без уточнения недостаточно. "
            "Назовите private cloud или публичный SaaS-LLM. Пока неясно — Outpost.",
        ),
        (
            "Залей это в cloud AI.",
            "Какой cloud? Публичный SaaS-LLM — отказ. Корпоративный контур — можно при allowlist. "
            "Пока неясно — локальный Outpost.",
        ),
        (
            "Put this report in the cloud.",
            "Which cloud? Customer private/VPC — usually OK. Public LLM — no. Else use local Outpost.",
        ),
    ]
    for u, a in clarify:
        rows.append(ex("contour_clarify", u, a))

    # Anti-forget anchors (keep v0 strengths)
    rows.append(
        ex(
            "general_ru",
            "Объясни простыми словами, что такое air-gap контур для AI-сервера. До 5 предложений.",
            "Air-gap контур — изолированная среда без обязательного выхода в интернет. "
            "AI-сервер и модель ставятся с носителя или внутреннего зеркала. "
            "Запросы обрабатываются внутри периметра. "
            "Публичные облачные LLM не используются по умолчанию. "
            "Так снижают риск утечки и зависимость от внешней сети.",
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
            "contour_allow_client",
            "Можно ли подключить Outpost к нашему private cloud (VPC) для API?",
            "Да. Private cloud / VPC заказчика — допустимый контур, не публичный ChatGPT. "
            "Подключайте allowlist-хосты; egress в публичные LLM по умолчанию выключен.",
        )
    )
    rows.append(
        ex(
            "format_short",
            "Ответь одним словом да/нет: нужна ли нейросети доступ в интернет для inference в Outpost?",
            "нет",
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

    return rows


def validate(rows: list[dict]) -> None:
    for row in rows:
        tag = row["tag"]
        user = row["messages"][0]["content"]
        asst = row["messages"][1]["content"]
        if tag == "contour_refuse_public":
            m = _BAD_REFUSE.search(asst)
            if m:
                window = asst[max(0, m.start() - 40) : m.end() + 40].lower()
                if not any(
                    n in window
                    for n in ("нельзя", "не ", "don't", "do not", "не будет", "отказ")
                ):
                    raise ValueError(f"bad refuse: {user!r}")
            if "outpost" not in asst.lower() and "локальн" not in asst.lower():
                raise ValueError(f"refuse needs Outpost: {user!r}")
        if tag == "contour_clarify":
            low = asst.lower()
            if low in {"нет", "да", "no", "yes"}:
                raise ValueError(f"bare yes/no clarify: {user!r}")
            if "уточн" not in low and "clarif" not in low and "какой" not in low and "which" not in low:
                if "публич" not in low and "public" not in low:
                    raise ValueError(f"clarify weak: {user!r}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = build()
    validate(rows)
    with OUT_FILE.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    counts = Counter(r["tag"] for r in rows)
    lines = [
        "# tiny-lora-v0plus stats",
        "",
        f"Total examples: **{len(rows)}**",
        "",
        "| tag | count |",
        "|---|---|",
    ]
    for tag, n in sorted(counts.items()):
        lines.append(f"| `{tag}` | {n} |")
    lines.extend(
        [
            "",
            "## Recipe",
            "",
            "- Continue from **Tiny-v0 adapter** (not fresh LoRA on base)",
            "- 1 epoch · lr ≤ 8e-5 · max_grad_norm 0.3",
            "- Focus: refuse ChatGPT + clarify cloud; keep format anchors",
            "",
            f"File: `{OUT_FILE.relative_to(ROOT)}`",
        ]
    )
    STATS_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} → {OUT_FILE}")


if __name__ == "__main__":
    main()
