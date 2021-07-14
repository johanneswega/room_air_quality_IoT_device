from machine import UART
from network import WLAN
import machine
import keys
import os

# settings for ubidots 
uart = UART(0, baudrate=115200)
os.dupterm(uart)
machine.main('main.py')

# connect to Wifi
wlan = WLAN(mode=WLAN.STA)
wlan.connect(ssid=keys.wifi_ssid, auth=(WLAN.WPA2, keys.wifi_password))
while not wlan.isconnected():
    machine.idle()
print("Wifi connected successfully")
