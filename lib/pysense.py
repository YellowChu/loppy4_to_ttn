from pycoproc import Pycoproc

__version__ = '1.5.1'

class Pysense(Pycoproc):

    def __init__(self, i2c=None, sda='P22', scl='P21'):
        Pycoproc.__init__(self, i2c, sda, scl)
