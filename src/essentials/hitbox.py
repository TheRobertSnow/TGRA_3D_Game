# https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_collision_detection
from src.essentials.settings import GAMER_MODE, EDIT_MODE
class Hitbox:
    def __init__(self, mode):
        # Set the visi
        if mode == GAMER_MODE:
            self.visibility = False
        elif mode == EDIT_MODE:
            self.visibility = True
        else:
            self.visibility = False

    def is_point_inside_aabb(self):
        pass

    def aabb_intersects_aabb(self):
        pass

    def is_point_inside_sphere(self):
        pass

    def sphere_intersects_sphere(self):
        pass

    def sphere_intersects_aabb(self):
        pass