from mcpi import block
import random

class palette():
    def __init__(self):
        self.Trim = None
        self.Floor = None
        self.Walls = None
        self.Ceiling = None
        self.Roof = None
        
    def initOak(self):
        self.Trim = block.WOOD.withData(0)
        self.Floor = block.WOOD_PLANKS
        self.Walls = block.WOOD_PLANKS
        self.Ceiling = block.STONE_BRICK
        self.Roof = block.STAIRS_COBBLESTONE
        
        
def palletePicker():
    housePalette = palette()
    
    #Edit below to how many palettes there are
    numOfPalettes = 1
    #^^^^^^^^^^^^^^^^
    
    choice = random.randint(0, numOfPalettes-1)
    
    if choice == 0:
        newHouse.initOak()
        return housePalette
    
    else:
        newHouse.initOak()
        return housePalette