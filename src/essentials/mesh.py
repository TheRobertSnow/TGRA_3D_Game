import numpy as numpy

from src.essentials.material import Material
from OpenGL.GL import *

class Mesh:
    def __init__(self):
        self.vertexArrays = dict()
        self.textureArrays = dict()
        self.normalArrays = dict()
        self.objectMaterials = dict()
        self.materials = dict()
        self.vertexBufferIds = dict()

    def add_vertex(self, objectId, vertexList):
        if objectId not in self.vertexArrays:
            self.vertexArrays[objectId] = vertexList

    def add_texture(self, objectId, textureList):
        if objectId not in self.textureArrays:
            self.textureArrays[objectId] = textureList

    def add_normal(self, objectId, normalList):
        if objectId not in self.normalArrays:
            self.normalArrays[objectId] = normalList

    def add_objectMaterial(self, objectId, material):
        if objectId not in self.objectMaterials:
            self.objectMaterials[objectId] = material

    def add_material(self, material, shininess, ambiance, diffuse, specular, transparency, textureFile):
        self.materials[material] = {'shininess': shininess, 'ambiance': ambiance, 'diffuse': diffuse,
                                    'specular': specular, 'transparency': transparency, 'textureFile': textureFile}

    def set_opengl_buffers(self):
        for objectId in self.objectMaterials.keys():
            self.vertexBufferIds[objectId] = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.vertexBufferIds[objectId])
            glBufferData(GL_ARRAY_BUFFER, numpy.array(self.vertexBufferIds[objectId], dtype='float32'), GL_STATIC_DRAW)
            glBindBuffer(GL_ARRAY_BUFFER, 0)

    def draw(self, shader, model_matrix):
        for key, value in self.objectMaterials.items():
            shader.set_position_attribute(self.vertexArrays[key])
            shader.set_normal_attribute(self.normalArrays[key])
            #shader.set_uv_attribute(self.textureArrays[key])
            shader.set_material_shininess(self.materials[value]['shininess'])
            shader.set_material_ambient(self.materials[value]['ambiance'])
            shader.set_material_diffuse(self.materials[value]['diffuse'])
            shader.set_material_specular(self.materials[value]['specular'])
            #shader.set_attribute_buffers_with_uv(self.vertexBufferIds[key])
            #model_matrix.push_matrix()
            #model_matrix.add_translation(2.0, 5.0, 2.0)
            #shader.set_model_matrix(model_matrix.matrix)
            i = 0
            for i in range(0, (int(len(self.vertexArrays[key]) / 3)) - 1, 3):
                glDrawArrays(GL_TRIANGLE_FAN, i, 3)
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            #model_matrix.pop_matrix()