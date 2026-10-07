"""Tests for `langgraph.graph.ui.push_ui_message` name validation."""

from __future__ import annotations

import pytest

from langgraph.graph.ui import push_ui_message


def test_push_ui_message_rejects_empty_name() -> None:
    """`push_ui_message` must reject an empty `name` argument."""
    with pytest.raises(ValueError, match="`name` must be a non-empty string"):
        push_ui_message("", props={"x": 1})


def test_push_ui_message_rejects_non_string_name() -> None:
    """`push_ui_message` must reject a non-string `name` argument."""
    with pytest.raises(TypeError, match="`name` must be a string"):
        push_ui_message(None, props={"x": 1})  # type: ignore[arg-type]
