import json
from collections.abc import Callable
from typing import NamedTuple, TypeVar

ENCODING = "utf-8"

_FIELDS_TR = {
    "_type": "ev_type",
    "_source": "ev_source",
}

NamedTupleT = TypeVar("NamedTupleT", bound=NamedTuple)


def json_to_namedtuple_deserializer(
    class_: type[NamedTupleT], encoding: str = ENCODING
) -> Callable[[bytes], NamedTupleT]:
    def deserializer(value: bytes) -> NamedTupleT:
        payload = json.loads(value.decode(encoding))
        transformed = [(_FIELDS_TR.get(k, k), v) for k, v in payload.items()]
        fields = set(f for f in class_._fields)
        data = {k: v for k, v in transformed if k in fields}
        return class_(**data)  # type: ignore

    return deserializer
