import itertools
import math
from ctypes import cast, POINTER
from math import log10

import psutil
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pycaw.utils import AudioSession

from VolumeControl.models.volume_control_models import AppVolumeDataModel


class AppVolumeController:
    app_id: int
    app_name: str
    _session: AudioSession
    icon_name: str or None
    volume: float
    mute: bool
    id_iter = itertools.count()

    def __init__(self, session: AudioSession):
        self.app_id = next(AppVolumeController.id_iter)
        if session.DisplayName == "@%SystemRoot%\System32\AudioSrv.Dll,-202":
            self.app_name = "System  Sounds"
        else:
            self.app_name = session.Process.name().replace(".exe", '')

        self._volume_controller = session.SimpleAudioVolume
        self._session = session
        self.icon_name = self._get_icon_path()
        self.volume = self._volume_controller.GetMasterVolume()
        self.mute = bool(self._volume_controller.GetMute())


    def change_volume(self, volume_percentage: float):
        volume_level = self.__percentage_to_decibel(volume_percentage)
        self._volume_controller.SetMasterVolume(volume_level, None)

    def toggle_mute(self):
        if self.mute:
            self.pulse_pointer.mute(self.sink_input_obj, False)
        else:
            self.pulse_pointer.mute(self.sink_input_obj, True)

    def _get_icon_path(self):
        process_id = self._session.ProcessId
        if process_id:
            try:
                process = psutil.Process(process_id)
                return process.exe()
            except psutil.Error as e:
                print(e)
                return ""

    def get_model(self):
        return AppVolumeDataModel(
            app_id=self.app_id,
            app_name=self.app_name,
            icon_name= self.icon_name if self.icon_name else "",
            volume=self.volume,
            muted=self.mute
        )

    def __percentage_to_decibel(self, volume_percentage):
        return min(max(volume_percentage / 100, 0.0), 1.0)


class WindowsVolumeController:
    def __init__(self):
        self.windows_speaker_controller = self.__get_device_controller(AudioUtilities.GetSpeakers())
        self.windows_microphone_controller = self.__get_device_controller(AudioUtilities.GetMicrophone())

        self.update_state()

        self.app_controllers = self.__collect_app_controllers()

    def __get_device_controller(self, device):
        interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return cast(interface, POINTER(IAudioEndpointVolume))

    def __collect_app_controllers(self) -> list[AppVolumeController]:
        AppVolumeController.id_iter = itertools.count() # reset the id_iter
        app_controllers_list: list[AppVolumeController] = []
        sessions = AudioUtilities.GetAllSessions()
        for app in sessions:
            app_controllers_list.append(AppVolumeController(app))
        return app_controllers_list

    def update_state(self):
        self.output_muted = self.windows_speaker_controller.GetMute()
        self.master_volume = self.__decibel_to_percentage(self.windows_speaker_controller.GetMasterVolumeLevelScalar())

        self.input_muted = self.windows_microphone_controller.GetMute()
        self.input_volume = self.__decibel_to_percentage(
            self.windows_microphone_controller.GetMasterVolumeLevelScalar())
        self.__collect_app_controllers()

    def change_master_volume(self, volume_percentage: float):
        volume_level = self.__percentage_to_decibel(volume_percentage)
        self.windows_speaker_controller.SetMasterVolumeLevelScalar(volume_level, None)

    def toggle_master_mute(self):
        self.windows_speaker_controller.SetMute(not self.output_muted, None)

    def change_input_volume(self, volume_percentage: float):
        volume_level = self.__percentage_to_decibel(volume_percentage)
        self.windows_microphone_controller.SetMasterVolumeLevelScalar(volume_level, None)

    def toggle_input_mute(self):
        self.windows_microphone_controller.SetMute(not self.input_muted, None)

    @staticmethod
    def __percentage_to_decibel(percentage):
        return percentage / 100.0

    @staticmethod
    def __decibel_to_percentage(decibel):
        return decibel * 100.0

    def toggle_mute_master_volume(self):
        self.windows_speaker_controller.SetMute(not self.output_muted, None)

