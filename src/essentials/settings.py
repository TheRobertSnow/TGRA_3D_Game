import math
import pygame
from dataclasses import dataclass

from math import pi

# |===== DISPLAY =====|
DISPLAY_WIDTH = 1440
DISPLAY_HEIGHT = 900
FOV = math.pi/2

# |===== INPUT =====|
MOUSE_SENSE = 4

@dataclass
class W_KEY:
    key: int = pygame.K_w
    isPressed: bool = False

@dataclass
class A_KEY:
    key: int = pygame.K_a
    isPressed: bool = False

@dataclass
class S_KEY:
    key: int = pygame.K_s
    isPressed: bool = False

@dataclass
class D_KEY:
    key: int = pygame.K_d
    isPressed: bool = False

@dataclass
class LSHIFT_KEY:
    key: int = pygame.K_LSHIFT
    isPressed: bool = False

# |===== PLAYER MOVEMENT =====|
MOVEMENTSPEED = 2

# |===== SCENES =====|
LEVEL_1 = "level1.json"
COLLISION_TEST = "collisionTest.json"

# |===== FILES =====|
COMPLEX_3D_VERT = "/src/shaders/vert/complex3D.vert"
COMPLEX_3D_FRAG = "/src/shaders/frag/complex3D.frag"

# |===== NETWORK =====|
EXTERNAL_IP = "157.97.11.131"
PORT = 6969   # Nice

# |===== RUN MODES =====|
EDIT_MODE = "edit"
GAMER_MODE = "gamer"
MODES = [EDIT_MODE, GAMER_MODE]