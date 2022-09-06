from mcpi import block
import random

class housePalette():
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
        
    def returnPalette(self):
        palette = []
        
        palette.append(self.Trim)
        palette.append(self.Floor)
        palette.append(self.Walls)
        palette.append(self.Ceiling)
        palette.append(self.Roof)
        
        return palette
        
        
def palletePicker():
    newHouse = housePalette()
    
    #Edit below to how many palettes there are
    numOfPalettes = 1
    #^^^^^^^^^^^^^^^^
    
    choice = random.randint(0, numOfPalettes-1)
    
    if choice == 0:
        newHouse.initOak()
        return newHouse.returnPalette()
    
    else:
        newHouse.initOak()
        return newHouse.returnPalette()