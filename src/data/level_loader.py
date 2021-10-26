#TODO: Add level loader

import json
import sys

from src.data.types.walls import Walls
from src.data.types.ground import Ground
from src.data.types.evilObjects import EvilObject
from src.data.types.startPoint import StartPoint
from src.data.types.endPoint import EndPoint


class LevelLoader:
    # Should load in levels from 'src/data/levels' into
    # appropriate class in 'src/assets/types'
    def __init__(self) -> None:
        self.fPrefix = sys.path[0] + "/src/assets/scenes/"

        self.walls = []
        self.ground = []
        self.evilObjects = []
        self.startPoint = []
        self.endPoint = []

    def read_level(self, fileName):
        f = open(self.fPrefix + fileName, 'r')
        data = json.loads(f.read())

        # Load walls
        for i in data["walls"]:
            wall = Walls(i["color3f"], i["translation3f"], i["rotate3f"], i["scale3f"])
            self.walls.append(wall)

        # Load ground
        for i in data["ground"]:
            ground = Ground(i["color3f"], i["translation3f"], i["rotate3f"], i["scale3f"])
            self.ground.append(ground)

        # Load evilObjects
        for i in data["evilObjects"]:
            evilObject = EvilObject(i["color3f"], i["translationStart3f"], i["translationEnd3f"], i["rotate3f"],
                                    i["scale3f"])
            self.evilObjects.append(evilObject)

        # Load startPoint
        for i in data["startPoint"]:
            startPoint = StartPoint(i["position"])
            self.startPoint.append(startPoint)

        # Load endPoint
        for i in data["endPoint"]:
            endPoint = EndPoint(i["color3f"], i["position"], i["scale3f"])
            self.endPoint.append(endPoint)


if __name__ == "__main__":
    LevelLoader().read_level("level1.json")