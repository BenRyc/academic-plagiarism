from mcpi import minecraft
from mcpi import block
import random
from Room import Room

mc = minecraft.Minecraft.create()

mc.postToChat("no squere")

def makeRoom(room, t):

    mc.setBlocks(room.x1, room.y, room.z1, room.x2, room.y +3, room.z2, t)


    for i in room.doors:
        mc.setBlock(i[0], room.y, i[1], 50)


def houseInator(x1, y1, z1):
    rooms = []
    x2 = x1 + random.randint(15, 30)
    z2 = z1 + random.randint(15, 30)



def roomMitosis(room, d):
    if d != 0 and abs(room.x1 - room.x2) >= 6 and abs(room.z1 - room.z2) >= 6:
        if random.randint(0,2) == 1:
            print(room.x1, room.x2)
            if room.x1 - room.x2 -3 > 0:
                devixor = random.randint(3, abs(room.x1 - room.x2 - 3))
            else:
                devixor = - random.randint(3, abs(room.x1 - room.x2 - 3))

            print(room.z1, room.z2)
            if room.z1 - room.z2 - 3 > 0:
                devizor = random.randint(3, abs(room.z1 - room.z2 - 3))
            else:
                devizor = -random.randint(3, abs(room.z1 - room.z2 - 3))

            room1 = Room(room.x1, room.z1, room.x1 - devixor, room.z2, room.y, None, [(room.x1 + devixor, room.z1 + devizor)], None)
            room2 = Room(room.x1 - devixor, room.z1, room.x2, room.z2, room.y, None, [(room.x1 + devixor, room.z1 + devizor)], None)

            print(room1)
            print(room2)

            if room.doors[-1][0] >= room.x1 + devixor:
                room1.doors.append(room.doors[-1])
            else:
                room2.doors.append(room.doors[-1])
        else:
            print(room.x1, room.x2)
            if room.x1 - room.x2 -3 > 0:
                devixor = random.randint(3, abs(room.x1 - room.x2 - 3))
            else:
                devixor = - random.randint(3, abs(room.x1 - room.x2 - 3))

            print(room.z1, room.z2)
            if room.z1 - room.z2 - 3 > 0:
                devizor = random.randint(3, abs(room.z1 - room.z2 - 3))
            else:
                devizor = -random.randint(3, abs(room.z1 - room.z2 - 3))

            room1 = Room(room.x1, room.z1, room.x2, room.z1 - devizor, room.y, None, [(room.x1 + devixor, room.z1 + devizor)], None)
            room2 = Room(room.x1, room.z1 - devizor, room.x2, room.z2, room.y, None, [(room.x1 + devixor, room.z1 + devizor)], None)

            print(room1)
            print(room2)

            if room.doors[-1][0] >= room.z1 + devizor:
                room1.doors.append(room.doors[-1])
            else:
                room2.doors.append(room.doors[-1])

        rooms = []

        for i in roomMitosis(room1, d-1):
            rooms.append(i)

        for i in roomMitosis(room2, d-1):
            rooms.append(i)


        return rooms
    else:
        return [room]



x, y, z = mc.player.getPos()

t = 14

rooms = roomMitosis(Room(x, z, x+25, z+25, y,None, [(x+3, z)], None), 5)

for room in rooms:
    makeRoom(room, t)
    t += 1
