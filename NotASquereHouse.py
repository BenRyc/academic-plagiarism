from mcpi import minecraft
from mcpi import block
import random
from Room import Room

mc = minecraft.Minecraft.create()

mc.postToChat("no squere")

def makeRoom(room, t):

    mc.setBlocks(room.x1, room.y, room.z1, room.x1, room.y +3, room.z2, t)
    mc.setBlocks(room.x2, room.y, room.z1, room.x2, room.y +3, room.z2, t)
    mc.setBlocks(room.x1, room.y, room.z1, room.x2, room.y +3, room.z1, t)
    mc.setBlocks(room.x1, room.y, room.z2, room.x2, room.y +3, room.z2, t)


    for i in room.doors:
        mc.setBlock(i[0], room.y, i[1], 50)


def houseInator(x1, y1, z1):
    rooms = []
    x2 = x1 + random.randint(15, 30)
    z2 = z1 + random.randint(15, 30)



def roomMitosis(room):
    if abs(room.x1 - room.x2) >= 13 or abs(room.z1 - room.z2) >= 13:

        zorx = random.randint(0,2)
        zof = 6
        xof = 6

        if abs(room.x1 - room.x2) < 13:
            zorx = 0
            xof = 1
        if abs(room.z1 - room.z2) < 13:
            zorx = 1
            zof = 1


        print(room.x1, room.x2)
        if room.x1 > room.x2:
            devixor = random.randint(int(room.x2 + xof), int(room.x1 -xof))
        else:
            devixor = random.randint(int(room.x1 + xof), int(room.x2 -xof))
        print(devixor)

        print(room.z1, room.z2)
        if room.z1 > room.z2:
            devizor = random.randint(int(room.z2 + zof), int(room.z1 -zof))
        else:
            devizor = random.randint(int(room.z1 + zof), int(room.z2 -zof))
        print(devizor)



        if zorx == 1:

            room1 = Room(room.x1, room.z1, devixor, room.z2, room.y, None, [(devixor,devizor)], None)
            room2 = Room(devixor, room.z1, room.x2, room.z2, room.y, None, [(devixor,devizor)], None)

            print(room1)
            print(room2)

            if room.doors[-1][0] >= devixor:
                room1.doors.append(room.doors[-1])
            else:
                room2.doors.append(room.doors[-1])
        else:
            room1 = Room(room.x1, room.z1, room.x2, devizor, room.y, None, [(devixor,devizor)], None)
            room2 = Room(room.x1, devizor, room.x2, room.z2, room.y, None, [(devixor,devizor)], None)

            print(room1)
            print(room2)

            if room.doors[-1][0] >=  devizor:
                room1.doors.append(room.doors[-1])
            else:
                room2.doors.append(room.doors[-1])

        rooms = []

        for i in roomMitosis(room1):
            rooms.append(i)

        for i in roomMitosis(room2):
            rooms.append(i)


        return rooms
    else:
        return [room]



x, y, z = mc.player.getPos()

t = 14

rooms = roomMitosis(Room(x, z, x+25, z+25, y,None, [(x+3, z)], None))

for room in rooms:
    makeRoom(room, t)
    #input('st')
    t += 1
