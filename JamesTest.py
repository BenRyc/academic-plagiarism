from mcpi.minecraft import Minecraft
from mcpi import block

mc = Minecraft.create()

origin = mc.player.getPos()

rangeX = 100
rangeZ = 100

scan = []
blockNum = 0

for Zcoord in range(rangeZ):
    scanZ = origin.z + ((rangeZ * (-1)) + Zcoord)
    row = []
    
    for Xcoord in range(rangeX):
        scanX = origin.x + ((rangeX * (-1)) + Xcoord)
        Y = mc.getHeight(scanX, scanZ)
        row.append((int(scanX), int(Y), int(scanZ)))
        blockNum += 1
        print(str(blockNum) + "/" + str(rangeX*rangeZ))
        
    scan.append(row)
    
print(scan)
        
        
