import mcpi
import random

class House():
    def __init__(self, x, z, length, width): 

        self.length = length
        self.width = width
        self.dimensions = {"x1":x, "z1":z, "x2":x+length, "z2":z+width}
        
        



