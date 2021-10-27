from src.essentials.material import Material

class Mesh:
    def __init__(self):
        self.vertexArrays = dict()
        self.textureArrays = dict()
        self.normalArrays = dict()
        self.materials = dict()
        self.vertexCounts = dict()
        self.vertexBufferIds = dict()

    def add_vertex(self, meshId, position, normal, uv=None):
        if meshId not in self.vertexArrays:
            self.vertexArrays[meshId] = []

    def set_mesh_material(self):
        pass



    def draw(self):
        pass
        # for meshId, meshMaterial in self.materials.items():
        #     material = self.materials[mesh]