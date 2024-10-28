from utility import *
run_as_admin()
wait_until_unlock(60)

preTm = int('220000')
begTm = int('233000')
endTm = int('060000')
INTERVAL = 0.1
BLACK_LIST = (  # preTm ~ begTm 间不允许前台的进程
    'Taskmgr.exe',
    'mmc.exe'
)
WHITE_LIST = (  # begTm ~ endTm 间允许前台的进程
    'LockApp.exe',
    'System Idle Process',
    'EXCEPTION',
    'StartMenuExperienceHost.exe',
    'SearchHost.exe',
    'coodesker-x64.exe',
    'explorer.exe',
    'QQ.exe',
    'WeChat.exe',
    'cloudmusic.exe',
)

SW_MINIMIZE = 6
WM_CLOSE = 0x0010
delay = 0
while True:
    tm.sleep(delay)
    if now_between(begTm, endTm):
        delay = INTERVAL
        violate = True
        hwnd, _, _, foreNm = fore_window_info()
        for white in WHITE_LIST:
            if white == foreNm:
                violate = False
        if violate:
            user32.ShowWindow(hwnd, SW_MINIMIZE)
            print(foreNm)
    elif now_between(preTm, begTm):
        delay = INTERVAL
        violate = False
        hwnd, _, _, foreNm = fore_window_info()
        for black in BLACK_LIST:
            if black == foreNm:
                violate = True
        if violate:
            user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)
            print(hwnd, foreNm)
    else:
        print('free')
        delay = 10
