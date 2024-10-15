from enum import StrEnum


class EventType(StrEnum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    REFRESH = "refresh"
    ENUMERATE = "enumerate"
