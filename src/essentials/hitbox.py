# https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_collision_detection

import math
from src.essentials.vector import Vector
class HitboxAABB:
    def __init__(self, vMin:Vector=None, vMax:Vector=None):
        if vMin != None:
            self.min = vMin
        else:
            self.min = Vector(0.0, 0.0, 0.0)
        if vMax != None:
            self.max = vMax
        else:
            self.max = Vector(0.0, 0.0, 0.0)
        self.vertArray = []


    def set_max(self, max: Vector):
        self.max = max

    def set_min(self, min: Vector):
        self.min = min

    def is_point_inside_aabb(self, point) -> bool:
        return ((point.x >= self.minX and point.x <= self.maxX) and
                (point.y >= self.minY and point.y <= self.maxY) and
                (point.z >= self.minZ and point.Z <= self.maxZ))

    def aabb_intersects_aabb(self, other) -> bool:
        return ((self.minX <= other.maxX and self.maxX >= other.minX) and
                (self.minY <= other.maxY and self.maxY >= other.minY) and
                (self.minZ <= other.maxZ and self.maxZ >= other.minZ))

    def ray_intersects_aabb(self, origin, direction) -> bool:
        tmin = (self.min.x - origin.x) / direction.x
        tmax = (self.max.x - origin.x) / direction.x

        if (tmin > tmax):
            temp = tmin
            tmin = tmax
            tmax = temp

        tymin = (self.min.y - origin.y) / direction.y
        tymax = (self.max.y - origin.y) / direction.y

        if (tmin > tymax):
            temp = tymin
            tymin = tymax
            tymax = temp

        if (tmin > tymax or tymin > tmax):
            return False

        if (tymin > tmin):
            tmin = tymin

        if (tymax < tmax):
            tmax = tymax

        tzmin = (self.min.z - origin.z) / direction.z
        tzmax = (self.max.z - origin.z) / direction.z

        if (tmin > tzmax):
            temp = tzmin
            tzmin = tzmax
            tzmax = temp

        if (tmin > tzmax or tzmin > tmax):
            return False

        return True


    def __str__(self):
        return "[" + str(self.max) + ", " + str(self.min) + "]"
