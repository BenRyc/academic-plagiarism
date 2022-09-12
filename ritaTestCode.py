from mcpi import minecraft
from mcpi import block
import Palettes 
import Decor
mc = minecraft.Minecraft.create()

playerPos = mc.player.getPos()
x,y,z = playerPos.x, playerPos.y, playerPos.z
#print(mc.getBlockWithData(playerPos.x, playerPos.y -1, playerPos.z))

mc.postToChat(mc.getBlockWithData(playerPos.x, playerPos.y-1, playerPos.z))


#-----Test Palette-----
#newPalette = Palettes.housePalette()

#newPalette.pickPalette()
#mc.postToChat(newPalette.returnPalette())


#-----Test Decor-----
newDecor = Decor([253,95,-17], [255,97,-15], [254,95,-15], 'bedroom')

newDecor.roomDecoratorInator()


