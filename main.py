

# from __future__ import absolute_import, division, print_function
# from __future__ import unicode_literals
from mcpi import minecraft
from mcpi import block
import random
import House
import Terraforming
import pathfinding2D
if __name__ == '__main__':
    #INITIALISE MC AND PLAYER COOR
    mc = minecraft.Minecraft.create()
    playerPos = mc.player.getPos()
    x,y,z = int(playerPos.x), int(playerPos.y), int(playerPos.z)


    ########################################################################
    #                         VILLAGE LAYOUT                               #
    ########################################################################

    houseList = []
    numHouses = 5
    forbiddenCoor = set()
    scanDiameter = 13 #increases after every house placement
    minDistance = 10

    for i in range(numHouses):

        #randomise size
        length = random.randint(13,25) #along x
        width = random.randint(13,25) #along z

        #tries a random position until it doesn't overlap with previous houses
        posFound = False

        loopIter = 0
        while posFound == False:
            loopIter += 1
            if loopIter > 5:
                scanDiameter +=5
            #new house position
            chosenX = x + random.randint(-scanDiameter,scanDiameter)
            chosenZ = z + random.randint(-scanDiameter,scanDiameter)

            #generates coordinates occuppied by the house (including buffer for minimum distance)
            houseCoor = set()
            for ax in range(chosenX-(minDistance//2), chosenX+width+(minDistance//2)):

                for az in range(chosenZ-(minDistance//2), chosenZ+length+(minDistance//2)):

                    houseCoor.add((ax,az))

            #checks if the house position doesnt't overlap
            if len(houseCoor.intersection(forbiddenCoor)) == 0:
                for val in houseCoor:
                    forbiddenCoor.add(val)
                posFound = True

        #add new house object
        houseList.append(House.House(chosenX, None, chosenZ, length, width))
        scanDiameter = scanDiameter + 5

    ########################################################################
    #                           TERRAFORMING                               #
    ########################################################################

    for house in houseList:
        house.foundation, house.foundationBlocks = Terraforming.terraform(house.x, house.z, length, width)
        house.y = house.foundation[0][1]


    for house in houseList:
        x = house.foundation[0][0]
        y = house.foundation[0][1]
        z = house.foundation[0][2]
        endx = house.foundation[len(house.foundation)-1][0]
        endz = house.foundation[len(house.foundation)-1][2]
        blockID = house.foundationBlocks.id
        blockData = house.foundationBlocks.data
        mc.setBlocks(x, y, z, endx, y-10, endz, blockID, blockData)

    ########################################################################
    #                           GENERATE HOUSES                            #
    ########################################################################
    fdoors = []
    houselocs = []
    for house in houseList:
        house.generateRooms()
        fdoors.append(house.frontdoor)
        houseloc = []
        houseloc.append(house.x)
        houseloc.append(house.z)
        houseloc.append(house.length)
        houseloc.append(house.width)
        houselocs.append(houseloc)
    for house in houseList:
        house.build(mc)
        house.decorate(mc)
    pathfinding2D.main(fdoors, houselocs)
    print('village generated!')
