from typing import Any


class ChClient:
    def __init__(self, session: Any, **kwargs: Any) -> None:
        pass

    async def execute(
        self,
        query: str,
        *args: Any,
        params: dict[str, Any] | None = None,
    ) -> None:
        pass

    async def fetch(
        self,
        query: str,
        *args: Any,
        params: dict[str, Any] | None = None,
    ) -> Any:
        pass
