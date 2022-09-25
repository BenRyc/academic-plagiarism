from mcpi import minecraft
from mcpi import block
import Palettes 
import House
import random


mc = minecraft.Minecraft.create()
 
playerPos = mc.player.getPos()
x,y,z = int(playerPos.x), int(playerPos.y), int(playerPos.z)


print(mc.getBlockWithData(x,y-1,z))


mc.setBlock(x+1,y,z, 54,2)

# random.seed(1)
# mc.setBlock(x,y,z,26,4,3)






