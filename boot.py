# boot.py -- run on boot-up
import pycom

pycom.heartbeat_on_boot(False)
pycom.wifi_on_boot(False)
