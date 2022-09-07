from mcpi.minecraft import Minecraft
from mcpi import block
import random
import Palettes
import Room 

mc = Minecraft.create()

def isAirBelow(x,y,z):
    if (Minecraft.create().getBlock(x, y-1, z) == block.AIR.id):
        return True
    else:
        return False
    

wall1Size = random.randint(2, 5)
wall2Size = random.randint(2, 5)

position = mc.player.getPos()

position.y = 255

for x in range(wall1Size):
    while isAirBelow(position[0], position[1], position[2]):
        position[1] -= 1
        

    
    




