import os
import websockets
import yaml
from Models.WebsocketMessage import WebsocketMessage, MessageType, IncomingMessage
from Macros.macro_messages import RunMacro, MacroList
from config import config
from logger import logger
from Macros.macro import Macro
from pydantic import ValidationError
from pydantic.error_wrappers import ValidationError


class MacroHandler:

    def __init__(self):
        self.macros = []
        self.load_macros()

    def load_macros(self):
        logger.info(f'Loading macros from {config.macroPath}')
        for index, filename in enumerate(os.listdir(config.macroPath)):
            if filename.endswith('.yaml'):
                file_path = os.path.join(config.macroPath, filename)
                try:
                    with open(file_path, 'r') as file:
                        macro_yaml = yaml.load(file, Loader=yaml.FullLoader)
                        self.handle_macro_yaml(macro_yaml, index)
                except (yaml.YAMLError, TypeError, ValidationError) as exc:
                    logger.error(f'Error loading/validating macro from {filename}: {exc}')

    def handle_macro_yaml(self, macro_yaml, index):
        if isinstance(macro_yaml, list):
            self.load_multiple_macros(macro_yaml, index)
        else:
            self.load_single_macro(macro_yaml, index)

    def load_multiple_macros(self, macro_yaml, index):
        for macro_data in macro_yaml:
            self.add_macro(macro_data, index)

    def load_single_macro(self, macro_yaml, index):
        self.add_macro(macro_yaml, index)

    def add_macro(self, macro_data, index):
        macro = Macro.from_yaml(macro_data, index=index)
        self.macros.append(macro)
        self.log_macro_loaded(macro)

    @staticmethod
    def log_macro_loaded(macro):
        logger.info(f'Loaded macro {macro.name}')


macro_handler = MacroHandler()




async def route_macro_message(message: IncomingMessage, websocket: websockets.WebSocketServerProtocol):

    match message.type:
        case MessageType.ACTION:
            action_message = RunMacro.model_validate(message.data)
            try:
                macro = macro_handler.macros[action_message.id]
                macro.run()
            except IndexError:
                logger.error(f'Macro with id {action_message.id} does not exist')
        case MessageType.DATA_REQUEST:
            outgoing = WebsocketMessage(
                data=MacroList(macros=[macro.model_dump() for macro in macro_handler.macros]).model_dump(),
            )
            await websocket.send(outgoing.model_dump_json())
        case MessageType.RESET:
            macro_handler.macros = []
            macro_handler.load_macros()
