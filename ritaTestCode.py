from mcpi import minecraft
from mcpi import block
import Palettes 
mc = minecraft.Minecraft.create()

playerPos = mc.player.getPos()
x,y,z = playerPos.x, playerPos.y, playerPos.z
#print(mc.getBlockWithData(playerPos.x, playerPos.y -1, playerPos.z))

mc.postToChat(mc.getBlockWithData(playerPos.x, playerPos.y-1, playerPos.z))

#newPalette = Palettes.housePalette()

#newPalette.pickPalette()
#mc.postToChat(newPalette.returnPalette())



