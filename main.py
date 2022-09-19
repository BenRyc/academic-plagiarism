from mcpi import minecraft
import random
import House

if __name__ == '__main__':

    #INITIALISE MC AND PLAYER COOR
    mc = minecraft.Minecraft.create()
    playerPos = mc.player.getPos()
    x,y,z = int(playerPos.x), int(playerPos.y), int(playerPos.z)


    #HOUSE PLACEMENT
    houseList = []
    numHouses = 5 #for test
    # numHouses = random.randint(5,15)

    forbiddenCoor = set()
    #starting position
    currX = x 
    currZ = z

    for i in range(numHouses):
        length = random.randint(13,25) #along x
        width = random.randint(13,25) #along z

        posFound = False
        while posFound == False:
            #new house position
            nextX = currX + random.randint(-75,75)
            nextZ = currZ + random.randint(-75,75)

            #generate coordinates occuppied by the house (including a rim of 2 blocks around the floorplan)
            houseCoor = set()
            for x in range(nextX-2, width+2):
                for z in range(nextZ-2, length+2):
                    houseCoor.add([x,z])

            #check if new position is valid
            if len(houseCoor.intersection(forbiddenCoor)) == 0:
                for val in houseCoor:
                    forbiddenCoor.add(val)

                currX = nextX
                currZ = nextZ
                posFound = True

            #create new house
        houseList.append[House(currX, currZ, length, width)]

        #append new forbidden coordinates to the set

        


