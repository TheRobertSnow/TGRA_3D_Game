from src.essentials.vector import Vector
from src.essentials.hitbox import HitboxSphere
from src.essentials.matrices import ViewMatrix
from src.essentials.point import Point
from src.essentials.settings import MOVEMENTSPEED


class Player:
    def __init__(self):
        # /==/ Positional Values /==/
        self.position = Point(0, 0, 0)
        self.u = Vector(1, 0, 0)
        self.v = Vector(0, 1, 0)
        self.n = Vector(0, 0, 1)
        self.direction = Vector(-1, 0, 0)
        # TODO: Add hitbox "self.hitbox = Hitbox or sumtn

        # /==/ Gameplay Values /==/
        self.health = 100
        self.armor = 50
        self.movement = MOVEMENTSPEED

    def move(self, del_u, del_v, del_n):
        self.camera.slide(del_u, del_v, del_n)

    def yaw(self, angle):
        self.camera.yaw(angle)

    def pitch(self, angle):
        self.camera.pitch(angle)

    def set_cam_to_player(self):
        self.camera.eye = Point(self.position.x, 2, self.position.z)

