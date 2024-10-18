from typing import Any


class Client:
    def __init__(**kwargs: Any):
        pass

    async def execute(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
        settings: dict[str, Any] | None = None,
    ) -> Any:
        pass
