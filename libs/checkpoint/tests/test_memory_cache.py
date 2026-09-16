from typing import Any

from langgraph.cache.memory import InMemoryCache


class FalsySerializer:
    def __bool__(self) -> bool:
        return False

    def dumps_typed(self, obj: Any) -> tuple[str, bytes]:
        return "value", str(obj).encode()

    def loads_typed(self, data: tuple[str, bytes]) -> Any:
        return data[1].decode()


def test_cache_honors_falsy_serializer() -> None:
    serde = FalsySerializer()
    cache = InMemoryCache(serde=serde)

    assert cache.serde is serde
    cache.set({(("namespace",), "key"): ("payload", None)})
    assert cache.get([(("namespace",), "key")]) == {
        (("namespace",), "key"): "payload"
    }
