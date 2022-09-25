from mcpi.minecraft import Minecraft
from mcpi import block

x = 10
z = 10
blocksAvoid = [8, 9, 10, 11, 18, 31, 32, 37, 38, 39, 40, 78]

mc = Minecraft.create()

origin = mc.player.getPos()

for zCoord in range(z):
    for xCoord in range(x):
        x = round(xCoord+origin.x)
        y = mc.getHeight(xCoord+origin.x, zCoord+origin.z)
        z = round(zCoord+origin.z)
        valid = True
        blockScan = mc.getBlockWithData(x, y, z)
        
        for scan in blocksAvoid:
            scannedBlock = blockScan.id
            if scannedBlock == scan:
                valid = False
                
        if valid == False:
            mc.setBlock(x, y, z, 0)
        
        
