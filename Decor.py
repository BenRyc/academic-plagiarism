from mcpi import minecraft
from mcpi import block
import Palettes 
import Decor

mc = minecraft.Minecraft.create()
class Decoration:

    def __init__(self, coor1, coor2, doorsCoor, type):
        self.coor1 = coor1
        self.coor2 = coor2
        self.doorsCoor = doorsCoor
        self.type = type
        self.length = coor2[2] - coor1[2] + 1 #z coordinate
        self.width = coor2[0] - coor1[0] +1 #x coordinate
        self.height = coor2[1] - coor1[1] + 1 # y coordinate

        if self.width < 3 or self.height < 3:
            raise ValueError('Room is too small. Must be minimum 3x3')

    def roomDecorator(self): #coor param are [x,y,z]
        #find what wall has a door
        doorX = self.doorsCoor[0]
        doorZ = self.doorsCoor[2]
        #mc.postToChat(f'{doorX},{doorZ}')

        #facing east
        if doorZ == self.coor1[2]:
            print('N')
            doorDir = 'N'
        #facing south
        elif doorZ == self.coor2[2]:
            print('+z')
            doorDir = '+z'

        elif doorX == self.coor2[0]:
            print('E')
            doorDir = 'E'
        #facing west
        elif doorX == self.coor1[0]:
            print('W')
            doorDir = 'W'

        else:
            raise ValueError('Door is not in a valid position.')


        #bedrooms can only have one door
        if self.type.lower() == 'bedroom':

            if doorDir == 'N':
                #bookshelf
                for i in range(0,self.height):
                    mc.setBlock(self.coor2[0],self.coor1[1]+i,self.coor1[2], 47,0)
                #crafting table
                mc.setBlock(self.coor1[0],self.coor1[1],self.coor1[2],58)
                #bed and table
                mc.setBlock(self.coor2[0],self.coor1[1],self.coor2[2]-1,26)
                mc.setBlock(self.coor2[0]-1,self.coor1[1],self.coor2[2],53,6)
                
            elif doorDir == 'S':
                for i in range(0,self.height):
                    mc.setBlock(self.coor1[0],self.coor1[1]+i,self.coor2[2], 47,0)
                mc.setBlock(self.coor2[0],self.coor1[1],self.coor2[2],58)

                

            elif doorDir == 'E':
                for i in range(0,self.height):
                    mc.setBlock(self.coor2[0],self.coor1[1]+i,self.coor2[2], 47,0)
                mc.setBlock(self.coor2[0],self.coor1[1],self.coor1[2],58)

            elif doorDir == 'W':
                for i in range(0,self.height):
                    mc.setBlock(self.coor1[0],self.coor1[1]+i,self.coor1[2], 47,0)
                mc.setBlock(self.coor1[0],self.coor1[1],self.coor2[2],58)
                mc.setBlock(self.coor2[0]-1,self.coor1[1],self.coor1[2],26)
                mc.setBlock(self.coor2[0],self.coor1[1],self.coor1[2]+1,53,4)
            
            #place bed and bedside table
            #place desk