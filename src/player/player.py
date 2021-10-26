from src.essentials.vector import Vector
from src.essentials.hitbox import HitboxSphere

class Player:
    def __init__(self, eye):
        self.eye = eye
        self.hitbox = HitboxSphere()
        self.health = 100
        self.armor = 100