from mcpi.minecraft import Minecraft
from mcpi import block

def getTopHeight(X, Z):
    
    Y = 255
    
    while mc.getBlock(X, Y, Z) == 0:
        Y -= 1
        
    return Y

mc = Minecraft.create()

origin = mc.player.getPos()

rangeX = 5
rangeZ = 5

scan = []

for Zcoord in range(rangeZ * 2):
    scanZ = origin.z + ((rangeZ * (-1)) + Zcoord)
    row = []
    
    for Xcoord in range(rangeX * 2):
        scanX = origin.x + ((rangeX * (-1)) + Xcoord)
        row.append((scanX, getTopHeight(scanX, scanZ), scanZ))
        mc.setBlock(scanX, getTopHeight(scanX, scanZ), scanZ, 1)
        
    scan.append(row)
    
print(scan)
        
        
