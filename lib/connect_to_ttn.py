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

    # # create an OTAA authentication parameters
    # app_eui = ubinascii.unhexlify('70B3D57ED003A888')
    # app_key = ubinascii.unhexlify('758ACFD0ACF0635A519F5B3063015A48')
    # # dev_eui = ubinascii.unhexlify('70B3D5499E3B06C1')
    #
    # # join a network using OTAA (Over the Air Activation)
    # lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
    # # lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

    # create an ABP authentication parameters
    dev_addr = struct.unpack(">l", ubinascii.unhexlify('2601139E'))[0]
    nwk_swkey = ubinascii.unhexlify('40AEB0C6FE63891E9359447420338682')
    app_swkey = ubinascii.unhexlify('66B80DBA96BA63BF8C04FE007C6AB76A')

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
