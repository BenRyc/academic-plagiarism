from mcpi.minecraft import Minecraft
from mcpi import block

def isAirBelow(x,y,z):
    if (Minecraft.create().getBlock(x, y-1, z) == block.AIR.id):
        return True
    else:
        return False
    
mc = Minecraft.create()
player = mc.player

origin = player.getPos()

if isAirBelow(origin.x, origin.y-1, origin.z):
    mc.postToChat("Yes")

else:
    mc.postToChat("No")



