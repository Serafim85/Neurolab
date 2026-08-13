"""Local web UI for Closed Sandbox (CS-P03 Run, CS-P04 Diff, CS-P05 Ask).

Host choice: neurolab `sandbox/ui/` (NL-ADR-018). Stdlib only.
"""

from __future__ import annotations

import copy
import json
import mimetypes
import threading
import tomllib
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from closed_sandbox.contour_ask import AskError, ask
from closed_sandbox.engine import EngineError, run_project, validate_loaded_project
from closed_sandbox.manifest import ManifestError, load_project
from closed_sandbox.report import (
    diff_metrics,
    load_metrics_json,
    write_json,
    write_markdown,
)

# sandbox/ (package lives in sandbox/src/closed_sandbox/)
SANDBOX_ROOT = Path(__file__).resolve().parents[2]
UI_ROOT = SANDBOX_ROOT / "ui"
DEFAULT_PROJECT = SANDBOX_ROOT / "examples" / "anomaly_v0" / "project.toml"

# Overview copies these from metrics.json when present (NL-ADR-025 / leftover L).
OVERVIEW_METRIC_KEYS = (
    "f1",
    "accuracy",
    "fit_score",
    "chip_fit_score",
    "spike_count",
    "synops",
    "latency_proxy_ms",
)

# Shared last-run artifacts for export (one session process).
_lock = threading.Lock()
_last: dict[str, Any] = {
    "metrics": None,
    "report_md": None,
    "project_path": None,
    "out_dir": None,
}


class UiError(RuntimeError):
    """Bad request or path policy."""


def _resolve_under_sandbox(raw: str | None, *, label: str) -> Path:
    if not raw or not str(raw).strip():
        raise UiError(f"{label} path required")
    candidate = Path(str(raw).strip()).expanduser()
    if not candidate.is_absolute():
        candidate = SANDBOX_ROOT / candidate
    path = candidate.resolve()
    if not path.is_file():
        raise UiError(f"{label} not found: {path}")
    try:
        path.relative_to(SANDBOX_ROOT.resolve())
    except ValueError as exc:
        raise UiError(
            f"{label} must be under {SANDBOX_ROOT} (got {path})"
        ) from exc
    return path


def _diff(a_raw: str | None, b_raw: str | None) -> dict[str, Any]:
    path_a = _resolve_under_sandbox(a_raw, label="a")
    path_b = _resolve_under_sandbox(b_raw, label="b")
    a = load_metrics_json(path_a)
    b = load_metrics_json(path_b)
    result = diff_metrics(a, b)
    return {
        "ok": True,
        "a": str(path_a),
        "b": str(path_b),
        "diff": result,
        "n_changed": result["n_changed"],
    }


def _ask_ui(
    *,
    project_raw: str | None,
    metrics_raw: str | None,
    question: str | None,
    provider_override: str | None,
) -> dict[str, Any]:
    if not question or not str(question).strip():
        raise UiError("question required")
    project_path = _resolve_project(project_raw)
    project = load_project(str(project_path))
    project = copy.deepcopy(project)
    contour = dict(project.get("contour") or {})
    if provider_override:
        provider = str(provider_override).lower().strip()
        if provider not in ("local", "public"):
            raise UiError("provider must be local|public")
        contour["provider"] = provider
        project["contour"] = contour
    if metrics_raw and str(metrics_raw).strip():
        metrics_path = _resolve_under_sandbox(metrics_raw, label="metrics")
    else:
        metrics_path = Path(project["_project_dir"]) / "out" / "metrics.json"
        if not metrics_path.is_file():
            raise UiError(
                f"metrics not found: {metrics_path}. Run a project first or pass metrics path."
            )
    metrics = load_metrics_json(metrics_path)
    provider = str(project.get("contour", {}).get("provider", "local")).lower()
    model = str(project.get("contour", {}).get("model", ""))
    raw = ask(project, metrics, str(question).strip())
    warning = None
    answer = raw
    if raw.startswith("WARNING:"):
        first, _, rest = raw.partition("\n")
        warning = first.strip()
        answer = rest.lstrip("\n")
    return {
        "ok": True,
        "provider": provider,
        "model": model,
        "answer": answer,
        "warning": warning,
        "risk_banner": provider == "public",
        "attached": {
            "project": str(project_path),
            "metrics": str(metrics_path),
        },
    }


def _resolve_project(raw: str | None) -> Path:
    if not raw:
        path = DEFAULT_PROJECT
    else:
        candidate = Path(raw).expanduser()
        if not candidate.is_absolute():
            # Relative paths are from sandbox root (not process cwd).
            candidate = SANDBOX_ROOT / candidate
        path = candidate.resolve()
    if not path.is_file():
        raise UiError(f"project.toml not found: {path}")
    # Soft allow: must live under sandbox tree (examples or local labs).
    try:
        path.relative_to(SANDBOX_ROOT.resolve())
    except ValueError as exc:
        raise UiError(
            f"project path must be under {SANDBOX_ROOT} (got {path})"
        ) from exc
    return path


def _run(project_path: Path, seed: int | None, out: Path | None) -> dict[str, Any]:
    project = load_project(str(project_path))
    metrics = run_project(project, seed=seed)
    out_dir = out if out is not None else Path(project["_project_dir"]) / "out"
    metrics_path = out_dir / "metrics.json"
    report_path = out_dir / "report.md"
    write_json(metrics, metrics_path)
    write_markdown(metrics, report_path)
    report_md = report_path.read_text(encoding="utf-8")
    with _lock:
        _last["metrics"] = metrics
        _last["report_md"] = report_md
        _last["project_path"] = str(project_path)
        _last["out_dir"] = str(out_dir)
    return {
        "ok": True,
        "exit_hint": 0 if metrics.get("budget_ok") else 2,
        "metrics": metrics,
        "report_md": report_md,
        "out_dir": str(out_dir),
        "scenarios": list(project.get("sandbox", {}).get("scenarios") or []),
        "project": {
            "id": project["project"]["id"],
            "domain": project["project"]["domain"],
            "path": str(project_path),
        },
    }


def _project_info(project_path: Path) -> dict[str, Any]:
    project = load_project(str(project_path))
    out_dir = Path(project["_project_dir"]) / "out"
    metrics = None
    metrics_path = out_dir / "metrics.json"
    if metrics_path.is_file():
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    contour = project.get("contour") or {}
    return {
        "ok": True,
        "project": {
            "id": project["project"]["id"],
            "name": project["project"].get("name", ""),
            "domain": project["project"]["domain"],
            "path": str(project_path),
        },
        "scenarios": list(project.get("sandbox", {}).get("scenarios") or []),
        "default_seed": int(project.get("sandbox", {}).get("seed", 42)),
        "last_metrics": metrics,
        "out_dir": str(out_dir),
        "contour": {
            "ask_enabled": bool(contour.get("ask_enabled", True)),
            "provider": str(contour.get("provider", "local")).lower(),
            "model": str(contour.get("model", "")),
            "base_url": str(contour.get("base_url", "")),
        },
    }


def _pick_metrics_file(out_dir: Path) -> Path | None:
    if not out_dir.is_dir():
        return None
    direct = out_dir / "metrics.json"
    candidates = list(out_dir.rglob("metrics.json"))
    if not candidates:
        return None
    if direct.is_file():
        # Prefer root out/metrics.json unless a nested file is newer.
        newest = max(candidates, key=lambda p: p.stat().st_mtime)
        return newest if newest.stat().st_mtime >= direct.stat().st_mtime else direct
    return max(candidates, key=lambda p: p.stat().st_mtime)


def _overview_metric_fields(
    project: dict[str, Any] | None,
    metrics: dict[str, Any] | None,
) -> dict[str, Any]:
    """Primary + whatever quality/cost keys the last run actually reported."""
    task = (project or {}).get("task") or {}
    primary = None
    if metrics and metrics.get("metric_primary"):
        primary = metrics["metric_primary"]
    elif task.get("metric_primary"):
        primary = task["metric_primary"]
    out: dict[str, Any] = {"metric_primary": primary}
    keys = list(OVERVIEW_METRIC_KEYS)
    if isinstance(primary, str) and primary and primary not in keys:
        keys.append(primary)
    if metrics:
        for key in keys:
            if key in metrics:
                out[key] = metrics[key]
    return out


def _list_projects() -> dict[str, Any]:
    examples = SANDBOX_ROOT / "examples"
    rows: list[dict[str, Any]] = []
    if examples.is_dir():
        for proj_path in sorted(examples.glob("*/project.toml")):
            try:
                project = load_project(proj_path)
            except (ManifestError, OSError, tomllib.TOMLDecodeError) as exc:
                rows.append(
                    {
                        "id": proj_path.parent.name,
                        "domain": "?",
                        "path": str(proj_path),
                        "rel": str(proj_path.relative_to(SANDBOX_ROOT)),
                        "status": "invalid",
                        "error": str(exc),
                        "metric_primary": None,
                        "budget_ok": None,
                        "last_run": None,
                    }
                )
                continue
            out_dir = Path(project["_project_dir"]) / "out"
            metrics_path = _pick_metrics_file(out_dir)
            metrics = None
            last_run = None
            if metrics_path and metrics_path.is_file():
                metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
                last_run = datetime.fromtimestamp(
                    metrics_path.stat().st_mtime, tz=timezone.utc
                ).strftime("%Y-%m-%d %H:%M")
            budget = metrics.get("budget_ok") if metrics else None
            if metrics is None:
                status = "idle"
            elif budget is False:
                status = "budget"
            else:
                status = "ok"
            row = {
                "id": project["project"]["id"],
                "name": project["project"].get("name", ""),
                "domain": project["project"]["domain"],
                "path": str(proj_path),
                "rel": str(proj_path.relative_to(SANDBOX_ROOT)),
                "status": status,
                "budget_ok": budget,
                "last_run": last_run,
                "metrics_path": str(metrics_path) if metrics_path else None,
            }
            row.update(_overview_metric_fields(project, metrics))
            rows.append(row)
    return {"ok": True, "projects": rows, "n": len(rows)}


def _validate_ui(
    *,
    path_raw: str | None,
    toml_text: str | None,
) -> dict[str, Any]:
    path: Path | None = None
    if path_raw and str(path_raw).strip():
        path = _resolve_project(path_raw)
    if toml_text is not None and str(toml_text).strip() != "":
        try:
            data = tomllib.loads(toml_text)
        except tomllib.TOMLDecodeError as exc:
            raise UiError(f"TOML parse error: {exc}") from exc
        base = path.parent if path is not None else DEFAULT_PROJECT.parent
        data["_project_dir"] = str(base)
        data["_project_path"] = str(path) if path is not None else str(base / "project.toml")
    elif path is not None:
        data = load_project(str(path))
    else:
        raise UiError("provide project path and/or toml text")
    try:
        validate_loaded_project(data)
    except (ManifestError, EngineError) as exc:
        return {
            "ok": False,
            "valid": False,
            "error": str(exc),
            "project": {
                "id": (data.get("project") or {}).get("id"),
                "domain": (data.get("project") or {}).get("domain"),
            },
            "path": str(path) if path else None,
        }
    return {
        "ok": True,
        "valid": True,
        "error": None,
        "project": {
            "id": data["project"]["id"],
            "domain": data["project"]["domain"],
            "name": data["project"].get("name", ""),
        },
        "path": str(path) if path else None,
        "seed": int(data.get("sandbox", {}).get("seed", 42)),
        "form": {
            "n_hidden": (data.get("network") or {}).get("n_hidden"),
            "max_spikes_per_sample": (data.get("budget") or {}).get(
                "max_spikes_per_sample"
            ),
            "seed": (data.get("sandbox") or {}).get("seed", 42),
            "provider": (data.get("contour") or {}).get("provider", "local"),
            "metric_primary": (data.get("task") or {}).get("metric_primary"),
        },
    }


def _read_manifest(path_raw: str | None) -> dict[str, Any]:
    path = _resolve_project(path_raw)
    text = path.read_text(encoding="utf-8")
    info = _validate_ui(path_raw=str(path), toml_text=text)
    return {
        "ok": True,
        "path": str(path),
        "rel": str(path.relative_to(SANDBOX_ROOT)),
        "toml": text,
        "valid": info.get("valid", False),
        "error": info.get("error"),
        "project": info.get("project"),
        "form": info.get("form"),
        "seed": info.get("seed"),
    }


def _save_manifest(path_raw: str | None, toml_text: str | None) -> dict[str, Any]:
    if toml_text is None:
        raise UiError("toml text required")
    path = _resolve_project(path_raw)
    check = _validate_ui(path_raw=str(path), toml_text=toml_text)
    if not check.get("valid"):
        raise UiError(check.get("error") or "validation failed — not saved")
    path.write_text(toml_text if toml_text.endswith("\n") else toml_text + "\n", encoding="utf-8")
    return {
        "ok": True,
        "saved": True,
        "path": str(path),
        "project": check.get("project"),
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "closed-sandbox-ui/0.1"

    def log_message(self, fmt: str, *args: Any) -> None:
        # Quiet default; CLI can still see stderr if needed.
        pass

    def _send(self, code: int, body: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, code: int, payload: dict[str, Any]) -> None:
        raw = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        self._send(code, raw, "application/json; charset=utf-8")

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        if not raw:
            return {}
        data = json.loads(raw.decode("utf-8"))
        if not isinstance(data, dict):
            raise UiError("JSON body must be an object")
        return data

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        try:
            if path in ("/", "/overview", "/overview.html"):
                return self._static("overview.html")
            if path in ("/run", "/run.html"):
                return self._static("run.html")
            if path in ("/editor", "/editor.html"):
                return self._static("editor.html")
            if path in ("/diff", "/diff.html"):
                return self._static("diff.html")
            if path in ("/ask", "/ask.html"):
                return self._static("ask.html")
            if path.startswith("/static/"):
                return self._static(path.removeprefix("/static/"))
            if path == "/api/health":
                return self._send_json(
                    200,
                    {
                        "ok": True,
                        "ui": "CS-P01+P02+P03+P04+P05",
                        "screens": [
                            "CS-P01",
                            "CS-P02",
                            "CS-P03",
                            "CS-P04",
                            "CS-P05",
                        ],
                        "sandbox_root": str(SANDBOX_ROOT),
                    },
                )
            if path == "/api/projects":
                return self._send_json(200, _list_projects())
            if path == "/api/manifest":
                return self._send_json(
                    200, _read_manifest((qs.get("path") or [None])[0])
                )
            if path == "/api/project":
                project_path = _resolve_project((qs.get("path") or [None])[0])
                return self._send_json(200, _project_info(project_path))
            if path == "/api/export/metrics.json":
                with _lock:
                    metrics = _last.get("metrics")
                if not metrics:
                    raise UiError("no run yet — press Run first")
                raw = json.dumps(metrics, indent=2, sort_keys=True).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header(
                    "Content-Disposition", 'attachment; filename="metrics.json"'
                )
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
                return
            if path == "/api/export/report.md":
                with _lock:
                    report = _last.get("report_md")
                if not report:
                    raise UiError("no run yet — press Run first")
                raw = report.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/markdown; charset=utf-8")
                self.send_header(
                    "Content-Disposition", 'attachment; filename="report.md"'
                )
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
                return
            self._send_json(404, {"ok": False, "error": f"not found: {path}"})
        except (UiError, ManifestError, EngineError, json.JSONDecodeError, OSError) as exc:
            self._send_json(400, {"ok": False, "error": str(exc)})

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        try:
            if parsed.path == "/api/diff":
                body = self._read_json()
                return self._send_json(200, _diff(body.get("a"), body.get("b")))
            if parsed.path == "/api/ask":
                body = self._read_json()
                return self._send_json(
                    200,
                    _ask_ui(
                        project_raw=body.get("project"),
                        metrics_raw=body.get("metrics"),
                        question=body.get("question"),
                        provider_override=body.get("provider"),
                    ),
                )
            if parsed.path == "/api/validate":
                body = self._read_json()
                result = _validate_ui(
                    path_raw=body.get("project") or body.get("path"),
                    toml_text=body.get("toml"),
                )
                code = 200 if result.get("valid") else 400
                return self._send_json(code, result)
            if parsed.path == "/api/manifest":
                body = self._read_json()
                return self._send_json(
                    200,
                    _save_manifest(
                        body.get("project") or body.get("path"),
                        body.get("toml"),
                    ),
                )
            if parsed.path != "/api/run":
                return self._send_json(
                    404, {"ok": False, "error": f"not found: {parsed.path}"}
                )
            body = self._read_json()
            project_path = _resolve_project(body.get("project"))
            seed = body.get("seed")
            seed_i = int(seed) if seed is not None else None
            out_raw = body.get("out")
            out_dir = Path(out_raw).expanduser().resolve() if out_raw else None
            if out_dir is not None:
                try:
                    out_dir.relative_to(SANDBOX_ROOT.resolve())
                except ValueError as exc:
                    raise UiError(f"out must be under {SANDBOX_ROOT}") from exc
            result = _run(project_path, seed_i, out_dir)
            self._send_json(200, result)
        except (
            UiError,
            ManifestError,
            EngineError,
            AskError,
            json.JSONDecodeError,
            OSError,
            ValueError,
        ) as exc:
            self._send_json(400, {"ok": False, "error": str(exc)})

    def _static(self, rel: str) -> None:
        # Prevent path escape.
        target = (UI_ROOT / rel).resolve()
        try:
            target.relative_to(UI_ROOT.resolve())
        except ValueError:
            self._send_json(403, {"ok": False, "error": "forbidden"})
            return
        if not target.is_file():
            self._send_json(404, {"ok": False, "error": f"missing static: {rel}"})
            return
        data = target.read_bytes()
        ctype, _ = mimetypes.guess_type(str(target))
        if ctype is None:
            ctype = "application/octet-stream"
        if ctype.startswith("text/") or ctype in (
            "application/javascript",
            "application/json",
        ):
            ctype = f"{ctype}; charset=utf-8"
        self._send(200, data, ctype)


def serve(
    *,
    host: str = "127.0.0.1",
    port: int = 8765,
    open_browser: bool = False,
) -> None:
    if not UI_ROOT.is_dir():
        raise UiError(f"UI root missing: {UI_ROOT}")
    httpd = ThreadingHTTPServer((host, port), Handler)
    url = f"http://{host}:{port}/"
    print(f"closed-sandbox ui · CS-P01…P05 · {url}", flush=True)
    print(f"  overview: {url}", flush=True)
    print(f"  editor:   {url}editor", flush=True)
    print(f"  run:      {url}run", flush=True)
    print(f"  diff:     {url}diff", flush=True)
    print(f"  ask:      {url}ask", flush=True)
    print(f"default project: {DEFAULT_PROJECT}", flush=True)
    if open_browser:
        import webbrowser

        webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped", flush=True)
    finally:
        httpd.server_close()
