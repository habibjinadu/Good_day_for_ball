# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)       #must do this if you want to add files to the board

import uos, machine     # import the uos (needed to add and remove files on the board)
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
#import webrepl
#webrepl.start()
gc.collect()



