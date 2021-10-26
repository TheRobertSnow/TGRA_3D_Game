from ..mesh_loader import MeshLoader
from OpenGL.GL import *
import sys

class Player:
    def __init__(self):
        self.angle = 0
        self.vertices = []
        self.faces = []
        self.coordinates = [0, 0, 0]  # [x,y,z]
        self.player = MeshLoader(sys.path[0] + "/src/data/objects/player.obj")
        self.position = [0, 0, -5]

    def render_scene(self):
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #glClearColor(0.902, 0.902, 1, 0.0)
        #glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(self.coordinates[0], self.coordinates[1], self.coordinates[2])