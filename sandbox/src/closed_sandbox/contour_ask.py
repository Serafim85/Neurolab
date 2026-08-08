"""Ask assistant via local Outpost or opt-in public OpenAI-compatible API."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any


class AskError(RuntimeError):
    """Ask provider failure."""


def _post_chat(
    *,
    base_url: str,
    model: str,
    api_key: str | None,
    messages: list[dict[str, str]],
    timeout_s: float = 120.0,
) -> str:
    url = base_url.rstrip("/") + "/chat/completions"
    body = json.dumps(
        {
            "model": model,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 512,
        }
    ).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise AskError(f"HTTP {exc.code} from {url}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise AskError(
            f"cannot reach ask provider at {url}: {exc.reason}. "
            "Start local Outpost or set provider=public with API key."
        ) from exc

    try:
        return str(payload["choices"][0]["message"]["content"])
    except (KeyError, IndexError, TypeError) as exc:
        raise AskError(f"unexpected response shape: {payload!r}") from exc


def ask(
    project: dict[str, Any],
    metrics: dict[str, Any],
    question: str,
) -> str:
    contour = project.get("contour", {})
    if not contour.get("ask_enabled", True):
        raise AskError("ask is disabled in [contour] (ask_enabled = false)")

    provider = str(contour.get("provider", "local")).lower()
    base_url = str(contour.get("base_url", "http://127.0.0.1:8090/v1"))
    model = str(contour.get("model", "outpost-tiny-hammer"))
    api_key: str | None = None

    if provider == "public":
        env_name = str(contour.get("api_key_env", "CLOSED_SANDBOX_LLM_API_KEY"))
        api_key = os.environ.get(env_name)
        if not api_key:
            raise AskError(
                f"provider=public requires env {env_name}. "
                "Export the key or switch contour.provider to local."
            )
        warning = (
            "WARNING: provider=public — manifest/metrics may leave the machine.\n"
        )
    elif provider == "local":
        warning = ""
    else:
        raise AskError(f"unknown contour.provider: {provider!r} (use local|public)")

    domain = str(project.get("project", {}).get("domain", ""))
    if domain == "synapse_import":
        class_owner = str(metrics.get("class_fix") or "specialist")
        system = (
            "CANONICAL FACTS — do not contradict:\n"
            f"- class_fix = {class_owner} means Synapse (local) repairs class_id on escalate rows.\n"
            "- brain_role = explain_plan means the LLM only explains; the LLM does NOT fix class_id.\n"
            "- escalate_rate = fraction of uncertain rows (~0.07), NOT another SNN and NOT accuracy.\n"
            "- oracle_accuracy = lab ceiling if escalate rows were perfect; NOT a product KPI.\n"
            f"If asked who fixes class_id, answer exactly: Synapse {class_owner} (not the LLM).\n"
            "Be concise; cite metrics; do not invent chip Joules."
        )
    elif domain == "neuro_chip":
        system = (
            "CANONICAL FACTS — do not contradict:\n"
            "- domain neuro_chip = rough map/estimate onto a named target profile.\n"
            "- chip_area_mm2 / chip_power_mw / chip_energy_pj_per_sample are LAB PROXIES, "
            "not measured silicon and not PDK results.\n"
            "- chip_luts_est / chip_bram18_est / chip_dsp_est (FPGA targets) are fabric proxies, "
            "not Vivado/Quartus utilization reports.\n"
            "- chip_export.json is a hook only — no automatic bitstream.\n"
            "- chip_fit_score = headroom vs budget caps; budget_ok is the hard gate.\n"
            "- Do not invent vendor part numbers, process nodes, or GDSII claims.\n"
            "Be concise; cite reported chip_* metrics only."
        )
    elif domain == "biocompute":
        system = (
            "CANONICAL FACTS — do not contradict:\n"
            "- domain biocompute = DIGITAL toy GRN / circuit sim only.\n"
            "- No wet-lab, culture, organoids, or measured ATP Joules.\n"
            "- bio_resource_proxy counts simulation ops, not biochemistry energy.\n"
            "- spike_count is 0 by design (not an SNN domain).\n"
            "Be concise; cite bio_* and accuracy/f1 from the report."
        )
    elif domain == "biosignal":
        system = (
            "CANONICAL FACTS — do not contradict:\n"
            "- domain biosignal = SYNTHETIC ECG/EEG-like traces only.\n"
            "- Not a medical device; not clinical diagnosis; not real patient data.\n"
            "- threshold encode → spike features → small LIF classifier.\n"
            "Be concise; cite signal_* and f1/accuracy from the report."
        )
    elif domain == "hybrid":
        system = (
            "CANONICAL FACTS — do not contradict:\n"
            "- domain hybrid = COMPOSITION: synthetic bio front → silicon SNN backend.\n"
            "- Front is digital synthetic signal (not wet-lab / not clinical).\n"
            "- Backend is LIF sim (snn_lif), not a vendor chip runtime.\n"
            "- Cite hybrid_pipeline / hybrid_front / hybrid_backend from metrics.\n"
            "Be concise; do not invent ATP Joules or medical claims."
        )
    else:
        system = (
            "You are a closed-sandbox engineering assistant. "
            "Help interpret SNN sandbox metrics and suggest safe manifest tweaks. "
            "Be concise and concrete."
        )
    user = (
        f"Question:\n{question}\n\n"
        f"Project:\n{json.dumps(project.get('project', {}), indent=2)}\n\n"
        f"Network:\n{json.dumps(project.get('network', {}), indent=2)}\n\n"
        f"Metrics:\n{json.dumps(metrics, indent=2)}\n"
    )
    answer = _post_chat(
        base_url=base_url,
        model=model,
        api_key=api_key,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return warning + answer
