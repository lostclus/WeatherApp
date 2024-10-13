from typing import Any

from django.http import HttpRequest
from ninja_extra import permissions


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, controller: Any) -> bool:
        return request.method in permissions.SAFE_METHODS
