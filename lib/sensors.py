import time
import pycom
from pysense import Pysense
import machine

from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

class Sensors:
    def __init__(self):
        py = Pysense()

        mp_alt = MPL3115A2(py,mode=ALTITUDE)
        altitude = mp_alt.altitude()    # need to define altitude before changing mode
        mp_pre = MPL3115A2(py,mode=PRESSURE)
        si = SI7006A20(py)
        li = LIS2HH12(py)

        self.Altitude = altitude
        self.Pressure = mp_pre.pressure()
        self.Temperature = si.temperature()
        self.Acceleration = li.acceleration()
        self.Battery = py.read_battery_voltage()
