from mcpi import minecraft
from mcpi import block
import random
from Room import Room

mc = minecraft.Minecraft.create()

mc.postToChat("no squere")


def houseInator(x1, y1, z1):
    rooms = []
    x2 = x1 + random.randint(15, 30)
    z2 = z1 + random.randint(15, 30)



def roomMitosis(room, d):
    if d == 0:
        if random.randint(0,2) == 1:
            devixor = random.randint(2, room.x1 - room.x2 - 5)
            devizor = random.randint(2, room.z1 - room.z2 - 2)

            room1 = Room(room.x1, room.z1, room.x1 + devixor, room.z2, room.y, palette, [(room.x1 + devixor, room.z1 + devizor)], None)
            room2 = Room(room.x1 + devixor, room.z1, room.x2, room.z2, room.y, palette, [(room.x1 + devixor, room.z1 + devizor)], None)

            if room.door[-1][0] >= room.x1 + devixor:
                room1.door.append(room.door)
            else:
                room2.door.append(room.door)
        else:
            devixor = random.randint(2, room.x1 - room.x2 - 5)
            devizor = random.randint(2, room.z1 - room.z2 - 2)

            room1 = Room(room.x1, room.z1, room.x1, room.z2 + devizor, room.y, palette, [(room.x1 + devixor, room.z1 + devizor)], None)
            room2 = Room(room.x1, room.z1 + devizor, room.x2, room.z2, room.y, palette, [(room.x1 + devixor, room.z1 + devizor)], None)

            if room.door[-1][0] >= room.z1 + devixor:
                room1.door.append(room.door)
            else:
                room2.door.append(room.door)
