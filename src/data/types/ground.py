from src.essentials.color import *
from src.essentials.vector import *
class Ground:
    # Class for handling ground objects
    def __init__(self, color, translation, rotate, scale) -> None:
        self.color = Color(float(color[0]), float(color[1]), float(color[2]))
        self.translation = Vector(float(translation[0]), float(translation[1]), float(translation[2]))
        self.rotate = Vector(float(rotate[0]), float(rotate[1]), float(rotate[2]))
        self.scale = Vector(float(scale[0]), float(scale[1]), float(scale[2]))