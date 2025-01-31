import os
from enum import Enum

import yaml

from pydantic import BaseModel, Field


class OperatingSystem(Enum):
    WINDOWS = 'nt'
    LINUX = 'posix'


APP_NAME = 'MarcoDeck Server'
USER_NAME_HOME = os.path.expanduser('~')
CONFIG_FILE_PATH = os.path.join(USER_NAME_HOME, APP_NAME, 'config.yaml')
MACRO_PATH = os.path.join(USER_NAME_HOME, APP_NAME, 'macros')
DEFAULT_LOG_PATH = os.path.join(USER_NAME_HOME, APP_NAME, 'logs')

DEFAULT_PORT = 9999


class Config:
    def __init__(self):
        self.load_or_initialize()

    def load_or_initialize(self):
        if os.path.exists(CONFIG_FILE_PATH):
            with open(CONFIG_FILE_PATH, 'r') as file:
                try:
                    data = yaml.load(file, Loader=yaml.FullLoader)
                    self.port = data.get('port', DEFAULT_PORT)
                    self.macroPath = data.get('macroPath', MACRO_PATH)
                    self.logPath = data.get('logPath', DEFAULT_LOG_PATH)
                    self.appName = APP_NAME
                    self.operatingSystem = OperatingSystem(os.name)

                except (yaml.YAMLError, TypeError) as exc:
                    print(exc)
                    print('Error loading config file, initializing with default values')
                    self.set_defaults()
        else:
            self.set_defaults()
            self.save_defaults()

    def set_defaults(self):
        self.port = DEFAULT_PORT
        self.macroPath = MACRO_PATH
        self.appName = APP_NAME
        self.logPath = DEFAULT_LOG_PATH

    def save_defaults(self):
        os.makedirs(os.path.dirname(CONFIG_FILE_PATH), exist_ok=True)
        _dict = self.__dict__
        _dict.pop('appName')

        with open(CONFIG_FILE_PATH, 'w') as file:
            yaml.dump(self.__dict__, file)


config = Config()
