import tkinter as tk
from tkinter import * 
from tkinter import messagebox as msgbox
from gtts import gTTS
import numpy as np
import time#常规时间操作模块
import  datetime#时间复杂操作模块（定时）
from bluepy.btle import UUID,Peripheral
import sys
import struct
import binascii#进制转化模块
import os
import signal
import skywriter
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
##---------------bluetooth setting-------------------------
RX_SERVICE_UUID=UUID('6e400001-b5a3-f393-e0a9-e50e24dcca9e')##只有这个是蓝牙插座的UUID
RX_CHAR_UUID=UUID('6e400003-b5a3-f393-e0a9-e50e24dcca9e')##接受设备uuid
TX_CHAR_UUID=UUID('6e400002-b5a3-f393-e0a9-e50e24dcca9e')##发送设备uuid
switch_staus="off"
##---------------bluetooth setting end---------------------
off='s'
on='l'
X='l'
window = tk.Tk()
window.title("控制界面")
T = Text(window,width=50)
S = Scrollbar(window)
S.pack(side=LEFT, fill=Y)
T.pack(side=LEFT, fill=Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
c=tk.StringVar()#绑定Entry中的textvariable,全局,获取get()
d=tk.StringVar()#绑定Entry中的textvariable,全局,获取get()
e=tk.StringVar()
##--------------插座RTC时间初始-------------------------------
##--------------动态检查和(checksum)计算-------------------
s=time.localtime()
year=(s.tm_year)%100
mon=  s. tm_mon
day= s. tm_mday
hour=s.tm_hour
minute=s.tm_min
sec=s.tm_sec
a6='0x'+str(sec)
a7='0x'+str(mon)
a8='0x'+str(hour)
a9='0x'+str(minute)
a10='0x'+str(day)
a11='0x'+str(year)
a12=int(a10,16)
a13=int(a9,16)
a14=int(a8,16)
a15=int(a7,16)
a16=int(a6,16)
a17=int(a11,16)
a4=a12+a13+a14+a15+a16+a17
year1=(s.tm_year)%100
mon1="%02d" % s. tm_mon
day1="%02d"% s. tm_mday
hour1="%02d"% s.tm_hour
minute1="%02d" %s.tm_min
sec1="%02d"% s.tm_sec
a1=str(sec1)+str(minute1)+str(hour1)+str(day1)+str(mon1)+str(year1)
a2=int('0x0B',16)
a3=int('0x2B',16)
a5=a2+a3+a4
checksum1=(hex(a5))[-2:]
r1='AA0B2B'+a1+checksum1+'55'
with Peripheral('C1:8F:CC:DC:57:19','random') as p:
        ch1=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
        val1=binascii.a2b_hex(r1)#取消定时
        ch1.write(val1)
##----------------------end------------------------------------------
def btn1_clicked():
        switch_staus="on"
        tk.messagebox.showinfo(title='提示',message='蓝牙插座已开启')
        with Peripheral('C1:8F:CC:DC:57:19','random') as p:
            ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
            val=binascii.a2b_hex('AA0630306655')
            ch.write(val)
            p.disconnect()
def btn2_clicked():
        switch_staus='off'
        tk.messagebox.showinfo(title='提示',message='蓝牙插座已关闭')
        with Peripheral('C1:8F:CC:DC:57:19','random') as p:
            ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
            val=binascii.a2b_hex('AA0630316755')
            ch.write(val)
            p.disconnect()
def btn3_clicked():
        tk.messagebox.showinfo(title='提示',message='请以XX时XX分的格式输入，例如定时1小时15分钟为0115')
        entry=tk.Entry(window,textvariable=d)
        entry.pack(fill=tk.X)
        btn7 = tk.Button(window, text = "确定关闭定时开始", activebackground='yellow',bg='hotpink',fg='black',command = btn7_clicked)#传值按键
        btn7.pack(fill=tk.X)
def btn7_clicked():
        on=d.get()
        a1=on[0:2]
        a2=on[2:4]
        a6='0x'+a1
        a9='0x'+a2
        a7=int(a6,16)
        a8=int(a9,16)
        a3=int('0x07',16)
        a4=int('0x31',16)
        a5=a7+a8+a3+a4
        checksum=hex(a5)[-2:]
        r='AA0731'+on+str(checksum)+'55'
        with Peripheral('C1:8F:CC:DC:57:19','random') as p:
                ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
                val=binascii.a2b_hex(r)
                ch.write(val)
                p.disconnect()     
def btn4_clicked():
        switch_staus='off'
        tk.messagebox.showinfo(title='提示',message='请以XX时XX分的格式输入，例如定时1小时15分钟为0115')
        entry=tk.Entry(window,textvariable=c)
        entry.pack(fill=tk.X)
        btn6 = tk.Button(window, text = "确定开启定时开始", activebackground='yellow',bg='hotpink',fg='black',command = btn6_clicked)#传值按键
        btn6.pack(fill=tk.X)
def btn6_clicked():        
        off=c.get()#按下去才get到entry的值
        a1=off[0:2]
        a2=off[2:4]
        a6='0x'+a1
        a9='0x'+a2
        a7=int(a6,16)
        a8=int(a9,16)
        a3=int('0x07',16)
        a4=int('0x35',16)
        a5=a7+a8+a3+a4
        checksum=hex(a5)[-2:]
        r='AA0735'+off+str(checksum)+'55'
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
def btn8_clicked():
        tk.messagebox.showinfo(title='提示',message='RTC时间同步校准成功')
        ##---------------------------动态检查和(checksum)计算--------------------------
        s=time.localtime()
        year=(s.tm_year)%100
        mon=  s. tm_mon
        day= s. tm_mday
        hour=s.tm_hour
        minute=s.tm_min
        sec=s.tm_sec
        a6='0x'+str(sec)
        a7='0x'+str(mon)
        a8='0x'+str(hour)
        a9='0x'+str(minute)
        a10='0x'+str(day)
        a11='0x'+str(year)
        a12=int(a10,16)
        a13=int(a9,16)
        a14=int(a8,16)
        a15=int(a7,16)
        a16=int(a6,16)
        a17=int(a11,16)
        a4=a12+a13+a14+a15+a16+a17
        year1=(s.tm_year)%100
        mon1="%02d" % s. tm_mon
        day1="%02d"% s. tm_mday
        hour1="%02d"% s.tm_hour
        minute1="%02d" %s.tm_min
        sec1="%02d"% s.tm_sec
        a1=str(sec1)+str(minute1)+str(hour1)+str(day1)+str(mon1)+str(year1)
        a2=int('0x0B',16)
        a3=int('0x2B',16)
        a5=a2+a3+a4
        checksum1=(hex(a5))[-2:]
        r='AA0B2B'+a1+checksum1+'55'
        with Peripheral('C1:8F:CC:DC:57:19','random') as p:
                ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
                val=binascii.a2b_hex(r)
                ch.write(val)
def btn10_clicked():
        switch_staus='off'
        tk.messagebox.showinfo(title='提示',message='预约定时开关请以月日时分格式输入，例如预约定时5月20日13时开启，5月21日22时5分关闭，那么请键入0520130005212205')
        entry=tk.Entry(window,textvariable=e)
        entry.pack(fill=tk.X)
        btn11 = tk.Button(window, text = "确定预约开启定时开始", activebackground='yellow',bg='hotpink',fg='black',command = btn11_clicked)#传值按键
        btn11.pack(fill=tk.X)
def btn11_clicked():
        X=e.get()
        a1=X[0:2]##起始月日时分
        a2=X[2:4]
        a3=X[4:6]
        a4=X[6:8]
        a5=X[8:10]##结束月日时分
        a6=X[10:12]
        a7=X[12:14]
        a8=X[14:16]
        a9=int('0X'+a1,16)
        a10=int('0X'+a2,16)
        a11=int('0X'+a3,16)
        a12=int('0X'+a4,16)
        a13=int('0X'+a5,16)
        a14=int('0X'+a6,16)
        a15=int('0X'+a7,16)
        a16=int('0X'+a8,16)
        a17=int('0X05',16)
        a18=int('0X34',16)
        a19=a1+a2+a3+a4+a5+a6+a7+a8
        checksum=(hex(a9+a10+a11+a12+a13+a14+a15+a16+a17+a18))[-2:]
        print(checksum)
        r='AA0534'+a19+checksum+'55'
        print(r)
        with Peripheral('C1:8F:CC:DC:57:19','random') as p:
                ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
                val=binascii.a2b_hex(r)
                ch.write(val)
##---------------------------------end-------------------------------------------------------
def btn9_clicked():
         tk.messagebox.showinfo(title='提示',message=time.strftime("%Y-%m-%d %H:%M:%S"))
##------------------------------實時時間顯示---------------------------
def tick():
    global time1
    # 从运行程序的计算机上面获取当前的系统时间
    time2 = time.strftime('%H:%M:%S')
    # 如果时间发生变化，代码自动更新显示的系统时间
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    clock.after(200, tick)
time1 = ''
chinese=1
english=0
def btn12_clicked():##英文語音提示
        global chinese,english
        english=1
        chinese=0
        tts = gTTS(text='Voice mode has been switched to English', lang='en')
        tts.save("hello.mp3")
        os.system('play hello.mp3')
        T.insert(END,'Voice mode has been switched to English\n')
def btn13_clicked():##中文語音提示
        global chinese,english
        chinese=1
        english=0
        tts = gTTS(text='已切換至中文語音提示模式', lang='zh-tw')
        tts.save("hello.mp3")
        os.system('play hello.mp3')
        T.insert(END,'已切換至中文語音提示模式\n')
##-------------------------end---------------------------------------------
##----------------------------------手勢控制-----------------------------------
t=0##用於判斷關閉函數的執行次數
t1=0##用於判斷開啟函數執行次數
a5=0
a6=0
ap=0
ad=0
@skywriter.flick()
def flick(start,finish):
    if(start=='west' and finish=='east'):
        T.insert(END,'插座已開啟\n')
        with Peripheral('C1:8F:CC:DC:57:19','random') as p:
                ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
                val=binascii.a2b_hex('AA0630306655')
                ch.write(val)
                p.disconnect()
                if(chinese==1):
                        tts = gTTS(text='插座已開啟', lang='zh-tw')
                        tts.save("hello.mp3")
                        os.system('play hello.mp3')
                if(english==1):
                        tts = gTTS(text='Socket turned on', lang='en')
                        tts.save("hello.mp3")
                        os.system('play hello.mp3')
    if(start=='east' and finish=='west'):
        T.insert(END,'插座已關閉\n')
        with Peripheral('C1:8F:CC:DC:57:19','random') as p: 
                ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
                val=binascii.a2b_hex('AA0630316755')
                ch.write(val)
                p.disconnect()
                if(chinese==1):
                        tts = gTTS(text='插座已關閉', lang='zh-tw')
                        tts.save("hello.mp3")
                        os.system('play hello.mp3')
                if(english==1):
                        tts = gTTS(text='Socket turned off', lang='en')
                        tts.save("hello.mp3")
                        os.system('play hello.mp3')
    if(start=='north' and finish=='south'):
                T.insert(END,'定時模式,向上點擊進入預約開啟模式，向下點擊進入預約關閉模式，觸摸中心退出定時模式\n')
                
                if(chinese==1):
                        tts = gTTS(text='定時模式,向上點擊進入預約開啟模式，向下點擊進入預約關閉模式', lang='zh-tw')
                        tts.save("hello.mp3")
                        os.system('play hello.mp3')
                if(english==1):
                        tts = gTTS(text=' timer mode, touch top entering timing start mode , thouch below entering timing off  mode', lang='en')
                        tts.save("hello.mp3")
                        os.system('play hello.mp3')
                @skywriter.touch()
                def touch(position):
                        print(position)
                        if(position=='south'):
                                T.insert(END,'預約關閉模式，向左點擊減少10分鐘定時，向右點擊增加10分鐘定時，觸摸中心退出模式\n')
                                if(chinese==1):
                                        tts = gTTS(text='預約關閉模式，向左點擊減少10分鐘定時，向右點擊增加10分鐘定時', lang='zh-tw')
                                        tts.save("hello.mp3")
                                        os.system('play hello.mp3')
                                if(english==1):
                                        tts = gTTS(text='subscribe shutdown mode, touch  left to  subtract 10 minutes , touch right to add 10 minutes ', lang='en')
                                        tts.save("hello.mp3")
                                        os.system('play hello.mp3')
                                @skywriter.touch()
                                def touch(position):
                                        global t,n1,a5,a6
                                        if(position=='west'):
                                                if(int(a6)>=10):
                                                        a6=a6-10
                                                elif(int(a5)==0):      
                                                        a6=0
                                                else:
                                                        a5=int(a5)-1
                                                        a6=50
                                        if(position=='east'):
                                                if(int(a6)>=60):
                                                        a6=int(a6)-60
                                                        a5=int(a5)+1
                                                        if(int(a5)>24):
                                                                T.insert(END,'超出最大設定時間\n')
                                                elif(int(a6)<50) :       
                                                        a6=int(a6)+10
                                                else:
                                                        a6=0
                                                        a5=int(a5)+1
                                        finish=time.localtime()
                                        hour1=finish.tm_hour
                                        minute1=finish.tm_min
                                        sec1=finish.tm_sec
                                        a1='AA'
                                        a2='0x07'
                                        a3='0x31'
                                        a4='00'  
                                        a7=int(a2,16)
                                        a8=int(a3,16)
                                        a9=int(str(a5),16)
                                        a10=int(str(a6),16)
                                        checksum=(hex(a7+a8+a9+a10))[-2:]
                                        if(int(a6)==0):
                                                a6='00'
                                        if(int(a5)<10 and len(str(a5))==1):
                                                a5='0'+str(a5)
                                        print(a6)
                                        print(str(a5))
                                        r='AA0731'+str(a5)+str(a6)+checksum+'55'
                                        print(r)
                                        T.insert(END,'您已定時:')
                                        T.insert(INSERT,a5)
                                        T.insert(INSERT,'時')
                                        T.insert(INSERT,a6)
                                        T.insert(INSERT,'分')
                                        T.insert(INSERT,'后關閉插座\n')
                                        e1=int(hour1)+int(a5)
                                        e2=int(minute1)+int(a6)
                                        e3=int(sec1)
                                        if(e2>=60):
                                                e1=e1+1
                                                if(e1>=24):
                                                        T.insert(END,'定時超過最大時限')
                                                        if(chinese==1):
                                                                tts = gTTS(text='定時超過最大時限', lang='zh-tw')
                                                                tts.save("hello.mp3")
                                                                os.system('play hello.mp3')
                                                        if(english==1):
                                                                tts = gTTS(text='the time you subscribe is overflow', lang='en')
                                                                tts.save("hello.mp3")
                                                                os.system('play hello.mp3')
                                                e2=e2-60
                                        T.insert(END,'預計于')
                                        T.insert(INSERT,e1)
                                        T.insert(INSERT,'時')
                                        T.insert(INSERT,e2)
                                        T.insert(INSERT,'分')
                                        T.insert(INSERT,'關閉插座\n')
                                        h3='預計于'+str(int(e1))+'時'+str(int(e2))+'分'+str(int(e3))+'秒'+'關閉插座'
                                        h4='Forecast in'+str(int(e1))+'hours'+str(int(e2))+'minutes'+str(int(e3))+'seconds'+'關閉插座'
                                        if(a5==0):
                                                h1=str('您已定時'+str(int(a6))+'分鐘'+'后關閉插座')
                                                h2=str('You have been timing '+str(int(a6))+'minutes'+'to shut down the socket')
                                        elif(a6==0):
                                                h1=str('您已定時'+str(int(a5))+'小時'+'后關閉插座')
                                                h2=str('You have been timing '+str(int(a5))+'hours'+'minutes'+'to shut down the socket')
                                        else:
                                                h1=str('您已定時'+str(int(a5))+'小時'+str(int(a6))+'分鐘'+'后關閉插座')
                                                h2=str('You have been timing '+str(int(a5))+'hours'+str(int(a6))+'minutes'+'to shut down the socket')
                                        if(chinese==1):
                                                tts = gTTS(text=h1, lang='zh-tw')
                                                tts.save("hello.mp3")
                                                os.system('play hello.mp3')
                                                tts = gTTS(text=h3, lang='zh-tw')
                                                tts.save("hello.mp3")
                                                os.system('play hello.mp3')
                                        if(english==1):
                                                tts = gTTS(text=h2, lang='en')
                                                tts.save("hello.mp3")
                                                os.system('play hello.mp3')
                                                tts = gTTS(text=h4, lang='en')
                                                tts.save("hello.mp3")
                                                os.system('play hello.mp3')
                                        with Peripheral('C1:8F:CC:DC:57:19','random') as p:
                                            ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
                                            val=binascii.a2b_hex(r)
                                            ch.write(val)
                                            p.disconnect()
                                            T.insert(END,'完成寫入\n')
                        if(position=='north'):
                                T.insert(END,'預約開啟模式，向左點擊減少10分鐘定時，向右點擊增加10分鐘定時，觸摸中心退出模式\n')
                                if(chinese==1):
                                        tts = gTTS(text='預約開啟模式，向左點擊減少10分鐘定時，向右點擊增加10分鐘定時', lang='zh-tw')
                                        tts.save("hello.mp3")
                                        os.system('play hello.mp3')
                                if(english==1):
                                        tts = gTTS(text='subscribe start mode, touch  left to  subtract 10 minutes , touch right to add 10 minutes ', lang='en')
                                        tts.save("hello.mp3")
                                        os.system('play hello.mp3')
                                @skywriter.touch()
                                def touch(position):
                                        global t,n1,ap,ad
                                        if(position=='west'):
                                                if(int(ad)>=10):
                                                        ad=ad-10
                                                elif(int(ap)==0):      
                                                        ad=0
                                                else:
                                                        ap=int(ap)-1
                                                        ad=50
                                        if(position=='east'):
                                                if(int(ad)>=60):
                                                        ad=int(ad)-60
                                                        ap=int(ap)+1
                                                        if(int(ap)>24):
                                                                T.insert(END,'超出最大設定時間\n')
                                                elif(int(ad)<50) :       
                                                        ad=int(ad)+10
                                                else:
                                                        ad=0
                                                        ap=int(ap)+1
                                        finish=time.localtime()
                                        hour2=finish.tm_hour
                                        minute2=finish.tm_min
                                        sec2=finish.tm_sec
                                        a1='AA'
                                        a2='0x07'
                                        a3='0x35'
                                        a4='00'
                                        a7=int(a2,16)
                                        a8=int(a3,16)
                                        a9=int(str(ap),16)
                                        a10=int(str(ad),16)
                                        checksum=(hex(a7+a8+a9+a10))[-2:]
                                        if(int(ad)==0):
                                                ad='00'
                                        if(int(ap)<10 and len(str(ap))==1):
                                                ap='0'+str(ap)
                                        print(ad)
                                        print(str(ap))
                                        r='AA0735'+str(ap)+str(ad)+checksum+'55'
                                        e4=int(hour2)+int(ap)
                                        e5=int(minute2)+int(ad)
                                        e6=int(sec2)
                                        if(e5>=60):
                                                e4=e4+1
                                                if(e4>=24):
                                                        T.insert(END,'定時超過最大時限')
                                                        if(chinese==1):
                                                                tts = gTTS(text='定時超過最大時限', lang='zh-tw')
                                                                tts.save("hello.mp3")
                                                                os.system('play hello.mp3')
                                                        if(english==1):
                                                                tts = gTTS(text='the time you subscribe is overflow', lang='en')
                                                                tts.save("hello.mp3")
                                                                os.system('play hello.mp3')
                                                e5=e5-60
                                        T.insert(END,'您已定時:')
                                        T.insert(INSERT,ap)
                                        T.insert(INSERT,'小時')
                                        T.insert(INSERT,ad)
                                        T.insert(INSERT,'分鐘')
                                        T.insert(INSERT,'后開啟插座\n')
                                        T.insert(END,'預計于')
                                        T.insert(INSERT,e4)
                                        T.insert(INSERT,'時')
                                        T.insert(INSERT,e5)
                                        T.insert(INSERT,'分')
                                        T.insert(INSERT,'開啟插座\n')
                                        h5='預計于'+str(int(e4))+'時'+str(int(e5))+'分'+str(int(e6))+'秒'+'開啟插座'
                                        h6='Forecast in'+str(int(e4))+'hours'+str(int(e5))+'minutes'+str(int(e6))+'seconds'+'開啟插座'
                                        if(ad==0):
                                                h1=str('您已定時'+str(int(ad))+'分鐘'+'后開啟插座')
                                                h2=str('You have been timing '+str(int(ad))+'minutes'+'to shut down the socket')
                                        elif(ap==0):
                                                h1=str('您已定時'+str(int(ap))+'小時'+'后開啟插座')
                                                h2=str('You have been timing '+str(int(ap))+'hours'+'minutes'+'to shut down the socket')
                                        else:
                                                h1=str('您已定時'+str(int(ap))+'小時'+str(int(ad))+'分鐘'+'后開啟插座')
                                                h2=str('You have been timing '+str(int(ap))+'hours'+str(int(ad))+'minutes'+'to shut down the socket')
                                        if(chinese==1):
                                                tts = gTTS(text=h1, lang='zh-tw')
                                                tts.save("hello.mp3")
                                                os.system('play hello.mp3')
                                                tts = gTTS(text=h5, lang='zh-tw')
                                                tts.save("hello.mp3")
                                                os.system('play hello.mp3')
                                        if(english==1):
                                                tts = gTTS(text=h2, lang='en')
                                                tts.save("hello.mp3")
                                                os.system('play hello.mp3')
                                                tts = gTTS(text=h6, lang='en')
                                                tts.save("hello.mp3")
                                                os.system('play hello.mp3')
                                        with Peripheral('C1:8F:CC:DC:57:19','random') as p:
                                                ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
                                                val=binascii.a2b_hex(r)
                                                ch.write(val)
                                                p.disconnect()
                                                T.insert(END,'完成寫入\n')

##-----------------------按鍵和佈局---------------------------------------
photo = tk.PhotoImage(file="pig.png")#file：t图片路径
imgLabel = tk.Label(window,image=photo)#把图片整合到标签类中
imgLabel.pack(side=tk.RIGHT)#自动对齐
photo1 = tk.PhotoImage(file="timg1.png")#file：t图片路径
imgLabel1 = tk.Label(window,image=photo1)#把图片整合到标签类中
imgLabel1.pack(side=tk.TOP)#自动对齐
w = Label(window, text="designed by su yu, in May 2018!",fg='red')  
w.pack()  
clock = Label(window, font=('times', 20, 'bold'))
clock.pack(fill=tk.X)
tick()
w1= Label(window, text="語音選項",fg='black')
w1.pack()
btn12 = tk.Button(window, text = "英文語音提示",activebackground='yellow', bg='pink',fg='black',command = btn12_clicked)
btn12.pack(fill=tk.X)
btn13 = tk.Button(window, text = "中文語音提示",activebackground='yellow', bg='pink',fg='black',command = btn13_clicked)
btn13.pack(fill=tk.X)
w2= Label(window, text="控制功能選項",fg='black')
w2.pack()
btn1 = tk.Button(window, text = "蓝牙插座开启", activebackground='yellow',bg='pink',fg='black',command = btn1_clicked)
btn1.pack(fill = tk.X)
btn2 = tk.Button(window, text = "蓝牙插座关闭", activebackground='yellow',bg='pink',fg='black',command = btn2_clicked)
btn2.pack(fill=tk.X)
btn4 = tk.Button(window, text = "定时开启插座", activebackground='yellow',bg='pink',fg='black',command = btn4_clicked)
btn4.pack(fill=tk.X)
btn3 = tk.Button(window, text = "定时关闭插座",activebackground='yellow', bg='pink',fg='black',command = btn3_clicked)
btn3.pack(fill=tk.X)
btn8 = tk.Button(window, text = "插座RTC时间同步校准", activebackground='yellow',bg='pink',fg='black',command = btn8_clicked)
btn8.pack(fill=tk.X)
btn9 = tk.Button(window, text = "查询插座RTC时间", activebackground='yellow',bg='pink',fg='black',command = btn9_clicked)
btn9.pack(fill=tk.X)
btn10 = tk.Button(window, text = "预约定时开关（长时）", activebackground='yellow',bg='pink',fg='black',command = btn10_clicked)
btn10.pack(fill=tk.X)
btn5 = tk.Button(window, text = "取消预约定时", activebackground='yellow',bg='pink',fg='black',command = btn5_clicked)
btn5.pack(fill=tk.X)
T.pack(fill=tk.X)
##--------------------------------------end------------------------------------
window.mainloop()
