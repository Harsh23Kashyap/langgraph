"""Re-export types moved to langgraph.types.

This module is kept for backwards compatibility. The deprecation
warning fires only on attribute access (e.g. `from
langgraph.pregel.types import StateSnapshot` or
`langgraph.pregel.types.StateSnapshot`), not on bare `import
langgraph.pregel.types`. The lazy-warn pattern matches
`langgraph.constants`, so users running with `-W error` can still
import the module without the import itself being an error.
"""

from importlib import import_module
from typing import TYPE_CHECKING, Any
from warnings import warn

from langgraph.warnings import LangGraphDeprecatedSinceV10

if TYPE_CHECKING:
    # Re-bind the names to their real types so static type checkers see
    # them as their concrete classes (not `object`) on the deprecated
    # import path. At runtime, `__getattr__` is the only resolution path.
    from langgraph.types import (  # noqa: F822
        All,
        CachePolicy,
        PregelExecutableTask,
        PregelTask,
        RetryPolicy,
        StateSnapshot,
        StateUpdate,
        StreamMode,
        StreamWriter,
        default_retry_on,
    )

__all__ = [
    "All",
    "StateUpdate",
    "CachePolicy",
    "PregelExecutableTask",
    "PregelTask",
    "RetryPolicy",
    "StateSnapshot",
    "StreamMode",
    "StreamWriter",
    "default_retry_on",
]

# Prefix preserved for users who filter the warning message text
# (e.g. `warnings.filterwarnings(message="Importing from langgraph.pregel.types...")`).
# The deprecated-name suffix is added on a second line so the original
# prefix is still a substring of the new message.
_DEPRECATION_PREFIX = (
    "Importing from langgraph.pregel.types is deprecated. "
    "Please use 'from langgraph.types import ...' instead. "
    "Deprecated name: {name}."
)


def __getattr__(name: str) -> Any:
    if name not in __all__:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    warn(
        _DEPRECATION_PREFIX.format(name=name),
        LangGraphDeprecatedSinceV10,
        stacklevel=2,
    )
    return getattr(import_module("langgraph.types"), name)
