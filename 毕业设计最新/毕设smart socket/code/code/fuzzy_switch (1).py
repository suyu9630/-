import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from grovepi import *
from grove_rgb_lcd import *
import time
import grovepi
import  datetime
import mysql.connector

from btle import UUID,Peripheral
import struct
import binascii

def sqlinsert(device,temp,hum,light,sound,air,output,command):
    try :
        device=str(device)
        senddevice='Raspberry_Pi_3'
        today=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cnx = mysql.connector.connect(user='abc', password='1234',host='120.110.7.27',database='smarttimersocket')
        cursor = cnx.cursor()
        add_test = ("INSERT INTO `socket1`"
                    "(`id`, `Deviceid`, `Senddevice`, `Date`, `temp`, `hum`, `light`, `sound`, `air`, `output`, `CommandLine`)"
                    "VALUES"
                    "(NULL, %s, %s, %s,%s, %s,%s,%s,%s,%s,%s);")
        data_test=(device,senddevice,today,temp,hum,light,sound,air,output,command)
        
        print ((add_test % data_test))
        cursor.execute(add_test, data_test)
        cnx.commit()
        cursor.close()
        cnx.close()
    except (IOError, TypeError) as e:
        print("sqlinsert IOError, TypeError:"+str(e))
    except Exception as e:
        print("sqlinsert Error:"+str(e))
        f = open('file.txt','r+')
        add_test = ("INSERT INTO `socket1`"
                    "(`id`, `Deviceid`, `Senddevice`, `Date`, `temp`, `hum`, `light`, `sound`, `air`, `output`, `CommandLine`)"
                    "VALUES"
                    "(NULL, '%s', '%s', '%s',%f, %f,%f,%f,%f,%f,'%s');")

        data_test=(device,senddevice,today,temp,hum,light,sound,air,output,command)
        a=(add_test % data_test)+'\n'
        #print(f.read()+str(a))
        f.write(f.read()+str(a))
        f.close()
def sqlget():
    try :
        cnx = mysql.connector.connect(user='abc', password='1234',host='120.110.7.27',database='smarttimersocket')
        cursor = cnx.cursor()
        #My SQL Command
        cursor.execute("SELECT * FROM `socket1` WHERE `Deviceid`=1 ORDER BY `socket1`.`id` DESC LIMIT 0,1")
        row=cursor.fetchone()
        cursor.close()
        cnx.close()
        return row[10]
    except (IOError, TypeError) as e:
        print ("sqlget IOError TypeError:"+str(e))
    except Exception as e:
        print("sqlget Error:"+str(e))
def sqlauto(deviceid):
    try :
        deviceid=str(deviceid)
        cnx = mysql.connector.connect(user='abc', password='1234',host='120.110.7.27',database='smarttimersocket')
        cursor = cnx.cursor()
        #My SQL Command
        cursor.execute("SELECT * FROM `device_switch` WHERE `id`="+deviceid)
        row=cursor.fetchone()
        cursor.close()
        cnx.close()
        return int(row[3])
    except (IOError, TypeError) as e:
        print ("sqlauto IOError TypeError:"+str(e))
    except Exception as e:
        print("sqlauto Error:"+str(e))   
##---------------bluetooth setting-------------------------
RX_SERVICE_UUID=UUID('6e400001-b5a3-f393-e0a9-e50e24dcca9e')
RX_CHAR_UUID=UUID('6e400003-b5a3-f393-e0a9-e50e24dcca9e')
TX_CHAR_UUID=UUID('6e400002-b5a3-f393-e0a9-e50e24dcca9e')
switch_staus="off"

##----------------Fuzzy Setting-----------------------------#
# New Antecedent/Consequent objects hold universe variables and membership
# functions
temp =ctrl.Antecedent(np.arange(0, 41, 1), 'temp')
light =ctrl.Antecedent(np.arange(0, 11, 1), 'light')
hum =ctrl.Antecedent(np.arange(0, 81, 1), 'hum')
switch_power = ctrl.Consequent(np.arange(0, 11, 1), 'switch_power')
temp.automf(3)
light.automf(3)
hum.automf(3)
#switch_power.automf(3)
switch_power['low'] = fuzz.trimf(switch_power.universe, [0, 0, 5])
switch_power['medium'] = fuzz.trimf(switch_power.universe, [0, 5, 10])
switch_power['high'] = fuzz.trimf(switch_power.universe, [5, 10, 10])

rule1 = ctrl.Rule(temp['good'],switch_power['high'])
rule2 = ctrl.Rule(temp['average'] | hum['good'] ,switch_power['high'])
rule3 = ctrl.Rule(temp['poor'], switch_power['low'])
rule4 = ctrl.Rule(light['poor'], switch_power['low'])
tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3,rule4])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)


# Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
# Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
#quality['average'].view()
#service.view()
#tip.view()
#rule1.view()
# Crunch the numbers
##----------------fuzzy setting end----------------------------------------#

#--------------Senor Grove pi  Setting-----------------------------#
#---Connect Analog Port---------------------------------
#Analog Port A0~A2
Sound_Senor_Port    = 0   # Connect the Sound sensor  to port A0
Air_Senor_Port      = 1   # Connect the Air sensor    to port A1
Light_Senor_Port    = 2   # Connect the Light sensor  to port A2
#-------------------------------------------------------

#---Connect Digital Port--------------------------------
#Digital Port D2~D8
DHT_Senor_Port      = 2   # Connect the DHT sensor    to port D2
Green_LED_Port      = 3   # Connect the GREEN LED     to port D3
RED_LED_Port        = 4   # Connect the RED LED       to port D4
#-------------------------------------------------------
#--------------Senor Grove pi setting End---------------------------#

try:
    time.sleep(1)
    Light_value=0
    temp=0
    hum=0
    Sound_value=0
    Air_value=0
    while Light_value == 0:          
        Light_value = grovepi.analogRead(Light_Senor_Port)
    while Sound_value == 0:
        Sound_value = grovepi.analogRead(Sound_Senor_Port)  
    while Air_value == 0:       
        Air_value = grovepi.analogRead(Air_Senor_Port)
    if  Light_value != 0:
        resistance  = (float)(1023 - Light_value) * 10 / Light_value
    else :
        resistance  = 0
    while temp == 0:          
        [t, h] = grovepi.dht(DHT_Senor_Port,0)
        temp          = float(t)
        hum          = float(h)

    Sound=Sound_value/100
    Air=Air_value/100
    light=Light_value/100
    tipping.input['temp'] = float(temp)
    tipping.input['light'] =float(light)
    tipping.input['hum'] = float(hum)
    tipping.compute()
    output=float(tipping.output['switch_power'])
    print('temp=%f, `hum=%f`, `light=%f`, `sound=%f`, `air=%f`, `output=%f`' % (temp,hum,light,Sound,Air,output))
    last=sqlget()
    if last==None:
        last=0
        
    print ('last=%s' % last)
    
    if output >=5 :
        print ("on")
        switch_staus="on"
        if(sqlauto(1)==1):
            print("Auto Model")
            with Peripheral('C1:8F:CC:DC:57:19','random') as p:
                ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
                val=binascii.a2b_hex('AA0630306655')
                ch.write(val)
                p.disconnect()
            if(last!=switch_staus):
                print ("Sql Insert On")
                print (sqlinsert(1,temp,hum,light,Sound,Air,output,'on'))
        else:
            print("Manual Model")
    else :
        print ("off")
        switch_staus="off"
        if(sqlauto(1)==1):
            print("Auto Model")
            with Peripheral('C1:8F:CC:DC:57:19','random') as p:
                ch=p.getCharacteristics(uuid=TX_CHAR_UUID)[0]
                val=binascii.a2b_hex('AA0630316755')
                ch.write(val)
                p.disconnect()
            if(last!=switch_staus):
                print ("Sql Insert off")
                print(sqlinsert(1,temp,hum,light,Sound,Air,output,'off'))
        else :
            print("Manual Model")
except (IOError, TypeError) as e:
    print ("Main IOError TypeError:"+str(e))
    #print (e)
except Exception as e:
    print("Main Error:"+str(e))
finally :
    print ("Finsh")
    time.sleep(10)







