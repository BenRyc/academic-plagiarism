from mcpi import minecraft
from mcpi import block
import random
import Palettes
from Room import Room

def decorBedroom(room, coor1, coor2, dirWithDoor):
    # #find what wall has a door
    #     doorX = self.doorsCoor[0]
    #     doorZ = self.doorsCoor[2]
    #     #mc.postToChat(f'{doorX},{doorZ}')

    #     #facing east
    #     if doorZ == self.coor1[2]:
    #         print('-z')
    #         doorDir = '-z'
    #     #facing south
    #     elif doorZ == self.coor2[2]:
    #         print('+z')
    #         doorDir = '+z'

    #     elif doorX == self.coor2[0]:
    #         print('+x')
    #         doorDir = '+x'
    #     #facing west
    #     elif doorX == self.coor1[0]:
    #         print('-x')
    #         doorDir = '-x'

    #     else:
    #         raise ValueError('Door is not in a valid position.')


    #bedrooms can only have one door
    if len(dirWithDoor) > 1:
        print('bedrooms must have only one wall with doors')
        return 

    if '-z' in dirWithDoor: 
        #bookshelf
        for i in range(0,room.height):
            mc.setBlock(room.coor2[0],room.coor1[1]+i,room.coor1[2], 47,0)
        #crafting table
        mc.setBlock(room.coor1[0],room.coor1[1],room.coor1[2],58)
        #bed and table
        mc.setBlock(room.coor2[0],room.coor1[1],room.coor2[2]-1,26)
        mc.setBlock(room.coor2[0]-1,room.coor1[1],room.coor2[2],53,6)
        
    elif '+z' in dirWithDoor:
        for i in range(0,room.height):
            mc.setBlock(room.coor1[0],room.coor1[1]+i,room.coor2[2], 47,0)
        mc.setBlock(room.coor2[0],room.coor1[1],room.coor2[2],58)

        

    elif '+x' in dirWithDoor:
        for i in range(0,room.height):
            mc.setBlock(room.coor2[0],room.coor1[1]+i,room.coor2[2], 47,0)
        mc.setBlock(room.coor2[0],room.coor1[1],room.coor1[2],58)

    elif '-x' in dirWithDoor:
        for i in range(0,room.height):
            mc.setBlock(room.coor1[0],room.coor1[1]+i,room.coor1[2], 47,0)
        mc.setBlock(room.coor1[0],room.coor1[1],room.coor2[2],58)
        mc.setBlock(room.coor2[0]-1,room.coor1[1],room.coor1[2],26)
        mc.setBlock(room.coor2[0],room.coor1[1],room.coor1[2]+1,53,4)
    
    #place bed and bedside table
    #place desk

def decorkitchen(self, coor1, coor2, dirWithDoor):
    pass
def decorDining(self, coor1, coor2, dirWithDoor):
    pass
def decorLiving(self, coor1, coor2, dirWithDoor):
    pass


def roomAdjinator(rooms):

    # wall adding

    for room in rooms:
        for i in range(room.x1, room.x2):
            room.walls.add((i, room.z1))
            room.walls.add((i, room.z2))

        for i in range(room.z1, room.z2):
            room.walls.add((room.x1, i))
            room.walls.add((room.x2, i))

        room.wallsEx = room.walls.copy()
        room.wallsEx.remove((room.x1, room.z1))
        room.wallsEx.remove((room.x1, room.z1+1))
        room.wallsEx.remove((room.x1+1, room.z1))

        room.wallsEx.remove((room.x2, room.z1))
        room.wallsEx.remove((room.x2, room.z1+1))
        room.wallsEx.remove((room.x2-1, room.z1))

        room.wallsEx.remove((room.x1, room.z2))
        room.wallsEx.remove((room.x1, room.z2-1))
        room.wallsEx.remove((room.x1+1, room.z2))

        # room.walls.remove((room.x2, room.z2))
        room.wallsEx.remove((room.x2, room.z2-1))
        room.wallsEx.remove((room.x2-1, room.z2))

        # print('walls done')
        # print(len(room.walls))
        # print((room.x2 - room.x1) *2 + (room.z2 - room.z1) *2 -4)
        # print()

    #adj adding
    for roomi in rooms:
        for roomj in rooms:
            #print(roomi.walls.intersection(roomj.walls))
            if roomi != roomj and len(roomi.wallsEx.intersection(roomj.wallsEx)) > 0:
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
    outWalls = set()
    for room in rooms:
        for adj in room.adj:
            if adj in rooms:
                door = list(room.wallsEx.intersection(adj.wallsEx))[0]
                if door[0] == room.x1:
                    door = door + tuple('x1')
                elif door[0] == room.x2:
                    door = door + tuple('x2')
                elif door[1] == room.z1:
                    door = door + tuple('z1')
                elif door[1] == room.z2:
                    door = door + tuple('z2')

                room.doors.append(door)

        outWalls.symmetric_difference_update(room.walls)

    fDoor = random.choice(list(outWalls))

    for room in rooms:
        if fDoor in list(room.walls):
            if fDoor[0] == room.x1:
                fDoor = fDoor + tuple('x1')
            elif fDoor[0] == room.x2:
                fDoor = fDoor + tuple('x2')
            elif fDoor[1] == room.z1:
                fDoor = fDoor + tuple('z1')
            elif fDoor[1] == room.z2:
                fDoor = fDoor + tuple('z2')

            room.doors.append(fDoor)
            room.decor = 'front'
    return rooms

def roomMitosis(room):
    # Tests if the room is big enough to split
    minSize = random.randint(13, 16)
    if abs(room.x1 - room.x2) >= minSize or abs(room.z1 - room.z2) >= minSize:

        # decides if we split in the x or yaxis
        zorx = random.randint(0,2)
        # the minimum size of the room in the x and z axis
        zof = 6
        xof = 6

        # sets the split direction depending if the room will be to small
        if abs(room.x1 - room.x2) < minSize:
            zorx = 0
            xof = 1
        if abs(room.z1 - room.z2) < minSize:
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
        self.foundation = []
        self.foundatonBlocks = []
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

        if random.randint(0,2) == 1:
            rooms = roomMitosis(Room(self.x, self.z, self.x+self.length, self.z+self.width, self.y+4, [], None))

            rooms = roomAdjinator(rooms)

            inRooms, outRooms = roomCull(rooms)

            inRooms = roomAdd(inRooms)

            for i in inRooms:
                self.inRooms.append(i)



    def build(self, mc):

        for room in reversed(self.inRooms):

            mc.setBlocks(room.x1, room.y, room.z1, room.x2, room.y +3, room.z2, 0)

            mc.setBlocks(room.x1, room.y, room.z1, room.x1, room.y +3, room.z2, self.palette.walls)
            mc.setBlocks(room.x2, room.y, room.z1, room.x2, room.y +3, room.z2, self.palette.walls)
            mc.setBlocks(room.x1, room.y, room.z1, room.x2, room.y +3, room.z1, self.palette.walls)
            mc.setBlocks(room.x1, room.y, room.z2, room.x2, room.y +3, room.z2, self.palette.walls)

            mc.setBlocks(room.x1, room.y, room.z1, room.x2, room.y, room.z2, self.palette.floor)
            mc.setBlocks(room.x1, room.y +4, room.z1, room.x2, room.y +4, room.z2, self.palette.ceiling)

            mc.setBlocks(room.x1, self.y-10, room.z1, room.x1, room.y +4, room.z1, self.palette.trim)
            mc.setBlocks(room.x1, self.y-10, room.z2, room.x1, room.y +4, room.z2, self.palette.trim)
            mc.setBlocks(room.x2, self.y-10, room.z1, room.x2, room.y +4, room.z1, self.palette.trim)
            mc.setBlocks(room.x2, self.y-10, room.z2, room.x2, room.y +4, room.z2, self.palette.trim)

        for room in self.inRooms:
            for door in room.doors:
                mc.setBlock(door[0], room.y +2, door[1], door[0], room.y +1, door[1], 0)

                mc.setBlock(door[0], room.y +2, door[1], block.DOOR_WOOD.withData(9))
                mc.setBlock(door[0], room.y+1, door[1], block.DOOR_WOOD.withData(0))

    def decorate(self,mc):
        pass
        #TODO iterate through every room object and decide the decor type, decorate it





if __name__ == '__main__':

    mc = minecraft.Minecraft.create()

    mc.postToChat("House main")

    x, y, z = mc.player.getPos()

    house = House(int(x), int(y), int(z), 20, 20)

    house.generateRooms()
    house.build(mc)

    # for i in range(12):
    #     mc.setBlock(x, y, z+i, block.DOOR_WOOD.withData(i))
