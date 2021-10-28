# https://inareous.github.io/posts/opening-obj-using-py
# https://en.wikipedia.org/wiki/Wavefront_.obj_file
from OpenGL.GL import *
from src.essentials.mesh import Mesh
from src.essentials.color import Color

class MeshLoader:
    def __init__(self):
        self.mtllib = ""
        self.o = ""
        self.usemtl = ""
        self.vTemp = []
        self.vtTemp = []
        self.vnTemp = []
        self.v = []
        self.vt = []
        self.vn = []
        self.f = []
        self.mesh = Mesh()
        self.meshv = []
        self.meshvt = []
        self.meshvn = []
        self.newmtl = ""
        self.shininess = 0.0
        self.ambiance = Color(0, 0, 0)
        self.diffuse = Color(0, 0, 0)
        self.specular = Color(0, 0, 0)
        self.transparency = 0.0
        self.textureFile = ""

    def obj_parser(self, line):
        temp = line.strip("\n").split(" ")
        # Name of mtl file
        if temp[0] == "mtllib":
            self.mtllib = temp[1]
        # Name of object
        elif temp[0] == "o":
            if temp[1] != self.o:
                self.meshv = []
                self.meshvt = []
                self.meshvn = []
                self.o = temp[1]
        # Which material to use
        elif temp[0] == "usemtl":
            if temp[1] != self.usemtl:
                self.usemtl = temp[1]
        elif temp[0] == "v":
            self.vTemp.append([float(temp[1]), float(temp[2]), float(temp[3])])
        elif temp[0] == "vt":
            self.vtTemp.append([float(temp[1]), float(temp[2])])
        elif temp[0] == "vn":
            self.vnTemp.append([float(temp[1]), float(temp[2]), float(temp[3])])
        elif temp[0] == "f":
            for index, value in enumerate(temp):
                if index != 0:
                    vid, tid, nid = value.split("/")
                    vid = int(vid)-1
                    tid = int(tid)-1
                    nid = int(nid)-1
                    # Append v
                    # [[x, y, z], [x, y, z],...]
                    # res: [x, y, z, x, y, z,...]
                    self.v.append(self.vTemp[vid][0])
                    self.v.append(self.vTemp[vid][1])
                    self.v.append(self.vTemp[vid][2])

                    self.meshv.append(self.vTemp[vid][0])
                    self.meshv.append(self.vTemp[vid][1])
                    self.meshv.append(self.vTemp[vid][2])
                    # Append vt
                    # [[x, y], [x, y],...]
                    # res: [x, y, x, y, x, y,...]
                    self.vt.append(self.vtTemp[tid][0])
                    self.vt.append(self.vtTemp[tid][1])

                    self.meshvt.append(self.vtTemp[tid][0])
                    self.meshvt.append(self.vtTemp[tid][1])
                    # Append vn
                    # [[x, y, z], [x, y, z],...]
                    # res: [x, y, z, x, y, z,...]
                    self.vn.append(self.vnTemp[nid][0])
                    self.vn.append(self.vnTemp[nid][1])
                    self.vn.append(self.vnTemp[nid][2])

                    self.meshvn.append(self.vnTemp[nid][0])
                    self.meshvn.append(self.vnTemp[nid][1])
                    self.meshvn.append(self.vnTemp[nid][2])

            self.mesh.add_vertex(self.o, self.meshv)
            self.mesh.add_texture(self.o, self.meshvt)
            self.mesh.add_normal(self.o, self.meshvn)
            self.mesh.add_objectMaterial(self.o, self.usemtl)

    def mtl_parser(self, line):
        temp = line.strip("\n").split(" ")
        # check if newmtl   name of material
        if temp[0] == "newmtl":
            if temp[1] != self.newmtl:
                self.newmtl = temp[1]
        # check if Ns       "shininess"
        elif temp[0] == "Ns":
            self.shininess = float(temp[1])
        # check if Ka       "ambience"
        elif temp[0] == "Ka":
            self.ambiance = Color(float(temp[1]), float(temp[2]), float(temp[3]))
        # check if Kd       "diffuse"
        elif temp[0] == "Kd":
            self.diffuse = Color(float(temp[1]), float(temp[2]), float(temp[3]))
        # check if Ks    "specular"  black (off) <==> Ks 0.000 0.000 0.000 |==| ranges between 0 and 1000 <==> Ns 10.000
        elif temp[0] == "Ks":
            self.specular = Color(float(temp[1]), float(temp[2]), float(temp[3]))
        # check if Ke       Dunno what the fuck this is
        # check if Ni       Honestly can ignore this part
        # check if d        "transparency" or "dissolved"
        elif temp[0] == "d":
            self.transparency = float(temp[1])
        # check if illum    I think we can ignore this too
        # check if map_Kd   name of texture file
        elif temp[0] == "map_Kd":
            self.textureFile = temp[1]

    def loadMtl(self, fName):
        with open(fName, "r") as file:
            for line in file:
                self.mtl_parser(line)
        self.mesh.add_material(self.newmtl, self.shininess, self.ambiance, self.diffuse,
                               self.specular, self.transparency, self.textureFile)

    def loadObj(self, fName):
        with open(fName, "r") as file:
            for line in file:
                self.obj_parser(line)
        self.mesh.set_opengl_buffers()

        print("VERTEX ARRAYS: ", self.mesh.vertexArrays)
        print("TEXTURE ARRAYS: ", self.mesh.textureArrays)
        print("NORMAL ARRAYS: ", self.mesh.normalArrays)
        print("OBJECT MATERIALS: ", self.mesh.objectMaterials)
        print("MATERIALS: ", self.mesh.materials)

