
# |===== IMPORTS =====|
from pygame.locals import *
import time
import random
from src.shaders.shaders import *
from src.essentials.matrices import *
from src.essentials.settings import *
from src.essentials.base_3d_objects import *
from src.essentials.color import Color
from src.data.level_loader import *
from src.network.interface import Interface
from src.data import mesh_loader
from src.player.player import *
from src.essentials.hitbox import HitboxAABB
from PIL import Image, ImageDraw, ImageFont

# |===== MAIN PROGRAM CLASS =====|ds
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
        self.spawnPoints = self.levelLoader.spawnPoints

        # /==/ Network Interface /==/
        self.netInterf = Interface()
        self.netId = id
        self.xzAngle = 0.0

        # /==/ Shaders /==/
        self.shader = Shader3D()
        self.shader.use()

        # /==/ Model Matrix /==/
        self.model_matrix = ModelMatrix()

        # /==/ View Matrix /==/
        self.view_matrix = ViewMatrix()
        randSpawnPoint = self.spawnPoints[random.randint(0, len(self.spawnPoints)-1)].position
        self.view_matrix.look(Point(randSpawnPoint.x, CAMERA_HEIGHT, randSpawnPoint.z), Point(0, 0, 0), Vector(0, 1, 0))

        # /==/ View Matrix For Health Bar and Crosshair /==/
        self.view_matrix2 = ViewMatrix()
        self.view_matrix2.look(Point(0.01, 0, 0), Point(0, 0, 0), Vector(0, 0.01, 0))

        # /==/ Projection Matrix /==/
        self.projection_matrix = ProjectionMatrix()
        self.projection_matrix.set_perspective(pi / 2, DISPLAY_WIDTH / DISPLAY_HEIGHT, 0.1, 100)

        # /==/ Projection Matrix For Health Bar and Crosshair /==/
        self.projection_matrix2 = ProjectionMatrix()
        self.projection_matrix2.set_orthographic(-0.5, 0.5, -0.5, 0.5, 0.5, 100)

        # /==/ Players /==/
        self.opponents = []

        # /==/ Meshes /==/
        self.cube = Cube()
        self.player = mesh_loader.load_obj_file(sys.path[0] + "/src/assets/meshes/player", "jeff.obj")

        # /==/ Texture Loader /==/
        self.jeff_texture = self.load_texture("/src/assets/meshes/player/jeff.png")
        self.base_texture = self.load_texture("/src/assets/meshes/base.png")
        self.ground_texture = self.load_texture("/src/assets/meshes/ground.jpg")
        self.walls_texture = self.load_texture("/src/assets/meshes/walls.jpg")
        self.evil_texture = self.load_texture("/src/assets/meshes/evil.jpg")
        self.health_texture = self.load_texture("/src/assets/meshes/health.jpg")
        self.health_back_texture = self.load_texture("/src/assets/meshes/health_back.jpg")

        # /==/ Time /==/
        self.clock = pygame.time.Clock()
        self.clock.tick()
        self.t0 = time.process_time()

        # /==/ Sounds /==/
        pygame.mixer.init()
        self.mainMusic = pygame.mixer.Sound(SOUND_MAIN_MUSIC)
        self.gunSound = pygame.mixer.Sound(SOUND_GUNSHOT)
        self.mainMusic.set_volume(0.1)
        self.gunSound.set_volume(0.1)
        pygame.mixer.Channel(0).play(self.mainMusic, -1)
        # self.mainMusic.play(-1)
        # pygame.mixer.Channel(0).play(self.mainMusic)
        # pygame.mixer.Channel(1).play(pygame.mixer.Sound(sys.path[0] + SOUND_GUNSHOT))

        # /==/ Init Input /==/
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)
        # Lock mouse and keyboard to game window
        pygame.event.set_grab(True)

        # /==/ Variables /==/
        self.speed = MOVEMENTSPEED
        self.upwards = 0
        self.jumping = False
        self.mouseMove = False
        self.fireGun = False
        self.gameMode = mode
        self.playersHit = []
        self.health = HEALTH
        self.died = False
        self.lives = LIVES
        self.aabb = HitboxAABB(Vector(-0.30, 0.01, -0.30), Vector(0.30, 2.15, 0.30))
        self.respawned = False
        self.left = False
        self.lost = False

    # |===== Loading and Binding Texture =====|
    def load_texture(self, filePath):
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

    # |===== Draws Objects =====|
    def drawObject(self, object, texture, trans=Vector(0.0, 0.0, 0.0), scale=Vector(1.0, 1.0, 1.0), rotate=Vector(0.0, 0.0, 0.0)):
        glBindTexture(GL_TEXTURE_2D, texture)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(trans.x, trans.y, trans.z)
        self.model_matrix.add_rotate_x(rotate.x)
        self.model_matrix.add_rotate_y(rotate.y)
        self.model_matrix.add_rotate_z(rotate.z)
        self.model_matrix.add_scale(scale.x, scale.y, scale.z)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        if object == self.cube:
            self.cube.set_vertices(self.shader)
        object.draw(self.shader)
        self.model_matrix.pop_matrix()

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
                    netStr += ";" + op.name + ":" + str(op.health)
        if self.respawned:
            netStr += ";" + self.netId + ":respawn"
            self.respawned = False
        if self.left:
            netStr += ";" + self.netId + ":left"
        if self.lost:
            netStr += ";" + self.netId + ":lost"
        self.playersHit.clear()
        netStr += "/"
        return netStr

    # |===== Decode Net String =====|
    def decode_net_str(self, netStr):
        if netStr.startswith("id:"):
            temp = netStr.split("/")
            temp1 = temp[0].split(";")
            n = temp1[0].replace("id:", "")
            try:
                eyex, eyey, eyez = temp1[1].split(',')
            except ValueError:
                # print("ERROR")
                return
            exists = False
            opponent = None
            for op in self.opponents:
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
                print("Player:", opponent.name, "joined :)")
            else:
                op.position = Point(float(eyex), float(eyey), float(eyez))
                op.angle = float(temp1[2])

            if len(temp1) > 3:
                for index, value in enumerate(temp1):
                    if index != 0 and index != 1 and index != 2:
                        k, v = temp1[index].split(":")
                        if k == self.netId:
                            if v != "died":
                                self.health = int(v)
                            else:
                                self.died = True
                        if v == "respawn":
                            for op in self.opponents:
                                if op.name == k:
                                    op.health = 100
                                    op.died = False
                        if v == "left" or v == "lost":
                            print("v:", v)
                            for index, op in enumerate(self.opponents):
                                if op.name == k:
                                    if v == "lost":
                                        print("You successfully killed player:", op.name)
                                        print("You Won!!!")
                                        self.netInterf.closeSock()
                                        exit()
                                    elif v == "left":
                                        print("Player:", op.name, "left :(")
                                    self.opponents.pop(index)

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

    # |===== Respawn Player =====|
    def respawn(self):
        self.lives -= 1
        if self.lives == 0:
            print("You are out of lives and therefore you lost ://")
            self.lost = True
            self.create_net_str()
            self.netInterf.closeSock()
            exit()
        self.health = 100
        self.xzAngle = 0.0
        self.died = False
        randSpawnPoint = self.spawnPoints[random.randint(0, len(self.spawnPoints)-1)].position
        self.view_matrix.look(Point(randSpawnPoint.x, CAMERA_HEIGHT, randSpawnPoint.z), Point(0, 0, 0), Vector(0, 1, 0))
        self.respawned = True

    # |===== UPDATE =====|
    def update(self):
        delta_time = self.clock.tick() / 1000.0

        # /==/ Respawn /==/
        if self.died:
            self.respawn()

        # Movement disabled
        slidePosX = False
        slideNegX = False
        slidePosZ = False
        slideNegZ = False

        # /==/ Update Max Min of AABB /==/
        self.aabb.set_max(
            Vector(0.50 + self.view_matrix.eye.x, 2.15 + self.view_matrix.eye.y, 0.50 + self.view_matrix.eye.z))
        self.aabb.set_min(
            Vector(-0.50 + self.view_matrix.eye.x, 0.01 + self.view_matrix.eye.y, -0.50 + self.view_matrix.eye.z))

        for wall in self.levelWalls:
            data = wall.checkIfCollission(self.aabb.min, self.aabb.max)
            if data[0]:
                if not slidePosX:
                    slidePosX = data[1]
                if not slideNegX:
                    slideNegX = data[2]
                if not slidePosZ:
                    slidePosZ = data[3]
                if not slideNegZ:
                    slideNegZ = data[4]

        for evilObject in self.levelEvilObjects:
            evilObject.update(1 * delta_time)  # Move evil objects back and forth
            if evilObject.checkIfCollission(self.aabb.min, self.aabb.max):  # if collission then player dies
                self.died = True

        # /==/ User Input /==/
        blockedPosArray = [slidePosX, slideNegX, slidePosZ, slideNegZ]
        if W_KEY.isPressed:
            self.view_matrix.move(0, 0, -self.speed * delta_time, blockedPosArray)
        if A_KEY.isPressed:
            self.view_matrix.move(-self.speed * delta_time, 0, 0, blockedPosArray)
        if S_KEY.isPressed:
            self.view_matrix.move(0, 0, self.speed * delta_time, blockedPosArray)
        if D_KEY.isPressed:
            self.view_matrix.move(self.speed * delta_time, 0, 0, blockedPosArray)
        if LSHIFT_KEY.isPressed:
            self.speed = MOVEMENTSPEED * 1.3
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
            self.player.isHit = self.player.aabb.ray_intersects_aabb(self.view_matrix.eye, (self.view_matrix.n * -1))
            for op in self.opponents:
                isHit = op.aabb.ray_intersects_aabb(self.view_matrix.eye, self.view_matrix.n * -1)
                if isHit:
                    op.health -= 10
                    if op.health <= 0:
                        op.died = True
                if op not in self.playersHit:
                    self.playersHit.append(op)
                # if mesh is hit add it to isHit list
            self.fireGun = False

        if self.netInterf.isAvailable:
            if self.check_if_player_moving():
                t1 = time.process_time() - self.t0
                if t1 >= 0.05 or self.left:
                    self.t0 = time.process_time()
                    self.netInterf.send(self.create_net_str())

            recvString = self.netInterf.recv()
            if recvString != "":
                self.decode_net_str(recvString)

    # |===== DISPLAY =====|
    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)

        glClearColor(0.78, 1.0, 1.0, 1.0)

        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.shader.set_eye_position(self.view_matrix.eye)
        self.model_matrix.load_identity()

        light_pos = [(21.0, 1.0, 1.75, 1.0), (-21.0, 1.5, 1.75, 1.0), (0.0, 1.5, 1.75, 1.0)]
        light_dif = [(1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0)]
        light_spe = [(0.8, 0.8, 0.8, 1.0), (0.8, 0.8, 0.8, 1.0), (0.8, 0.8, 0.8, 1.0)]
        light_amb = [(0.05, 0.05, 0.05, 1.0), (0.05, 0.05, 0.05, 1.0), (0.05, 0.05, 0.05, 1.0)]

        self.shader.set_light_pos(light_pos)
        self.shader.set_light_diffuse(light_dif)
        self.shader.set_light_specular(light_spe)
        self.shader.set_light_ambient(light_amb)
        self.shader.set_global_ambient(0.2, 0.2, 0.2)

        # |===== DRAW OBJECTS =====|
        # DRAW GROUND
        for ground in self.levelGround:
            self.shader.set_material_diffuse(ground.color)
            self.shader.set_material_specular(Color(0.1, 0.1, 0.1))
            self.shader.set_material_ambient(Color(0.1, 0.1, 0.1))
            self.shader.set_material_shininess(1.0)
            self.drawObject(self.cube, self.base_texture, ground.translation, ground.scale, ground.rotate)

        # DRAW WALLS
        for wall in self.levelWalls:
            self.shader.set_material_diffuse(wall.color)
            self.shader.set_material_specular(Color(0.1, 0.1, 0.1))
            self.shader.set_material_ambient(Color(0.1, 0.1, 0.1))
            self.shader.set_material_shininess(1.0)
            self.drawObject(self.cube, self.base_texture, wall.translation, wall.scale, wall.rotate)

        # DRAW EVIL OBJECTS
        for evilObject in self.levelEvilObjects:
            self.shader.set_material_diffuse(Color(1.0, 1.0, 1.0))
            self.drawObject(self.cube, self.evil_texture, evilObject.translationCurr, evilObject.scale, evilObject.rotate)

        # /==/ Draw Opponents /==/
        for op in self.opponents:
            # if not op.died:
            op.aabb.set_min(Vector(-0.30 + op.position.x, 0.01 + op.position.y, -0.30 + op.position.z))
            op.aabb.set_max(Vector(0.30 + op.position.x, 2.15 + op.position.y, 0.30 + op.position.z))
            self.drawObject(self.player, self.jeff_texture, op.position, Vector(1.0, 1.0, 1.0), Vector(0.0, 1.5708 + op.angle, 0.0))

        glDisable(GL_DEPTH_TEST)

        # /==/ Draw Health Bar /==/
        glClear(GL_DEPTH_BUFFER_BIT)
        glViewport(10, 10, 50, 200)
        glClearColor(0.78, 1.0, 1.0, 1.0)
        self.shader.set_view_matrix(self.view_matrix2.get_matrix())
        self.shader.set_projection_matrix(self.projection_matrix2.get_matrix())
        self.model_matrix.load_identity()

        self.drawObject(self.cube, self.health_back_texture)
        self.drawObject(self.cube, self.health_texture, Vector(0.0, -1.0 * (1 - self.health/100), 0.0))

        glDisable(GL_DEPTH_TEST)

        # /==/ Draw Crosshair /==/
        glClear(GL_DEPTH_BUFFER_BIT)
        glViewport(720 - 10, 450 - 1, 20, 2)
        glClearColor(0.78, 1.0, 1.0, 1.0)
        self.shader.set_view_matrix(self.view_matrix2.get_matrix())
        self.shader.set_projection_matrix(self.projection_matrix2.get_matrix())
        self.model_matrix.load_identity()

        self.drawObject(self.cube, self.health_texture)

        glDisable(GL_DEPTH_TEST)

        glClear(GL_DEPTH_BUFFER_BIT)
        glViewport(720 - 1, 450 - 10, 2, 20)
        glClearColor(0.78, 1.0, 1.0, 1.0)
        self.shader.set_view_matrix(self.view_matrix2.get_matrix())
        self.shader.set_projection_matrix(self.projection_matrix2.get_matrix())
        self.model_matrix.load_identity()

        self.drawObject(self.cube, self.health_texture)

        glDisable(GL_DEPTH_TEST)

        # /==/ Draw Death Count /==/
        glClear(GL_DEPTH_BUFFER_BIT)
        glViewport(1290, 10, 140, 30)
        glClearColor(0.78, 1.0, 1.0, 1.0)
        self.shader.set_view_matrix(self.view_matrix2.get_matrix())
        self.shader.set_projection_matrix(self.projection_matrix2.get_matrix())
        self.model_matrix.load_identity()

        img = Image.new('RGB', (280, 60), color=(0, 0, 0))
        d = ImageDraw.Draw(img)
        fnt = ImageFont.truetype('/Assets/Fonts/arial.ttf', 40)
        d.text((35, 5), "Lives left: " + str(self.lives), font=fnt, fill=(255, 0, 0))
        img.save("src/assets/meshes/DeathCounter.png")
        deathCounter_texture = self.load_texture("/src/assets/meshes/DeathCounter.png")
        self.drawObject(self.cube, deathCounter_texture, Vector(0.0, 0.0, 0.0), Vector(1.0, 1.0, 1.0), Vector(0.0, 1.57, 0.0))

        glDisable(GL_DEPTH_TEST)

        pygame.display.flip()

    # |===== MAIN PROGRAM FUNCTION =====|
    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    self.left = True
                    self.create_net_str()
                    self.netInterf.closeSock()
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        self.left = True
                        self.create_net_str()
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
                    pygame.mixer.Channel(1).play(self.gunSound)
                else:
                    self.mouseMove = False

            self.update()
            self.display()

        # OUT OF GAME LOOP
        exit()

    # |===== STARTS THE PROGRAM =====|
    def start(self):
        self.program_loop()


if __name__ == "__main__":
    FpsGame().start()