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
        print('num doors', len(room.doors))
        for i in room.doors:
            mc.setBlock(i[0], room.y +1, i[1], 0)
            mc.setBlock(i[0], room.y +2, i[1], 0)
            mc.setBlock(i[0], room.y +5, i[1], 50)


def doorInRoom(door, room):
    print('doors')
    print(room)
    print(door[0], door[1])

    if door[0] == room.x1:
        if room.z1 < door[1] < room.z2 or room.z1 > door[1] > room.z2:
            print('True')
            return True
    elif door[0] == room.x2:
        if room.z1 < door[1] < room.z2 or room.z1 > door[1] > room.z2:
            print('True')
            return True
    elif door[0] == room.z1:
        if room.x1 < door[0] < room.x2 or room.x1 > door[0] > room.x2:
            print('True')
            return True
    elif door[0] == room.z2:
        if room.x1 < door[0] < room.x2 or room.x1 > door[0] > room.x2:
            print('True')
            return True

    print('False')
    print()
    print()
    return False


def doorAdd(room, dir):
    if room.z1 < room.z2:
        if dir == 'x1':
            room.doors.append((room.x1, random.randint(room.z1+2, room.z2 - 2)))
        elif dir == 'x2':
            room.doors.append((room.x2, random.randint(room.z1+2, room.z2 - 2)))
    else:
        if dir == 'x1':
            room.doors.append((room.x1, random.randint(room.z2+2, room.z1 - 2)))
        elif dir == 'x2':
            room.doors.append((room.x2, random.randint(room.z2+2, room.z1 - 2)))

    if room.x1 < room.x2:
        if dir == 'z1':
            room.doors.append((random.randint(room.x1+2, room.x2 - 2), room.z1))
        elif dir == 'z2':
            room.doors.append((random.randint(room.x1+2, room.x2 - 2), room.z2))
    else:
        if dir == 'z1':
            room.doors.append((random.randint(room.x2+2, room.x1 - 2), room.z1))
        elif dir == 'z2':
            room.doors.append((random.randint(room.x2+2, room.x1 - 2), room.z2))

def doorCreator(rooms):


    for room in rooms:
        choices = ['x1', 'x2', 'z1', 'z2']
        for door in room.doors:

            try:
                if int(door[0]) == int(room.x1):
                    choices.remove('x1')
                elif int(door[0]) == int(room.x2):
                    choices.remove('x2')
                elif int(door[1]) == int(room.z1):
                    choices.remove('z1')
                elif int(door[1]) == int(room.z2):
                    choices.remove('z2')
            except:
                print('the remove list thing didnt work')

        doorAdd(room, random.choice(choices))

        for room1 in rooms:
            if doorInRoom(room.doors[-1], room1) and room1 != room:
                room1.doors.append(room.doors[-1])



def roomAdjinator(rooms):

    # wall adding

    for room in rooms:
        for i in range(room.x1, room.z2):
            room.walls.add((i, room.z1))
            room.walls.add((i, room.z2))

        for i in range(room.z1, room.z2):
            room.walls.add((room.x1, i))
            room.walls.add((room.x2, i))

    #adj adding
    for roomi in rooms:
        for roomj in rooms:
            if roomi != roomj and len(roomi.walls.intersection(roomj.walls)) > 0:
                roomi.adj.add(roomj)
                roomj.adj.add(roomi)

    return rooms


def roomCull(rooms):
    pass



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

            room1 = Room(room.x1, room.z1, devixor, room.z2, room.y, True, [], None)
            room2 = Room(devixor, room.z1, room.x2, room.z2, room.y, True, [], None)

            print(room1)
            print(room2)


        else:
            room1 = Room(room.x1, room.z1, room.x2, devizor, room.y, True, [], None)
            room2 = Room(room.x1, devizor, room.x2, room.z2, room.y, True, [], None)

            print(room1)
            print(room2)

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

rooms = roomMitosis(Room(int(x), int(z), int(x)+100, int(z)+100, int(y),None, [(x+3, z)], None))

rooms = roomAdjinator(rooms)

for room in rooms:
    print(room.adj)
# for room in rooms:
#     print(room)
# doorCreator(rooms)
# doorCreator(rooms)
# for i in range(len(rooms)):
#     if len(rooms[i].doors) == 1 and random.randint(0,2) == 1:
#         rooms[i].palette = False


makeRoom(rooms, t)
