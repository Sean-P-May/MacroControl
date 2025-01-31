import base64

import websockets
from icoextract import IconExtractor
from IconGetter.icon_model import IconModelMessage, IconRequestModel
from Models.WebsocketMessage import IncomingMessage


async def get_icon_message(message: IncomingMessage, websocket: websockets.WebSocketServerProtocol):
    """
    :param message: An instance of IncomingMessage, representing the message with icon request data.
    :param websocket: An instance of WebSocketServerProtocol, representing the WebSocket connection.

    :return: None

    This method takes in an incoming message and a WebSocket connection. It validates the icon request data from the
    message, retrieves the corresponding icon using the icon path, creates * an IconModelMessage object with the icon
    data, and sends the JSON-encoded icon message through the WebSocket connection.
    """
    icon_request = IconRequestModel.model_validate(message.data)
    icon = get_icon(icon_request.icon_path)
    icon_base64 = base64.b64encode(icon).decode()
    icon_message = IconModelMessage(
        icon_name=icon_request.icon_name,
        icon_path=icon_request.icon_path,
        icon_data=icon_base64
    )
    await websocket.send(icon_message.model_dump_json())


def get_icon(path: str) -> bytes:
    """Get the icon from the given path.

    :param path: The path of the file or directory from which to extract the icon.
    :return: The bytes object representi g the icon.
    """
    extractor = IconExtractor(path)
    icon = extractor.get_icon()
    return icon.getvalue()
