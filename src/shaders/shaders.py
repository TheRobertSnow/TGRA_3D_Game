from OpenGL.GL import *
from OpenGL.GLU import *
from math import *  # trigonometry

import sys

from src.essentials.base_3d_objects import *
from src.essentials.color import Color
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

        #self.uvLoc = glGetAttribLocation(self.renderingProgramID, "a_uv")
        #glEnableVertexAttribArray(self.uvLoc)

        self.modelMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.viewMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")

        # self.colorLoc                         = glGetUniformLocation(self.renderingProgramID, "u_color")
        self.eyePositionLoc = glGetUniformLocation(self.renderingProgramID, "u_eye_position")

        #self.diffuseTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_tex01")
        #self.specularTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_tex02")
        #self.ambientTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_tex03")

        #self.usingTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_using_texture")

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

    #def set_uv_attribute(self, vertex_array):
        #print(vertex_array)
        #glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 0, vertex_array)


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

    def set_material_diffuse(self, diffuse: Color):
        glUniform4f(self.materialDiffuseLoc, diffuse.red, diffuse.green, diffuse.blue, 1.0)

    def set_material_specular(self, specular: Color):
        glUniform4f(self.materialSpecularLoc, specular.red, specular.green, specular.blue, 1.0)

    def set_material_ambient(self, ambient: Color):
        glUniform4f(self.materialAmbientLoc, ambient.red, ambient.green, ambient.blue, 1.0)

    def set_material_shininess(self, shine):
        glUniform1f(self.materialShininessLoc, shine)

    # UV TEXTURES
    def set_attribute_buffers_with_uv(self, vertexBufferId):
        glUniform1f(self.usingTextureLoc, 1.0)
        glBindBuffer(GL_ARRAY_BUFFER, vertexBufferId)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat),
                              OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 8 * sizeof(GLfloat),
                              OpenGL.GLU.ctypes.c_void_p(6 * sizeof(GLfloat)))