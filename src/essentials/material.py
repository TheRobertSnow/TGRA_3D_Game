from src.essentials.color import Color

class Material:
    def __init__(self, diffuse: Color = None, specular: Color = None, ambient: Color = None, shininess: Color = None):
        self.diffuse = Color(0.0, 0.0, 0.0) if diffuse == None else diffuse
        self.specular = Color(0.0, 0.0, 0.0) if specular == None else specular
        self.ambient = Color(0.0, 0.0, 0.0) if ambient == None else ambient
        self.shininess = 1.0 if shininess == None else shininess
