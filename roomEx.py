from mcpi import minecraft
from mcpi import block
import random
from Room import Room

mc = minecraft.Minecraft.create()

mc.postToChat("roomEx")


def genRoom(s, x, y, z):
    doors = []
    z2 = int(z + random.randint(4, 7))
    x2 = int(x + random.randint(4, 7))



    if random.randint(0, 3) == 1 or s == 0:
        doors.append((x, z + random.randint(1, int(z2 - z))))
    if random.randint(0, 3) == 1 or s == 1:
        doors.append((x2, z + random.randint(1, int(z2 - z))))
    if random.randint(0, 3) == 1 or s == 2:
        doors.append((x + random.randint(1, int(x2 - x)), z))
    if random.randint(0, 3) == 1 or s == 3:
        doors.append((x + random.randint(1, int(x2 - x)), z2))

    return Room(x, z, x2, z2, y-1, None, doors, None)




def makeRoom(room):

    mc.setBlocks(room.x1, room.y, room.z1, room.x2, room.y, room.z2, 34)

    for i in room.doors:
        mc.setBlock(i[0], room.y, i[1], 50)



x, y, z = mc.player.getPos()

room = genRoom(0, x, y, z)

makeRoom(room)
