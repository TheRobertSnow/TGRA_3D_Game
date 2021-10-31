from src.essentials.vector import *
class StartPoint:
    # Class for handling start point
    def __init__(self, position) -> None:
        self.position = Vector(float(position[0]), float(position[1]), float(position[2]))