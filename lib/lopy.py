import pycom
import struct
import time
import ubinascii
from network import LoRa

def connect():
    # Initialise LoRa in LORAWAN mode.
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
    lora.nvram_restore()

    if not lora.has_joined():
        print("Fristly join")
        # create an OTAA authentication parameters, change them to the provided credentials
        app_eui = ubinascii.unhexlify('0000000000000000')
        app_key = ubinascii.unhexlify('D20FAEC47B8610BFA234A62402240EE4')
        # join a network using OTAA (Over The Air Activation)
        lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

        # Blinking blue led if connecting
        while not lora.has_joined():
            pycom.rgbled(0x000011)
            time.sleep(1)
            pycom.rgbled(0x000000)
            print("has not joined")
            time.sleep(1)
    else:
        print("Connection restored")

    # # create an ABP authentication parameters
    # dev_addr = struct.unpack(">l", ubinascii.unhexlify('26013660'))[0]
    # nwk_swkey = ubinascii.unhexlify('3AF9FB99FD7576CE48441A6673D49ED0')
    # app_swkey = ubinascii.unhexlify('260F192E04FC4CDBE9CBDE84A0AD615F')
    # # join a network using ABP (Activation By Personalization)
    # lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

    # Blue led when connected
    pycom.rgbled(0x000011)
    print("has joined")

    return lora


# change color of led and data rate if asked for
def process_downlink(downlink):
    downlinkHex = ubinascii.hexlify(downlink)
    downlinkStr = downlinkHex.decode("utf-8")

    rgbStr = downlinkStr[2:]
    if not rgbStr == "05":
        if rgbStr == "00":
            pycom.nvs_set("rgb", 0x880000)
        if rgbStr == "01":
            pycom.nvs_set("rgb", 0x008800)
        if rgbStr == "02":
            pycom.nvs_set("rgb", 0x000088)
        if rgbStr == "03":
            pycom.nvs_set("rgb", 0x880088)
        if rgbStr == "04":
            pycom.nvs_set("rgb", 0x888800)

        pycom.rgbled(pycom.nvs_get("rgb"))

    drStr = downlinkStr[0:2]
    drInt = int(drStr, 10)
    if not drStr == "06" and not drInt == pycom.nvs_get("dr"):
        pycom.nvs_set("dr", drInt)

        if drInt == 5:
            pycom.nvs_set("sleep_time", 300000)
        if drInt == 4:
            pycom.nvs_set("sleep_time", 600000)
        if drInt == 3:
            pycom.nvs_set("sleep_time", 900000)
        if drInt == 2:
            pycom.nvs_set("sleep_time", 1800000)
        if drInt == 1:
            pycom.nvs_set("sleep_time", 3600000)
        if drInt == 0:
            pycom.nvs_set("sleep_time", 5400000)
