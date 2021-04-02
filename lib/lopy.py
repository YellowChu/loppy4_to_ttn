import pycom
import struct
import time
import ubinascii
from network import LoRa

def connect():
    # Initialise LoRa in LORAWAN mode.
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
    # try to restore connection
    lora.nvram_restore()
    if not lora.has_joined():
        # if restoring connection did not work, device connects for the first time
        print("Fristly join")
        # create an OTAA authentication parameters, change them to the provided credentials
        app_eui = ubinascii.unhexlify(pycom.nvs_get("app_eui"))
        app_key = ubinascii.unhexlify(pycom.nvs_get("app_key"))
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
        # connection was restored
        print("Connection restored")

    # Blue led when connected
    pycom.rgbled(0x000011)
    print("has joined")

    return lora


# function triggers when downlink comes
def process_downlink(downlink):
    # unpack the downlink message to string
    downlinkHex = ubinascii.hexlify(downlink)
    downlinkStr = downlinkHex.decode("utf-8")

    # last two bytes are color information
    # 0-red, 1-green, 2-blue, 3-purple, 4-yellow, 5-do not change
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

        # set new color values
        pycom.rgbled(pycom.nvs_get("rgb"))

    # last two bytes are data rate and sleep time information
    # 5-dr5 5min, 4-dr4 10min, 3-dr3 15min, 2-dr2 30min, 1-dr1 60min, 0-dr0 90min, 6-do not change
    drStr = downlinkStr[0:2]
    drInt = int(drStr, 10)
    if not drStr == "06" and not drInt == pycom.nvs_get("dr"):
        # set new data rate
        pycom.nvs_set("dr", drInt)

        # set new sleep time
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
