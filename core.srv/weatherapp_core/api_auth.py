from django.http import HttpRequest


async def auth(request: HttpRequest) -> bool:
    return True


async def async_auth(request: HttpRequest) -> bool:
    return True
