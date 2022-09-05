from mcpi.minecraft import Minecraft

mc = Minecraft.create()
player = mc.player

position = player.getPos()


player.setPos(position.x-1,position.y,position.z-1)

mc.setBlock(position.x,position.y,position.z,46)
mc.setBlock(position.x,position.y+1,position.z,70)
player.setPos(position.x,position.y+2,position.z)
