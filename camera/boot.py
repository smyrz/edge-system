# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import network
import main

def wifi_connection(username, password):

    # connect to wifi
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(username, password)  # username and password
    while not wlan.isconnected():
        pass
    print('wlan configuration:', wlan.ifconfig())
    
wifi_connection('Redmi Note 10 Pro', '00000000')
main.init()