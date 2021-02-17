import array
import struct
import pycom
import socket
import time
import os

from connect_to_ttn import connect_to_ttn
from sensors import Sensors
from generateID import generateID

# Setting timer, delete later
from machine import Timer
chrono = Timer.Chrono()

# turn off lopy heartbeat (blinking led)
pycom.heartbeat(False)

# establish connection between the device and the TTN
lora = connect_to_ttn()

# create socket to be used for LoRa communication
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
# configure data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 6)

# keep sending data from sensors to the ttn every minute
while True:
    # check if still connected to ttn
    if not lora.has_joined:
        pycom.rgbled(0x110000)
        break
    # purple led when fetching the data
    pycom.rgbled(0x110011)

    # make the socket blocking
    # (waits for the data to be sent and for the 2 receive windows to expire)
    s.setblocking(True)
    #define which port with the socket bind
    s.bind(2)
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
    bytes_to_send = id_ba
    bytes_to_send.extend(alt_ba)
    bytes_to_send.extend(pre_ba)
    bytes_to_send.extend(tem_ba)
    bytes_to_send.extend(acc_ba)

    # send the data
    s.send(bytes_to_send)
    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)

    # Green led when data was sent
    pycom.rgbled(0x001100)

    # sleep
    time.sleep(300)
