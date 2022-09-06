from mcpi import minecraft
from mcpi import block
import Palettes 
mc = minecraft.Minecraft.create()

playerPos = mc.player.getPos()

print(mc.getBlockWithData(playerPos.x, playerPos.y -1, playerPos.z))

newPalette = Palettes.housePalette()

newPalette.pickPalette()
mc.postToChat(newPalette.returnPalette())
