"""Tests for `langgraph.graph.ui.delete_ui_message` id validation."""

from __future__ import annotations

import pytest

from langgraph.graph.ui import delete_ui_message


def test_delete_ui_message_rejects_empty_id() -> None:
    """`delete_ui_message` must reject an empty `id` argument."""
    with pytest.raises(ValueError, match="`id` must be a non-empty string"):
        delete_ui_message("")


def test_delete_ui_message_rejects_non_string_id() -> None:
    """`delete_ui_message` must reject a non-string `id` argument."""
    with pytest.raises(TypeError, match="`id` must be a string"):
        delete_ui_message(None)  # type: ignore[arg-type]
