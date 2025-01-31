from pydantic import BaseModel as basemodel
from enum import StrEnum


class ClipboardActions(StrEnum):
    PASTE = "paste"
    DELETE = "delete"


class ClipboardActionData(basemodel):
    action: ClipboardActions
    index: int
