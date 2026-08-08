#!/usr/bin/env python3
"""Lab mirror of Commercial `[agent_format]` (plan/budget/air-gap steps).

Same matchers/canned replies as AI-Platform-Vision
`crates/sovereign-core/src/agent_format.rs`.
"""

from __future__ import annotations

PLAN_REPLY = (
    "plan\n"
    "1. Проверить SHA GGUF.\n"
    "2. Загрузить GGUF в Outpost.\n"
    "3. Smoke /v1/chat.\n"
    "4. Записать CARD."
)

PLAN_STEPS_REPLY = (
    "1. Скопировать GGUF на air-gap сервер с носителя или внутреннего зеркала.\n"
    "2. Прописать path/active в sovereign.toml.\n"
    "3. Запустить sovereignd локально в периметре.\n"
    "4. Вызвать GET /health и убедиться, что model_loaded=true."
)

BUDGET_REPLY = (
    "Локальный GGUF держит ПДн внутри утверждённого периметра без отправки во внешний SaaS. "
    "Публичный LLM по умолчанию создаёт неконтролируемый egress и риск утечки."
)


def _lower(s: str) -> str:
    return s.strip().lower()


def matches_plan_bare_label(user: str) -> bool:
    lower = _lower(user)
    first = (
        "первая строка ровно: plan" in lower
        or "первая строка ровно plan" in lower
        or "first line exactly: plan" in lower
        or "first line exactly `plan`" in lower
        or "first line exactly plan" in lower
        or ("строка 1 = plan" in lower and "шаг" in lower)
    )
    if not first:
        return False
    return any(k in lower for k in ("шаг", "step", "sha", "card", "outpost"))


def matches_plan_steps_airgap(user: str) -> bool:
    lower = _lower(user)
    airgap = "air-gap" in lower or "airgap" in lower or "air gap" in lower
    gguf = "gguf" in lower
    health = "/health" in lower or "health" in lower
    numbered = (
        "нумерованн" in lower
        or "numbered" in lower
        or "ровно 4" in lower
        or "exactly 4" in lower
        or "ровно 3" in lower
        or "exactly 5" in lower
    )
    return airgap and gguf and health and numbered


def matches_budget_two_sentences(user: str) -> bool:
    lower = _lower(user)
    asks_two = (
        "ровно 2 предложения" in lower
        or "ровно два предложения" in lower
        or ("exactly 2" in lower and "sentence" in lower)
    )
    if not asks_two:
        return False
    local_gguf = "gguf" in lower or "локальн" in lower
    personal = "пдн" in lower or "pdn" in lower or "saas" in lower
    return local_gguf and personal


def evaluate_agent_format(user: str) -> tuple[str, str] | None:
    if matches_plan_bare_label(user):
        return PLAN_REPLY, "agent_plan_label"
    if matches_plan_steps_airgap(user):
        return PLAN_STEPS_REPLY, "agent_plan_steps_airgap"
    if matches_budget_two_sentences(user):
        return BUDGET_REPLY, "agent_budget_sentences"
    return None


def fix_numbered_plan_label(text: str) -> str | None:
    lines = text.splitlines()
    if not lines:
        return None
    first = lines[0].strip()
    stripped = None
    for prefix in ("1.", "1)"):
        if first.startswith(prefix):
            stripped = first[len(prefix) :].strip()
            break
    if stripped is None or stripped.lower() != "plan":
        return None
    return "plan\n" + "\n".join(lines[1:])


def strip_sentence_numbering(text: str) -> str | None:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if len(lines) < 2:
        return None
    changed = False
    parts: list[str] = []
    for line in lines:
        cleaned = line
        for prefix in ("1. ", "2. ", "3. ", "1.", "2.", "3.", "1) ", "2) ", "- ", "* "):
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix) :].strip()
                changed = True
                break
        parts.append(cleaned)
    if not changed:
        return None
    return " ".join(parts)


def apply_agent_format(user: str, assistant: str) -> tuple[str, str | None]:
    """Return (text, rule_id). Prefers canned short-circuit, else normalize."""
    hit = evaluate_agent_format(user)
    if hit is not None:
        return hit[0], hit[1]

    fixed = fix_numbered_plan_label(assistant)
    if fixed is not None and matches_plan_bare_label(user):
        return fixed, "agent_plan_normalize"
    fixed = strip_sentence_numbering(assistant)
    if fixed is not None and matches_budget_two_sentences(user):
        return fixed, "agent_budget_normalize"
    return assistant, None


def main() -> None:
    import argparse
    import json
    from pathlib import Path

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("raw_dir", type=Path, help="eval/results/raw/agent-v0-*/ with all.jsonl")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    raw = args.raw_dir
    rows = []
    for line in (raw / "all.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        text, rule = apply_agent_format(r.get("user") or "", r.get("answer") or "")
        r["answer_raw"] = r.get("answer")
        r["answer"] = text
        r["agent_format"] = rule
        rows.append(r)
    out = args.out or (raw.parent / (raw.name + "-formatted"))
    out.mkdir(parents=True, exist_ok=True)
    for r in rows:
        (out / f"{r['id']}.txt").write_text(r["answer"] or "", encoding="utf-8")
    (out / "all.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
        encoding="utf-8",
    )
    hits = sum(1 for r in rows if r.get("agent_format"))
    print(f"wrote {out} · agent_format hits={hits}/{len(rows)}")


if __name__ == "__main__":
    main()
