from src.essentials.color import *
from src.essentials.vector import *
class Walls:
    # Class for handling walls
    def __init__(self, color, translation, rotate, scale) -> None:
        self.color = Color(float(color[0]), float(color[1]), float(color[2]))
        self.translation = Vector(float(translation[0]), float(translation[1]), float(translation[2]))
        self.rotate = Vector(float(rotate[0]), float(rotate[1]), float(rotate[2]))
        self.scale = Vector(float(scale[0]), float(scale[1]), float(scale[2]))

    def checkIfCollission(self, min: Vector, max: Vector):
        # Return list:
        # [bool, bool, bool, bool, bool]
        # [Collision detected, disable +x, disable -x, disable +z, disable -z]
        P1_x = self.translation.x - (self.scale.x * 0.5)
        P1_z = self.translation.z - (self.scale.z * 0.5)
        P2_x = self.translation.x + (self.scale.x * 0.5)
        P2_z = self.translation.z + (self.scale.z * 0.5)
        if max.x >= P1_x and max.z >= P1_z and min.x <= P2_x and min.z <= P2_z:
            # Check if left or right
            if max.x >= P1_x and min.x <= P2_x:
                if max.z - 0.25 <= P1_z: # Left side of wall
                    # Disable move +z
                    return [True, False, False, True, False]
                elif min.z + 0.25 >= P2_z: # Right side of  wall
                    # Disable move -z
                    return [True, False, False, False, True]
            # Check if above or below
            if max.z >= P1_z and min.z <= P2_z:
                if max.x - 0.25 <= P1_x: # Under side of wall
                    # Disable move +x
                    return [True, True, False, False, False]
                elif min.x + 0.25 >= P2_x: # Top side of wall
                    # Disable move -x
                    return [True, False, True, False, False]
        return [False, False, False, False, False]