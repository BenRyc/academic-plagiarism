from mcpi import minecraft
from mcpi import block

mc = minecraft.Minecraft.create()

playerPos = mc.player.getPos()

print(mc.getBlockWithData(playerPos.x, playerPos.y -1, playerPos.z))