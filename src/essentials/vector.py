from math import *


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def __len__(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        length = self.__len__()
        self.x /= length
        self.y /= length
        self.z /= length

    def multiply_with_matrix(self, matrix):
        m = matrix
        temp_x = (self.x * m[0]) + (self.y * m[1]) + (self.z * m[2])
        temp_y = (self.x * m[3]) + (self.y * m[4]) + (self.z * m[5])
        self.z = (self.x * m[6]) + (self.y * m[7]) + (self.z * m[8])
        self.x = temp_x
        self.y = temp_y

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)

    def __str__(self):
        return "Vector(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"