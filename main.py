import time
from machine import Pin
import pycom
import ubidots
from machine import I2C
from dht import DHT # https://github.com/JurassicPork/DHT_PyCom
import CCS811 # https://github.com/Notthemarsian/CCS811

# turn off blinking of blue LED
pycom.heartbeat(False)

# DHT11
th = DHT(Pin('P23', mode=Pin.OPEN_DRAIN), 0) # 0 = dht11
time.sleep(2)

# CCS811
i2c = I2C(0)                         # create on bus 0
i2c = I2C(0, I2C.MASTER)             # create and init as a master
i2c = I2C(0, pins=('P9','P10'))      # PIN assignments (P9=SDA, P10=SCL)
i2c.init(I2C.MASTER, baudrate=10000) # init as a master
ccs = CCS811.CCS811(i2c=i2c,addr=90)
time.sleep(2)

while True:
    result = th.read()
    temp = result.temperature
    hum = result.humidity
    print('Temp:', temp, '°C')
    print('RH:', hum, '%')
    time.sleep(1)

    ccs.data_ready()
    time.sleep(1)
    CO2 = ccs.eCO2
    tVOC = ccs.tVOC
    if CO2 > 10:
        print('c(CO2): ' + str(CO2) + ' ppm')
        print('c(tVOC): ' + str(tVOC) + 'ppb')
    time.sleep(2)
    ubidots.post_var("lopy", temp, hum, CO2, tVOC)
    print('')
    time.sleep(5)
