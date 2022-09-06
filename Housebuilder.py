from mcpi.minecraft import Minecraft
from mcpi import block
import random
import Palettes

def isAirBelow(x,y,z):
    if (Minecraft.create().getBlock(x, y-1, z) == block.AIR.id):
        return True
    else:
        return False

wall1Size = random.randint(2, 5)
wall2Size = random.randint(2, 5)

palette = Palettes.palletePicker()

print(palette)
