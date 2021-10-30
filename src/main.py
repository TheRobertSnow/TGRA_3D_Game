
# |===== IMPORTS =====|

from OpenGL.GL import *
from OpenGL.GLU import *

from math import *

import pygame
from pygame.locals import *

import uuid
import sys
import time

from src.shaders.shaders import *
from src.essentials.matrices import *
from src.essentials.settings import *
from src.essentials.base_3d_objects import *
from src.essentials.color import Color
from src.data.level_loader import *
from src.network.interface import Interface
from src.data import kari_loader
from src.player.player import *
from src.essentials.hitbox import HitboxAABB

# |===== MAIN PROGRAM CLASS =====|
class FpsGame:
    def __init__(self, mode, id):

        pygame.init()
        pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)

        # /==/ Level Loader /==/
        self.levelLoader = LevelLoader()
        self.levelLoader.read_level(LEVEL_1)
        self.levelGround = self.levelLoader.ground
        self.levelWalls = self.levelLoader.walls
        self.levelEvilObjects = self.levelLoader.evilObjects
        self.startPoint = self.levelLoader.startPoint
        self.endPoint = self.levelLoader.endPoint

        # /==/ Network Interface /==/
        self.netInterf = Interface()
        # self.netId = uuid.uuid1()
        self.netId = id
        self.xzAngle = 0.0

        # /==/ Mesh Loader /==/
        self.player = kari_loader.load_obj_file(sys.path[0] + "/src/assets/meshes/player", "jeff.obj")
        self.mr_box = kari_loader.load_obj_file(sys.path[0] + "/src/assets/meshes/mr_box", "mr_box.obj")
        self.cent = kari_loader.load_obj_file(sys.path[0] + "/src/data/objects", "cent.obj")
        self.soldier = kari_loader.load_obj_file(sys.path[0] + "/src/assets/meshes/soldier", "dusty_2.obj")

        # /==/ Texture Loader /==/
        self.texture_0 = self.load_texture("/src/assets/meshes/player/jeff.png")
        self.texture_1 = self.load_texture("/src/assets/meshes/mr_box/box.png")
        self.texture_2 = self.load_texture("/src/assets/meshes/bricks.jpg")

        # /==/ Shaders /==/
        self.shader = Shader3D()
        self.shader.use()

        # /==/ Model Matrix /==/
        self.model_matrix = ModelMatrix()

        # /==/ View Matrix /==/
        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(1, 1.8, 0), Point(0, 0, 0), Vector(0, 1, 0))

        # /==/ Projection Matrix /==/
        self.projection_matrix = ProjectionMatrix()
        # self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 100)
        self.projection_matrix.set_perspective(pi / 2, DISPLAY_WIDTH / DISPLAY_HEIGHT, 0.1, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        # /==/ Players /==/
        self.playerCharacter = Player()
        self.opponents = []

        self.bullets = []

        # /==/ Meshes /==/
        self.cube = Cube()
        self.sphere = Sphere()

        # /==/ Time /==/
        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.t0 = time.process_time()

        # /==/ Init Input /==/
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)
        # Lock mouse and keyboard to game window
        pygame.event.set_grab(True)

        # /==/ Variables /==/
        self.angle = 0
        self.speed = MOVEMENTSPEED
        self.upwards = 0
        self.jumping = False
        self.mouseMove = False
        self.fireGun = False
        self.white_background = False
        self.gameMode = mode
        self.playersHit = []

    def load_texture(self, filePath):
        # Loading and Binding Texture
        surface = pygame.image.load(sys.path[0] + filePath)
        tex_string = pygame.image.tostring(surface, "RGBA", 1)
        width = surface.get_width()
        height = surface.get_height()
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_string)
        return tex_id

    # |===== Create Network Str =====|
    def create_net_str(self):
        netStr = "id:" + str(self.netId) + ";"
        netStr += self.view_matrix.get_eye_str()
        netStr += str(self.xzAngle)
        if self.playersHit:
            for op in self.playersHit:
                if op.died:
                    netStr += ";" + op.name + ":died"
                else:
                    netStr += ";" + op.name + str(op.health)
            self.playersHit.clear()
        netStr += "/"
        print("Sending: " + netStr)
        return netStr

    # |===== Decode Net String =====|
    def decode_net_str(self, netStr):
        if netStr.startswith("id:"):
            temp = netStr.split("/")
            # temp[0].strip("id:")
            temp1 = temp[0].split(";")
            n = temp1[0].replace("id:", "")
            print("Temp: ", temp)
            try:
                eyex, eyey, eyez = temp1[1].split(',')
            except ValueError:
                # print("ERROR")
                return
            exists = False
            opponent = None
            for op in self.opponents:
                print("Name: " + op.name)
                if op.name == n:
                    exists = True
                    opponent = op
            if not exists:
                newPlayer = Player()
                newPlayer.name = n
                newPlayer.position = Point(float(eyex), float(eyey), float(eyez))
                newPlayer.angle = float(temp1[2])
                opponent = newPlayer
                self.opponents.append(opponent)
            else:
                op.position = Point(float(eyex), float(eyey), float(eyez))
                op.angle = float(temp1[2])

            if len(temp1) > 3:
                # print(temp1)
                for index, value in enumerate(temp1):
                    if index != 0 and index != 1 and index != 2:
                        k, v = temp1[index].split(":")
                        if (v != "died"):
                            opponent.health -= int(v)
                        else:
                            opponent.died = True
            print(self.opponents)



    def check_if_player_moving(self):
        if W_KEY.isPressed:
            return True
        elif A_KEY.isPressed:
            return True
        elif S_KEY.isPressed:
            return True
        elif D_KEY.isPressed:
            return True
        elif self.jumping:
            return True
        elif self.mouseMove:
            return True
        else:
            return False


    # |===== UPDATE =====|
    def update(self):
        delta_time = self.clock.tick() / 1000.0

        self.angle += pi * delta_time
        # if self.angle > 2 * pi:
        #     self.angle -= (2 * pi)

        # /==/ User Input /==/
        if W_KEY.isPressed:
            self.view_matrix.slide(0, 0, -self.speed * delta_time)
        if A_KEY.isPressed:
            self.view_matrix.slide(-self.speed * delta_time, 0, 0)
        if S_KEY.isPressed:
            self.view_matrix.slide(0, 0, self.speed * delta_time)
        if D_KEY.isPressed:
            self.view_matrix.slide(self.speed * delta_time, 0, 0)
        if LSHIFT_KEY.isPressed:
            self.speed = MOVEMENTSPEED * 2
        if not LSHIFT_KEY.isPressed:
            self.speed = MOVEMENTSPEED

        # /==/ Jumping Logic /==/
        self.upwards += GRAVITY * delta_time
        self.view_matrix.eye.y += self.upwards * delta_time
        if (self.view_matrix.eye.y < CAMERA_HEIGHT):
            self.upwards = 0
            self.view_matrix.eye.y = CAMERA_HEIGHT
            self.jumping = False

        if self.mouseMove:
            mouseXNew, mouseYNew = pygame.mouse.get_rel()
            mouseXNew = (mouseXNew / 25) * 4
            self.xzAngle += -mouseXNew * delta_time
            mouseYNew = (mouseYNew / 25) * 4
            if mouseXNew > 0:
                self.view_matrix.yaw(-mouseXNew * delta_time)
            if mouseXNew < 0:
                self.view_matrix.yaw(-mouseXNew * delta_time)
            if mouseYNew > 0:
                self.view_matrix.pitch(-mouseYNew * delta_time)
            if mouseYNew < 0:
                self.view_matrix.pitch(-mouseYNew * delta_time)

        if self.fireGun:
            # /==/ Do some gun shit /==/
            # cast ray and see if it hits player
            self.player.isHit = self.player.aabb.ray_intersects_aabb(self.view_matrix.eye, (self.view_matrix.n * -1) * 100)
            for op in self.opponents:
                # print(val["aabb"])
                isHit = op.aabb.ray_intersects_aabb(self.view_matrix.eye, (self.view_matrix.n * -1) * 100)
                print(isHit)
                if isHit:
                    self.op.health -= 10
                if op not in self.playersHit:
                    self.playersHit.append(op)
                # if mesh is hit add it to isHit list
            self.fireGun = False

        if self.netInterf.isAvailable:
            if self.check_if_player_moving():
                t1 = time.process_time() - self.t0
                if t1 >= 0.1:
                    # Add zxAngle to send()
                    self.t0 = time.process_time()
                    self.netInterf.send(self.create_net_str())
                    self.zxAngle = 0.0

            recvString = self.netInterf.recv()
            if recvString != "":
                self.decode_net_str(recvString)

    # |===== DISPLAY =====|
    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)

        glClearColor(0.78, 1.0, 1.0, 1.0)

        self.projection_matrix.set_perspective(pi / 2, DISPLAY_WIDTH / DISPLAY_HEIGHT, 0.1, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.shader.set_eye_position(self.view_matrix.eye)
        self.model_matrix.load_identity()
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        light_pos = [(21.0, 10.0, 1.75, 1.0), (-21.0, 1.5, 1.75, 1.0), (0.0, 1.5, 1.75, 1.0)]
        light_dif = [(1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0)]
        light_spe = [(0.8, 0.8, 0.8, 1.0), (0.8, 0.8, 0.8, 1.0), (0.8, 0.8, 0.8, 1.0)]
        light_amb = [(0.05, 0.05, 0.05, 1.0), (0.05, 0.05, 0.05, 1.0), (0.05, 0.05, 0.05, 1.0)]

        self.shader.set_light_pos(light_pos)
        self.shader.set_light_diffuse(light_dif)
        self.shader.set_light_specular(light_spe)
        self.shader.set_light_ambient(light_amb)
        self.shader.set_global_ambient(0.2, 0.2, 0.2)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_0)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.texture_1)
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, self.texture_2)

        self.cube.set_vertices(self.shader)

        # |===== DRAW OBJECTS =====|

        # DRAW GROUND
        # for ground in self.levelGround:
        #     self.shader.set_material_diffuse(Color(ground.color[0], ground.color[1], ground.color[2]))
        #     self.shader.set_material_specular(Color(0.1, 0.1, 0.1))
        #     self.shader.set_material_ambient(Color(0.1, 0.1, 0.1))
        #     self.shader.set_material_shininess(1.0)
        #     self.model_matrix.push_matrix()
        #     self.model_matrix.add_translation(ground.translation[0], ground.translation[1], ground.translation[2])
        #     self.model_matrix.add_rotate_x(ground.rotate[0])
        #     self.model_matrix.add_rotate_y(ground.rotate[1])
        #     self.model_matrix.add_rotate_z(ground.rotate[2])
        #     self.model_matrix.add_scale(ground.scale[0], ground.scale[1], ground.scale[2])
        #     self.shader.set_model_matrix(self.model_matrix.matrix)
        #     self.cube.draw(self.shader)
        #     self.model_matrix.pop_matrix()
        #
        # # DRAW WALLS
        # for wall in self.levelWalls:
        #     self.shader.set_material_diffuse(Color(wall.color[0], wall.color[1], wall.color[2]))
        #     self.shader.set_material_specular(Color(0.1, 0.1, 0.1))
        #     self.shader.set_material_ambient(Color(0.1, 0.1, 0.1))
        #     self.shader.set_material_shininess(1.0)
        #     self.model_matrix.push_matrix()
        #     self.model_matrix.add_translation(wall.translation[0], wall.translation[1], wall.translation[2])
        #     self.model_matrix.add_rotate_x(wall.rotate[0])
        #     self.model_matrix.add_rotate_y(wall.rotate[1])
        #     self.model_matrix.add_rotate_z(wall.rotate[2])
        #     self.model_matrix.add_scale(wall.scale[0], wall.scale[1], wall.scale[2])
        #     self.shader.set_model_matrix(self.model_matrix.matrix)
        #     self.cube.draw(self.shader)
        #     self.model_matrix.pop_matrix()
        #
        # # DRAW EVIL OBJECTS
        # for evilObject in self.levelEvilObjects:
        #     self.shader.set_material_diffuse(evilObject.color[0], evilObject.color[1], evilObject.color[2])
        #     self.shader.set_material_specular(0.1, 0.1, 0.1)
        #     self.shader.set_material_ambient(0.1, 0.1, 0.1)
        #     self.shader.set_material_shininess(1.0)
        #     self.model_matrix.push_matrix()
        #     self.model_matrix.add_translation(evilObject.translationCurr.x, evilObject.translationCurr.y,
        #                                          evilObject.translationCurr.z)
        #     self.model_matrix.add_rotate_x(evilObject.rotate[0])
        #     self.model_matrix.add_rotate_y(evilObject.rotate[1])
        #     self.model_matrix.add_rotate_z(evilObject.rotate[2])
        #     self.model_matrix.add_scale(evilObject.scale[0], evilObject.scale[1], evilObject.scale[2])
        #     self.shader.set_model_matrix(self.model_matrix.matrix)
        #     self.cube.draw(self.shader)
        #     self.model_matrix.pop_matrix()
        #
        # # DRAW FINISH LINE BOX
        # self.shader.set_material_diffuse(self.endPoint[0].color[0], self.endPoint[0].color[1],
        #                                 self.endPoint[0].color[2])
        # self.shader.set_material_specular(0.1, 0.1, 0.1)
        # self.shader.set_material_ambient(0.1, 0.1, 0.1)
        # self.shader.set_material_shininess(1.0)
        # self.model_matrix.push_matrix()
        # self.model_matrix.add_translation(self.endPoint[0].position[0], self.endPoint[0].position[1],
        #                                 self.endPoint[0].position[2])
        # self.model_matrix.add_scale(self.endPoint[0].scale[0], self.endPoint[0].scale[1], self.endPoint[0].scale[2])
        # self.shader.set_model_matrix(self.model_matrix.matrix)
        # self.cube.draw(self.shader)
        # self.model_matrix.pop_matrix()


        # self.sphere.set_vertices(self.shader)
        # Draw the lines of the polygon, but not fill it
        # Good for working with hitbox
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        self.shader.set_diffuse_tex(2)
        self.shader.set_specular_tex(2)
        self.shader.set_ambient_tex(2)
        self.shader.set_material_diffuse(Color(0.8, 0.8, 0.2))
        self.shader.set_material_ambient(Color(1.0, 1.0, 0.0))
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(3.0, 5.0, 10.0)
        self.model_matrix.add_scale(2.0, 2.0, 2.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.sphere.draw(self.shader)
        self.model_matrix.pop_matrix()

        # glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        #self.cube.set_vertices(self.shader)
        #self.shader.set_diffuse_tex(1)
        # self.shader.set_specular_tex(1)
        # self.shader.set_ambient_tex(1)
        # self.shader.set_material_diffuse(Color(0.2, 0.2, 0.8))
        # self.shader.set_material_ambient(Color(0.0, 0.0, 1.0))
        # self.model_matrix.push_matrix()
        # self.model_matrix.add_translation(0.0, 3.0, 0.0)
        # self.model_matrix.add_rotate_y(self.angle)
        # self.model_matrix.add_rotate_z(self.angle)
        # self.model_matrix.add_scale(0.2, 2.5, 1.5)
        # self.shader.set_model_matrix(self.model_matrix.matrix)
        # self.cube.draw(self.shader)
        # self.model_matrix.pop_matrix()

        # self.shader.set_diffuse_tex(1)
        # self.shader.set_specular_tex(1)
        # self.shader.set_ambient_tex(1)
        # self.shader.set_material_diffuse(Color(0.8, 0.2, 0.8))
        # self.shader.set_material_ambient(Color(1.0, 0.0, 1.0))
        # self.model_matrix.push_matrix()
        # self.model_matrix.add_translation(0.0, 0.0, -3.0)
        # self.model_matrix.add_rotate_x(self.angle * 0.4)
        # self.model_matrix.add_rotate_y(self.angle * 0.2)
        # self.model_matrix.add_scale(0.5, 0.5, 0.5)
        # self.shader.set_model_matrix(self.model_matrix.matrix)
        # self.cube.draw(self.shader)
        # self.model_matrix.pop_matrix()
        #
        self.shader.set_diffuse_tex(2)
        self.shader.set_specular_tex(2)
        self.shader.set_ambient_tex(2)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(5.0, 1.0, 1.0)
        self.model_matrix.add_scale(1.0, 1.0, 1.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.mr_box.draw(self.shader)
        self.model_matrix.pop_matrix()

        if not self.player.isHit:
            self.shader.set_diffuse_tex(0)
            self.shader.set_specular_tex(0)
            self.shader.set_ambient_tex(0)
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(1.0, 1.0, 1.0)
            self.model_matrix.add_scale(1.0, 1.0, 1.0)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.player.recalc_aabb()
            self.player.draw(self.shader)
            self.model_matrix.pop_matrix()

        # self.model_matrix.push_matrix()
        # self.model_matrix.add_translation(4.0, 4.0, 4.0)
        # self.model_matrix.add_scale(0.1, 0.1, 0.1)
        # self.shader.set_model_matrix(self.model_matrix.matrix)
        # self.cent.draw(self.shader)
        # self.model_matrix.pop_matrix()
        #
        # self.model_matrix.push_matrix()
        # self.model_matrix.add_translation(0.0, 0.0, 4.0)
        # self.model_matrix.add_scale(0.001, 0.001, 0.001)
        # self.shader.set_model_matrix(self.model_matrix.matrix)
        # self.soldier.draw(self.shader)
        # self.model_matrix.pop_matrix()
        #
        # self.shader.set_diffuse_tex(1)
        # self.shader.set_specular_tex(1)
        # self.shader.set_ambient_tex(1)
        # self.model_matrix.push_matrix()
        # self.model_matrix.add_translation(0.0, 0.0, -3.0)
        # self.model_matrix.add_rotate_x(self.angle * 0.4)
        # self.model_matrix.add_scale(1.0, 1.0, 1.0)
        # self.shader.set_model_matrix(self.model_matrix.matrix)
        # self.cube.draw(self.shader)
        # self.model_matrix.pop_matrix()

        # /==/ Draw Opponents /==/
        for op in self.opponents:
            self.shader.set_diffuse_tex(0)
            self.shader.set_specular_tex(0)
            self.shader.set_ambient_tex(0)
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(op.position.x, op.position.y, op.position.z)
            self.model_matrix.add_rotate_y(1.5708 + op.angle)
            self.model_matrix.add_scale(1.0, 1.0, 1.0)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            op.calc_aabb(self.player.vertex_arrays)
            self.player.draw(self.shader)
            self.model_matrix.pop_matrix()

        # /==/ Draw Hud /==/
        glDisable(GL_DEPTH_TEST)
        pygame.display.flip()

    # |===== MAIN PROGRAM FUNCTION =====|
    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    self.netInterf.closeSock()
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        self.netInterf.closeSock()
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
                    if event.key == SPACE_BAR.key:
                        SPACE_BAR.isPressed = True
                        if not self.jumping:
                            self.upwards = JUMP_POWER
                            self.jumping = True

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
                    if event.key == SPACE_BAR.key:
                        SPACE_BAR.isPressed = False

                elif event.type == pygame.MOUSEMOTION:
                    self.mouseMove = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.fireGun = True
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