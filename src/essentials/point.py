from src.essentials.vector import Vector


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __str__(self) -> str:
        return "[" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + "]"