from mcpi import minecraft
from mcpi import block
import Palettes 
import House
import random


mc = minecraft.Minecraft.create()

playerPos = mc.player.getPos()
x,y,z = int(playerPos.x), int(playerPos.y), int(playerPos.z)


random.seed(1)
testHouse = House.House(x,y,z, 20,20)

testHouse.generateRooms()
testHouse.build(mc)
testHouse.decorate





