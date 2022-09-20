from mcpi import minecraft
from mcpi import block
import random
import Palettes
from Room import Room


def roomAdjinator(rooms):

    # wall adding

    for room in rooms:
        for i in range(room.x1, room.x2):
            room.walls.add((i, room.z1))
            room.walls.add((i, room.z2))

        for i in range(room.z1, room.z2):
            room.walls.add((room.x1, i))
            room.walls.add((room.x2, i))

        room.walls.remove((room.x1, room.z1))
        room.walls.remove((room.x1, room.z1+1))
        room.walls.remove((room.x1+1, room.z1))

        room.walls.remove((room.x2, room.z1))
        room.walls.remove((room.x2, room.z1+1))
        room.walls.remove((room.x2-1, room.z1))

        room.walls.remove((room.x1, room.z2))
        room.walls.remove((room.x1, room.z2-1))
        room.walls.remove((room.x1+1, room.z2))

        # room.walls.remove((room.x2, room.z2))
        room.walls.remove((room.x2, room.z2-1))
        room.walls.remove((room.x2-1, room.z2))

        # print('walls done')
        # print(len(room.walls))
        # print((room.x2 - room.x1) *2 + (room.z2 - room.z1) *2 -4)
        # print()

    #adj adding
    for roomi in rooms:
        for roomj in rooms:
            #print(roomi.walls.intersection(roomj.walls))
            if roomi != roomj and len(roomi.walls.intersection(roomj.walls)) > 0:
                roomi.adj.add(roomj)
                roomj.adj.add(roomi)

    return rooms


def roomCull(rooms):

    inRooms = []
    ajRooms = set()
    outRooms = []

    # adds the first room to the inrooms
    inRooms.append(rooms[0])
    for room in inRooms[0].adj:
        ajRooms.add(room)

    # picks a certan percentage of the rooms to keep and makes sure they are adjacent
    for i in range(int(len(rooms)/1.4)):
        choice = random.choice(list(ajRooms))

        ajRooms.remove(choice)
        inRooms.append(choice)
#nice
        for room in choice.adj:
            ajRooms.add(room)

    for i in rooms:
        if room not in inRooms:
            outRooms.append(room)

    return inRooms, outRooms

def roomAdd(rooms):
    # adds walls between every room
    for room in rooms:
        for adj in room.adj:
            if adj in rooms:
                room.doors.append(list(room.walls.intersection(adj.walls))[0])

    rooms[0].doors.append((rooms[0].x1 +3, rooms[0].z1))
    return rooms

def roomMitosis(room):
    # Tests if the room is big enough to split
    if abs(room.x1 - room.x2) >= 13 or abs(room.z1 - room.z2) >= 13:

        # decides if we split in the x or yaxis
        zorx = random.randint(0,2)
        # the minimum size of the room in the x and z axis
        zof = 6
        xof = 6

        # sets the split direction depending if the room will be to small
        if abs(room.x1 - room.x2) < 13:
            zorx = 0
            xof = 1
        if abs(room.z1 - room.z2) < 13:
            zorx = 1
            zof = 1


        # Finds a mid point of the room that can be devided apon
        if room.x1 > room.x2:
            devixor = random.randint(int(room.x2 + xof), int(room.x1 -xof))
        else:
            devixor = random.randint(int(room.x1 + xof), int(room.x2 -xof))

        if room.z1 > room.z2:
            devizor = random.randint(int(room.z2 + zof), int(room.z1 -zof))
        else:
            devizor = random.randint(int(room.z1 + zof), int(room.z2 -zof))

        # makes 2 rooms devieded on the already created midpoint
        if zorx == 1:
            room1 = Room(room.x1, room.z1, devixor, room.z2, room.y, [], None)
            room2 = Room(devixor, room.z1, room.x2, room.z2, room.y, [], None)

        else:
            room1 = Room(room.x1, room.z1, room.x2, devizor, room.y, [], None)
            room2 = Room(room.x1, devizor, room.x2, room.z2, room.y, [], None)

        rooms = []

        # recursivly devides the rooms once again
        for i in roomMitosis(room1):
            rooms.append(i)
        for i in roomMitosis(room2):
            rooms.append(i)



        return rooms
    else:
        return [room]



class House:
    def __init__(self, x, y, z, length, width):
        self.x = x
        self.z = z
        self.y = y
        self.length = length
        self.width = width

        self.palette = Palettes.housePalette()
        self.palette.pickPalette()

        self.inRooms = []
        self.outRooms = []


    #generate floorplan
    def generateRooms(self):
        rooms = roomMitosis(Room(self.x, self.z, self.x+self.length, self.z+self.width, self.y, [], None))

        rooms = roomAdjinator(rooms)

        self.inRooms, self.outRooms = roomCull(rooms)

        self.inRooms = roomAdd(self.inRooms)


    def build(self, mc):

        for room in self.inRooms:

            mc.setBlocks(room.x1, room.y, room.z1, room.x1, room.y +3, room.z2, self.palette.walls)
            mc.setBlocks(room.x2, room.y, room.z1, room.x2, room.y +3, room.z2, self.palette.walls)
            mc.setBlocks(room.x1, room.y, room.z1, room.x2, room.y +3, room.z1, self.palette.walls)
            mc.setBlocks(room.x1, room.y, room.z2, room.x2, room.y +3, room.z2, self.palette.walls)

            mc.setBlocks(room.x1, room.y, room.z1, room.x2, room.y, room.z2, self.palette.floor)
            mc.setBlocks(room.x1, room.y +4, room.z1, room.x2, room.y +4, room.z2, self.palette.ceiling)

            mc.setBlocks(room.x1, room.y, room.z1, room.x1, room.y +4, room.z1, self.palette.trim)
            mc.setBlocks(room.x1, room.y, room.z2, room.x1, room.y +4, room.z2, self.palette.trim)
            mc.setBlocks(room.x2, room.y, room.z1, room.x2, room.y +4, room.z1, self.palette.trim)
            mc.setBlocks(room.x2, room.y, room.z2, room.x2, room.y +4, room.z2, self.palette.trim)

            for door in room.doors:

                mc.setBlocks(door[0], room.y+1, door[1], door[0], room.y +2, door[1], 0)



if __name__ == '__main__':

    mc = minecraft.Minecraft.create()

    mc.postToChat("House main")

    x, y, z = mc.player.getPos()

    house = House(int(x), int(y), int(z), 25, 25)

    house.generateRooms()
    house.build(mc)
