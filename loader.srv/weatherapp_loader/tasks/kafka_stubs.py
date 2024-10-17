from collections.abc import Callable, Sequence
from typing import Any


class AIOKafkaProducer:
    def __init__(
        self,
        bootstrap_servers: Sequence[str],
        key_serializer: Callable[[Any], bytes] | None = None,
        value_serializer: Callable[[Any], bytes] | None = None,
    ) -> None:
        pass

    async def start(self) -> None:
        pass

    async def stop(self) -> None:
        pass

    async def flush(self) -> None:
        pass

    async def send(self, topic: str, value: Any) -> None:
        pass


class KafkaError(Exception):
    pass


class KafkaConnectionError(KafkaError):
    pass
