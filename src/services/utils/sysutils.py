from time import sleep
import ctypes
import psutil
import os
import sys
from ctypes import wintypes

__all__ = (
    "is_admin",
    "run_as_admin",
    "fore_window_info",
    "start",
    "is_locked",
    "wait_until_unlock",
    "os",
    "user32",
    "sleep",
)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def run_as_admin():
    # 如果当前用户不是管理员，则以管理员身份重新启动脚本
    if not is_admin():
        # 重新运行脚本作为管理员
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()


# 定义需要的 Windows API 函数和常量
user32 = ctypes.WinDLL("user32", use_last_error=True)


def fore_window_info():
    # 获取前台进程信息（睡眠、锁屏时
    # Process Name: System Idle Process    LockApp.exe）
    hwnd = user32.GetForegroundWindow()
    # 获取窗口标题
    length = user32.GetWindowTextLengthW(hwnd) + 1
    buffer = ctypes.create_unicode_buffer(length)
    window_name = (
        (user32.GetWindowTextW(hwnd, buffer, length) > 0)
        and buffer.value
        or "EXCEPTION"
    )
    # 获取进程 ID
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    # 获取进程名称
    try:
        process = psutil.Process(pid.value)
        process_name = process.name()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        process_name = "EXCEPTION"
    return (hwnd, pid.value, window_name, process_name)


def start(pth):  # 依据路径启动或打开 并返回是否成功
    try:
        os.startfile(pth)
        return True
    except FileNotFoundError:
        return False


def is_locked():
    _, _, _, nm = fore_window_info()
    SLEEP_LIST = ("LockApp.exe", "System Idle Process", "EXCEPTION")
    return nm in SLEEP_LIST


def wait_until_unlock(delay, interval=1):
    while is_locked():
        sleep(interval)
    sleep(delay)


if __name__ == "__main__":
    while True:
        sleep(0.5)
        s = fore_window_info()
        print(s[3])
