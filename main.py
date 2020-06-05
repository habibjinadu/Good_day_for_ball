# main.py

import machine
import time
import good_time_for_ball
#import testing

led = machine.Pin(15, machine.Pin.OUT)

led.value(1)
time.sleep(1)
led.value(0)

good_time_for_ball.run_code()
#testing.run_code()
