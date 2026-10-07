"""Tests for `langgraph.graph.ui.push_ui_message` id validation."""

from __future__ import annotations

import pytest

from langgraph.graph.ui import push_ui_message


def test_push_ui_message_rejects_non_string_id() -> None:
    """`push_ui_message` must reject a non-string `id` argument (when not None)."""
    with pytest.raises(TypeError, match="`id` must be a string or None"):
        push_ui_message("component", props={"x": 1}, id=42)  # type: ignore[arg-type]


def test_push_ui_message_accepts_string_id() -> None:
    """`push_ui_message` must accept a string `id` argument."""
    with pytest.raises(
        RuntimeError,
        match="Called get_config outside of a runnable context",
    ):
        # Validation passes; runtime context is required to actually emit.
        push_ui_message("component", props={"x": 1}, id="abc-123")
