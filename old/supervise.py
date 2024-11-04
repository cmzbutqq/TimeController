
INTERVAL = 0.1
BLACK_LIST = ( 
)
WHITE_LIST = ( 
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
        print("free")
        delay = 10
