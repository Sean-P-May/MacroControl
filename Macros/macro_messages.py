from pydantic import BaseModel, Field
from Macros.macro import Macro


class RunMacro(BaseModel):
    id: int


class MacroList(BaseModel):
    macros: list[Macro]
