"""Tests for `langgraph.types.Send` constructor validation."""

from __future__ import annotations

import pytest

from langgraph.types import Send


def test_send_rejects_empty_node() -> None:
    """`Send` must reject an empty `node` argument."""
    with pytest.raises(ValueError, match="`node` must be a non-empty string"):
        Send("", {"x": 1})


def test_send_rejects_non_string_node() -> None:
    """`Send` must reject a non-string `node` argument."""
    with pytest.raises(TypeError, match="`node` must be a string"):
        Send(None, {"x": 1})  # type: ignore[arg-type]


def test_send_accepts_non_empty_node() -> None:
    """`Send` must accept a non-empty `node` argument."""
    packet = Send("worker", {"x": 1})
    assert packet.node == "worker"
    assert packet.arg == {"x": 1}
