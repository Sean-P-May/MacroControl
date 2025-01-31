from pydantic import BaseModel


class IconModelMessage(BaseModel):
    icon_name: str
    icon_path: str
    icon_data: bytes


class IconRequestModel(BaseModel):
    icon_name: str
    icon_path: str
