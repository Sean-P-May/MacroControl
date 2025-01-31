import asyncio
import clipboard
import pyautogui
import websockets
from pydantic import BaseModel

from Clipboard.clipboard_messages import ClipboardActionData, ClipboardActions
from Models.WebsocketMessage import IncomingMessage, MessageType


class _Clipboard(BaseModel):
    """A class representing the clipboard functionality.

    Attributes:
        values (list[str]): A list to store the clipboard values.

    Methods:
        monitor_clipboard: Continuously monitors the clipboard and stores any new values.
        paste_value: Pastes the specified value from the clipboard.
        delete_value: Deletes the specified value from the clipboard.

    """
    values: list[str] = []

    async def monitor_clipboard(self, interval: float = .1):
        last_value = None
        while True:
            current_value = clipboard.paste()
            if current_value != last_value:
                last_value = current_value
                self.values.append(current_value)
                if len(self.values) > 30:
                    self.values.pop(len(self.values) - 1)

            await asyncio.sleep(interval)

    def paste_value(self, value: int):
        pyautogui.write(self.values[value])

    def delete_value(self, value: int):
        self.values.pop(value)


clipboard_instance = _Clipboard()

async  def route_clipboard_message(message: IncomingMessage, websocket: websockets.WebSocketServerProtocol):
    match message.type:
        case MessageType.DATA_REQUEST:
            await websocket.send(
                IncomingMessage(
                    data=clipboard_instance.model_dump()
                ).model_dump_json())

        case MessageType.ACTION:
            message = ClipboardActionData.model_validate(message.data)
            match message.action:
                case ClipboardActions.PASTE:
                    clipboard_instance.paste_value(message.value)
                case ClipboardActions.DELETE:
                    clipboard_instance.delete_value(message.value)
                case _:
                    ValueError(f'Invalid action {message.action}')


