class Color:
    def __init__(self, r, g, b):
        self.r = self.red = r
        self.g = self.green = g
        self.b = self.blue = b

    def __str__(self):
        return "(" + str(self.r) + ", " + str(self.g) + ", " + str(self.b) + ")"
