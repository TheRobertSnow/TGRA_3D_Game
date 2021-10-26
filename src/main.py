# 10.25.2021
# Róbert Snær Harðarson

# |===== IMPORTS =====|

from OpenGL.GL import *
from OpenGL.GLU import *

from math import *

import pygame
from pygame.locals import *

import sys
import time

from src.shaders.shaders import *
from src.essentials.matrices import *
from src.essentials.settings import *
from src.essentials.base_3d_objects import *


class FpsGame:
    def __init__(self):

        pygame.init()
        pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Lock mouse and keyboard to game window
        pygame.event.set_grab(True)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(3, 3, 3), Point(0, 0, 0), Vector(0, 1, 0))

        self.projection_matrix = ProjectionMatrix()
        # self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 100)
        self.projection_matrix.set_perspective(pi / 2, DISPLAY_WIDTH / DISPLAY_HEIGHT, 0.1, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.cube = Cube()
        self.sphere = Sphere()

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.mouseMove = False

        self.white_background = False

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        self.angle += pi * delta_time
        # if angle > 2 * pi:
        #     angle -= (2 * pi)

        if W_KEY.isPressed:
            self.view_matrix.slide(0, 0, -2 * delta_time)
        if A_KEY.isPressed:
            self.view_matrix.slide(-2 * delta_time, 0, 0)
        if S_KEY.isPressed:
            self.view_matrix.slide(0, 0, 2 * delta_time)
        if D_KEY.isPressed:
            self.view_matrix.slide(2 * delta_time, 0, 0)

        if self.mouseMove:
            mouseXNew, mouseYNew = pygame.mouse.get_rel()
            mouseXNew = (mouseXNew / 25) * 4
            mouseYNew = (mouseYNew / 25) * 4
            if mouseXNew > 0:
                self.view_matrix.yaw(-mouseXNew * delta_time)
            if mouseXNew < 0:
                self.view_matrix.yaw(-mouseXNew * delta_time)
            if mouseYNew > 0:
                self.view_matrix.pitch(-mouseYNew * delta_time)
            if mouseYNew < 0:
                self.view_matrix.pitch(-mouseYNew * delta_time)

    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)

        self.projection_matrix.set_perspective(pi / 2, DISPLAY_WIDTH / DISPLAY_HEIGHT, 0.1, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.model_matrix.load_identity()
        self.sphere.set_vertices(self.shader)

        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.shader.set_eye_position(self.view_matrix.eye)
        self.shader.set_global_ambient(0.2, 0.2, 0.2)

        light_pos = [(0.0, 10.0, 0.0, 1.0), (0.0, 0.0, 10.0, 1.0)]
        light_dif = [(1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0)]
        light_spe = [(0.8, 0.8, 0.8, 1.0), (0.8, 0.8, 0.8, 1.0)]
        light_amb = [(0.05, 0.05, 0.05, 1.0), (0.05, 0.05, 0.05, 1.0)]

        self.shader.set_light_pos(light_pos)
        self.shader.set_light_diffuse(light_dif)
        self.shader.set_light_specular(light_spe)
        self.shader.set_light_ambient(light_amb)

        self.shader.set_material_specualar(0.5, 0.5, 0.5)
        self.shader.set_material_shininess(5)

        self.shader.set_material_diffuse(0.8, 0.8, 0.2)
        self.shader.set_material_ambient(1.0, 1.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(3.0, 0.0, 0.0)
        self.model_matrix.add_scale(2.0, 2.0, 2.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.sphere.draw(self.shader)
        self.model_matrix.pop_matrix()

        self.cube.set_vertices(self.shader)

        self.shader.set_material_diffuse(0.2, 0.2, 0.8)
        self.shader.set_material_ambient(0.0, 0.0, 1.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0.0, 3.0, 0.0)
        self.model_matrix.add_rotate_y(self.angle)
        self.model_matrix.add_rotate_z(self.angle)
        self.model_matrix.add_scale(0.2, 2.5, 1.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        self.shader.set_material_diffuse(0.8, 0.2, 0.8)
        self.shader.set_material_ambient(1.0, 0.0, 1.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0.0, 0.0, -3.0)
        self.model_matrix.add_rotate_x(self.angle * 0.4)
        self.model_matrix.add_rotate_y(self.angle * 0.2)
        self.model_matrix.add_scale(0.5, 0.5, 0.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        pygame.display.flip()

    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True


                    if event.key == W_KEY.key:
                        W_KEY.isPressed = True
                    if event.key == A_KEY.key:
                        A_KEY.isPressed = True
                    if event.key == S_KEY.key:
                        S_KEY.isPressed = True
                    if event.key == D_KEY.key:
                        D_KEY.isPressed = True
                    if event.key == LSHIFT_KEY.key:
                        LSHIFT_KEY.isPressed = True


                elif event.type == pygame.KEYUP:
                    if event.key == W_KEY.key:
                        W_KEY.isPressed = False
                    if event.key == A_KEY.key:
                        A_KEY.isPressed = False
                    if event.key == S_KEY.key:
                        S_KEY.isPressed = False
                    if event.key == D_KEY.key:
                        D_KEY.isPressed = False
                    if event.key == LSHIFT_KEY.key:
                        LSHIFT_KEY.isPressed = False

                elif event.type == pygame.MOUSEMOTION:
                    self.mouseMove = True
                else:
                    self.mouseMove = False

            self.update()
            self.display()

        # OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()


if __name__ == "__main__":
    FpsGame().start()