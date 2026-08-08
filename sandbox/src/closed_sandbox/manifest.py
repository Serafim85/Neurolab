"""Load and validate Closed Sandbox project manifests (TOML)."""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any


class ManifestError(ValueError):
    """Invalid or incomplete project.toml."""


def load_project(path: Path | str) -> dict[str, Any]:
    """Load TOML project and resolve relative dataset paths against project dir."""
    project_path = Path(path).resolve()
    if not project_path.is_file():
        raise ManifestError(f"project file not found: {project_path}")

    with project_path.open("rb") as f:
        data = tomllib.load(f)

    data["_project_dir"] = str(project_path.parent)
    data["_project_path"] = str(project_path)
    validate_project(data)
    return data


def validate_project(project: dict[str, Any]) -> None:
    """Validate common fields; domain-specific checks happen in the plugin."""
    if "project" not in project:
        raise ManifestError("missing [project] table")
    proj = project["project"]
    for key in ("id", "domain"):
        if key not in proj:
            raise ManifestError(f"[project] missing required key: {key}")

    domain = proj["domain"]
    if not isinstance(domain, str) or not domain:
        raise ManifestError("[project].domain must be a non-empty string")

    if "sandbox" not in project:
        project["sandbox"] = {}
    sandbox = project["sandbox"]
    if "seed" not in sandbox:
        sandbox["seed"] = 42
    if "scenarios" not in sandbox:
        sandbox["scenarios"] = ["nominal", "anomaly", "noise"]

    if "contour" not in project:
        project["contour"] = {}
    contour = project["contour"]
    contour.setdefault("ask_enabled", True)
    contour.setdefault("provider", "local")
    contour.setdefault("base_url", "http://127.0.0.1:8090/v1")
    contour.setdefault("model", "outpost-tiny-hammer")
    contour.setdefault("api_key_env", "CLOSED_SANDBOX_LLM_API_KEY")
