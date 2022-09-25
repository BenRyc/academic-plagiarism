from mcpi import minecraft
from mcpi import block
import Palettes 
import House
import random


mc = minecraft.Minecraft.create()

playerPos = mc.player.getPos()
x,y,z = int(playerPos.x), int(playerPos.y), int(playerPos.z)


print(mc.getBlockWithData(x+1,y,z))

for i in range(13):

    mc.setBlock(x, y, z+i, block.BED.withData(i))
# random.seed(1)
# mc.setBlock(x,y,z,26,4,3)






