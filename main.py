# main.py

import machine
import time
import good_time_for_ball
from time import sleep
#import testing

#led = machine.Pin(15, machine.Pin.OUT) # Configure D8-GPIO15 as an output pin
powerButton = machine.Pin(15, machine.Pin.OUT) # Configure D8-GPIO15 as an output pin
wifiButton = machine.Pin(13, machine.Pin.OUT)   # configure D7-GPIO13 as an output pin
wakeButton = machine.Pin(16, machine.Pin.IN) # Configure D0-GPIO16 as an input pin
hourButton = machine.Pin(14, machine.Pin.IN) # Configure D5-GPI14 as an input pin
nowButton = machine.Pin(12, machine.Pin.IN) # Configure D6-GPI12 as an input pin

while (1):
    
    if (good_time_for_ball.do_connect()):
        wifiButton.on()
        print('connected')
        good_time_for_ball.run_code()
    else:
        print('wifi is not connected')
        wifiButton.on()
        sleep(1)
        wifiButton.off()
        sleep(1) 

# while (1):
#     powerButton.value(1)
#     sleep(1)
#     powerButton.value(0)
#     sleep(1)

#good_time_for_ball.run_code()      #run the good_time_for_ball code
#testing.run_code()
