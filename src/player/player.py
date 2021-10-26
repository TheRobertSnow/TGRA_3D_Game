from src.essentials.vector import Vector
from src.essentials.hitbox import Hitbox

class Player:
    def __init__(self, eye, mode):
        self.eye = eye
        self.hitbox = Hitbox(mode)