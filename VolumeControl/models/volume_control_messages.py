import enum
from typing import Union, Optional

from pydantic.dataclasses import dataclass
from pydantic import BaseModel

class ActionType(enum.StrEnum):
    CHANGE_VOLUME = "change_volume"
    TOGGLE_MUTE = "toggle_mute"
    CHANGE_INPUT_VOLUME = "change_input_volume"
    TOGGLE_INPUT_MUTE = "toggle_input_mute"
    APP_CHANGE_VOLUME = "app_change_volume"
    APP_TOGGLE_MUTE = "app_toggle_mute"


class VolumeControlMessage(BaseModel):
    action: ActionType
    value: Union[float, bool]
    app_id: Optional[int] = None
