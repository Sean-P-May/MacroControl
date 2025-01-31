from pydantic import BaseModel, Field


class AppVolumeDataModel(BaseModel):
    app_id: int
    app_name: str
    icon_name: str
    volume: float
    muted: bool


class VolumeControlModel(BaseModel):
    master_volume: float
    input_volume: float
    output_muted: bool
    input_muted: bool
    app_controllers: list[AppVolumeDataModel]
