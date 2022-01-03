import array
import machine
import struct
import pycom
import socket
import time
import os
import ubinascii

from lopy import connect, process_downlink
from sensors import Sensors
from generateID import generateID
from network import LoRa

# callback function (triggers during RX/TX events)
def lora_callback(lora):
    print('A LoRa event occured: ', end='')
    events = lora.events()
    # process downlink message
    if events & LoRa.RX_PACKET_EVENT:
        print('Lora packet received')
        downlink = s.recv(256)
        print(downlink)
        process_downlink(downlink)
    # annouces that packet was sent
    elif events & LoRa.TX_PACKET_EVENT:
        print('Lora packet sent')

# establish connection between the device and the TTN
lora = connect()
# set callback
lora.callback(LoRa.RX_PACKET_EVENT | LoRa.TX_PACKET_EVENT, lora_callback)

# create socket to be used for LoRa communication
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# change color of led
rgb = pycom.nvs_get("rgb")
pycom.rgbled(rgb)

# configure sf (dr0=sf12, dr1=sf11, dr2=sf10, dr3=sf9, dr4=sf8, dr5=sf7)
dr = pycom.nvs_get("dr")
s.setsockopt(socket.SOL_LORA, socket.SO_DR, dr)
# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

# get data from pysense sensors
sensors = Sensors()
# float to bytearrays
pre_ba = bytearray(struct.pack("f", sensors.Pressure))
tem_ba = bytearray(struct.pack("f", sensors.Temperature))
acc_ba = bytearray(struct.pack("f", sensors.Battery))
# create unique id
id = generateID()
id_ba = bytearray(id)
# compile the arrays into one
uplink = id_ba
uplink.extend(pre_ba)
uplink.extend(tem_ba)
uplink.extend(acc_ba)

# send the data
s.send(uplink)
# this sleep is here so the user of the module can key board interrupt
time.sleep(2)
# saves the lora configuration so the connection can be restored after waking up
# from the deep sleep
lora.nvram_save()
# make the socket non-blocking
# (because if there's no data received it will block forever...)
s.setblocking(False)
# machine goes to deep sleep, after it wakes up the code starts all over again
sleep_time = pycom.nvs_get("sleep_time")
sensors.Pysense.setup_sleep(sleep_time/1000)
sensors.Pysense.go_to_sleep()

#testing commit 1
