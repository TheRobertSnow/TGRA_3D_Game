import numpy as numpy

from src.essentials.material import Material
from OpenGL.GL import *
from src.essentials.hitbox import HitboxAABB

class Mesh:
    def __init__(self):
        self.vertexArrays = dict()
        self.textureArrays = dict()
        self.normalArrays = dict()
        self.objectMaterials = dict()
        self.materials = dict()
        self.materialFile = ""
        self.vertex_counts = dict()
        self.vertexBufferIds = dict()
        self.aabb = HitboxAABB()

    #def add_vertex(self, objectId, vertexList):
        #if objectId not in self.vertexArrays:
            #self.vertexArrays[objectId] = vertexList
            #self.vertex_counts[objectId] = 0
        #self.vertex_counts[objectId] += 1

    def add_vertex(self, objectId, position, normal, uv=None):
        if objectId not in self.vertexArrays:
            self.vertexArrays[objectId] = []
            self.vertex_counts[objectId] = 0
        self.vertexArrays[objectId] += [position.x, position.y, position.z, normal.x, normal.y, normal.z, uv.x, uv.y]
        self.vertex_counts[objectId] += 1

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

    def draw(self, shader):
        for key, value in self.objectMaterials.items():
            print(key)
            #shader.set_position_attribute(self.vertexArrays[key])
            #shader.set_normal_attribute(self.normalArrays[key])
            #shader.set_uv_attribute(self.textureArrays[key])
            shader.set_material_shininess(self.materials[self.materialFile]['shininess'])
            shader.set_material_ambient(self.materials[self.materialFile]['ambiance'])
            shader.set_material_diffuse(self.materials[self.materialFile]['diffuse'])
            shader.set_material_specular(self.materials[self.materialFile]['specular'])
            shader.set_attribute_buffers_with_uv(self.vertexBufferIds[key])
            glDrawArrays(GL_TRIANGLES, 0, self.vertex_counts[key])
            glBindBuffer(GL_ARRAY_BUFFER, 0)