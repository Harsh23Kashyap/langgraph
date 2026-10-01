from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Generic

from typing_extensions import Self

from langgraph._internal._typing import MISSING
from langgraph.channels.base import BaseChannel, Value
from langgraph.errors import (
    EmptyChannelError,
    ErrorCode,
    InvalidUpdateError,
    create_error_message,
)
from langgraph.types import Overwrite

__all__ = ("AnyValue",)


class AnyValue(Generic[Value], BaseChannel[Value, Value, Value]):
    """Stores the last value received, assumes that if multiple values are
    received, they are all equal."""

    __slots__ = ("typ", "value")

    value: Value | Any

    def __init__(self, typ: Any, key: str = "") -> None:
        super().__init__(typ, key)
        self.value = MISSING

    def __eq__(self, value: object) -> bool:
        return isinstance(value, AnyValue)

    @property
    def ValueType(self) -> type[Value]:
        """The type of the value stored in the channel."""
        return self.typ

    @property
    def UpdateType(self) -> type[Value]:
        """The type of the update received by the channel."""
        return self.typ

    def copy(self) -> Self:
        """Return a copy of the channel."""
        empty = self.__class__(self.typ, self.key)
        empty.value = self.value
        return empty

    def from_checkpoint(self, checkpoint: Value) -> Self:
        empty = self.__class__(self.typ, self.key)
        if checkpoint is not MISSING:
            empty.value = checkpoint
        return empty

    def update(self, values: Sequence[Value]) -> bool:
        if len(values) == 0:
            if self.value is MISSING:
                return False
            else:
                self.value = MISSING
                return True
        # Reject `Overwrite` early: `Overwrite` is only supported on
        # `BinaryOperatorAggregate` channels (i.e. channels with an
        # `Annotated[KeyType, Reducer]` reducer). On an `AnyValue`
        # channel the bare `Overwrite` instance would otherwise be
        # stored as the channel value, producing a silent bug where
        # `get()` returns an `Overwrite` instead of the underlying value.
        for value in values:
            if isinstance(value, Overwrite):
                msg = create_error_message(
                    message=(
                        f"At key '{self.key}': Received `Overwrite` value but "
                        f"`AnyValue` does not support `Overwrite`. "
                        f"`Overwrite` is only supported on `BinaryOperatorAggregate` "
                        f"channels (i.e. channels with an `Annotated[KeyType, Reducer]` "
                        f"reducer). To bypass the reducer on a single value, declare "
                        f"the channel with a reducer like `operator.add`."
                    ),
                    error_code=ErrorCode.INVALID_CONCURRENT_GRAPH_UPDATE,
                )
                raise InvalidUpdateError(msg)

        self.value = values[-1]
        return True

    def get(self) -> Value:
        if self.value is MISSING:
            raise EmptyChannelError()
        return self.value

    def is_available(self) -> bool:
        return self.value is not MISSING

    def checkpoint(self) -> Value:
        return self.value
