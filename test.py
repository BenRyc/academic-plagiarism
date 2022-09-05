from mcpi import minecraft

mc = minecraft.Minecraft.create()

mc.postToChat("Hello world")

x, y, z = mc.player.getPos()


print(x, y, z)

mc.player.setPos(x, y+100, z)
