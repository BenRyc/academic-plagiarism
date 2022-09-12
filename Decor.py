global mc

class Decor:
    def __init__(self, coor1, coor2, doorsCoor, type):
        self.coor1 = coor1
        self.coor2 = coor2
        self.doorsCoor = doorsCoor
        self.type = type
        self.length = coor2[2] - coor1[2] #z coordinate
        self.width = coor2[0] - coor1[0] #x coordinate

    def roomDecoratorInator(self): #coor param are [x,y,z]
        #find what wall has a door
        doorX = self.doorsCoor[0][0]
        doorZ = self.doorsCoor[0][2]

        #facing east
        if doorX == self.coor2[0]:
            doorDir = 'E'
        #facing west
        if doorX == self.coor1[0]:
            doorDir = 'W'
        #facing north
        if doorZ == self.coor1[2]:
            doorDir = 'N'
        #facing south
        if doorZ == self.coor2[2]:
            doorDir = 'S'


        #bedrooms can only have one door
        if self.type.lower() == 'bedroom':
            mc.postToChat('decorated bedroom')
            #place bookshelf
            if doorDir == 'N':
                mc.setBlock(self.coor1[0]+self.width-1,self.coor1[1],self.coor1[2], 47,0)

            elif doorDir == 'S':
                mc.setBlock(self.coor1[0]+self.width-1,self.coor1[1],self.coor1[2]+self.length-1, 47,0)

            elif doorDir == 'E':
                mc.setBlock(self.coor1[0],self.coor2[1],self.coor1[2], 47,0)

            elif doorDir == 'W':
                mc.setBlock(self.coor1[0],self.coor1[1],self.coor1[2], 47,0)
            #place bed and bedside tabl
            #place desk
