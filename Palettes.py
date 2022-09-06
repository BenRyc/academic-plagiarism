from mcpi import block
import random

class housePalette():
    def __init__(self, trim=None, floor=None, walls=None, ceiling=None, roof=None):
        self.trim = trim
        self.floor = floor
        self.walls = walls
        self.ceiling = ceiling
        self.roof = roof

    def returnPalette(self):
        
        return f'trim:{self.trim}, floor:{self.floor}, walls:{self.walls}, ceiling:{self.ceiling}, roof:{self.roof}'
        
        
    def pickPalette(self):
        trimOptions = [block.WOOD]
        floorOptions = [block.WOOD]
        wallOptions = [block.WOOD]
        ceilingOptions = [block.WOOD]
        roofOptions = [block.WOOD]

        allOptions = [trimOptions, floorOptions, wallOptions, ceilingOptions, roofOptions]
        choicesArr = []

        #choose palette 
        for arr in allOptions:
            choiceInt = random.randint(0, len(arr)-1)
            choicesArr.append(arr[choiceInt])

        #change house attributes
        self.trim = choicesArr[0]
        self.floor = choicesArr[1]
        self.walls = choicesArr[2]
        self.ceiling = choicesArr[3]
        self.roof = choicesArr[4]

