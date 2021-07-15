import time
from machine import Pin
import pycom
import ubidots
from machine import I2C
from dht import DHT # library from: https://github.com/JurassicPork/DHT_PyCom
import CCS811 # library from: https://github.com/Notthemarsian/CCS811

# turn off blinking of blue LED
pycom.heartbeat(False)

# DHT11 setup
th = DHT(Pin('P23', mode=Pin.OPEN_DRAIN), 0) # 0 specifies that the DHT11 is used because the library can also be used with another sensor
time.sleep(2)

# CCS811 setup
i2c = I2C(0)                         # create on bus 0
i2c = I2C(0, I2C.MASTER)             # create and init as a master
i2c = I2C(0, pins=('P9','P10'))      # PIN assignments (P9=SDA, P10=SCL)
i2c.init(I2C.MASTER, baudrate=10000) # init as a master
ccs = CCS811.CCS811(i2c=i2c,addr=90)
time.sleep(2)

# function to calaculate the average of a list
def average(liste):
    return sum(liste)/len(liste)

# send data to ubidots
while True:
    # intialize empty variable lists 
    temp_list = []
    hum_list = []
    CO2_list = []
    tVOC_list = []

    # make readings with both sensors 
    # wait a second each and add sensors values to lists
    for i in range(45):
        # read temperature and humidity from DHT11
        result = th.read()
        time.sleep(1)
        temp = result.temperature
        hum = result.humidity
        temp_list.append(temp)
        hum_list.append(hum)

        # read c(CO2) and c(tVOC) from CCS811
        ccs.data_ready()
        time.sleep(1)
        CO2 = ccs.eCO2
        tVOC = ccs.tVOC
        CO2_list.append(CO2)
        tVOC_list.append(tVOC)

    # send the average sensor value collected in the last 90s to ubidots
    post_var("lopy", average(temp_list), average(hum_list), average(CO2_list), average(tVOC_list))

