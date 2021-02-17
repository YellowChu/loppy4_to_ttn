import pycom
import struct
import time
import ubinascii
from network import LoRa

def connect_to_ttn():
    # Initialise LoRa in LORAWAN mode.
    # Please pick the region that matches where you are using the device:
    # Asia = LoRa.AS923
    # Australia = LoRa.AU915
    # Europe = LoRa.EU868
    # United States = LoRa.US915
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

    # create an ABP authentication parameters
    dev_addr = struct.unpack(">l", ubinascii.unhexlify('Enter dev_addr'))[0]
    nwk_swkey = ubinascii.unhexlify('Enter nwk_swkey')
    app_swkey = ubinascii.unhexlify('Enter app_swkey')
    # join a network using ABP (Activation By Personalization)
    lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

    # Blinking blue led if connecting
    while not lora.has_joined():
        # pycom.rgbled(0x000011)
        time.sleep(3)
        # pycom.rgbled(0x000000)
        print("has not joined")

    # Blue led when connected
    pycom.rgbled(0x000011)
    print("has joined")

    return lora
