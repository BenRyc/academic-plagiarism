
class Room:
    def __init__(self, x1, z1, x2, z2, y, palette, doors, decor):
        self.corner1 = (x1, z1)
        self.corner2 = (x2, z2)
        self.y = y

        self.palette = palette

        self.doors = doors
        self.decor = decor
