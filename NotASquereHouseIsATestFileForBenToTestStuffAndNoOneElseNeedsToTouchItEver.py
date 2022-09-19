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




def makeRoom(rooms, t):

    for room in rooms:
        if room.palette == True:

            if t == 20:
                t = 14

            mc.setBlocks(room.x1, room.y, room.z1, room.x1, room.y +3, room.z2, t)
            mc.setBlocks(room.x2, room.y, room.z1, room.x2, room.y +3, room.z2, t)
            mc.setBlocks(room.x1, room.y, room.z1, room.x2, room.y +3, room.z1, t)
            mc.setBlocks(room.x1, room.y, room.z2, room.x2, room.y +3, room.z2, t)
            mc.setBlocks(room.x1, room.y, room.z1, room.x2, room.y, room.z2, t)
            mc.setBlocks(room.x1, room.y +4, room.z1, room.x2, room.y +4, room.z2, t)

            t += 1

    for room in rooms:
        # print('num doors', len(room.doors))
        for i in room.doors:
            mc.setBlock(i[0], room.y +1, i[1], 0)
            mc.setBlock(i[0], room.y +2, i[1], 0)
            mc.setBlock(i[0], room.y +5, i[1], 50)

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

        print('walls done')
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

    inRooms.append(rooms[0])
    for room in inRooms[0].adj:
        ajRooms.add(room)

    for i in range(int(len(rooms)/0.8)):
        choice = random.choice(list(ajRooms))

        ajRooms.remove(choice)
        inRooms.append(choice)

        for room in choice.adj:
            ajRooms.add(room)

    for i in rooms:
        if room not in inRooms:
            outRooms.append(room)

    return inRooms, outRooms

def roomAdd(rooms):
    for room in rooms:
        for adj in room.adj:
            room.doors.append(list(room.walls.intersection(adj.walls))[0])

    return rooms

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


        if room.x1 > room.x2:
            devixor = random.randint(int(room.x2 + xof), int(room.x1 -xof))
        else:
            devixor = random.randint(int(room.x1 + xof), int(room.x2 -xof))

        if room.z1 > room.z2:
            devizor = random.randint(int(room.z2 + zof), int(room.z1 -zof))
        else:
            devizor = random.randint(int(room.z1 + zof), int(room.z2 -zof))


        if zorx == 1:

            room1 = Room(room.x1, room.z1, devixor, room.z2, room.y, True, [], None)
            room2 = Room(devixor, room.z1, room.x2, room.z2, room.y, True, [], None)

        else:
            room1 = Room(room.x1, room.z1, room.x2, devizor, room.y, True, [], None)
            room2 = Room(room.x1, devizor, room.x2, room.z2, room.y, True, [], None)

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

rooms = roomMitosis(Room(int(x), int(z), int(x)+25, int(z)+25, int(y),None, [(x+3, z)], None))

rooms = roomAdjinator(rooms)

inRooms, outRooms = roomCull(rooms)

inRooms = roomAdd(inRooms)
# for room in rooms:
#     print(room)
# doorCreator(rooms)
# doorCreator(rooms)
# for i in range(len(rooms)):
#     if len(rooms[i].doors) == 1 and random.randint(0,2) == 1:
#         rooms[i].palette = False


makeRoom(inRooms, t)
