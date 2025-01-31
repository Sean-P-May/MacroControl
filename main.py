import asyncio
import websockets

from Clipboard.clipboard_gui import clipboard_instance, route_clipboard_message
from Models.WebsocketMessage import MessageRoute, IncomingMessage
from logger import logger
from Macros.macro_controller import route_macro_message, MacroHandler
from VolumeControl.volume_control_controller import route_audio_control_message, update_volume_data
from IconGetter.icon_getter import get_icon_message
from config import config


async def route_message(message, websocket):
    match message.route:
        case MessageRoute.MACRO:
            return await route_macro_message(message, websocket)
        case MessageRoute.VOLUME_CONTROL:
            return await route_audio_control_message(message, websocket)
        case MessageRoute.ICON_DATA:
            return await get_icon_message(message, websocket)
        case MessageRoute.CLIPBOARD:
            return await route_clipboard_message(message, websocket)


async def handler(websocket):
    try:
        async for message in websocket:
            print(message)
            message = IncomingMessage.model_validate_json(message)
            await route_message(message, websocket)
    except websockets.exceptions.WebSocketException as e:
        logger.error(e)


async def main():
    logger.info(f'Starting {config.appName} on port {config.port}...')

    async with websockets.serve(handler, '0.0.0.0', config.port):
        clipboard_task = asyncio.create_task(clipboard_instance.monitor_clipboard())
        volume_controller_task = asyncio.create_task(update_volume_data())

        logger.info(f'{config.appName} started')
        await volume_controller_task
        await clipboard_task


if __name__ == '__main__':
    asyncio.run(main())
