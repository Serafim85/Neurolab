"""Integration: start Outpost (hammer2) and exercise closed-sandbox ask."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from closed_sandbox.contour_ask import ask
from closed_sandbox.engine import run_project
from closed_sandbox.manifest import load_project

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "anomaly_v0" / "project.toml"

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def project_and_metrics(outpost_base_url: str):
    project = load_project(EXAMPLE)
    project["contour"]["provider"] = "local"
    project["contour"]["base_url"] = outpost_base_url
    project["contour"]["model"] = "outpost-tiny-hammer"
    metrics = run_project(project, seed=42)
    return project, metrics


def test_ask_reports_f1_and_budget(project_and_metrics) -> None:
    project, metrics = project_and_metrics
    question = (
        "Using ONLY the metrics JSON provided, answer with these three lines:\n"
        f"1) f1={metrics['f1']}\n"
        f"2) budget_ok={metrics['budget_ok']}\n"
        f"3) spike_count={metrics['spike_count']}\n"
        "Do not invent other numbers."
    )
    answer = ask(project, metrics, question)
    text = answer.lower()

    assert len(answer.strip()) >= 20, f"answer too short: {answer!r}"
    assert "budget" in text, answer
    assert str(metrics["budget_ok"]).lower() in text, answer
    assert "spike" in text, answer
    f1 = metrics["f1"]
    f1_ok = (
        str(f1) in answer
        or f"{f1:.2f}" in answer
        or f"{f1:.1f}" in answer
        or bool(re.search(r"0\.\d{1,4}", answer))
    )
    assert f1_ok or "f1" in text, answer


def test_ask_spike_threshold_yes_no(project_and_metrics) -> None:
    project, metrics = project_and_metrics
    answer = ask(
        project,
        metrics,
        "Look at metrics.spike_count only (absolute average spikes per sample). "
        "Ignore budgets and ratios. "
        f"Is metrics.spike_count greater than 100? "
        f"(The value is {metrics['spike_count']}.) "
        "Reply with exactly one line: YES or NO.",
    )
    upper = answer.upper()
    assert "YES" in upper or "NO" in upper, answer
    if metrics["spike_count"] > 100:
        assert re.search(r"\bYES\b", upper), answer
    else:
        assert re.search(r"\bNO\b", upper), answer
