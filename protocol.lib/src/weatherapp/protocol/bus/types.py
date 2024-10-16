from enum import StrEnum


class EventType(StrEnum):
    CREATE = "create"  # object was createed
    UPDATE = "update"  # object was updated
    DELETE = "delete"  # object was deleted
    REFRESH = "refresh"  # nothing happened to the object, just refresh data
    ENUMERATE = "enumerate"  # enumerate IDs of existing objects
    EOS = "eos"  # end of stream
