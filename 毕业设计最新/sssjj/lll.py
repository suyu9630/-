import itchat
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
import speech_recognition
from pydub import AudioSegment
#itchat框架，关注TEXT消息
r=speech_recognition.Recognizer()
t=1
RX_SERVICE_UUID=UUID('6e400001-b5a3-f393-e0a9-e50e24dcca9e')##只有这个是蓝牙插座的UUID
RX_CHAR_UUID=UUID('6e400003-b5a3-f393-e0a9-e50e24dcca9e')##接受设备uuid
TX_CHAR_UUID=UUID('6e400002-b5a3-f393-e0a9-e50e24dcca9e')##发送设备uuid
@itchat.msg_register(itchat.content.TEXT)#關注text框架方法
def text_reply(msg):
    global t
    if(t==1):##功能
        print('hello')
        itchat.send(msg='歡迎您使用智能插座wechat遠控端\n發送1,開啟插座\n發送2,關閉插座\n發送3,預約插座開啟\n發送4,預約插座關閉\n發送5,插座日誌查詢\n發送6,功能菜單索取\n發送7,預約定時開關\n發送8,RTC時間查詢\n發送9,校準RTC時間',toUserName=msg['FromUserName'])
    if(msg.text=='1'):
        itchat.send(msg='插座已开启',toUserName=msg['FromUserName'])
        with Peripheral('C1:8F:CC:DC:57:19','random') as p:
            ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
            val=binascii.a2b_hex('AA0630306655')
            ch.write(val)
            p.disconnect()
        s=time.localtime()
        year="%02d"%((s.tm_year)%100)
        mon="%02d"%s. tm_mon
        day="%02d"%s. tm_mday
        hour="%02d"%s.tm_hour
        minute="%02d"%s.tm_min
        fo = open("foo.txt", "a")
        fo.write( year+'-'+mon+'-'+day+'\t'+hour+':'+minute+'\n')
        fo.close()
        tts = gTTS(text='插座已开启', lang='zh-tw')
        tts.save('debug1.mp3')
        os.system('play debug1.mp3')
    if(msg.text=='2'):
        itchat.send(msg='插座已關閉',toUserName=msg['FromUserName'])
        with Peripheral('C1:8F:CC:DC:57:19','random') as p: 
                ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
                val=binascii.a2b_hex('AA0630316755')
                ch.write(val)
                p.disconnect()
        tts = gTTS(text='插座已關閉', lang='zh-tw')
        tts.save('debug1.mp3')
        os.system('play debug1.mp3')
    if(msg.text=='5'):
        fo = open("foo.txt", "r+")
        str1 = fo.readline()
        fo.close()
        itchat.send(msg=str(str1),toUserName=msg['FromUserName'])
        tts = gTTS(text='操作日誌已發送', lang='zh-tw')
        tts.save('debug1.mp3')
        os.system('play debug1.mp3')
        if(msg.text=='6'):
            itchat.send(msg='歡迎您使用智能插座wechat遠控端\n發送1,開啟插座\n發送2,關閉插座\n發送3,預約插座開啟\n發送4,預約插座關閉\n發送5,插座日誌查詢\n發送6,功能菜單索取\n發送7,預約定時開關\n發送8,RTC時間查詢\n發送9,校準RTC時間',toUserName=msg['FromUserName'])
    t=t+1
    print(msg.text)
@itchat.msg_register(itchat.content.RECORDING)#語音模塊
def text_reply(msg):
    global r
    msg.download(msg.fileName)
    sound = AudioSegment.from_mp3(msg.fileName)
    sound.export('/home/pi/Desktop/sssjj/123.wav',format="wav")
    itchat.send(msg='i got the voice',toUserName=msg['FromUserName'])
    r=speech_recognition.Recognizer()
    with speech_recognition.AudioFile('/home/pi/Desktop/sssjj/123.wav') as source:
        audio=r.record(source)
        r=r.recognize_google(audio,language='zh-tw')
        print(r)
@itchat.msg_register(itchat.content.PICTURE)
def text_reply(msg):
    itchat.send(msg='別發表情包了，我是不會理你的',toUserName=msg['FromUserName'])
itchat.auto_login()
itchat.run() 
