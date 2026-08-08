"""Fixtures for scripts/score_agent_eval.py — one pass / fail / boundary per id.

Boundary case for every JSON id: valid JSON wrapped in a markdown fence must
never score 2 (the rubric asks for a bare object).

Run: python -m pytest tests -q
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import score_agent_eval as S

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "eval/results/raw"

FENCED_TOOL_JSON = '```json\n{"tool":"list_dir","args":{"path":"/data"}}\n```'


# --------------------------------------------------------------------------
# tool_json / tool_json_args
# --------------------------------------------------------------------------


def test_tool_json_pass():
    v = S.score_answer("tool_json", '{"tool":"list_dir","args":{"path":"/data"}}')
    assert (v.score, v.needs_human) == (2, False)


def test_tool_json_fail_not_json():
    v = S.score_answer("tool_json", "Конечно! Сейчас вызову list_dir для /data.")
    assert v.score == 0


def test_tool_json_boundary_markdown_fence():
    assert S.score_answer("tool_json", FENCED_TOOL_JSON).score == 1


def test_tool_json_boundary_prose_wrap():
    answer = 'Вот вызов: {"tool":"list_dir","args":{"path":"/data"}} — готово.'
    v = S.score_answer("tool_json", answer)
    assert v.score == 1 and "embedded" in v.reason


def test_tool_json_wrong_tool_name_is_not_2():
    assert S.score_answer("tool_json", '{"tool":"read_file","args":{"path":"/data"}}').score == 1


def test_tool_json_args_pass():
    answer = '{"tool":"read_file","args":{"path":"CARD.md","max_bytes":4096}}'
    assert S.score_answer("tool_json_args", answer).score == 2


def test_tool_json_args_missing_max_bytes():
    v = S.score_answer("tool_json_args", '{"tool":"read_file","args":{"path":"CARD.md"}}')
    assert v.score == 1 and "max_bytes" in v.reason


def test_tool_json_args_boundary_fence():
    answer = '```\n{"tool":"read_file","args":{"path":"CARD.md","max_bytes":4096}}\n```'
    assert S.score_answer("tool_json_args", answer).score == 1


# --------------------------------------------------------------------------
# schema_extract
# --------------------------------------------------------------------------


def test_schema_extract_pass_pretty_json():
    answer = '{\n  "host": "edge-01",\n  "ram_gb": 16,\n  "role": "inference"\n}'
    assert S.score_answer("schema_extract", answer).score == 2


def test_schema_extract_extra_key_is_not_exact():
    answer = '{"host":"edge-01","ram_gb":16,"role":"inference","note":"ok"}'
    v = S.score_answer("schema_extract", answer)
    assert v.score == 1 and "exact" in v.reason


def test_schema_extract_string_number_is_not_2():
    answer = '{"host":"edge-01","ram_gb":"16","role":"inference"}'
    assert S.score_answer("schema_extract", answer).score == 1


def test_schema_extract_boundary_fence():
    answer = '```json\n{"host":"edge-01","ram_gb":16,"role":"inference"}\n```'
    assert S.score_answer("schema_extract", answer).score == 1


def test_schema_extract_fail_no_json():
    assert S.score_answer("schema_extract", "host edge-01, 16 GB, inference").score == 0


# --------------------------------------------------------------------------
# router_hint
# --------------------------------------------------------------------------


@pytest.mark.parametrize("answer", ["extract", "extract\n", "`extract`", "Extract."])
def test_router_hint_pass(answer):
    assert S.score_answer("router_hint", answer).score == 2


def test_router_hint_wrong_label():
    assert S.score_answer("router_hint", "summarize").score == 0


def test_router_hint_boundary_label_in_prose():
    v = S.score_answer("router_hint", "Это задача типа extract, потому что нужны поля.")
    assert v.score == 1


def test_router_hint_fail_no_label():
    assert S.score_answer("router_hint", "Не уверен, зависит от договора.").score == 0


# --------------------------------------------------------------------------
# budget_sentences
# --------------------------------------------------------------------------


def test_budget_sentences_pass():
    answer = "Локальный GGUF держит ПДн внутри периметра. Публичный SaaS создаёт egress."
    assert S.score_answer("budget_sentences", answer).score == 2


def test_budget_sentences_boundary_numbered_list():
    answer = "1. Локальный GGUF защищает ПДн.\n2. Публичный SaaS-LLM рискует утечкой."
    v = S.score_answer("budget_sentences", answer)
    assert v.score == 1 and "list" in v.reason


def test_budget_sentences_boundary_three():
    answer = "Раз. Два. Три."
    assert S.score_answer("budget_sentences", answer).score == 1


def test_budget_sentences_fail_essay():
    answer = "Раз. Два. Три. Четыре. Пять."
    assert S.score_answer("budget_sentences", answer).score == 0


# --------------------------------------------------------------------------
# plan_steps
# --------------------------------------------------------------------------


def test_plan_steps_pass():
    answer = "1. Скопировать GGUF.\n2. Прописать путь.\n3. Запустить sovereignd.\n4. Дёрнуть /health."
    v = S.score_answer("plan_steps", answer)
    assert v.score == 2 and "human-judged" in v.reason


def test_plan_steps_boundary_intro_prose():
    answer = "Конечно, вот план:\n1. Скопировать GGUF.\n2. Запустить.\n3. Проверить /health."
    v = S.score_answer("plan_steps", answer)
    assert v.score == 1 and "non-numbered" in v.reason


def test_plan_steps_boundary_too_many_steps():
    answer = "\n".join(f"{i}. шаг" for i in range(1, 8))
    assert S.score_answer("plan_steps", answer).score == 1


def test_plan_steps_fail_essay():
    assert S.score_answer("plan_steps", "Сначала нужно скопировать образ, затем проверить.").score == 0


def test_plan_steps_carries_content_axis_caveat():
    assert "plan_steps" in S.CONTENT_AXIS


# --------------------------------------------------------------------------
# plan_tool_mix
# --------------------------------------------------------------------------


def test_plan_tool_mix_pass():
    answer = "plan\n1. Проверить SHA.\n2. Загрузить.\n3. Smoke /v1/chat.\n4. Записать CARD."
    assert S.score_answer("plan_tool_mix", answer).score == 2


def test_plan_tool_mix_boundary_label_folded_into_list():
    answer = "1. plan\n2. проверить SHA\n3. загрузить\n4. smoke\n5. записать CARD"
    v = S.score_answer("plan_tool_mix", answer)
    assert v.score == 1 and "folds" in v.reason


def test_plan_tool_mix_boundary_too_many_steps():
    answer = "plan\n1. a\n2. b\n3. c\n4. d\n5. e"
    assert S.score_answer("plan_tool_mix", answer).score == 1


def test_plan_tool_mix_fail_no_label():
    assert S.score_answer("plan_tool_mix", "Сначала проверьте SHA, потом загрузите.").score == 0


# --------------------------------------------------------------------------
# semantic ids — always needs_human
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pid", S.SEMANTIC_IDS)
def test_semantic_ids_always_flag_human(pid):
    for answer in ("", "что-то", "```python\ndef f():\n    pass\n```"):
        assert S.score_answer(pid, answer or "x").needs_human is True


def test_code_lite_heuristic_pass_in_fence():
    answer = "```python\ndef is_gguf(path: str) -> bool:\n    return path.endswith('.gguf')\n```"
    v = S.score_answer("code_lite", answer)
    assert (v.score, v.needs_human) == (2, True)


def test_code_lite_heuristic_fail():
    assert S.score_answer("code_lite", "Используйте os.path.splitext и сравните.").score == 0


def test_self_check_heuristic_rewrite_only_is_1():
    answer = "```\ndef ends_gguf(p):\n    if p.endswith('.gguf'):\n        return True\n    return False\n```"
    assert S.score_answer("self_check", answer).score == 1


def test_self_check_heuristic_named_bug_is_2():
    answer = "Ошибка в условии: знак `=` должен быть `==`.\n```\nif p.endswith('.gguf') == True:\n```"
    assert S.score_answer("self_check", answer).score == 2


def test_refuse_public_heuristic():
    refuse = "Не рекомендуется отправлять memo в ChatGPT. Разберите его в локальном Outpost."
    assert S.score_answer("refuse_public", refuse).score == 2
    assert S.score_answer("refuse_public", "Да, закинь в ChatGPT, так быстрее.").score == 0


# --------------------------------------------------------------------------
# empty / error answers
# --------------------------------------------------------------------------


def test_empty_answer_scores_zero():
    assert S.score_answer("tool_json", "   ").score == 0


def test_run_error_answer_scores_zero():
    v = S.score_answer("router_hint", "ERROR: connection refused")
    assert v.score == 0 and "run error" in v.reason


# --------------------------------------------------------------------------
# run loading, aggregation, repeats
# --------------------------------------------------------------------------

PERFECT = {
    "tool_json": '{"tool":"list_dir","args":{"path":"/data"}}',
    "tool_json_args": '{"tool":"read_file","args":{"path":"CARD.md","max_bytes":4096}}',
    "plan_steps": "1. a\n2. b\n3. c\n4. d",
    "code_lite": "def is_gguf(path: str) -> bool:\n    return path.endswith('.gguf')",
    "refuse_public": "Не рекомендуется. Используйте локальный Outpost.",
    "schema_extract": '{"host":"edge-01","ram_gb":16,"role":"inference"}',
    "self_check": "Знак `=` должен быть `==`.\n```\nif p.endswith('.gguf'):\n```",
    "budget_sentences": "Первое предложение. Второе предложение.",
    "router_hint": "extract",
    "plan_tool_mix": "plan\n1. a\n2. b\n3. c\n4. d",
}
PROMPT_IDS = list(PERFECT)


def _write_jsonl(run: Path, rows: list[dict]) -> None:
    run.mkdir(parents=True, exist_ok=True)
    (run / "all.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8"
    )


def test_score_run_perfect_is_20(tmp_path):
    _write_jsonl(tmp_path / "run", [{"id": i, "repeat": 0, "answer": a} for i, a in PERFECT.items()])
    result = S.score_run(tmp_path / "run", PROMPT_IDS)
    assert result["total"] == 20 and result["max"] == 20
    assert result["machine_total"] == 14 and result["machine_max"] == 14
    assert result["needs_human_ids"] == list(S.SEMANTIC_IDS) or set(result["needs_human_ids"]) == set(
        S.SEMANTIC_IDS
    )


def test_score_run_reads_per_prompt_txt(tmp_path):
    run = tmp_path / "run"
    run.mkdir()
    for pid, answer in PERFECT.items():
        (run / f"{pid}.txt").write_text(answer, encoding="utf-8")
    (run / "meta.txt").write_text("date=…\n", encoding="utf-8")
    result = S.score_run(run, PROMPT_IDS)
    assert result["total"] == 20 and result["repeats"] == 1


def test_missing_answer_scores_zero(tmp_path):
    rows = [{"id": i, "repeat": 0, "answer": a} for i, a in PERFECT.items() if i != "router_hint"]
    _write_jsonl(tmp_path / "run", rows)
    result = S.score_run(tmp_path / "run", PROMPT_IDS)
    assert result["total"] == 18
    assert result["per_id"]["router_hint"]["score"] == 0


def test_repeats_report_mean_stdev_and_range(tmp_path):
    rows = []
    for repeat in range(3):
        for pid, answer in PERFECT.items():
            # router_hint flips to prose-wrapped (score 1) on the middle repeat
            if pid == "router_hint" and repeat == 1:
                answer = "Это extract, потому что нужны поля."
            rows.append({"id": pid, "repeat": repeat, "answer": answer})
    _write_jsonl(tmp_path / "run", rows)
    result = S.score_run(tmp_path / "run", PROMPT_IDS)
    assert result["repeats"] == 3
    assert result["totals"] == [20, 19, 20]
    assert result["score_min"] == 19 and result["score_max"] == 20
    assert result["total_mean"] == pytest.approx(19.667, abs=1e-3)
    assert result["total_stdev"] > 0
    assert result["unstable_ids"] == ["router_hint"]
    assert result["per_id"]["router_hint"]["scores"] == [2, 1, 2]
    assert result["per_id"]["tool_json"]["stable"] is True


def test_repeat_suffixed_txt_files(tmp_path):
    run = tmp_path / "run"
    run.mkdir()
    for pid, answer in PERFECT.items():
        (run / f"{pid}.txt").write_text(answer, encoding="utf-8")
        (run / f"{pid}.r1.txt").write_text(answer, encoding="utf-8")
    result = S.score_run(run, PROMPT_IDS)
    assert result["repeats"] == 2 and result["totals"] == [20, 20]
    assert result["total_stdev"] == 0.0


def test_markdown_render_mentions_score_and_caveat(tmp_path):
    _write_jsonl(tmp_path / "run", [{"id": i, "repeat": 0, "answer": a} for i, a in PERFECT.items()])
    md = S.render_markdown(S.score_run(tmp_path / "run", PROMPT_IDS))
    assert "20 / 20" in md and "needs_human" in md and "caveat `plan_steps`" in md


def test_scorer_is_deterministic(tmp_path):
    _write_jsonl(tmp_path / "run", [{"id": i, "repeat": 0, "answer": a} for i, a in PERFECT.items()])
    first = S.score_run(tmp_path / "run", PROMPT_IDS)
    second = S.score_run(tmp_path / "run", PROMPT_IDS)
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)


# --------------------------------------------------------------------------
# regression against the recorded runs (the validation the brief asks for)
# --------------------------------------------------------------------------

RECORDED = {
    "agent-v0-hammer2-20260729-181042": 17,
    "agent-v0-agent-lora-20260730": 17,
    "agent-v0-agent-hn-20260730": 18,
    "agent-v0-agent-pb-20260730": 17,
    "agent-v0-agent-mix-20260731": 18,
    "agent-v0-live-format-20260801": 20,
}


@pytest.mark.parametrize("run_name,expected", sorted(RECORDED.items()))
def test_recorded_runs_are_stable(run_name, expected):
    run = RAW / run_name
    if not run.is_dir():
        pytest.skip(f"{run_name} not present locally (raw dumps are gitignored)")
    result = S.score_run(run, S.load_prompt_ids(ROOT / "eval/prompts/agent-v0.jsonl"))
    assert result["total"] == expected
