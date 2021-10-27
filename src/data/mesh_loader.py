# https://inareous.github.io/posts/opening-obj-using-py
# https://en.wikipedia.org/wiki/Wavefront_.obj_file
from OpenGL.GL import *
from src.essentials.mesh import Mesh

class MeshLoader:
    def __init__(self):
        self.vTemp =[]
        self.vtTemp = []
        self.vnTemp = []
        self.v = []
        self.vt = []
        self.vn = []
        self.f = []

    def obj_parser(self, line):
        temp = line.strip("\n").split(" ")
        # Name of mtl file
        if temp[0] == "mtllib":
            # TODO: Implement
            pass
        # Name of object
        elif temp[0] == "o":
            # TODO: Implement
            pass
        # Which material to use
        elif temp[0] == "usemtl":
            # TODO: Implement
            pass
        elif temp[0] == "v":
            self.vTemp.append([float(temp[1]), float(temp[2]), float(temp[3])])
            # self._vTemp.append(float(temp[1]))
            # self._vTemp.append(float(temp[2]))
            # self._vTemp.append(float(temp[3]))
        elif temp[0] == "vt":
            self.vtTemp.append([float(temp[1]), float(temp[2])])
        elif temp[0] == "vn":
            self.vnTemp.append([float(temp[1]), float(temp[2]), float(temp[3])])
            # self.vn.append(float(temp[1]))
            # self.vn.append(float(temp[2]))
            # self.vn.append(float(temp[3]))
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
                    # Append vt
                    # [[x, y], [x, y],...]
                    # res: [x, y, x, y, x, y,...]
                    self.vt.append(self.vtTemp[tid][0])
                    self.vt.append(self.vtTemp[tid][1])
                    # Append vn
                    # [[x, y, z], [x, y, z],...]
                    # res: [x, y, z, x, y, z,...]
                    self.vn.append(self.vnTemp[nid][0])
                    self.vn.append(self.vnTemp[nid][1])
                    self.vn.append(self.vnTemp[nid][2])

    def mtl_parser(self, line):
        temp = line.strip("\n").split(" ")
        # check if newmtl   name of material
        if temp[0] == "newmtl":
            # TODO: Implement
            pass
        # check if Ns       "shininess"
        elif temp[0] == "Ns":
            # TODO: Implement
            pass
        # check if Ka       "ambience"
        elif temp[0] == "Ka":
            # TODO: Implement
            pass
        # check if Kd       "diffuse"
        elif temp[0] == "Kd":
            # TODO: Implement
            pass
        # check if Ks    "specular"  black (off) <==> Ks 0.000 0.000 0.000 |==| ranges between 0 and 1000 <==> Ns 10.000
        elif temp[0] == "Ks":
            # TODO: Implement
            pass
        # check if Ke       Dunno what the fuck this is
        # check if Ni       Honestly can ignore this part
        # check if d        "transparency" or "dissolved"
        elif temp[0] == "d":
            # OPTIONAL TODO: Implement
            pass
        # check if illum    I think we can ignore this too
        # check if map_Kd   name of texture file
        elif temp[0] == "map_Kd":
            # TODO: Implement
            pass

    def loadMtl(self, fName):
        # TODO: Fine, I'll do it myself
        with open(fName, "r") as file:
            for line in file:
                self.mtl_parser(line)

    def laodObj(self, fName):
        with open(fName, "r") as file:
            for line in file:
                self.obj_parser(line)
