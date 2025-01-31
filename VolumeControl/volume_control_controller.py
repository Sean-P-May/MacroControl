import asyncio

import websockets
from Models.WebsocketMessage import MessageType, IncomingMessage, WebsocketMessage, OutgoingMessage, MessageRoute
from VolumeControl.models.volume_control_messages import ActionType, VolumeControlMessage
from VolumeControl.volume_control import VolumeController

volume_controller_instance = VolumeController()


async def update_volume_data():
    volume_controller_instance.__init__()
    await asyncio.sleep(1)


async def route_audio_control_message(
        message: IncomingMessage,
        websocket: websockets.WebSocketServerProtocol):

    print(message)

    match message.type:

        case MessageType.DATA_REQUEST:
            print('data request')

            await websocket.send(
               OutgoingMessage(
                    route=MessageRoute.VOLUME_CONTROL,
                    data=volume_controller_instance.get_volume_data_model().model_dump()
                ).model_dump_json())

        case MessageType.ACTION:
            action_message = VolumeControlMessage.model_validate(message.data)
            match action_message.action:
                case ActionType.CHANGE_VOLUME:
                    volume_controller_instance.change_master_volume(action_message.volume)
                case ActionType.TOGGLE_MUTE:
                    volume_controller_instance.toggle_master_mute()
                case ActionType.CHANGE_INPUT_VOLUME:
                    volume_controller_instance.change_input_volume(action_message.volume)
                case ActionType.TOGGLE_INPUT_MUTE:
                    volume_controller_instance.toggle_input_mute()
                case ActionType.APP_CHANGE_VOLUME:
                    volume_controller_instance.change_app_volume(action_message.app_id, action_message.value)
                case ActionType.APP_TOGGLE_MUTE:
                    volume_controller_instance.toggle_app_mute(action_message.app_id)

        case _:
            raise ValueError(f'Invalid message type {message.type}')
