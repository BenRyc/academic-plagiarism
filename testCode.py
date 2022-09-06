from mcpi import minecraft
from mcpi import block

mc = minecraft.Minecraft.create()

mc.postToChat("Hello world")

x, y, z = mc.player.getPos()


print(x, y, z)

#mc.player.setPos(x, y+100, z)

mc.setBlock(x+1, y, z, 34)

while True:
    x, y, z = mc.player.getPos()
    block_beneath = mc.getBlock(x, y-1, z)
    print(block_beneath)
    if block_beneath == block.AIR.id:
        mc.setBlock(x, y-1, z, 34)
