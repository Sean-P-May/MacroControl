from config import config, OperatingSystem
from VolumeControl.models.volume_control_models import VolumeControlModel


class VolumeController:

    def __init__(self):
        match config.operatingSystem:
            case OperatingSystem.LINUX:
                from VolumeControl.linux.linux_volume_control import LinuxVolumeController
                self.OSVolumeController = LinuxVolumeController()
            case OperatingSystem.WINDOWS:
                from VolumeControl.windows.windows_volume_control import WindowsVolumeController
                self.OSVolumeController = WindowsVolumeController()
            case _:
                raise OSError("OS not supported!")

    @property
    def master_volume(self):
        return self.OSVolumeController.master_volume

    @property
    def input_volume(self):
        return self.OSVolumeController.input_volume

    @property
    def output_muted(self):
        return self.OSVolumeController.output_muted

    @property
    def input_muted(self):
        return self.OSVolumeController.input_muted

    def change_master_volume(self, volume: float):
        self.OSVolumeController.change_master_volume(volume)

    def toggle_master_mute(self):
        self.OSVolumeController.toggle_mute_master_volume()

    def change_input_volume(self, volume: float):
        self.OSVolumeController.change_input_volume(volume)

    def toggle_input_mute(self):
        self.OSVolumeController.toggle_input_mute()

    def get_app_volume_controllers(self):
        return self.OSVolumeController.app_controllers

    def change_app_volume(self, app_id: int, volume: float):
        self.get_app_volume_controllers()[app_id].change_volume(volume)

    def toggle_app_mute(self, app_id: int):
        self.get_app_volume_controllers()[app_id].toggle_mute()

    def update_state(self):
        self.OSVolumeController.update_state()

    def get_volume_data_model(self):
        return VolumeControlModel(
            master_volume=self.master_volume,
            input_volume=self.input_volume,
            output_muted=self.output_muted,
            input_muted=self.input_muted,
            app_controllers=[app_controller.get_model() for app_controller in self.get_app_volume_controllers()]
        )


