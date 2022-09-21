from mcpi import minecraft
from mcpi import block
import Palettes 
import Decor


mc = minecraft.Minecraft.create()

playerPos = mc.player.getPos()
x,y,z = int(playerPos.x), int(playerPos.y), int(playerPos.z)

#mc.postToChat(mc.getBlockWithData(playerPos.x, playerPos.y-1, playerPos.z))


#-----Test Palette-----
#newPalette = Palettes.housePalette()

#newPalette.pickPalette()
#mc.postToChat(newPalette.returnPalette())


#-----Test Decor-----

newDecor = Decor.Decoration([253,95,-18], [255,97,-16], [254,95,-16], 'bedroom')

newDecor.roomDecoratorInator()


