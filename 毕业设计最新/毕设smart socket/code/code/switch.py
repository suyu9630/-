import numpy as np
import time#常规时间操作模块
import  datetime#时间复杂操作模块（定时）
from bluepy.btle import UUID,Peripheral
import struct
import binascii#进制转化模块
##---------------bluetooth setting-------------------------
RX_SERVICE_UUID=UUID('6e400001-b5a3-f393-e0a9-e50e24dcca9e')##只有这个是蓝牙插座的UUID
RX_CHAR_UUID=UUID('6e400003-b5a3-f393-e0a9-e50e24dcca9e')
TX_CHAR_UUID=UUID('6e400002-b5a3-f393-e0a9-e50e24dcca9e')
switch_staus="off"
##---------------bluetooth setting end---------------------
##蓝牙插座的mac:C1:8F:CC:DC:57:19
##蓝牙插座的UUID：6e400001-b5a3-f393-e0a9-e50e24dcca9e
##---------------开关设定----------------------------------
switch_staus="on"
with Peripheral('C1:8F:CC:DC:57:19','random') as p:
    ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
    val=binascii.a2b_hex('AA0630306655')
    ch.write(val)
    p.disconnect()  
