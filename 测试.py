#from turtle import *
#import turtle
#forward(100)
#ts = turtle.getscreen()
#ts.getcanvas().postscript(file="duck.jpg")
import win32gui
import win32api
import win32con
import time
import os
import threading#多线程
def job():
    os.system('python 迷宫绘制.py')
    time.sleep(1)
t1=threading.Thread(target=job)
t1.start()
time.sleep(3)
def shortcut():#截图，保存图片
    # 获取鼠标当前位置的坐标
    a=win32api.GetCursorPos()
    #classname = "pythonClass"
    titlename = "Python Turtle Graphics"
    #获取句柄
    hwnd = win32gui.FindWindow(None, titlename)
    #将窗口提到最前
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)#强行显示界面
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.2)#0.1s强显界面导致窗口透明化
    #获取窗口左上角和右下角坐标
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    #win32键盘模拟
    win32api.keybd_event(18,0,0,0)      #Alt
    win32api.keybd_event(17,0,0,0)     # ctrl
    win32api.keybd_event(65,0,0,0)     # A
    win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)  #释放按键
    win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)
    win32api.keybd_event(65,0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(0.1)#否则速度太快将会拖动到其他的东西
    #win32鼠标模拟 
    win32api.SetCursorPos((left, top))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    print('ok')
    win32api.SetCursorPos((right, bottom))
    print(a,right,bottom)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
    time.sleep(0.1)
    win32api.keybd_event(17,0,0,0)#ctrl
    win32api.keybd_event(83,0,0,0)#s
    time.sleep(0.1)
    win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
    win32api.keybd_event(83,0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(0.1)
    win32api.keybd_event(13,0,0,0)#按下enter，保存截图完成
    win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
for num in range(0,5):#截图5次
    print(num)
    shortcut()
    time.sleep(1.4)
