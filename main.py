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
    numHouses = random.randint(5,10)

    forbiddenCoor = set()
    #starting position
    currX = x 
    currZ = z

    for i in range(numHouses):
        length = random.randint(13,25) #along x
        width = random.randint(13,25) #along z

        posFound = False
        while posFound == False:
            print('tried')
            #new house position
            nextX = currX + random.randint(-30,30)
            nextZ = currZ + random.randint(-30,30)

            #generate coordinates occuppied by the house (including a rim of 2 blocks around the floorplan)
            houseCoor = set()
            for ax in range(nextX-2, nextX+width+2):
                for az in range(nextZ-2, nextZ+length+2):
                    houseCoor.add((ax,az))
                    

            #check if new position is valid
            if len(houseCoor.intersection(forbiddenCoor)) == 0:

                for val in houseCoor:
                    forbiddenCoor.add(val)
                    mc.setBlock(val[0], y, val[1], 1)

                currX = nextX
                currZ = nextZ
                mc.setBlock(currX, y, currZ, 159)
                posFound = True

            #create new house
        houseList.append(House.newHouse(currX, currZ, length, width))

        #append new forbidden coordinates to the set
        for coor in houseCoor:
            forbiddenCoor.add(coor)

    for house in houseList:
        print(house)

        


