from os import DirEntry
from src.essentials.color import *
from src.essentials.vector import *

class EvilObject:
    # Class for handeling walls
    def __init__(self, color, translationStart, translationEnd, rotate, scale) -> None:
        self.color = Color(float(color[0]), float(color[1]), float(color[2]))
        self.translationStart = Vector(float(translationStart[0]), float(translationStart[1]), float(translationStart[2]))
        self.translationEnd = Vector(float(translationEnd[0]), float(translationEnd[1]), float(translationEnd[2]))
        self.translationCurr = Vector(float(translationStart[0]), float(translationStart[1]), float(translationStart[2]))
        self.rotate = Vector(float(rotate[0]), float(rotate[1]), float(rotate[2]))
        self.scale = Vector(float(scale[0]), float(scale[1]), float(scale[2]))
        self.direction = self.translationStart - self.translationEnd

    def update(self, move):
        if self.direction.x != 0:
            if self.direction.x > 0:
                self.translationCurr.x -= move
                if self.translationCurr.x < self.translationStart.x:
                    self.direction.x = -self.direction.x
            elif self.direction.x < 0:
                self.translationCurr.x += move
                if self.translationCurr.x > self.translationEnd.x:
                    self.direction.x = -self.direction.x
        if self.direction.z != 0:
            if self.direction.z > 0:
                self.translationCurr.z -= move
                if self.translationCurr.z < self.translationStart.z:
                    self.direction.z = -self.direction.z
            elif self.direction.z < 0:
                self.translationCurr.z += move
                if self.translationCurr.z > self.translationEnd.z:
                    self.direction.z = -self.direction.z

    def checkIfCollission(self, min: Vector, max: Vector):
        P1_x = self.translationCurr.x - (self.scale.x * 0.5)
        P1_z = self.translationCurr.z - (self.scale.z * 0.5)
        P2_x = self.translationCurr.x + (self.scale.x * 0.5)
        P2_z = self.translationCurr.z + (self.scale.z * 0.5)
        if max.x >= P1_x and max.z >= P1_z and min.x <= P2_x and min.z <= P2_z:
            return True
        return False