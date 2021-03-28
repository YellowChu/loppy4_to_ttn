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

from pysense import Pysense

# callback function (triggers during RX/TX events)
def lora_callback(lora):
    print('A LoRa event occured: ', end='')
    events = lora.events()
    if events & LoRa.RX_PACKET_EVENT:
        print('Lora packet received')
        downlink = s.recv(256)
        print(downlink)
        process_downlink(downlink)
    elif events & LoRa.TX_PACKET_EVENT:
        print('Lora packet sent')
    else:
        print('Other event: %s' % events)

## POSITION OF THIS CODE DEPENDS ON TYPE OF SLEEP ###
# establish connection between the device and the TTN
lora = connect()
# set callback
lora.callback(LoRa.RX_PACKET_EVENT | LoRa.TX_PACKET_EVENT, lora_callback)

# create socket to be used for LoRa communication
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# keep sending data from sensors to the ttn every minute
while True:
    #getting config values
    rgb = pycom.nvs_get("rgb")
    dr = pycom.nvs_get("dr")
    sleep_time = pycom.nvs_get("sleep_time")

    pycom.rgbled(rgb)

    # configure data rate
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, dr)
    # make the socket blocking
    # (waits for the data to be sent and for the 2 receive windows to expire)
    s.setblocking(True)

    # get data from pysense sensors
    sensors = Sensors()
    # float to bytearrays
    alt_ba = bytearray(struct.pack("f", sensors.Altitude))
    pre_ba = bytearray(struct.pack("f", sensors.Pressure))
    tem_ba = bytearray(struct.pack("f", sensors.Temperature))
    acc_ba = bytearray(struct.pack("f", sensors.Battery))
    # create unique id
    id = generateID()
    id_ba = bytearray(id)
    # compile the arrays into one
    uplink = id_ba
    uplink.extend(alt_ba)
    uplink.extend(pre_ba)
    uplink.extend(tem_ba)
    uplink.extend(acc_ba)

    # send the data
    s.send(uplink)
    lora.nvram_save()
    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)

    pycom.rgbled(rgb)
    time.sleep(2)
    # sleep
    sensors.Pysense.setup_sleep(sleep_time/1000)
    sensors.Pysense.go_to_sleep()
    # machine.deepsleep(sleep_time)
