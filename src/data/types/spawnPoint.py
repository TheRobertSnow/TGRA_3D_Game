from src.essentials.point import *
class SpawnPoint:
    # Class for handling spawnpoints
    def __init__(self, position) -> None:
        self.position = Point(float(position[0]), float(position[1]), float(position[2]))