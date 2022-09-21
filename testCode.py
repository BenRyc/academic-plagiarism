from mcpi import minecraft
from mcpi import block
from mctools import RCONClient
from mcrcon import MCRcon


mc = minecraft.Minecraft.create()

mcr = MCRcon('localhost', 8080)
mcr.connect()
resp = mcr.command("/whitelist add bob")
print(resp)
mcr.disconnect()

playerPos = mc.player.getPos()