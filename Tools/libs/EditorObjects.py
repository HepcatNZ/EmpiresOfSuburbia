from panda3d.core import Geom, GeomVertexData, GeomVertexFormat, GeomVertexWriter, GeomTriangles, GeomNode, NodePath, LineSegs
from pandac.PandaModules import CollisionTube, CollisionRay, CollisionTraverser, CollisionHandlerEvent,CollisionSphere, CollisionNode, CardMaker, TransparencyAttrib, CollisionPlane


class ObjectsManager:
    def __init__(self):
        print "Object Manager Initialised"

class GameObject:
    def __init__(self):
        self.my_id = None
        self.name = ""
        self.x = 0
        self.y = 0
        self.scale = 1.0
        self.model = None
        self.node_path = None
        self.node_col = None
        self.player = 0
        self.selected = True

    def selection_ring_create(self, segments = 16,size = 1.0):
        ls = LineSegs()
        ls.setThickness(2)
        ls.setColor(0.8,0.8,0.8)

        radians = deg2Rad(360)

        for i in range(segments+1):
            a = radians * i / segments
            y = math.sin(a)*size
            x = math.cos(a)*size

            ls.drawTo(x, y, 0.2)

        node = ls.create()

        return NodePath(node)

    def destroy(self):
        self.node_path.removeNode()

    def hide(self):
        self.node_path.hide()

    def show(self):
        self.node_path.show()

    def set_name(self,name):
        self.name = name

    def get_name(self):
        return self.name

    def set_position(self,x,y):
        self.node_path.setPos(x,y,0)

    def get_position(self):
        return self.node_path.getPos()

    def get_np(self):
        return self.node_path

    def get_id(self):
        return self.my_id

    def get_x(self):
        return (self.node_path.getX())

    def get_y(self):
        return (self.node_path.getY())

    def get_type(self):
        return self.type

    def select(self):
        self.selected = True
        try:
            self.selection_ring.show()
        except:
            print "Error showing"

    def deselect(self):
        self.selected = False
        try:
            self.selection_ring.hide()
        except:
            print "Error hiding"

class PlacementGhost(GameObject):
    def __init__(self,player,type,scale):
        self.type = type
        self.player = player
        self.node_path = NodePath("PlacementGhost")
        self.scale = scale
        self.model_dict = {"army":["../models/infantry_counter_grey.egg","../models/infantry_counter_red.egg","../models/infantry_counter_green.egg"],"tower":["../models/tower_grey.egg","../models/tower_red.egg","../models/tower_green.egg"]}
        self.model = loader.loadModel(self.model_dict[type][player])
        self.model.reparentTo(self.node_path)
        self.node_path.reparentTo(render)
        self.node_path.setScale(self.scale,self.scale,self.scale)
        self.node_path.setColor(1,1,1,0.4)
        self.node_path.setTransparency(True)

    def place(self,type,x,y):
        if self.type == "tower":
            tower = Tower(self.player,base.object_scale,self.node_path.getX(),self.node_path.getY())
            return tower
        if self.type == "army":
            army = Army(self.player,base.object_scale,self.node_path.getX(),self.node_path.getY())
            return army

    def change_player(self,player):
        if base.state == "placement":
            self.model.remove()
            self.player = player
            self.model = loader.loadModel(self.model_dict[self.type][self.player])
            self.model.reparentTo(self.node_path)

    def change_type(self,type):
        if base.state == "placement":
            self.model.remove()
            self.type = type
            self.model = loader.loadModel(self.model_dict[self.type][self.player])
            self.model.reparentTo(self.node_path)

class Tower(GameObject):
    def __init__(self,player,scale,x,y):
        self.my_id = base.tower_count
        base.tower_count += 1
        self.name = "Tower"+str(self.my_id)
        self.player = player
        self.scale = scale
        self.type = "tower"
        self.income = 1.0

        self.node_path = NodePath("tower"+str(self.my_id)+"_node_path")
        self.node_path.setPos(x,y,0)
        self.node_path.setTag("player","p"+str(player))
        self.node_path.setScale(self.scale,self.scale,self.scale)

        self.model_list = ["../models/tower_grey.egg","../models/tower_red.egg","../models/tower_green.egg"]
        self.model = loader.loadModel(self.model_list[player])
        self.model.reparentTo(self.node_path)

        self.node_col = self.node_path.attachNewNode(CollisionNode("tower"+str(self.my_id)+"_c_node"))
        self.node_col.setScale((2,2,1))
        self.node_col.setPos(0,0,0)
        self.node_col.node().addSolid(CollisionSphere(0,0,0,1))
        self.node_col.setTag("type","tower")

        base.cTrav.addCollider(self.node_col,base.col_manager.col_handler)

        self.node_path.reparentTo(render)

        self.selected = False

    def change_player(self,player):
        self.model.remove()
        self.player = player
        self.model = loader.loadModel(self.model_list[player])

class Army(GameObject):
    def __init__(self,player,scale,x,y):
        self.my_id = base.army_count
        base.army_count += 1
        self.name = "Army"+str(self.my_id)
        self.player = player
        self.scale = scale
        self.type = "army"

        self.node_path = NodePath("army"+str(self.my_id)+"_node_path")
        self.node_path.setPos(x,y,0)
        self.node_path.setTag("player","p"+str(player))
        self.node_path.setScale(self.scale,self.scale,self.scale)

        self.model_list = ["../models/infantry_counter_grey.egg","../models/infantry_counter_red.egg","../models/infantry_counter_green.egg"]
        self.model = loader.loadModel(self.model_list[player])
        self.model.reparentTo(self.node_path)

        self.node_col = self.node_path.attachNewNode(CollisionNode("tower"+str(self.my_id)+"_c_node"))
        self.node_col.setScale((2,2,1))
        self.node_col.setPos(0,0,0)
        self.node_col.node().addSolid(CollisionSphere(0,0,0,1))
        self.node_col.setTag("type","army")

        base.cTrav.addCollider(self.node_col,base.col_manager.col_handler)

        self.node_path.reparentTo(render)

        self.selected = False

    def change_player(self,player):
        self.model.remove()
        self.player = player
        self.model = loader.loadModel(self.model_list[player])