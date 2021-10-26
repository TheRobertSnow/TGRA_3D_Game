from OpenGL.GL import *
from math import *  # trigonometry

import sys

from src.essentials.base_3d_objects import *
from src.essentials.settings import COMPLEX_3D_VERT, COMPLEX_3D_FRAG


class Shader3D:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + COMPLEX_3D_VERT)
        glShaderSource(vert_shader, shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if (result != 1):  # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + COMPLEX_3D_FRAG)
        glShaderSource(frag_shader, shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if (result != 1):  # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        self.positionLoc = glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)

        self.normalLoc = glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)

        self.modelMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.viewMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")

        # self.colorLoc                         = glGetUniformLocation(self.renderingProgramID, "u_color")
        self.eyePositionLoc = glGetUniformLocation(self.renderingProgramID, "u_eye_position")

        self.globalAmbientLoc = glGetUniformLocation(self.renderingProgramID, "u_global_ambient")
        self.lightPositionLoc = glGetUniformLocation(self.renderingProgramID, "u_light_position")
        self.lightDiffuseLoc = glGetUniformLocation(self.renderingProgramID, "u_light_diffuse")
        self.lightSpecularLoc = glGetUniformLocation(self.renderingProgramID, "u_light_specular")
        self.lightAmbientLoc = glGetUniformLocation(self.renderingProgramID, "u_light_ambient")

        self.materialDiffuseLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_diffuse")
        self.materialSpecularLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_specular")
        self.materialShininessLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_shininess")
        self.materialAmbientLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_ambient")

    def use(self):
        try:
            glUseProgram(self.renderingProgramID)
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    # def set_solid_color(self, red, green, blue):
    #     glUniform4f(self.colorLoc, red, green, blue, 1.0)

    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_normal_attribute(self, vertex_array):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, vertex_array)


    # MULTIPLE LIGHTS
    def set_eye_position(self, pos):
        glUniform4f(self.eyePositionLoc, pos.x, pos.y, pos.z, 1.0)

    def set_global_ambient(self, red, green, blue):
        glUniform4f(self.globalAmbientLoc, red, green, blue, 1.0)

    def set_light_pos(self, pos):
        glUniform4fv(self.lightPositionLoc, len(pos), pos)

    def set_light_diffuse(self, diffuse):
        glUniform4fv(self.lightDiffuseLoc, len(diffuse), diffuse)

    def set_light_specular(self, specular):
        glUniform4fv(self.lightSpecularLoc, len(specular), specular)

    def set_light_ambient(self, ambient):
        glUniform4fv(self.lightAmbientLoc, len(ambient), ambient)

    def set_material_diffuse(self, red, green, blue):
        glUniform4f(self.materialDiffuseLoc, red, green, blue, 1.0)

    def set_material_specualar(self, red, green, blue):
        glUniform4f(self.materialSpecularLoc, red, green, blue, 1.0)

    def set_material_ambient(self, red, green, blue):
        glUniform4f(self.materialAmbientLoc, red, green, blue, 1.0)

    def set_material_shininess(self, shine):
        glUniform1f(self.materialShininessLoc, shine)