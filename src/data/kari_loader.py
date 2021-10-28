from src.essentials.kari_mesh import MeshModel
from src.essentials.material import Material
from src.essentials.color import Color
from src.essentials.point import *
from src.essentials.vector import *

def load_mtl_file(file_location, file_name, mesh_model):
    mtl = None
    fin = open(file_location + "/" + file_name)
    for line in fin.readlines():
        tokens = line.split()
        if len(tokens) == 0:
            continue
        if tokens[0] == "newmtl":
            mtl = Material()
            mesh_model.add_material(tokens[1], mtl)
        elif tokens[0] == "Ka":
            mtl.ambient = Color(float(tokens[1]), float(tokens[2]), float(tokens[3]))
        elif tokens[0] == "Kd":
            mtl.diffuse = Color(float(tokens[1]), float(tokens[2]), float(tokens[3]))
        elif tokens[0] == "Ks":
            mtl.specular = Color(float(tokens[1]), float(tokens[2]), float(tokens[3]))
        elif tokens[0] == "Ns":
            mtl.shininess = float(tokens[1])

def load_obj_file(file_location, file_name):
    mesh_model = MeshModel()
    current_object_id = None
    current_position_list = []
    current_normal_list = []
    current_uv_list = []
    fin = open(file_location + "/" + file_name)
    for line in fin.readlines():
        tokens = line.split()
        if len(tokens) == 0:
            continue
        if tokens[0] == "mtllib":
            # load the next token as material
            load_mtl_file(file_location, tokens[1], mesh_model)
        elif tokens[0] == "o":
            # we are starting a new object
            current_object_id = tokens[1]
        elif tokens[0] == "v":
            current_position_list.append(Point(float(tokens[1]), float(tokens[2]), float(tokens[3])))
        elif tokens[0] == "vn":
            current_normal_list.append(Vector(float(tokens[1]), float(tokens[2]), float(tokens[3])))
        elif tokens[0] == "vt":
            current_uv_list.append(Point(float(tokens[1]), float(tokens[2]), 0.0))
        elif tokens[0] == "usemtl":
            mesh_model.set_mesh_material(current_object_id, tokens[1])
        elif tokens[0] == "f":
            for i in range(1, len(tokens)):
                tokens[i] = tokens[i].split("/") # Get
                # print("Tokens: ", tokens[i])
                # print("len tokens: ", len(tokens))
            vertex_count = len(tokens) - 1
            for i in range(vertex_count - 2):
                if current_position_list == None:
                    current_position_list = []
                if current_normal_list == None:
                    current_normal_list = []
                if current_uv_list == None:
                    current_uv_list = []
                mesh_model.add_vertex(current_object_id, current_position_list[int(tokens[1][0])-1], current_normal_list[int(tokens[1][2])-1], current_uv_list[int(tokens[1][1])-1])
                mesh_model.add_vertex(current_object_id, current_position_list[int(tokens[i+2][0])-1], current_normal_list[int(tokens[i+2][2])-1], current_uv_list[int(tokens[i+2][1])-1])
                mesh_model.add_vertex(current_object_id, current_position_list[int(tokens[i+3][0])-1], current_normal_list[int(tokens[i+3][2])-1], current_uv_list[int(tokens[i+3][1])-1])
    # All models, vertices, and materials have been added to mesh_model, so set buffers
    mesh_model.set_opengl_buffers()
    return mesh_model