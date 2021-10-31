from src.essentials.color import *
from src.essentials.vector import *

class EndPoint:
    # Class for handling end point
    def __init__(self, color, position, scale) -> None:
        self.color = Color(float(color[0]), float(color[1]), float(color[2]))
        self.position = Vector(float(position[0]), float(position[1]), float(position[2]))
        self.scale = Vector(float(scale[0]), float(scale[1]), float(scale[2]))

    def checkIfCollission(self, x, z, r):
        P1_x = self.position.x - (self.scale.x * 0.5)
        P1_z = self.position.z - (self.scale.z * 0.5)
        P2_x = self.position.x + (self.scale.x * 0.5)
        P2_z = self.position.z + (self.scale.z * 0.5)
        if x + r >= P1_x and z + r >= P1_z and x - r <= P2_x and z - r <= P2_z:
            return True
        return False