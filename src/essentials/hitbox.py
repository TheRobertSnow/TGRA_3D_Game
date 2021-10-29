# https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_collision_detection

import math
from src.essentials.vector import Vector


class HitboxSphere:
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius

    def is_point_inside_sphere(self, point) -> bool:
        distance = math.sqrt((point.x - self.position.x) * (point.x - self.position.x) +
                        (point.y - self.position.y) * (point.y - self.position.y) +
                        (point.z - self.position.z) * (point.z - self.position.z))
        return distance < self.radius

    def sphere_intersects_sphere(self, other) -> bool:
        distance = math.sqrt((self.position.x - other.position.x) + (self.position.x - other.position.x) +
                        (self.position.y - other.position.y) + (self.position.y - other.position.y) +
                        (self.position.z - other.position.z) + (self.position.z - other.position.z))
        return distance < (self.radius + other.radius)

    def sphere_intersects_aabb(self, aabb) -> bool:
        # get box's closest point to sphere center by clamping
        x = max(aabb.minX, min(self.position.x, aabb.maxX))
        y = max(aabb.minY, min(self.position.y, aabb.maxY))
        z = max(aabb.minZ, min(self.position.z, aabb.maxZ))

        # same as point inside sphere
        distance = math.sqrt((x - self.position.x) * (x - self.position.x) +
                             (y - self.position.y) * (y - self.position.y) +
                             (z - self.position.z) * (z - self.position.z))

        return distance < self.radius


class HitboxAABB:
    def __init__(self):
        self.min = Vector(0.0, 0.0, 0.0)
        self.max = Vector(0.0, 0.0, 0.0)

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

    def ray_intersects_aabb(self, ray) -> bool:
        # max
        return False

    def __str__(self):
        return "[" + str(self.max) + ", " + str(self.min) + "]"
