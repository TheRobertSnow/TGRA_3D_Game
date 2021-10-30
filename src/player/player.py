from src.essentials.vector import Vector
from src.essentials.hitbox import HitboxSphere, HitboxAABB
from src.essentials.matrices import ViewMatrix
from src.essentials.point import Point
from src.essentials.settings import MOVEMENTSPEED


class Player:
    def __init__(self):
        # /==/ Positional Values /==/
        self.name = ""
        self.aabb = HitboxAABB()
        self.angle = 0
        self.position = Point(0, 0, 0)
        self.u = Vector(1, 0, 0)
        self.v = Vector(0, 1, 0)
        self.n = Vector(0, 0, 1)
        self.direction = Vector(-1, 0, 0)

        # /==/ Gameplay Values /==/
        self.health = 100
        self.armor = 50
        self.died = False
        self.movement = MOVEMENTSPEED

    def move(self, del_u, del_v, del_n):
        self.camera.slide(del_u, del_v, del_n)

    def yaw(self, angle):
        self.camera.yaw(angle)

    def pitch(self, angle):
        self.camera.pitch(angle)

    def set_cam_to_player(self):
        self.camera.eye = Point(self.position.x, 2, self.position.z)

    def calc_aabb(self, vArray):
        tMax = Vector(0.0, 0.0, 0.0)
        tMin = Vector(0.0, 0.0, 0.0)
        for key, val in vArray.items():
            for i in range(0, int(len(val)/3) -1, 3):
                if val[i] > tMax.x: tMax.x = val[i]
                if val[i] < tMin.x: tMin.x = val[i]
                if val[i+1] > tMax.y: tMax.y = val[i+1]
                if val[i+1] < tMin.y: tMin.y = val[i+1]
                if val[i+2] > tMax.z: tMax.z = val[i+2]
                if val[i+2] < tMin.z: tMin.z = val[i+2]
        self.aabb.set_min(tMin)
        self.aabb.set_max(tMax)

