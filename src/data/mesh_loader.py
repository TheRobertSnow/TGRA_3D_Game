#TODO: Create a mesh loader to load .obj files  https://inareous.github.io/posts/opening-obj-using-py
from OpenGL.GL import *
class MeshLoader:
    def __init__(self, filename):
        self.v = []
        self.vt = []
        self.vn = []
        self.f = []
        self.filename = filename
        #
        self.readFromFile()

    def lineParser(self, line):
        temp = line.strip("\n").split(" ")
        if temp[0] == "v":
            self.v.append([float(temp[1]), float(temp[2]), float(temp[3])])
        elif temp[0] == "vt":
            self.vt.append([float(temp[1]), float(temp[2])])
        elif temp[0] == "vn":
            self.vn.append([float(temp[1]), float(temp[2]), float(temp[3])])
        elif temp[0] == "f":
            temp1 = []
            for index, value in enumerate(temp):
                if index != 0:
                    vid, tid, nid = value.split("/")
                    temp1.append([int(vid), int(tid), int(nid)])
            self.f.append(temp1)


    def readFromFile(self):
        with open(self.filename, "r") as file:
            for line in file:
                self.lineParser(line)





"""
class MeshLoader:
    def __init__( self, default_mtl='default_mtl' ):
        self.path      = None               # path of loaded object
        self.mtllibs   = []                 # .mtl files references via mtllib
        self.mtls      = [ default_mtl ]    # materials referenced
        self.mtlid     = []                 # indices into self.mtls for each polygon
        self.vertices  = []                 # vertices as an Nx3 or Nx6 array (per vtx colors)
        self.normals   = []                 # normals
        self.texcoords = []                 # texture coordinates
        self.polygons  = []                 # M*Nv*3 array, Nv=# of vertices, stored as vid,tid,nid (-1 for N/A)

def load_obj( filename: str, default_mtl='default_mtl', triangulate=False ) -> MeshLoader:
    # parses a vertex record as either vid, vid/tid, vid//nid or vid/tid/nid
    # and returns a 3-tuple where unparsed values are replaced with -1
    def parse_vertex( vstr ):
        vals = vstr.split('/')
        vid = int(vals[0])-1
        tid = int(vals[1])-1 if len(vals) > 1 and vals[1] else -1
        nid = int(vals[2])-1 if len(vals) > 2 else -1
        return (vid,tid,nid)

    with open( filename, 'r' ) as objf:
        obj = MeshLoader(default_mtl=default_mtl)
        obj.path = filename
        cur_mat = obj.mtls.index(default_mtl)
        for line in objf:
            print(line)
            toks = line.split()
            if not toks:
                continue
            if toks[0] == 'v':
                obj.vertices.append( [ float(v) for v in toks[1:]] )
            elif toks[0] == 'vn':
                obj.normals.append( [ float(v) for v in toks[1:]] )
            elif toks[0] == 'vt':
                obj.texcoords.append( [ float(v) for v in toks[1:]] )
            elif toks[0] == 'f':
                poly = [ parse_vertex(vstr) for vstr in toks[1:] ]
                if triangulate:
                    for i in range(2,len(poly)):
                        obj.mtlid.append( cur_mat )
                        obj.polygons.append( (poly[0], poly[i-1], poly[i] ) )
                else:
                    obj.mtlid.append(cur_mat)
                    obj.polygons.append( poly )
            elif toks[0] == 'mtllib':
                obj.mtllibs.append( toks[1] )
            elif toks[0] == 'usemtl':
                if toks[1] not in obj.mtls:
                    obj.mtls.append(toks[1])
                cur_mat = obj.mtls.index( toks[1] )
        return obj
"""