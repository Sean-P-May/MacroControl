import win32gui
import win32process
import psutil


def get_active_executable_name():
    window_handle = win32gui.GetForegroundWindow()
    window_name = win32gui.GetWindowText(window_handle)


    # Get the PID of the active window:
    _, pid = win32process.GetWindowThreadProcessId(window_handle)

    # Use psutil to get the process based on the PID and the name of the exe file:
    try:
        return psutil.Process(pid).name()+ " - " + window_name
    except psutil.NoSuchProcess:
        return ""
    except ValueError:
        return ""


while True:
    print(get_active_executable_name())
