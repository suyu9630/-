import tkinter as tk
from tkinter import * 
from tkinter import messagebox as msgbox
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
        tk.messagebox.showinfo('提示','蓝牙插座已开启')
        with Peripheral('C1:8F:CC:DC:57:19','random') as p:
            ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
            val=binascii.a2b_hex('AA0630306655')
            ch.write(val)
            p.disconnect()
            T.insert(END,'藍牙插座已開啟\n')
def btn2_clicked():
        switch_staus='off'
        tk.messagebox.showinfo(title='提示',message='蓝牙插座已关闭')
        with Peripheral('C1:8F:CC:DC:57:19','random') as p:
            ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
            val=binascii.a2b_hex('AA0630316755')
            ch.write(val)
            p.disconnect()
            T.insert(END,'藍牙插座已關閉\n')
def btn3_clicked():
        tk.messagebox.showinfo(title='提示',message='请以XX时XX分的格式输入，例如定时1小时15分钟为0115')
        entry=tk.Entry(window,textvariable=d)
        entry.pack(fill=tk.X)
        btn7 = tk.Button(window, text = "确定关闭定时开始",activebackground='yellow', bg='hotpink',fg='black',command = btn7_clicked)#传值按键
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
        btn11 = tk.Button(window, text = "确定预约开启定时开始", bg='hotpink',fg='black',command = btn11_clicked)#传值按键
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
##-------------------------end---------------------------------------------
##----------------------------------手勢控制-----------------------------------
t=0##用於判斷關閉函數的執行次數
t1=0##用於判斷開啟函數執行次數
a5=0
a6=0
ap=0
ad=0
hour4=0
sec4=0
minute4=0
houru2=0
secu2=0
minuteu2=0
houru4=0
secu4=0
minuteu4=0
houru3=0
secu3=0
minuteu3=0
hour2=0
sec2=0
minute2=0
switch1=1
switch2=1
switch3=1
xc=1
xcc=0
hour3=0
minute3=0
sec3=0
tn=0
tm=0
tns=0
#--------
hour31=0
minute31=0
sec31=0
hour311=0
minute311=0
sec311=0
#---------
@skywriter.flick()
def flick(start,finish):
    if(start=='west' and finish=='east'):
        with Peripheral('C1:8F:CC:DC:57:19','random') as p:
            ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
            val=binascii.a2b_hex('AA0630306655')
            ch.write(val)
            p.disconnect()
            T.insert(END,'藍牙插座已開啟\n')
    if(start=='east' and finish=='west'):
        with Peripheral('C1:8F:CC:DC:57:19','random') as p:
            ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
            val=binascii.a2b_hex('AA0630316755')
            ch.write(val)
            p.disconnect()
            T.insert(END,'藍牙插座已關閉\n')
    if(start=='north' and finish=='south'):
                T.insert(END,'進入定時模式,向上點擊進入定時開啟設定，向下點擊進入定時關閉設定，觸摸中心退出定時模式\n')
                @skywriter.touch()
                def touch(position):
                        print(position)
                        if(position=='south'):
                                T.insert(END,'進入關閉定時模式，向左點擊減少10分鐘定時，向右點擊增加10分鐘定時，觸摸中心退出模式\n')
                                @skywriter.touch()
                                def touch(position):
                                        global t,n1,a5,a6,switch1,switch2,switch3,switch4,tn,tm,xc,xcc,hour31,hour311,sec31,sec311,minute31,minute311
                                        t=t+1##控制執行次數
                                        if(position=='west'):
                                                global start,hour2,minute2,sec2,hour4,hour3,sec3,minute3,minute4,sec4,startu,houru2,minuteu2,secu2,houru4,houru3,secu3,minuteu3,minuteu4,secu4,tns
                                                switch1=0##switch賦值0改變switch的值證明進行過函數
                                                tn=tn+1
                                                tns=1
                                                if(int(a6)>=10):
                                                        a6=a6-10
                                                elif(int(a5)==0):      
                                                        a6=0
                                                else:
                                                        a5=int(a5)-1
                                                        a6=int(a6)+50
                                                if(switch2==0 and t!=1):
                                                        tns=tns-1##控制切換次數
                                                        switch2=1##置1還原變量switch，作下次判斷
                                                        finish=time.localtime()
                                                        hour3=finish.tm_hour
                                                        minute3=finish.tm_min
                                                        sec3=finish.tm_sec
                                                        print('進入左切換')
                                                        if(tm>1):##減去切換的時間減右邊
                                                                if(hour3>=houru3 and minute3>=minuteu3 and sec3<=secu3):
                                                                        hour4=hour3-houru3
                                                                        minute4=minute3-minuteu3
                                                                        if(secu3==sec3): 
                                                                                minute4=minute4
                                                                        elif(minute4==0 and hour4>0):
                                                                                hour4=hour4-1
                                                                                minute4=59
                                                                                sec4=sec3-secu3+60
                                                                        else:
                                                                                minute4=minute4-1
                                                                                sec4=sec3-secu3+60
                                                                        print('當前時間',hour3,minute3,sec3)
                                                                        print('時差',hour4,minute4,sec4)
                                                                        print('a1')
                                                                if(hour3>=houru3 and minute3<=minuteu3 and sec3>secu3):
                                                                        hour4=hour3-houru3
                                                                        if(hour4==0 and minuteu3==minute3):
                                                                                hour4=0
                                                                                minute4=minuteu3-minute3
                                                                                sec4=sec3-secu3
                                                                        else:
                                                                                hour4=hour4-1
                                                                                minute=60+minute3-minuteu3
                                                                                sec4=sec3-secu3
                                                                        print('當前時間',hour3,minute3,sec3)
                                                                        print('時差',hour4,minute4,sec4)
                                                                        print('b1')
                                                                if(hour3>=houru3 and minute3<minuteu3 and sec3<=secu3):        
                                                                        hour4=hour3-houru3
                                                                        hour4=hour4-1
                                                                        minute4=60+minute3-minuteu3-1
                                                                        sec4=sec3-secu3+60
                                                                        if(sec4>=60):
                                                                                sec4=sec4-60
                                                                                minute4=minute4+1
                                                                        print('當前時間',hour3,minute3,sec3)
                                                                        print('時差',hour4,minute4,sec4)
                                                                        print('c1')
                                                                if(hour3>=houru3 and minute3>minuteu3 and sec3>secu3):
                                                                        hour4=hour3-houru3
                                                                        minute4=minute3-minuteu3
                                                                        sec4=sec3-secu3
                                                                        print('當前時間',hour3,minute3,sec3)
                                                                        print('時差',hour4,minute4,sec4)
                                                                        print('d1')
                                                        elif(tm==1):
                                                                if(hour3>=houru3 and minute3>=minuteu3 and sec3<=secu3):
                                                                        hour4=hour3-houru3
                                                                        minute4=minute3-minuteu3
                                                                        if(secu3==sec3): 
                                                                                minute4=minute4
                                                                                sec4=0
                                                                        elif(minute4==0 and hour4>0):
                                                                                hour4=hour4-1
                                                                                minute4=59
                                                                                sec4=sec3-secu3+60
                                                                        else:
                                                                                minute4=minute4-1
                                                                                sec4=sec3-secu3+60
                                                                        print('相反面首次按下')
                                                                        print('當前時間',hour3,minute3,sec3)
                                                                        print('時差',hour4,minute4,sec4)
                                                                        print('a11')
                                                                if(hour3>=houru3 and minute3<=minuteu3 and sec3>secu3):
                                                                        hour4=hour3-houru3
                                                                        if(hour4==0 and minuteu3==minute3):
                                                                                hour4=0
                                                                                minute4=minute3-minuteu3
                                                                                sec4=sec3-secu3
                                                                        else:
                                                                                hour4=hour4-1
                                                                                minute4=60+minute3-minuteu3
                                                                                sec4=sec3-secu3
                                                                        print('相反面首次按下')
                                                                        print('當前時間',hour3,minute3,sec3)
                                                                        print('時差',hour4,minute4,sec4)
                                                                        print('b11')
                                                                if(hour3>=houru3 and minute3<minuteu3 and sec3<=secu3):        
                                                                        hour4=hour3-houru3
                                                                        hour4=hour4-1
                                                                        minute4=60+minute3-minuteu3-1
                                                                        sec4=sec3-secu3+60
                                                                        print('相反面首次按下')
                                                                        print('當前時間',hour3,minute3,sec3)
                                                                        print('時差',hour4,minute4,sec4)
                                                                        print('c11')
                                                        hour31=hour3
                                                        minute31=minute3
                                                        sec31=sec3
                                                        a5=int(a5)+int(hour4)
                                                        a6=int(a6)+int(minute4)
                                                        print(a5,a6)
                                                if(t==1):##首次執行的時間記錄
                                                        switch3=0
                                                        start=time.localtime()
                                                        hour2=start.tm_hour
                                                        minute2=start.tm_min
                                                        sec2=start.tm_sec                                               
                                                        print('首次執行時間',hour2,minute2,sec2)
                                                        T.insert(END,'首次執行時間')
                                                        T.insert(INSERT,hour2)
                                                        T.insert(INSERT,'時')
                                                        T.insert(INSERT,minute2)
                                                        T.insert(INSERT,'分')
                                                        T.insert(INSERT,sec2)
                                                        T.insert(INSERT,'秒\n')
                                                        hour31=hour2
                                                        sec31=sec2
                                                        minute31=minute2
                                                elif(tns==1):            
                                                        finish=time.localtime()
                                                        hour311=finish.tm_hour
                                                        minute311=finish.tm_min
                                                        sec311=finish.tm_sec
                                                        print('上次時間',hour31,minute31,sec31)
                                                        print('當前時間',hour311,minute311,sec311)
                                                        if(switch3==1):  
                                                                if(hour311>=hour31 and minute311>=minute31 and sec311<=sec31):
                                                                        hour4=hour311-hour31
                                                                        minute4=minute311-minute31
                                                                        if(sec311==sec31): 
                                                                                minute4=minute4
                                                                        elif(minute4==0 and hour4>0):
                                                                                hour4=hour4-1
                                                                                minute4=59
                                                                                sec4=sec311-sec31+60
                                                                        else:
                                                                                minute4=minute4-1
                                                                                sec4=sec311-sec31+60
                                                                        print('當前時間',hour311,minute311,sec311)
                                                                        print('時差',hour4,minute4,sec4)
                                                                        print('a12212')
                                                                if(hour311>=hour31 and minute311<=minute31 and sec311>sec31):
                                                                        hour4=hour311-hour31
                                                                        if(hour4==0 and minute311==minute31):
                                                                                hour4=0
                                                                                minute4=minute311-minute31
                                                                                sec4=sec311-sec31
                                                                        else:
                                                                                hour4=hour4-1
                                                                                minute=60+minute311-minute31
                                                                                sec4=sec31-sec31
                                                                        print('當前時間',hour311,minute311,sec311)
                                                                        print('時差',hour4,minute4,sec4)
                                                                        print('b1212')
                                                                if(hour311>=hour31 and minute311<minute31 and sec311<=sec31):        
                                                                        hour4=hour311-hour31
                                                                        hour4=hour4-1
                                                                        minute4=60+minute311-minute31-1
                                                                        sec4=sec311-sec31+60
                                                                        print('當前時間',hour311,minute311,sec311)
                                                                        print('時差',hour4,minute4,sec4)
                                                                        print('c1212')
                                                                if(hour311>=hour31 and minute311>minute31 and sec311>sec31):
                                                                        hour4=hour311-hour31
                                                                        minute4=minute311-minute31
                                                                        sec4=sec311-sec31
                                                                        print('當前時間',hour311,minute311,sec311)
                                                                        print('時差',hour4,minute4,sec4)
                                                                        print('d1212')
                                                                hour31=hour311##末時間賦值初時間
                                                                minute3=minute311
                                                                sec31=sec311
                                                                print(hour31,minute3,sec31)
                                                ##-----減去首次時間的部分，并還原switch3的值，跳出對首次的減法，引導連續自減
                                                if(switch3==0):
                                                        if(hour31>=hour2 and minute31>=minute2 and sec31<=sec2):
                                                                hour4=hour31-hour2
                                                                minute4=minute31-minute2
                                                                if(sec31==sec2): 
                                                                        minute4=minute4
                                                                elif(minute4==0 and hour4>0):
                                                                        hour4=hour4-1
                                                                        minute4=59
                                                                        sec4=sec31-sec2+60
                                                                else:
                                                                        minute4=minute4-1
                                                                        sec4=sec31-sec2+60
                                                                        print('當前時間',hour31,minute31,sec31)
                                                                        print('時差1',hour4,minute4,sec4)
                                                                        print('a12212')
                                                        if(hour31>=hour2 and minute31<=minute2 and sec31>sec2):
                                                                hour4=hour31-hour2
                                                                if(hour4==0 and minute31==minute2):
                                                                        hour4=0
                                                                        minute4=minute31-minute2
                                                                        sec4=sec31-sec2
                                                                else:
                                                                        hour4=hour4-1
                                                                        minute=60+minute31-minute2
                                                                        sec4=sec31-sec2
                                                                print('當前時間',hour31,minute31,sec31)
                                                                print('時差2',hour4,minute4,sec4)
                                                                print('b1212')
                                                        if(hour31>=hour2 and minute31<minute2 and sec31<=sec2):        
                                                                hour4=hour31-hour2
                                                                hour4=hour4-1
                                                                minute4=60+minute31-minute2-1
                                                                sec4=sec31-sec2+60
                                                                print('當前時間3',hour31,minute31,sec31)
                                                                print('時差',hour4,minute4,sec4)
                                                                print('c1212')
                                                        if(hour31>=hour2 and minute31>minute2 and sec31>sec2):
                                                                hour4=hour31-hour2
                                                                minute4=minute31-minute2
                                                                sec4=sec31-sec2
                                                                print('當前時間4',hour31,minute31,sec31)
                                                                print('時差',hour4,minute4,sec4)
                                                                print('d12123')
                                                        switch3=1##還原變量引導連續自減
                                                        ####--------------------------------------------------------------------
                                        
                                                        
                                                        
                                                #start=time.localtime()##在首次執行后，求得和第一次的時間差值，并初始化第一次的時間
                                                #hour2=start.tm_hour
                                                #minute2=start.tm_min
                                                #sec2=start.tm_sec
                                                
                                                if(int(a6)>0):
                                                        a5=int(a5)+int(hour4)
                                                        a6=int(a6)+int(minute4)
                                                if(int(a5)==0 and int(a6)==0):
                                                        a5=0
                                                        a6=0
                                                if(int(a6)>=60):
                                                        a6=int(a6)-60
                                                        a5=int(a5)+1
                                                print(a5,a6)
                                                T.insert(END,'距離您上次操作經過了')
                                                T.insert(INSERT,hour4)
                                                T.insert(INSERT,'時')
                                                T.insert(INSERT,minute4)
                                                T.insert(INSERT,'分')
                                                T.insert(INSERT,sec4)
                                                T.insert(INSERT,'秒\n')
                                                T.insert(END,'您已定時:')
                                                T.insert(INSERT,a5)
                                                T.insert(INSERT,'時')
                                                T.insert(INSERT,a6)
                                                T.insert(INSERT,'分')
                                                T.insert(INSERT,'后關閉插座\n')
                                ##west============================================

                                        if(position=='east'):
                                                global startu,houru2,secu2                  
                                                xo=2
                                                tns=0
                                                if(int(a6)<=50):
                                                        a6=int(a6)+10
                                                        xo=1
                                                        if(int(a6)>=60):
                                                                a6=int(a6)-60
                                                                a5=int(a5)+1                          
                                                if(int(a6)>50 and xo!=1):
                                                        a6=int(a6)-50
                                                        a5=int(a5)+1
                                                if(int(a5)>24):
                                                        T.insert(END,'超出最大設定時間\n')                          
                                                print('我是執行后普通自增的a5,a6',a5,a6)
                                                switch2=0##switch賦值0改變switch的值證明進行過函數
                                                tm=tm+1
                                                print('我是tn',tn)
                                                if(xcc==5 and tn<2):##XCC變量用來驗證是否是第一次按下同側的第二下,tn變量轉向引導連續自增
                                                                finish=time.localtime()
                                                                hour3=finish.tm_hour
                                                                minute3=finish.tm_min
                                                                sec3=finish.tm_sec        
                                                                print('進入13號')
                                                                print('當前時間',houru3,minuteu3,secu3)
                                                                print('當前時間',hour3,minute3,sec3)
                                                                if(hour3>=houru3 and minute3>=minuteu3 and sec3<=secu3):
                                                                        houru4=hour3-houru3
                                                                        minuteu4=minute3-minuteu3
                                                                        if(secu3==sec3): 
                                                                                minuteu4=minuteu4
                                                                        elif(minuteu4==0 and houru4>0):
                                                                                houru4=houru4-1
                                                                                minuteu4=59
                                                                                secu4=sec3-secu3+60
                                                                        else:
                                                                                minuteu4=minuteu4-1
                                                                                secu4=sec3-secu3+60
                                                                        print('當前時間',houru3,minuteu3,secu3)
                                                                        print('時差',houru4,minuteu4,secu4)
                                                                        print('a13')
                                                                if(hour3>=houru3 and minute3<minuteu3 and sec3>secu3):
                                                                        houru4=hour3-houru3
                                                                        if(houru4==0):
                                                                                houru4=0
                                                                                minuteu4=minute3-minuteu3
                                                                                secu4=sec3-secu3
                                                                        else:
                                                                                houru4=houru4-1
                                                                                minuteu4=60+minute3-minuteu3
                                                                                secu4=sec3-secu3
                                                                        print('當前時間',houru3,minuteu3,secu3)
                                                                        print('時差',houru4,minuteu4,secu4)
                                                                        print('b13')
                                                                if(hour3>=houru3 and minute3<minuteu3 and sec3<=secu3):        
                                                                        houru4=hour3-houru3
                                                                        houru4=houru4-1
                                                                        minuteu4=60+minute3-minuteu3-1
                                                                        secu4=sec3-secu3+60
                                                                        print('當前時間',houru3,minuteu3,secu3)
                                                                        print('時差',houru4,minuteu4,secu4)
                                                                        print('c13')
                                                                if(hour3>=houru3 and minute3>=minuteu3 and sec3>=secu3):
                                                                        houru4=hour3-houru3
                                                                        minuteu4=minute3-minuteu3
                                                                        secu4=sec3-secu3
                                                                        print('當前時間',houru3,minuteu3,secu3)
                                                                        print('時差',houru4,minuteu4,secu4)
                                                                        print('c133')
                                                                houru3=finish.tm_hour##時間記錄并初始化被減時間
                                                                minuteu3=finish.tm_min
                                                                secu3=finish.tm_sec 
                                                                a5=int(a5)+int(houru4)
                                                                a6=int(a6)+int(minuteu4)
                                                                print(a5,a6)
                                                                
                                                if(switch1==0):
                                                        switch1=1##置1還原變量switch，作下次判斷             
                                                        print('進入右切換')
                                                        xcc=5
                                                        ##再判斷對方是不是首次按下，用t進行控制
                                                        if(tn>1): 
                                                                finish=time.localtime()
                                                                houru3=finish.tm_hour
                                                                minuteu3=finish.tm_min
                                                                secu3=finish.tm_sec            
                                                                print('進入1號')
                                                                print(houru3,minuteu3,secu3)
                                                                print(hour3,minute3,sec3)
                                                                if(houru3>=hour3 and minuteu3>=minute3 and secu3<=sec3):
                                                                        houru4=houru3-hour3
                                                                        minuteu4=minuteu3-minute3
                                                                        if(secu3==sec3): 
                                                                                minuteu4=minuteu4
                                                                        elif(minuteu4==0 and houru4>0):
                                                                                houru4=houru4-1
                                                                                minuteu4=59
                                                                                secu4=secu3-sec3+60
                                                                        else:
                                                                                minuteu4=minuteu4-1
                                                                                secu4=secu3-sec3+60
                                                                        print('當前時間',houru3,minuteu3,secu3)
                                                                        print('時差',houru4,minuteu4,secu4)
                                                                        print('a13')
                                                                if(houru3>=hour3 and minuteu3<=minute3 and secu3>sec3):
                                                                        houru4=houru3-hour3
                                                                        if(houru4==0 and minuteu3==minute3):
                                                                                houru4=0
                                                                                minuteu4=minuteu3-minute3
                                                                                secu4=secu3-sec3
                                                                        else:
                                                                                houru4=houru4-1
                                                                                minuteu=60+minuteu3-minute3
                                                                                secu4=secu3-sec3
                                                                        print('當前時間',houru3,minuteu3,secu3)
                                                                        print('時差',houru4,minuteu4,secu4)
                                                                        print('b13')
                                                                if(houru3>=hour3 and minuteu3<minute3 and sec3u<=sec3):        
                                                                        houru4=houru3-hour3
                                                                        houru4=houru4-1
                                                                        minuteu4=60+minuteu3-minute3-1
                                                                        secu4=secu3-sec3+60
                                                                        print('當前時間',houru3,minuteu3,secu3)
                                                                        print('時差',houru4,minuteu4,secu4)
                                                                        print('c13')
                                                                a5=int(a5)+int(houru4)
                                                                a6=int(a6)+int(minuteu4)
                                                                if(len(str(a5))==1):
                                                                        a5='0'+str(a5)
                                                                if(len(str(a6))==1):
                                                                        a6='0'+str(a6)
                                                        elif(tn==1):##123
                                                                hour3=hour311
                                                                minute3=minute311
                                                                sec3=sec311
                                                                print('進入2號')
                                                                finish=time.localtime()
                                                                houru3=finish.tm_hour
                                                                minuteu3=finish.tm_min
                                                                secu3=finish.tm_sec
                                                                print(hour2,minute2,sec2)
                                                                print(houru3,minuteu3,secu3)
                                                                if(houru3>=hour2 and minuteu3>=minute2 and secu3<=sec2):
                                                                        houru4=houru3-hour2
                                                                        minuteu4=minuteu3-minute2
                                                                        if(secu3==sec2): 
                                                                                minuteu4=minuteu4
                                                                                secu4=0
                                                                        elif(minuteu4==0 and houru4>0):
                                                                                houru4=houru4-1
                                                                                minuteu4=59
                                                                                secu4=secu3-sec2+60
                                                                        else:
                                                                                minuteu4=minuteu4-1
                                                                                secu4=secu3-sec2+60
                                                                        print('相反面首次按下')
                                                                        print('當前時間',houru3,minuteu3,secu3)
                                                                        print('時差',houru4,minuteu4,secu4)
                                                                        print('a113')
                                                                if(houru3>=hour2 and minuteu3<=minute2 and secu3>sec2):
                                                                        houru4=houru3-hour2
                                                                        if(houru4==0 and minuteu3==minute2):
                                                                                houru4=0
                                                                                minuteu4=minuteu3-minute2
                                                                                secu4=secu3-sec2
                                                                        else:
                                                                                houru4=houru4-1
                                                                                minuteu=60+minuteu3-minute2
                                                                                secu4=secu3-sec2
                                                                        print('相反面首次按下')
                                                                        print('當前時間',houru3,minuteu3,secu3)
                                                                        print('時差',houru4,minuteu4,secu4)
                                                                        print('b113')
                                                                if(houru3>=hour2 and minuteu3<minute2 and secu3<=sec2):        
                                                                        houru4=houru3-hour2
                                                                        houru4=houru4-1
                                                                        minuteu4=60+minuteu3-minute2-1
                                                                        secu4=secu3-sec2+60
                                                                        print('相反面首次按下')
                                                                        print('當前時間',houru3,minuteu3,secu3)
                                                                        print('時差',houru4,minuteu4,secu4)
                                                                        print('c113')
                                                                if(houru3>=hour2 and minuteu3>minute2 and secu3>sec2):
                                                                        houru4=houru3-hour2
                                                                        minuteu4=minuteu3-minute2
                                                                        secu4=secu3-sec2
                                                                        print('當前時間',houru3,minuteu3,secu3)
                                                                        print('時差',houru4,minuteu4,secu4)
                                                                        print('d113')
                                                                ##減方首次按下不做加減
                                                        xc=0
                                                        xcc=0
                                                
                                                if(t==1):##首次執行的時間記錄
                                                        print('進入3號')
                                                        startu=time.localtime()
                                                        houru2=startu.tm_hour
                                                        minuteu2=startu.tm_min
                                                        secu2=startu.tm_sec                                               
                                                        T.insert(END,'首次執行時間')
                                                        T.insert(INSERT,houru2)
                                                        T.insert(INSERT,'時')
                                                        T.insert(INSERT,minuteu2)
                                                        T.insert(INSERT,'分')
                                                        T.insert(INSERT,secu2)
                                                        T.insert(INSERT,'秒\n')
                                                        print('無切換首次執行時間',houru2,minuteu2,secu2)
                                                        print(t)
                                                        print(xc)
                                                elif(xc!=0):##連續自增的時間算法
                                                        xc=1
                                                        print('進入4號')
                                                        ##檢查無誤，功能完成-----------------------------------
                                                        print(t)
                                                        finish=time.localtime()
                                                        houru3=finish.tm_hour
                                                        minuteu3=finish.tm_min
                                                        secu3=finish.tm_sec
                                                        print('當前時間a',houru3,minuteu3,secu3)
                                                        print('上次時間',houru2,minuteu2,secu2)
                                                        if(houru3>=houru2 and minuteu3>=minuteu2 and secu3<=secu2):
                                                                houru4=houru3-houru2
                                                                minuteu4=minuteu3-minuteu2
                                                                if(secu3==secu2): 
                                                                        minuteu4=minuteu4
                                                                elif(minuteu4==0 and houru4>0):
                                                                        houru4=houru4-1
                                                                        minuteu4=59
                                                                        secu4=secu3-secu2+60
                                                                else:
                                                                        minuteu4=minuteu4-1
                                                                        secu4=secu3-secu2+60
                                                                print('當前時間',houru3,minuteu3,secu3)
                                                                print('時差',houru4,minuteu4,secu4)
                                                                print('a')
                                                        if(houru3>=houru2 and minuteu3<=minuteu2 and secu3>secu2):
                                                                houru4=houru3-houru2
                                                                if(houru4==0 and minuteu3==minuteu2):
                                                                        houru4=0
                                                                        minuteu4=minuteu3-minuteu2
                                                                        secu4=secu3-secu2
                                                                else:
                                                                        houru4=houru4-1
                                                                        minuteu=60+minuteu3-minuteu2
                                                                        secu4=secu3-secu2
                                                                print('當前時間',houru3,minuteu3,secu3)
                                                                print('時差',houru4,minuteu4,secu4)
                                                                print('b')
                                                        if(houru3>=houru2 and minuteu3<minuteu2 and secu3<=secu2):        
                                                                houru4=houru3-houru2
                                                                houru4=houru4-1
                                                                minuteu4=60+minuteu3-minuteu2-1
                                                                secu4=secu3-secu2+60
                                                                print('當前時間',houru3,minuteu3,secu3)
                                                                print('時差',houru4,minuteu4,secu4)
                                                                print('c')
                                                        if(houru3>=houru2 and minuteu3>minuteu2 and secu3>secu2):
                                                                houru4=houru3-houru2
                                                                minuteu4=minuteu3-minuteu2
                                                                secu4=secu3-secu2
                                                                print('當前時間',houru3,minuteu3,secu3)
                                                                print('時差',houru4,minuteu4,secu4)
                                                                print('d')
                                                        if(houru3<houru2 and minuteu3>minuteu2):
                                                                if(secu3>secu2):
                                                                        houru4=houru3-houru2+24
                                                                        minuteu4=minuteu3-minuteu2
                                                                        secu4=secu3-secu2
                                                                        print('當前時間',houru3,minuteu3,secu3)
                                                                        print('時差',houru4,minuteu4,secu4)
                                                                        print('e')
                                                                if(secu3<secu2):
                                                                        houru4=houru3-houru2+24
                                                                        minuteu4=minuteu3-minuteu2-1
                                                                        secu4=secu3-secu2+60
                                                                        print('當前時間',houru3,minuteu3,secu3)
                                                                        print('時差',houru4,minuteu4,secu4)
                                                                        print('f')             
                                                        if(houru3<houru2 and minuteu3<=minuteu2):
                                                                if(minuteu3==minuteu2 and secu3==secu2):
                                                                        secu4=0
                                                                        minuteu4=0
                                                                        houru4=houru3-houru2+24
                                                                elif(secu3<secu2):
                                                                        houru4=houru3-houru2+24-1
                                                                        minuteu4=minuteu3-minuteu2+60-1
                                                                        secu4=secu3-secu2+60     
                                                                else:
                                                                        houru4=houru3-houru2+24-1
                                                                        minuteu4=minuteu3-minuteu2+60
                                                                        secu4=secu3-secu2            
                                                                print('當前時間',houru3,minuteu3,secu3)
                                                                print('時差',houru4,minuteu4,secu4)
                                                                print('g')
                                                        startu=time.localtime()##在首次執行后，求得和第一次的時間差值，并初始化第一次的時間
                                                        houru2=startu.tm_hour
                                                        minuteu2=startu.tm_min
                                                        secu2=startu.tm_sec
                                                        a5=int(a5)+int(houru4)
                                                        a6=int(a6)+int(minuteu4)
                                                        print(a5,a6)
                                                T.insert(END,'距離您上次操作經過了')
                                                T.insert(INSERT,houru4)
                                                T.insert(INSERT,'時')
                                                T.insert(INSERT,minuteu4)
                                                T.insert(INSERT,'分')
                                                T.insert(INSERT,secu4)
                                                T.insert(INSERT,'秒\n')
                                                if(len(str(a5))==1):
                                                        a5='0'+str(a5)
                                                if(len(str(a6))==1):
                                                        a6='0'+str(a6)
                                                T.insert(END,'您已定時:')
                                                T.insert(INSERT,a5)
                                                T.insert(INSERT,'時')
                                                T.insert(INSERT,a6)
                                                T.insert(INSERT,'分')
                                                T.insert(INSERT,'后關閉插座\n')
                                                       ##檢查無誤，功能完成-----------------------------------
                                        a1='AA'
                                        a2='0x07'
                                        a3='0x31'
                                        a4='00'  
                                        a7=int(a2,16)
                                        a8=int(a3,16)
                                        a9=int(str(a5),16)
                                        a10=int(str(a6),16)
                                        checksum=(hex(a7+a8+a9+a10))[-2:]
                                        if(len(str(a5))==1):
                                                 a5='0'+str(a5)
                                        if(len(str(a6))==1):
                                                 a6='0'+str(a6)
                                        r='AA0731'+str(a5)+str(a6)+checksum+'55'
                                        print(r)
                                        
                                        with Peripheral('C1:8F:CC:DC:57:19','random') as p:
                                            ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
                                            val=binascii.a2b_hex(r)
                                            ch.write(val)
                                            p.disconnect()
                                            T.insert(END,'完成寫入\n')
                        if(position=='north'):
                                T.insert(END,'進入開啟定時模式，向左點擊減少10分鐘定時，向右點擊增加10分鐘定時，觸摸中心退出模式\n')
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
                                        print(t1)
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
                                        T.insert(END,'您已定時:')
                                        T.insert(INSERT,ap)
                                        T.insert(INSERT,'時')
                                        T.insert(INSERT,ad)
                                        T.insert(INSERT,'分')
                                        T.insert(INSERT,'后開啟插座\n')
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
btn1 = tk.Button(window, text = "蓝牙插座开启", activebackground='yellow',bg='pink',fg='black',command = btn1_clicked)
btn1.pack(fill = tk.X)
btn2 = tk.Button(window, text = "蓝牙插座关闭",activebackground='yellow', bg='pink',fg='black',command = btn2_clicked)
btn2.pack(fill=tk.X)
btn4 = tk.Button(window, text = "定时开启插座",activebackground='yellow', bg='pink',fg='black',command = btn4_clicked)
btn4.pack(fill=tk.X)
btn3 = tk.Button(window, text = "定时关闭插座", activebackground='yellow',bg='pink',fg='black',command = btn3_clicked)
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
