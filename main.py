

# from __future__ import absolute_import, division, print_function
# from __future__ import unicode_literals
from mcpi import minecraft
from mcpi import block
import random
import House    
import Terraforming

if __name__ == '__main__':
    #INITIALISE MC AND PLAYER COOR
    mc = minecraft.Minecraft.create()
    playerPos = mc.player.getPos()
    x,y,z = int(playerPos.x), int(playerPos.y), int(playerPos.z)


    ########################################################################
    #                         VILLAGE LAYOUT                               #
    ########################################################################

    houseList = []
    numHouses = random.randint(5,15)
    forbiddenCoor = set()
    scanDiameter = 13 #increases after every house placement
    minDistance = 4
    
    for i in range(numHouses):
        
        #randomise size
        length = random.randint(13,25) #along x
        width = random.randint(13,25) #along z

        #tries a random position until it doesn't overlap with previous houses
        posFound = False
        
        #TODO DELETE VARIABLE
        loopIter = 0
        
        while posFound == False:
            loopIter += 1
            #new house position
            chosenX = x + random.randint(-scanDiameter,scanDiameter)
            chosenZ = z + random.randint(-scanDiameter,scanDiameter)

            #generates coordinates occuppied by the house (including buffer for minimum distance)
            houseCoor = set()
            for ax in range(chosenX-(minDistance//2), chosenX+width+(minDistance//2)):
                
                for az in range(chosenZ-(minDistance//2), chosenZ+length+(minDistance//2)):
                    
                    #TODO DELETE PRINT
                    print(f'Initialising house {i}/{numHouses}, iteration {loopIter}, ({ax}, {az})')
                    
                    houseCoor.add((ax,az))
                    
            #checks if the house position doesnt't overlap
            if len(houseCoor.intersection(forbiddenCoor)) == 0:
                for val in houseCoor:
                    forbiddenCoor.add(val)
                posFound = True

        #add new house object
        houseList.append(House.House(chosenX, None, chosenZ, length, width))
        scanDiameter = scanDiameter + 5
    
    #TODO DELETE
    #illustrates the house placement, for testing
    # 
    # randomColour = random.randint(0,16)
    # for house in houseList:
    #     for ax in range(house.x, house.x+house.width):
    #         for az in range(house.z, house.z+house.length):
    #             mc.setBlock(ax, y, az, 159, randomColour)

    ########################################################################
    #                           TERRAFORMING                               #
    ########################################################################

    # TODO DELETE PRINT
    print("Generating terrain")
    
    for house in houseList:
        house.foundation, house.foundationBlocks = Terraforming.terraform(house.x, house.z, length, width)
        house.y = house.foundation[0][1]
        
    #TODO DELETE PRINT
    print("Finalizing foundations")
    
    for house in houseList:
        for index in range(len(house.foundation)-1):
            x = house.foundation[index][0]
            y = house.foundation[index][1]
            z = house.foundation[index][2]
            blockID = house.foundationBlocks[index].id
            blockData = house.foundationBlocks[index].data
            mc.setBlock(x, y, z, blockID, blockData)
        
    ########################################################################
    #                           GENERATE HOUSE                             #
    ########################################################################
    for house in houseList:
        house.generateRooms()
        house.build(mc)