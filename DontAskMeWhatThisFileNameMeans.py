from mcpi import minecraft
from mcpi import block
import random
from Room import Room

mc = minecraft.Minecraft.create()

mc.postToChat("roomEx")


def genRoom(s, x, y, z, x2, z2):
    doors = []


    if random.randint(0, 3) == 1 or s == 0:
        doors.append((x, z + random.randint(1, int(z2 - z)), 0))
    if random.randint(0, 3) == 1 or s == 1:
        doors.append((x2, z + random.randint(1, int(z2 - z)), 1))
    if random.randint(0, 3) == 1 or s == 2:
        doors.append((x + random.randint(1, int(x2 - x)), z, 2))
    if random.randint(0, 3) == 1 or s == 3:
        doors.append((x + random.randint(1, int(x2 - x)), z2, 3))

    return Room(x, z, x2, z2, y-1, None, doors, None)



def roomRange(rooms, s, x, z):
    maxx = 999999
    maxz = 999999
    minx = -999999
    minz = -999999

    for room in rooms:
        if room != rooms[-1]:
            if s == 0:
                d1 = z - room.z1
                d2 = z - room.z2

                if d1 >= 0 and d2 >= 0:
                    if d1 < d2 and d1 < maxz:
                        maxz = d1
                    elif d2 < d1 and d2 < maxz:
                        maxz = d2
                elif d1 < 0 and d2 < 0:
                    if d1 > d2 and d1 > maxz:
                        maxSz = d1
                    elif d2 > d1 and d2 > maxz:
                        maxz = d2
                elif d1 >= 0 and d2 < 0:
                    if d1 > maxz:
                        maxz = d1
                    elif d2 > d1 and d2 > maxz:
                        maxz = d2

            elif s == 1:
                x1 = x
                x2 = x1 + random.randint(4, 7)
                z1 = z - random.randint(1, 4)
                z2 = z + random.randint(1, 4)

                room = genRoom(0, x1, y, z1, x2, z2)
                rooms.append(room)
            elif s == 2:
                x1 = x
                x2 = x1 + random.randint(4, 7)
                z1 = z - random.randint(1, 4)
                z2 = z + random.randint(1, 4)

                room = genRoom(3, x1, y, z1, x2, z2)
                rooms.append(room)
            elif s == 3:
                x1 = x
                x2 = x1 + random.randint(4, 7)
                z1 = z - random.randint(1, 4)
                z2 = z + random.randint(1, 4)

                room = genRoom(2, x1, y, z1, x2, z2)
                rooms.append(room)



def makeRoom(room):

    mc.setBlocks(room.x1, room.y, room.z1, room.x2, room.y +3, room.z2, 5)


    for i in room.doors:
        mc.setBlock(i[0], room.y, i[1], 50)

def genHouse(x, y, z):
    rooms = []

    s = 0

    for i in range(0, 3):
        if s == 0:
            x1 = x
            x2 = x1 + random.randint(4, 7)
            z1 = z - random.randint(1, 4)
            z2 = z + random.randint(1, 4)

            room = genRoom(1, x1, y, z1, x2, z2)
            rooms.append(room)
        elif s == 1:
            x1 = x
            x2 = x1 + random.randint(4, 7)
            z1 = z - random.randint(1, 4)
            z2 = z + random.randint(1, 4)

            room = genRoom(0, x1, y, z1, x2, z2)
            rooms.append(room)
        elif s == 2:
            x1 = x
            x2 = x1 + random.randint(4, 7)
            z1 = z - random.randint(1, 4)
            z2 = z + random.randint(1, 4)

            room = genRoom(3, x1, y, z1, x2, z2)
            rooms.append(room)
        elif s == 3:
            x1 = x
            x2 = x1 + random.randint(4, 7)
            z1 = z - random.randint(1, 4)
            z2 = z + random.randint(1, 4)

            room = genRoom(2, x1, y, z1, x2, z2)
            rooms.append(room)

        s = room.doors[0][2]
        x = room.doors[0][0]
        z = room.doors[0][1]
        makeRoom(room)






x, y, z = mc.player.getPos()

genHouse(x, y, z)
