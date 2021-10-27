from src.essentials.vector import Vector
from src.essentials.hitbox import HitboxSphere

class Player:
    def __init__(self, position, camera):
        self.camera = camera
        # TODO: Add hitbox "self.hitbox = Hitbox or sumtn
        self.position = position
        self.health = 100
        self.armor = 100
        # TODO: Add mesh  "self.mesh = mesh"