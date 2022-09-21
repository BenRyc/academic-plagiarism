
class Room:
    def __init__(self, x1, z1, x2, z2, y, doors, decor):
        self.x1 = x1
        self.z1 = z1
        self.x2 = x2
        self.z2 = z2
        self.y = y


        self.doors = doors
        self.decor = decor

        self.walls = set()
        self.wallsEx = set()
        self.adj = set()

    def __str__(self):
        return f'x1:{self.x1} x2:{self.x2} xd:{self.x1-self.x2}  z1:{self.z1} z2:{self.z2} zd:{self.z1-self.z2}'
