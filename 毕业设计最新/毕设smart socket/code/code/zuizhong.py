import time
import RPi.GPIO as GPIO
led_pin = 24
led_pin1 =17
led_pin2 =27
button_pin = 23
button_pin1 = 25
button_pin2 =12
button_pin3 =5
GPIO.setwarnings(False)
GPIO.setmode( GPIO.BCM )
GPIO.setup( led_pin,GPIO.OUT )
GPIO.setup( led_pin1,GPIO.OUT )
GPIO.setup( led_pin2,GPIO.OUT )
GPIO.setup( button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup( button_pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup( button_pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup( button_pin3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    if GPIO.input(button_pin)==0:
            GPIO.output(led_pin,1)
            time.sleep(5)
    if GPIO.input(button_pin1):
        GPIO.output(led_pin2,0)
    else :
        GPIO.output(led_pin2,1)
    if GPIO.input(button_pin2):
        GPIO.output(led_pin2,0)
        GPIO.output(led_pin,0)
        GPIO.output(led_pin1,0)
    else :
        GPIO.output(led_pin1,1)
        time.sleep(1)
        GPIO.output(led_pin1,0)
        GPIO.output(led_pin2,1)
        time.sleep(1)
        GPIO.output(led_pin2,0)
        GPIO.output(led_pin,1)
        time.sleep(1)
        GPIO.output(led_pin,0)
        while(1):
                GPIO.output(led_pin2,1)
                GPIO.output(led_pin,1)
                GPIO.output(led_pin1,1)
                time.sleep(0.03)
                GPIO.output(led_pin2,0)
                GPIO.output(led_pin,0)
                GPIO.output(led_pin1,0)
                time.sleep(0.03)
                if GPIO.input(button_pin3)==0:
                    break