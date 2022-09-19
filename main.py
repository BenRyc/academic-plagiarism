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
    numHouses = random.randint(5,15)
    forbiddenCoor = set()
    placeRange = 13
    randomColour = random.randint(0,16) #TODO DELETE
    minDistance = 10
    
    for i in range(numHouses):
        length = random.randint(13,25) #along x
        width = random.randint(13,25) #along z

        posFound = False
        placeRange = placeRange + 5
        while posFound == False:

            #new house position
            nextX = x + random.randint(-placeRange,placeRange)
            nextZ = z + random.randint(-placeRange,placeRange)

            #generate coordinates occuppied by the house (including a rim of 2 blocks around the floorplan)
            houseCoor = set()
            for ax in range(nextX-(minDistance//2), nextX+width+(minDistance//2)):
                for az in range(nextZ-(minDistance//2), nextZ+length+(minDistance//2)):
                    houseCoor.add((ax,az))
                    
            #run position is valid
            if len(houseCoor.intersection(forbiddenCoor)) == 0:
                for val in houseCoor:
                    forbiddenCoor.add(val)
                    mc.setBlock(nextX, y, nextZ, 1)
                posFound = True

            #create new house
        houseList.append(House.newHouse(nextX, nextZ, length, width))

    for house in houseList:
        for ax in range(house.x, house.x+house.width):
            for az in range(house.z, house.z+house.length):
                mc.setBlock(ax, y, az, 159,randomColour)

