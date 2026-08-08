from __future__ import annotations

import pytest

from closed_sandbox.manifest import ManifestError, load_project, validate_project


def test_validate_defaults() -> None:
    project = {
        "project": {"id": "x", "domain": "snn_lif"},
    }
    validate_project(project)
    assert project["sandbox"]["seed"] == 42
    assert project["contour"]["provider"] == "local"


def test_missing_project_table() -> None:
    with pytest.raises(ManifestError):
        validate_project({})


def test_load_example() -> None:
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / "examples" / "anomaly_v0" / "project.toml"
    data = load_project(path)
    assert data["network"]["kind"] == "snn_lif"
