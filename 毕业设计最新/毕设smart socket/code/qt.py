import tkinter as tk
from tkinter import * 
from tkinter import messagebox as msgbox
import numpy as np
import time#常规时间操作模块
import  datetime#时间复杂操作模块（定时）
from bluepy.btle import UUID,Peripheral
import struct
import binascii#进制转化模块
import os
import signal
##---------------bluetooth setting-------------------------
RX_SERVICE_UUID=UUID('6e400001-b5a3-f393-e0a9-e50e24dcca9e')##只有这个是蓝牙插座的UUID
RX_CHAR_UUID=UUID('6e400003-b5a3-f393-e0a9-e50e24dcca9e')##接受设备uuid
TX_CHAR_UUID=UUID('6e400002-b5a3-f393-e0a9-e50e24dcca9e')##发送设备uuid
switch_staus="off"
##---------------bluetooth setting end---------------------
off='s'
on='l'
window = tk.Tk()
window.title("控制界面")
#window.geometry("400x200")
c=tk.StringVar()#绑定Entry中的textvariable,全局，获取get()
d=tk.StringVar()#绑定Entry中的textvariable,全局，获取get()
def btn1_clicked():
        switch_staus="on"
        tk.messagebox.showinfo(title='操作提示',message='蓝牙插座已开启')
        with Peripheral('C1:8F:CC:DC:57:19','random') as p:
            ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
            val=binascii.a2b_hex('AA0630306655')
            ch.write(val)
            p.disconnect()
def btn2_clicked():
        switch_staus='off'
        tk.messagebox.showinfo(title='操作提示',message='蓝牙插座已关闭')
        with Peripheral('C1:8F:CC:DC:57:19','random') as p:
            ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
            val=binascii.a2b_hex('AA0630316755')
            ch.write(val)
            p.disconnect()
def btn3_clicked():
        tk.messagebox.showinfo(title='操作提示',message='请以XX时XX分的格式输入，例如定时1小时15分钟为0115')
        entry=tk.Entry(window,textvariable=d)
        entry.pack(fill=tk.X)
        btn7 = tk.Button(window, text = "确定关闭定时开始", bg='lightpink',fg='black',command = btn7_clicked)#传值按键
        btn7.pack(fill=tk.X)
def btn7_clicked():
        on=d.get()
        r='AA0731'+on+'3955'
        print(r)
        with Peripheral('C1:8F:CC:DC:57:19','random') as p:
                ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
                val=binascii.a2b_hex(r)#定时一分钟关闭插座
                ch.write(val)
def btn4_clicked():
        switch_staus='off'
        tk.messagebox.showinfo(title='操作提示',message='请以XX时XX分的格式输入，例如定时1小时15分钟为0115')
        entry=tk.Entry(window,textvariable=c)
        entry.pack(fill=tk.X)
        btn6 = tk.Button(window, text = "确定开启定时开始", bg='hotpink',fg='black',command = btn6_clicked)#传值按键
        btn6.pack(fill=tk.X)
def btn6_clicked():        
        off=c.get()#按下去才get到entry的值
        r='AA0730'+off+'3855'
        print(r)
        with Peripheral('C1:8F:CC:DC:57:19','random') as p:
                ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
                val=binascii.a2b_hex(r)#定时开启插座
                ch.write(val)
def btn5_clicked():
        print('取消预约定时')
        with Peripheral('C1:8F:CC:DC:57:19','random') as p:
            ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
            val=binascii.a2b_hex('AA05333855')#取消定时
            ch.write(val)
photo = tk.PhotoImage(file="pig.png")#file：t图片路径
imgLabel = tk.Label(window,image=photo)#把图片整合到标签类中
imgLabel.pack(side=tk.RIGHT)#自动对齐
w = Label(window, text="designer su, in May 2018!",fg='red')  
w.pack()  
btn1 = tk.Button(window, text = "蓝牙插座开启", bg='pink',fg='black',command = btn1_clicked)
btn1.pack(fill = tk.X)
btn2 = tk.Button(window, text = "蓝牙插座关闭", bg='pink',fg='black',command = btn2_clicked)
btn2.pack(fill=tk.X)
btn4 = tk.Button(window, text = "定时开启插座", bg='pink',fg='black',command = btn4_clicked)
btn4.pack(fill=tk.X)
btn3 = tk.Button(window, text = "定时关闭插座", bg='pink',fg='black',command = btn3_clicked)
btn3.pack(fill=tk.X)
btn5 = tk.Button(window, text = "取消预约定时", bg='pink',fg='black',command = btn5_clicked)
btn5.pack(fill=tk.X)
window.mainloop()
