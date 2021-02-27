import pycom
import struct
import time
import ubinascii
from network import LoRa

def connect():
    # Initialise LoRa in LORAWAN mode.
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

    # # create an ABP authentication parameters
    # dev_addr = struct.unpack(">l", ubinascii.unhexlify('26013660'))[0]
    # nwk_swkey = ubinascii.unhexlify('3AF9FB99FD7576CE48441A6673D49ED0')
    # app_swkey = ubinascii.unhexlify('260F192E04FC4CDBE9CBDE84A0AD615F')
    # # join a network using ABP (Activation By Personalization)
    # lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

    # create an OTAA authentication parameters, change them to the provided credentials
    app_eui = ubinascii.unhexlify('70B3D57ED003A888')
    app_key = ubinascii.unhexlify('4544CCA57A3A1A706EC9F906CE9D5C3B')
    # join a network using OTAA (Over The Air Activation)
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

    # Blinking blue led if connecting
    while not lora.has_joined():
        pycom.rgbled(0x000011)
        time.sleep(1)
        pycom.rgbled(0x000000)
        print("has not joined")
        time.sleep(1)

    # Blue led when connected
    pycom.rgbled(0x000011)
    print("has joined")

    return lora
