
class Room:
    def __init__(self, x1, z1, x2, z2, y, palette, doors, decor):
        self.x1 = x1
        self.z1 = z1
        self.x2 = x2
        self.z2 = z2
        self.y = y

        self.palette = palette

        self.doors = doors
        self.decor = decor
