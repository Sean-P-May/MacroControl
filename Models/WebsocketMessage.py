from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class MessageType(Enum):
    ACTION = 'ACTION'
    DATA_REQUEST = 'DATA_REQUEST'
    RESET = 'RESET'


class MessageRoute(Enum):
    CLIPBOARD = 'CLIPBOARD'
    MACRO = 'MACRO'
    VOLUME_CONTROL = 'VOLUME_CONTROL'
    ICON_DATA = 'ICON_DATA'


class WebsocketMessage(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)


class IncomingMessage(WebsocketMessage):
    type: MessageType
    route: MessageRoute


class OutgoingMessage(WebsocketMessage):
    type: MessageType = Field(default=MessageType.DATA_REQUEST)
    route: MessageRoute
    data: dict
