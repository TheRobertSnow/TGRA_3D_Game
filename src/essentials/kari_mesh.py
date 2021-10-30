import numpy as numpy
from OpenGL.GL import *

from src.essentials.hitbox import HitboxAABB
from src.essentials.settings import TYPE_PLAYER, TYPE_ENVIRON

class MeshModel:
    def __init__(self):
        self.vertex_arrays = dict()
        self.mesh_materials = dict()  # Key table between mesh and materials
        self.materials = dict()
        self.vertex_counts = dict()
        self.vertex_buffer_ids = dict()
        self.aabb = HitboxAABB()
        self.type = None
        self.isHit = False

    def add_vertex(self, mesh_id, position, normal, uv=None):
        if mesh_id not in self.vertex_arrays:
            self.vertex_arrays[mesh_id] = []
            self.vertex_counts[mesh_id] = 0
        self.vertex_arrays[mesh_id] += [position.x, position.y, position.z, normal.x, normal.y, normal.z, uv.x, uv.y]
        self.vertex_counts[mesh_id] += 1

    def set_mesh_material(self, mesh_id, mat_id):
        self.mesh_materials[mesh_id] = mat_id

    def add_material(self, mat_id, mat):
        self.materials[mat_id] = mat

    def set_aabb(self, vMax, vMin):
        self.aabb.set_max(vMax)
        self.aabb.set_min(vMin)

    def recalc_aabb(self):
        for key, val in self.vertex_arrays.items():
            for i in range(0, int(len(val)/3) -1, 3):
                if val[i] > self.aabb.max.x: self.aabb.max.x = val[i]
                if val[i] < self.aabb.min.x: self.aabb.min.x = val[i]
                if val[i+1] > self.aabb.max.y: self.aabb.max.y = val[i+1]
                if val[i+1] < self.aabb.min.y: self.aabb.min.y = val[i+1]
                if val[i+2] > self.aabb.max.z: self.aabb.max.z = val[i+2]
                if val[i+2] < self.aabb.min.z: self.aabb.min.z = val[i+2]

    # Makes buffers for each of the mesh id
    def set_opengl_buffers(self):
        for mesh_id in self.mesh_materials.keys():
            self.vertex_buffer_ids[mesh_id] = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_ids[mesh_id])
            glBufferData(GL_ARRAY_BUFFER, numpy.array(self.vertex_arrays[mesh_id], dtype='float32'), GL_STATIC_DRAW)
            glBindBuffer(GL_ARRAY_BUFFER, 0)

    def set_type_player(self):
        self.type = TYPE_PLAYER

    def set_type_environment(self):
        self.type = TYPE_ENVIRON

    def draw(self, shader):
        for mesh_id, mesh_material in self.mesh_materials.items():
            material = self.materials[mesh_material]
            shader.set_material_ambient(material.ambient)
            shader.set_material_diffuse(material.diffuse)
            shader.set_material_specular(material.specular)
            shader.set_material_shininess(material.shininess)
            shader.set_attribute_buffers_with_uv(self.vertex_buffer_ids[mesh_id])
            glDrawArrays(GL_TRIANGLES, 0, self.vertex_counts[mesh_id])
            glBindBuffer(GL_ARRAY_BUFFER, 0)