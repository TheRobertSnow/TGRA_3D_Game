class EndPoint:
    # Class for handling end point
    def __init__(self, color, position, scale) -> None:
        self.color = color
        self.position = position
        self.scale = scale

    def checkIfCollission(self, x, z, r):
        P1_x = self.position[0] - (self.scale[0] * 0.5)
        P1_z = self.position[2] - (self.scale[2] * 0.5)
        P2_x = self.position[0] + (self.scale[0] * 0.5)
        P2_z = self.position[2] + (self.scale[2] * 0.5)
        if x + r >= P1_x and z + r >= P1_z and x - r <= P2_x and z - r <= P2_z:
            return True
        return False