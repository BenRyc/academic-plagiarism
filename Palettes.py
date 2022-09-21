from mcpi import block
import random
'''
This class generates the building materials used for each house

***Materials Key***
WALLS:
(159,1) terracotta orange
(159,3) terracotta light blue
(159,4) terracotta yellow
(159,5) terracotta green
(159,6) terracotta pink
(159,9) teracotta cyan
(159,14) teracotta red
(251,0) concrete white

TRIM:
(17,0) log oak
(17,1) log spruce
(162,1) log dark oak

(171.1.4) carpet red
'''
class housePalette():
    def __init__(self, trim=None, floor=None, walls=None, ceiling=None, roof=None):
        self.trim = trim
        self.floor = floor
        self.walls = walls
        self.ceiling = ceiling
        self.roof = roof

    def __str__(self):
        return f'trim:{self.trim}, floor:{self.floor}, walls:{self.walls}, ceiling:{self.ceiling}, roof:{self.roof}'
        
        
    def pickPalette(self):
        trimOptions = [[17,0], [17,1], [162,1]]
        floorOptions = [block.WOOD, block.STONE]
        wallOptions = [[159, 1], [159,3], [159,4],[159,5],[159,6],[159,9],[159,14]]
        ceilingOptions = [block.WOOD, block.STONE]
        roofOptions = [block.WOOD, block.STONE]

        #randomised palette
        self.trim = random.choice(trimOptions)
        self.floor = random.choice(floorOptions)
        self.walls = random.choice(wallOptions)
        self.ceiling = random.choice(ceilingOptions)
        self.roof = random.choice(roofOptions)

