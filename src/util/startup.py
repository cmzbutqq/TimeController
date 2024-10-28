from utility import *
import pyautogui
run_as_admin()
wait_until_unlock(5)

def loc(pth):
    try:
        return pyautogui.locateCenterOnScreen(pth, confidence=0.95)
    except Exception:
        return None

start('D:\SOFTWARE\CloudMusic\cloudmusic.exe')
tm.sleep(5)
c = loc('asset/wyy.png')
if c:
    pyautogui.click(x=c[0], y=c[1])
print(f'wyy:{c}')

start('C:\Program Files\\Nutstore\\Nutstore.exe')
tm.sleep(5)
n = loc('asset/nut.png')
if n:
    pyautogui.click(x=n[0], y=n[1])
print(f'nutStore:{n}')

start('D:\SOFTWARE\QQ nt\QQ.exe')
tm.sleep(3)
q = loc('asset/qq.png')
if q:
    pyautogui.click(x=q[0], y=q[1])
print(f'qq:{q}')
tm.sleep(2)

start('D:\SOFTWARE\WeChat\WeChat.exe')
tm.sleep(3)
w = loc('asset/wx.png')
if w:
    pyautogui.click(x=w[0], y=w[1])
print(f'wx:{w}')

print('startup finished.')