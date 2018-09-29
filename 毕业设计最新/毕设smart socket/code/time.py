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
##蓝牙插座的mac:C1:8F:CC:DC:57:19
##蓝牙插座的UUID：6e400001-b5a3-f393-e0a9-e50e24dcca9e
##---------------开关设定----------------------------------
##---------------开关开启与关闭—————————————————
switch_staus="on"
print('蓝牙插座开关开启')
with Peripheral('C1:8F:CC:DC:57:19','random') as p:
    ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
    val=binascii.a2b_hex('AA073100013955')
    ch.write(val)
