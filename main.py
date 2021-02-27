import array
import struct
import pycom
import socket
import time
import os
import ubinascii

from lopy import connect
from sensors import Sensors
from generateID import generateID
from network import LoRa

# global dictionary
_G = {'RGB': 0x001100, 'DR': 5, 'SLEEP': 300}

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

# change color of led and data rate if asked for
def process_downlink(downlink):
    downlinkHex = ubinascii.hexlify(downlink)
    downlinkStr = downlinkHex.decode("utf-8")

    rgbStr = "0x" + downlinkStr[2:]
    if not rgbStr == "0x000000":
        _G['RGB'] = int(downlinkStr, 16)
        pycom.rgbled(_G['RGB'])

    drStr = downlinkStr[0:2]
    drInt = int(drStr, 10)
    if not drStr == "06" and not drInt == _G['DR']:
        _G['DR'] = drInt
        s.setsockopt(socket.SOL_LORA, socket.SO_DR, _G['DR'])

        if drInt == 5:
            _G['SLEEP'] = 300
        if drInt == 4:
            _G['SLEEP'] = 600
        if drInt == 3:
            _G['SLEEP'] = 900
        if drInt == 2:
            _G['SLEEP'] = 1200
        if drInt == 1:
            _G['SLEEP'] = 2400
        if drInt == 0:
            _G['SLEEP'] = 4800


# turn off lopy heartbeat (blinking led)
pycom.heartbeat(False)

# establish connection between the device and the TTN
lora = connect()
# set callback
lora.callback(LoRa.RX_PACKET_EVENT | LoRa.TX_PACKET_EVENT, lora_callback)

# create socket to be used for LoRa communication
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
# configure data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, _G['DR'])

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
    # s.bind(1)
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
    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)

    # Green led when data was sent
    pycom.rgbled(_G['RGB'])

    print(_G['DR'])
    print(_G['SLEEP'])
    # sleep
    time.sleep(_G['SLEEP'])
