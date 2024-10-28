import time as tm
import ctypes
from ctypes import wintypes
import psutil
import os
import sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def run_as_admin():
    # 如果当前用户不是管理员，则以管理员身份重新启动脚本
    if not is_admin():
        # 重新运行脚本作为管理员
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()


def dprint(var):  # 同时打印变量及其类型
    print(f'{var}\t{type(var)}')


def now_int():  # 当前时间转字符串再转整数
    return int(tm.strftime('%H%M%S',))


def now_between(beg_tm, end_tm):
    now_tm = now_int()
    if beg_tm >= end_tm:
        result = now_tm <= end_tm or now_tm >= beg_tm
    else:
        result = now_tm <= end_tm and now_tm >= beg_tm
    return result


# 定义需要的 Windows API 函数和常量
user32 = ctypes.WinDLL('user32', use_last_error=True)
psapi = ctypes.WinDLL('psapi', use_last_error=True)


def fore_window_info():  # 获取前台进程信息（睡眠、锁屏时 Process Name: System Idle Process      LockApp.exe）
    hwnd = user32.GetForegroundWindow()
    # 获取窗口标题
    length = user32.GetWindowTextLengthW(hwnd) + 1
    buffer = ctypes.create_unicode_buffer(length)
    window_name = (user32.GetWindowTextW(hwnd, buffer, length) > 0) and buffer.value or "EXCEPTION"
    # 获取进程 ID
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    # 获取进程名称
    try:
        process = psutil.Process(pid.value)
        process_name = process.name()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        process_name = "EXCEPTION"
    return hwnd, pid.value, window_name, process_name


def start(pth):  # 依据路径启动或打开 并返回是否成功
    try:
        os.startfile(pth)
        return True
    except FileNotFoundError:
        return False

def is_locked():
    _, _, _, nm = fore_window_info()
    WHITE_LIST = (
        'LockApp.exe',
        'System Idle Process',
        'EXCEPTION'
    )
    for name in WHITE_LIST:
        if name == nm:
            return True
    return False

def wait_until_unlock(post_delay,detect_delay=1):
    while is_locked():
        tm.sleep(detect_delay)
    tm.sleep(post_delay)


if __name__ == '__main__':
    while True:
        tm.sleep(0.5)
        hwnd, _, _, nm = fore_window_info()
        print(nm)
