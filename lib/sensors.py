from pysense import Pysense
from SI7006A20 import SI7006A20
from MPL3115A2 import MPL3115A2, PRESSURE

class Sensors:
    def __init__(self):
        py = Pysense()

        mp_pre = MPL3115A2(py,mode=PRESSURE)
        si = SI7006A20(py)

        self.Pysense = py
        self.Pressure = mp_pre.pressure()
        self.Temperature = si.temperature()
        self.Battery = py.read_battery_voltage()
