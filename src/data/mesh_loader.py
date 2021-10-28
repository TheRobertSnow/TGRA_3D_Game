# https://inareous.github.io/posts/opening-obj-using-py
# https://en.wikipedia.org/wiki/Wavefront_.obj_file
from OpenGL.GL import *
from src.essentials.mesh import Mesh
from src.essentials.color import Color
from src.essentials.point import *
from src.essentials.vector import *

def mtl_parser(fileName, name, mesh):
    newmtl = None
    shininess = 0.0
    ambiance = Color(0, 0, 0)
    diffuse = Color(0, 0, 0)
    specular = Color(0, 0, 0)
    transparency = 0.0
    textureFile = ""
    with open(fileName, "r") as file:
        for line in file:
            temp = line.strip("\n").split(" ")
            # check if newmtl   name of material
            if temp[0] == "newmtl":
                if temp[1] != newmtl:
                    newmtl = name
            # check if Ns       "shininess"
            elif temp[0] == "Ns":
                shininess = float(temp[1])
            # check if Ka       "ambience"
            elif temp[0] == "Ka":
                ambiance = Color(float(temp[1]), float(temp[2]), float(temp[3]))
            # check if Kd       "diffuse"
            elif temp[0] == "Kd":
                diffuse = Color(float(temp[1]), float(temp[2]), float(temp[3]))
            # check if Ks    "specular"  black (off) <==> Ks 0.000 0.000 0.000 |==| ranges between 0 and 1000 <==> Ns 10.000
            elif temp[0] == "Ks":
                specular = Color(float(temp[1]), float(temp[2]), float(temp[3]))
            # check if Ke       Dunno what the fuck this is
            # check if Ni       Honestly can ignore this part
            # check if d        "transparency" or "dissolved"
            elif temp[0] == "d":
                transparency = float(temp[1])
            # check if illum    I think we can ignore this too
            # check if map_Kd   name of texture file
            elif temp[0] == "map_Kd":
                textureFile = temp[1]
    mesh.add_material(newmtl, shininess, ambiance, diffuse, specular, transparency, textureFile)

def obj_parser(fLoc, fName):
    mesh = Mesh()
    v = []
    vt = []
    vn = []
    o = ""
    #usemtl = ""
    with open(fLoc + "/" + fName, "r") as file:
        for line in file:
            temp = line.strip("\n").split(" ")
            # Name of mtl file
            if temp[0] == "mtllib":
                mesh.materialFile = temp[1]
                mtl_parser(fLoc + "/" + temp[1], temp[1], mesh)
            # Name of object
            elif temp[0] == "o":
                if temp[1] != o:
                    o = temp[1]
            # Which material to use
            elif temp[0] == "usemtl":
                #if temp[1] != usemtl:
                    #usemtl = temp[1]
                mesh.add_objectMaterial(o, temp[1])
            elif temp[0] == "v":
                v.append(Point(float(temp[1]), float(temp[2]), float(temp[3])))
            elif temp[0] == "vt":
                vt.append(Vector(float(temp[1]), float(temp[2]), 0.0))
            elif temp[0] == "vn":
                vn.append(Vector(float(temp[1]), float(temp[2]), float(temp[3])))
            elif temp[0] == "f":
                for i in range(1, len(temp)):
                    temp[i] = temp[i].split("/")
                vertex_count = len(temp) - 1
                for i in range(vertex_count - 2):
                    if v == None:
                        v = []
                    if vn == None:
                        vn = []
                    if vt == None:
                        vt = []
                    mesh.add_vertex(o, v[int(temp[1][0]) - 1], vn[int(temp[1][2]) - 1], vt[int(temp[1][1]) - 1])
                    mesh.add_vertex(o, v[int(temp[i + 2][0]) - 1], vn[int(temp[i + 2][2]) - 1], vt[int(temp[i + 2][1]) - 1])
                    mesh.add_vertex(o, v[int(temp[i + 3][0]) - 1], vn[int(temp[i + 3][2]) - 1], vt[int(temp[i + 3][1]) - 1])
            mesh.set_opengl_buffers()
    return mesh

def loadObj(fLoc, fName):
    return obj_parser(fLoc, fName)
