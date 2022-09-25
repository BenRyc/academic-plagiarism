from mcpi import minecraft
from mcpi import block
import random
import Palettes
from Room import Room

random.seed(1) #TODO delete
def decorBedroom(room, dirWithDoor): 
    # --Block key--
    # chest
    # bed: 26,
    #         1 -x
    #         2 -z
    #         3 +x
    #         4 +z
    # bookshelf: 47
    # crafting table: 58
    # wood stairs: 53
    # slabs
    # glowstone: 89
    # red carpet: 171,1,4
    
    print('decorating bedroom')

    #floor lighting
    mc.setBlocks(room.x1+3, room.y, room.z+3, room.x1-3, room.y, room.z2-3, 89) 
    mc.setBlocks(room.x1+3, room.y+1, room.z+3, room.x1-3, room.y+1, room.z2-3, 171,1,4) 

    #directionally dependent decorations
    if '-z' in dirWithDoor: #-z
        #bed
        mc.setBlock(room.x1 + (room.x2-room.x1)//2, room.y+1, room.z2-1,26,4)
        mc.setBlock(room.x1 + (room.x2-room.x1)//2, room.y+1, room.z2-2,26,4)
        mc.setBlock(room.x1 + (room.x2-room.x1)//2+1, room.y+1, room.z2-1,26,4)
        mc.setBlock(room.x1 + (room.x2-room.x1)//2+1, room.y+1, room.z2-2,26,4)
        #bookshelf
        mc.setBlocks(room.x1+1, room.y+1, room.z1+1, room.x1+1, room.y+2, room.z1+1, 47)
        mc.setBlocks(room.x1+1, room.y+3, room.z1+1, room.x1+1, room.y+3, room.z2-1, 47)

    elif '+z' in dirWithDoor:
        #bed
        mc.setBlock(room.x1 + (room.x2-room.x1)//2, room.y+1, room.z1+1,26,2)
        mc.setBlock(room.x1 + (room.x2-room.x1)//2, room.y+1, room.z1+2,26,2)
        mc.setBlock(room.x1 + (room.x2-room.x1)//2+1, room.y+1, room.z1+1,26,2)
        mc.setBlock(room.x1 + (room.x2-room.x1)//2+1, room.y+1, room.z1+2,26,2)
        #bookshelf
        mc.setBlocks(room.x2-1, room.y+1, room.z2-1, room.x2-1, room.y+2, room.z2-1, 47)
        mc.setBlocks(room.x2-1, room.y+3, room.z2-1, room.x2-1, room.y+3, room.z1+1, 47)

    elif '+x' in dirWithDoor:
        #bed
        mc.setBlock(room.x1+1, room.y+1, room.z1 + (room.z2-room.z1)//2,26,1)
        mc.setBlock(room.x1+2, room.y+1, room.z1 + (room.z2-room.z1)//2,26,1)
        mc.setBlock(room.x1+1, room.y+1, room.z1 + (room.z2-room.z1)//2+1,26,1)
        mc.setBlock(room.x1+2, room.y+1, room.z1 + (room.z2-room.z1)//2+1,26,1)
        #bookshelf
        mc.setBlocks(room.x2-1, room.y+1, room.z1+1,room.x2-1, room.y+2, room.z1+1, 47)
        mc.setBlocks(room.x2-1, room.y+3, room.z1+1, room.x1+1, room.y+3, room.z1+1, 47)
    elif '-x' in dirWithDoor:
        #bed
        mc.setBlock(room.x2-1, room.y+1, room.z1 + (room.z2-room.z1)//2,26,3)
        mc.setBlock(room.x2-2, room.y+1, room.z1 + (room.z2-room.z1)//2,26,3)
        mc.setBlock(room.x2-1, room.y+1, room.z1 + (room.z2-room.z1)//2+1,26,3)
        mc.setBlock(room.x2-2, room.y+1, room.z1 + (room.z2-room.z1)//2+1,26,3)
        #bookshelf
        mc.setBlocks(room.x1+1, room.y+1, room.z2-1, room.x1+1, room.y+2, room.z2-1, 47)
        mc.setblocks(room.x1+1, room.y+3, room.z2-1, room.x2-1, room.y+3, room.z2-1, 47)
    

def decorkitchen(self, coor1, coor2, dirWithDoor):
    pass
def decorDining(self, coor1, coor2, dirWithDoor):
    pass
def decorLiving(self, coor1, coor2, dirWithDoor):
    pass


def roomAdjinator(rooms):

    # wall adding

    for room in rooms:
        # adds a tuple for each block ing the wall
        for i in range(room.x1, room.x2):
            room.walls.add((i, room.z1))
            room.walls.add((i, room.z2))

        for i in range(room.z1, room.z2):
            room.walls.add((room.x1, i))
            room.walls.add((room.x2, i))

        # makes a copy of the walls and then removes the corner blocks
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

    #for every room it tests if every other room shairs and walls making them adjacent
    for roomi in rooms:
        for roomj in rooms:
            #print(roomi.walls.intersection(roomj.walls))
            if roomi != roomj and not roomi.wallsEx.isdisjoint(roomj.wallsEx):
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

        for room in choice.adj:
            ajRooms.add(room)

    for room in rooms:
        if room not in inRooms:
            outRooms.append(room)

    for room in inRooms:
        room.adj.difference_update(outRooms)

    for room in inRooms:
        room.wallsOut = room.walls.copy()
        for adj in room.adj:
            room.wallsOut.difference_update(adj.walls)

    return inRooms, outRooms

def roomAdd(rooms):
    # adds walls between every room

    # iterates through the room list making a door between each adjacent room

    for room in rooms:

        for adj in range(len(list(room.adj))):
            door = list(room.wallsEx.intersection(list(room.adj)[adj].wallsEx))[0]
            # seting the side of the room the door is on
            if door[0] == room.x1:
                door = door + tuple('x1')
            elif door[0] == room.x2:
                door = door + tuple('x2')
            elif door[1] == room.z1:
                door = door + tuple('z1')
            elif door[1] == room.z2:
                door = door + tuple('z2')

            room.doors.append(door)

            # out walls
            room.wallsOut.difference_update(list(room.adj)[adj].walls)


        print()
        print(len(room.adj), len(room.doors))
        print()
        outWalls.update(room.wallsOut)
        avalableWalls.update(room.wallsEx)

    # making the front door out of one of the external walls that is not a corner
    outWalls.intersection_update(avalableWalls)
    fDoor = random.choice(list(outWalls))
    outWalls.remove(fDoor)

    for room in rooms:
        # if the door is a part of a room it will be added to the room
        if fDoor in list(room.wallsOut):
            # seting the side of the room the door is on
            if fDoor[0] == room.x1:
                fDoor = fDoor + tuple('x1')
            elif fDoor[0] == room.x2:
                fDoor = fDoor + tuple('x2')
            elif fDoor[1] == room.z1:
                fDoor = fDoor + tuple('z1')
            elif fDoor[1] == room.z2:
                fDoor = fDoor + tuple('z2')

            # seting the room type
            fDoor = fDoor + tuple('F')
            room.doors.append(fDoor)
            room.decor = 'front'

    windows = outWalls
    # makes a master list of al the windows in the house by randomly picking from the avalable blocks
    # for i in range(0, int(len(outWalls)/1.2)):
    #     windows.add(random.choice(list(outWalls)))

    # checks if the window is a part of the room and if so adds it
    for window in list(windows):
        for room in rooms:
            if window in list(room.walls):
                room.windows.append(window)

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

        #TODO change
        #self.stories = random.randint(1, 3) # how many levels of the hopuse there are
        self.stories = 1
        self.palette = Palettes.housePalette() # the block palet of the hous
        self.palette.pickPalette() # the block palet of the house

        self.inRooms = [] # rooms inside the house
        self.outRooms = [] # rooms outside the house


    #generate floorplan
    def generateRooms(self):

        # based on the number of stories it makes the rooms
        for i in range(0, self.stories):
            # recursivly makes a list of rooms
            rooms = roomMitosis(Room(self.x, self.z, self.x+self.length, self.z+self.width, self.y+(4*i), [], None))
            # creates the adjacencies for each room
            rooms = roomAdjinator(rooms)

            # splits the rooms into rooms that are going to be biuld and ones that are not
            inRooms, outRooms = roomCull(rooms)

            # appends the new rooms to the master room list
            for room in inRooms:
                self.inRooms.append(room)
                # removes exces front doors
                if i != 0:
                    for door in room.doors:
                        if len(door) == 4:
                            room.doors.remove(door)
                            room.decor = None
            if i == 0:
                outWalls = set() # a set of all the walls on the ouside of the house
                avalableWalls = set() # a set of all the walls not including the corner blocks
                for room in inRooms:
                    outWalls.update(room.wallsOut)
                    avalableWalls.update(room.wallsEx)

                # making the front door out of one of the external walls that is not a corner
                outWalls.intersection_update(avalableWalls)
                fDoor = random.choice(list(outWalls))

                for room in rooms:
                    # if the door is a part of a room it will be added to the room
                    if fDoor in list(room.wallsOut):
                        # seting the side of the room the door is on
                        if fDoor[0] == room.x1:
                            fDoor = fDoor + tuple('x1')
                        elif fDoor[0] == room.x2:
                            fDoor = fDoor + tuple('x2')
                        elif fDoor[1] == room.z1:
                            fDoor = fDoor + tuple('z1')
                        elif fDoor[1] == room.z2:
                            fDoor = fDoor + tuple('z2')

                        # seting the room type
                        fDoor = fDoor + tuple('F')
                        room.doors.append(fDoor)
                        room.decor = 'front'

                # making the front door out of one of the external walls that is not a corner
                outWalls.intersection_update(avalableWalls)
                fDoor = random.choice(list(outWalls))

        # adds doors to the rooms
        self.inRooms = roomAdd(self.inRooms)

    def build(self, mc):

        #TODO uncomment
        # biulds the roof blocks first
        # for room in self.inRooms:
        #     for i in range(room.x1, room.x2+1):
        #         mc.setBlocks(i, room.y + 4 , room.z1, i, room.y + 4 + int((i-room.x1)/2+1), room.z2, self.palette.roof)

        # places the rooms in reverse order
        for room in reversed(self.inRooms):
            mc.setBlocks(room.x1, room.y, room.z1, room.x2, room.y +3, room.z2, 0)

            # places the 4 walls
            mc.setBlocks(room.x1, room.y, room.z1, room.x1, room.y +3, room.z2, self.palette.walls)
            mc.setBlocks(room.x2, room.y, room.z1, room.x2, room.y +3, room.z2, self.palette.walls)
            mc.setBlocks(room.x1, room.y, room.z1, room.x2, room.y +3, room.z1, self.palette.walls)
            mc.setBlocks(room.x1, room.y, room.z2, room.x2, room.y +3, room.z2, self.palette.walls)

            # places the floor and ceiling
            mc.setBlocks(room.x1+1, room.y, room.z1+1, room.x2-1, room.y, room.z2-1, self.palette.floor)
            #mc.setBlocks(room.x1, room.y +4, room.z1, room.x2, room.y +4, room.z2, self.palette.walls) #TODO uncomment

            # places the 4 corner pilars s
            mc.setBlocks(room.x1, self.y-10, room.z1, room.x1, room.y +4, room.z1, self.palette.trim)
            mc.setBlocks(room.x1, self.y-10, room.z2, room.x1, room.y +4, room.z2, self.palette.trim)
            mc.setBlocks(room.x2, self.y-10, room.z1, room.x2, room.y +4, room.z1, self.palette.trim)
            mc.setBlocks(room.x2, self.y-10, room.z2, room.x2, room.y +4, room.z2, self.palette.trim)


        for room in self.inRooms:

            for window in list(room.wallsOut.intersection(room.wallsEx)):
                mc.setBlocks(window[0], room.y+2, window[1], window[0], room.y+3, window[1], block.GLASS)

            for door in room.doors:
                print(door)
                mc.setBlock(door[0], room.y +2, door[1], door[0], room.y +1, door[1], 0)

                mc.setBlock(door[0], room.y +2, door[1], block.DOOR_WOOD.withData(9))
                mc.setBlock(door[0], room.y+1, door[1], block.DOOR_WOOD.withData(0))
            # input()

        # stairs
        room1 = self.inRooms[0]
        for i in range(0, self.stories-1):
            print('st')
            mc.setBlocks(room1.x1+2, room1.y+4 +(i*4), room1.z1+2, room1.x1+3, room1.y+4+(i*4), room1.z1+3, 0)
            mc.setBlock(room1.x1+2, room1.y+1+(i*4), room1.z1+2, block.STAIRS_WOOD.withData(3))
            mc.setBlock(room1.x1+3, room1.y+2+(i*4), room1.z1+2, block.STAIRS_WOOD.withData(0))
            mc.setBlock(room1.x1+3, room1.y+3+(i*4), room1.z1+3, block.STAIRS_WOOD.withData(2))
            mc.setBlock(room1.x1+2, room1.y+4+(i*4), room1.z1+3, block.STAIRS_WOOD.withData(1))


    def decorate(self,mc):
        #door facing: '1' is pos, '2' is neg
        #TODO iterate through every room object and decide the decor type, decorate it
        
    
        for room in self.inRooms:
            #determine which directions have doors
            dirWithDoor = []
            for door in room.doors:
                if '-x' not in dirWithDoor and door[2]=='x' and door[3]=='1':
                    dirWithDoor.append('-x')
                elif '+x' not in dirWithDoor and door[2]=='x' and door[3]=='2':
                    dirWithDoor.append('+x')
                elif '-z' not in dirWithDoor and door[2]=='z' and door[3]=='1':
                    dirWithDoor.append('-z')
                elif '+z' not in dirWithDoor and door[2]=='z' and door[3]=='2':
                    dirWithDoor.append('+z')
            print('directions with doors on em:', dirWithDoor)
            #determine what decoration type/s are appropriate
            if len(dirWithDoor) == 1:
                print('bedroom detected')
                decorBedroom(room, dirWithDoor)






if __name__ == '__main__':
    random.seed(1) #TODO delete
    mc = minecraft.Minecraft.create()

    mc.postToChat("House main")

    x, y, z = mc.player.getPos()

    mc.setBlocks(int(x)-25, int(y)-10, int(z)-25, int(x)+25, int(y)+25, int(z)+25, 0)

    house = House(int(x), int(y), int(z), 16, 16)

    
    house.generateRooms()
    house.build(mc)
    house.decorate(mc)

    # for i in range(12):
    #     mc.setBlock(x, y, z+i, block.DOOR_WOOD.withData(i))
