"""Tests for `langgraph.errors.NodeCancelledError` node validation."""

from __future__ import annotations

import pytest

from langgraph.errors import NodeCancelledError


def test_rejects_empty_node() -> None:
    """Empty `node` would produce a malformed error message with an empty node name."""
    with pytest.raises(ValueError, match="`node` must be a non-empty string"):
        NodeCancelledError("")


def test_rejects_non_string_node() -> None:
    """Non-string `node` would break the `f\"Node {node!r} ...\"` string interpolation."""
    with pytest.raises(TypeError, match="`node` must be a string"):
        NodeCancelledError(None)  # type: ignore[arg-type]


def test_accepts_non_empty_node() -> None:
    """Valid non-empty string `node` produces a working error."""
    error = NodeCancelledError("worker")
    assert error.node == "worker"
    assert "worker" in str(error)
    assert "asyncio.CancelledError" in str(error)


def test_accepts_explicit_message() -> None:
    """Explicit `message` overrides the default message format."""
    error = NodeCancelledError("worker", message="custom cancellation reason")
    assert error.node == "worker"
    assert str(error) == "custom cancellation reason"
