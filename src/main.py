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
from src.data.level_loader import *
from src.player.player import Player


# |===== MAIN PROGRAM CLASS =====|
class FpsGame:
    def __init__(self, mode):

        pygame.init()
        pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Lock mouse and keyboard to game window
        pygame.event.set_grab(True)

        # Load level
        self.levelLoader = LevelLoader()
        self.levelLoader.read_level(LEVEL_1)
        self.levelGround = self.levelLoader.ground
        self.levelWalls = self.levelLoader.walls
        self.levelEvilObjects = self.levelLoader.evilObjects
        self.startPoint = self.levelLoader.startPoint
        self.endPoint = self.levelLoader.endPoint

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(3, 3, 3), Point(0, 0, 0), Vector(0, 1, 0))

        self.projection_matrix = ProjectionMatrix()
        # self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 100)
        self.projection_matrix.set_perspective(pi / 2, DISPLAY_WIDTH / DISPLAY_HEIGHT, 0.1, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        # TODO: Add Player

        self.cube = Cube()
        self.sphere = Sphere()

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.speed = MOVEMENTSPEED

        self.mouseMove = False

        self.white_background = False

        self.gameMode = mode

    # |===== UPDATE =====|
    def update(self):
        delta_time = self.clock.tick() / 1000.0

        self.angle += pi * delta_time
        # if angle > 2 * pi:
        #     angle -= (2 * pi)

        if W_KEY.isPressed:
            self.view_matrix.slide(0, 0, -self.speed * delta_time)
        if A_KEY.isPressed:
            self.view_matrix.slide(-self.speed * delta_time, 0, 0)
        if S_KEY.isPressed:
            self.view_matrix.slide(0, 0, self.speed * delta_time)
        if D_KEY.isPressed:
            self.view_matrix.slide(self.speed * delta_time, 0, 0)
        if LSHIFT_KEY.isPressed:
            self.speed = MOVEMENTSPEED * 4
        if not LSHIFT_KEY.isPressed:
            self.speed = MOVEMENTSPEED

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

    # |===== DISPLAY =====|
    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)

        glClearColor(0.78, 1.0, 1.0, 1.0)

        self.projection_matrix.set_perspective(pi / 2, DISPLAY_WIDTH / DISPLAY_HEIGHT, 0.1, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.model_matrix.load_identity()


        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.shader.set_eye_position(self.view_matrix.eye)
        self.shader.set_global_ambient(0.2, 0.2, 0.2)

        light_pos = [(21.0, 1.5, 1.75, 1.0), (-21.0, 1.5, 1.75, 1.0), (0.0, 1.5, 1.75, 1.0)]
        light_dif = [(1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0)]
        light_spe = [(0.8, 0.8, 0.8, 1.0), (0.8, 0.8, 0.8, 1.0), (0.8, 0.8, 0.8, 1.0)]
        light_amb = [(0.05, 0.05, 0.05, 1.0), (0.05, 0.05, 0.05, 1.0), (0.05, 0.05, 0.05, 1.0)]

        self.shader.set_light_pos(light_pos)
        self.shader.set_light_diffuse(light_dif)
        self.shader.set_light_specular(light_spe)
        self.shader.set_light_ambient(light_amb)

        self.shader.set_material_specular(0.5, 0.5, 0.5)
        self.shader.set_material_shininess(5)

        self.cube.set_vertices(self.shader)

        # |===== DRAW OBJECTS =====|

        # DRAW GROUND
        for ground in self.levelGround:
            self.shader.set_material_diffuse(ground.color[0], ground.color[1], ground.color[2])
            self.shader.set_material_specular(0.1, 0.1, 0.1)
            self.shader.set_material_ambient(0.1, 0.1, 0.1)
            self.shader.set_material_shininess(1.0)
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(ground.translation[0], ground.translation[1], ground.translation[2])
            self.model_matrix.add_rotate_x(ground.rotate[0])
            self.model_matrix.add_rotate_y(ground.rotate[1])
            self.model_matrix.add_rotate_z(ground.rotate[2])
            self.model_matrix.add_scale(ground.scale[0], ground.scale[1], ground.scale[2])
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.cube.draw(self.shader)
            self.model_matrix.pop_matrix()

        # DRAW WALLS
        for wall in self.levelWalls:
            self.shader.set_material_diffuse(wall.color[0], wall.color[1], wall.color[2])
            self.shader.set_material_specular(0.1, 0.1, 0.1)
            self.shader.set_material_ambient(0.1, 0.1, 0.1)
            self.shader.set_material_shininess(1.0)
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(wall.translation[0], wall.translation[1], wall.translation[2])
            self.model_matrix.add_rotate_x(wall.rotate[0])
            self.model_matrix.add_rotate_y(wall.rotate[1])
            self.model_matrix.add_rotate_z(wall.rotate[2])
            self.model_matrix.add_scale(wall.scale[0], wall.scale[1], wall.scale[2])
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.cube.draw(self.shader)
            self.model_matrix.pop_matrix()

        # DRAW EVIL OBJECTS
        for evilObject in self.levelEvilObjects:
            self.shader.set_material_diffuse(evilObject.color[0], evilObject.color[1], evilObject.color[2])
            self.shader.set_material_specular(0.1, 0.1, 0.1)
            self.shader.set_material_ambient(0.1, 0.1, 0.1)
            self.shader.set_material_shininess(1.0)
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(evilObject.translationCurr.x, evilObject.translationCurr.y,
                                                 evilObject.translationCurr.z)
            self.model_matrix.add_rotate_x(evilObject.rotate[0])
            self.model_matrix.add_rotate_y(evilObject.rotate[1])
            self.model_matrix.add_rotate_z(evilObject.rotate[2])
            self.model_matrix.add_scale(evilObject.scale[0], evilObject.scale[1], evilObject.scale[2])
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.cube.draw(self.shader)
            self.model_matrix.pop_matrix()

        # DRAW FINISH LINE BOX
        self.shader.set_material_diffuse(self.endPoint[0].color[0], self.endPoint[0].color[1],
                                        self.endPoint[0].color[2])
        self.shader.set_material_specular(0.1, 0.1, 0.1)
        self.shader.set_material_ambient(0.1, 0.1, 0.1)
        self.shader.set_material_shininess(1.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.endPoint[0].position[0], self.endPoint[0].position[1],
                                        self.endPoint[0].position[2])
        self.model_matrix.add_scale(self.endPoint[0].scale[0], self.endPoint[0].scale[1], self.endPoint[0].scale[2])
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()


        self.sphere.set_vertices(self.shader)
        # Draw the lines of the polygon, but not fill it
        # Good for working with hitbox
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        self.shader.set_material_diffuse(0.8, 0.8, 0.2)
        self.shader.set_material_ambient(1.0, 1.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(3.0, 0.0, 0.0)
        self.model_matrix.add_scale(2.0, 2.0, 2.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.sphere.draw(self.shader)
        self.model_matrix.pop_matrix()

        # glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

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

    # |===== MAIN PROGRAM FUNCTION =====|
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

    # |===== STARTS THE PROGRAM =====|
    def start(self):
        self.program_loop()


if __name__ == "__main__":
    FpsGame().start()