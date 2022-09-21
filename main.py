from mcpi import minecraft
import random
import House
import Teraforming

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
    minDistance = 10
    
    for i in range(numHouses):
        
        # TODO DELETE 
        print(f'Initialising house {i}/{numHouses}')
        
        #randomise size
        length = random.randint(13,25) #along x
        width = random.randint(13,25) #along z

        #tries a random position until it doesn't overlap with previous houses
        posFound = False
        while posFound == False:
            #new house position
            chosenX = x + random.randint(-scanDiameter,scanDiameter)
            chosenZ = z + random.randint(-scanDiameter,scanDiameter)

            #generates coordinates occuppied by the house (including buffer for minimum distance)
            houseCoor = set()
            for ax in range(chosenX-(minDistance//2), chosenX+width+(minDistance//2)):
                
                #TODO DELETE
                print(f'Initialising house {i}/{numHouses}, ax = {ax}')
                
                for az in range(chosenZ-(minDistance//2), chosenZ+length+(minDistance//2)):
                    
                    #TODO DELETE
                    print(f'Initialising house {i}/{numHouses}, az = {az}')
                    
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
    '''
    for house in houseList:
        for ax in range(house.x, house.x+house.width):
            for az in range(house.z, house.z+house.length):
                mc.setBlock(ax, y, az, 159,random.randint(0,16))
    '''
    ########################################################################
    #                           TERRAFORMING                               #
    ########################################################################

    # TODO DELETE 
    print("Generating terrain")
    
    for house in houseList:
        house.y = Terraforming.terraform(house.x+house.length, house,z+house.width, length, width)
        
    ########################################################################
    #                           GENERATE HOUSE                             #
    ########################################################################

