"""Tests for `langgraph.errors.NodeTimeoutError` node validation."""

from __future__ import annotations

import pytest

from langgraph.errors import NodeTimeoutError


def test_rejects_empty_node() -> None:
    """Empty `node` would produce a malformed error message with an empty node name."""
    with pytest.raises(ValueError, match="`node` must be a non-empty string"):
        NodeTimeoutError("", elapsed=1.0, kind="run", run_timeout=2.0)


def test_rejects_non_string_node() -> None:
    """Non-string `node` would break the `f\"Node '{node}' exceeded ...\"` string interpolation."""
    with pytest.raises(TypeError, match="`node` must be a string"):
        NodeTimeoutError(None, elapsed=1.0, kind="run", run_timeout=2.0)  # type: ignore[arg-type]


def test_accepts_idle_kind() -> None:
    """Valid `node` with `kind='idle'` produces a working error with idle_timeout set."""
    error = NodeTimeoutError("worker", elapsed=1.0, kind="idle", idle_timeout=2.0)
    assert error.node == "worker"
    assert error.kind == "idle"
    assert error.timeout == 2.0
    assert error.idle_timeout == 2.0
    assert error.run_timeout is None
    assert "worker" in str(error)
    assert "idle" in str(error)


def test_accepts_run_kind() -> None:
    """Valid `node` with `kind='run'` produces a working error with run_timeout set."""
    error = NodeTimeoutError("worker", elapsed=1.0, kind="run", run_timeout=2.0)
    assert error.node == "worker"
    assert error.kind == "run"
    assert error.timeout == 2.0
    assert error.idle_timeout is None
    assert error.run_timeout == 2.0
    assert "worker" in str(error)
    assert "run" in str(error)
