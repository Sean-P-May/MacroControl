import time
from enum import Enum

from random import randint

from uuid import uuid4, UUID

from typing import Any

from typing_extensions import Literal

import yaml
from pydantic import BaseModel, Field
from config import config, OperatingSystem
import webbrowser
import subprocess
import keyboard


def generate_random_id():
    return hex(randint(0, 2 ** 16 - 1))

class MacroType(Enum):
    openWebpage = 'openWebpage'
    runTerminalCommand = 'runTerminalCommand'
    keyboardShortcut = 'keyboardShortcut'
    runPythonScript = 'runPythonScript'
    runApplication = 'runApplication'
    ContinuousApp = 'ContinuousApp'


class Macro(BaseModel):
    id: int
    unique_id: str = Field(default_factory=generate_random_id)
    type: MacroType
    name: str
    description: str
    iconFile: str
    color: str

    class Config:
        use_enum_values = True

    def run(self):
        raise NotImplementedError

    @classmethod
    def from_yaml(cls, _yaml: dict, index: int):
        match _yaml['type']:
            case MacroType.openWebpage.value:
                return OpenWebpageMacro(**_yaml, id=index)
            case MacroType.runTerminalCommand.value:
                return RunTerminalCommandMacro(**_yaml, id=index)
            case MacroType.keyboardShortcut.value:
                return KeyboardShortcutMacro(**_yaml, id=index)
            case MacroType.runPythonScript.value:
                return RunPythonScriptMacro(**_yaml, id=index)
            case MacroType.runApplication.value:
                return RunApplicationMacro(**_yaml, id=index)
            case MacroType.ContinuousApp.value:
                return ContinuousMacro(**_yaml, id=index)




    def to_yaml(self):
        return yaml.dump(self.model_dump(exclude={'id'}))



class OpenWebpageMacro(Macro):
    url: str

    def run(self):
        webbrowser.open(self.url)


class RunTerminalCommandMacro(Macro):
    command: str
    args: list[str]

    def run(self):
        if config.operatingSystem == OperatingSystem.WINDOWS:
            commands_from_args = ["wt", self.command, *self.args]
            subprocess.Popen(commands_from_args, shell=True)
        else:
            raise NotImplementedError


class KeyboardShortcutMacro(Macro):
    keys: list[str]

    def run(self):
        keyboard.send(self.keys)


class RunPythonScriptMacro(Macro):
    script: str
    args: list[str]

    def run(self):
        commands_from_args = ['Python', self.script, *self.args]
        subprocess.Popen(commands_from_args, shell=True)


class RunApplicationMacro(Macro):
    app: str
    args: list[str]

    def run(self):
        commands_from_args = [self.app, *self.args]
        subprocess.Popen(commands_from_args)


class ContinuousMacro(RunApplicationMacro):
    running: bool = Field(default=False)
    _process: subprocess.Popen or None = None


    def run(self):
        if not self.running:
            self._process = subprocess.Popen([self.app, *self.args]
                                         , creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
            self.running = True
        else:
            self.stop()
            self.running = False



    def stop(self):
        self._process.terminate()
        self.running = False



