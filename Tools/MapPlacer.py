from panda3d.core import NodePath
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from libs import EditorCam, EditorDrawer, EditorCol, EditorVis, EditorInterface, EditorMenus, EditorXML
#from libs import TimObjects,TimCol,TimVisuals,TimNetwork,TimXML,TimMenus,TimEconomy
import random
import Image

class MapPlacement(ShowBase):
    def __init__(self,editor):
        ShowBase.__init__(self)
        base.disableMouse()

        wp = WindowProperties()
        wp.setFullscreen(True)

        self.win_width = 1920.0
        self.win_height = 1080.0
        #self.win_width = 1366
        #self.win_height = 768
        self.screen_width = self.win_width/self.win_height
        wp.setSize(int(self.win_width), int(self.win_height))
        base.win.requestProperties(wp)

        self.txt_instructions = OnscreenText(text="",fg=(1,1,0,1),pos=(-base.screen_width+0.05,0.9),scale=0.08,align=TextNode.ALeft)

        self.cam = EditorCam.Camera()
        self.game_vars()

        self.state = "menus"

        self.menu_manager = EditorMenus.MenuManager()
        self.menu_manager.menu_goto(self.menu_manager.menu_map_create)
        self.xml_manager = EditorXML.XMLManager()

    def start_map(self):

        self.details_box = EditorVis.DetailsBox()
        self.details_box.hide()

        self.draw_manager = EditorDrawer.Map(self.map_width,self.map_height,self.map_texture,base.map_scale)#editor.map_width,editor.map_height,editor.image,1.0)
        self.col_manager = EditorCol.CollisionManager()

        self.change_state("placement")

    def game_vars(self):
        self.object_scale = 10.0
        self.tower_count = 0
        self.army_count = 0

        self.towers = []
        self.armies = []

    def get_obj_from_node(self,node):
        for t in base.towers:
            if t.get_np() == node:
                return t
        for a in base.armies:
            if a.get_np() == node:
                return a

    def set_instructions(self,text):
        self.txt_instructions.setText(text)

    def change_state(self,new_state):
        old_state = self.state
        if old_state == "placement":
            self.col_manager.placement_ghost.hide()
        elif old_state == "modifying":
            self.details_box.hide()
        elif old_state == "moving":
            self.txt_instructions.setText(self.details_box.last_text)

        if new_state == "placement":
            self.state = "placement"
            self.txt_instructions.setText("<Left Click> Place Objects\n<Right Click> Selection Mode\n<A>rmy\n<T>ower\n<0> <1> <2> Select Faction\n<Ctrl+S> Save Map")
            self.cam.enable()
            self.col_manager.placement_ghost.show()
        elif new_state == "modifying":
            self.state = "modifying"
            self.cam.disable()
            self.details_box.show()
        elif new_state == "moving":
            self.state = "moving"
            self.cam.enable()
        elif new_state == "selecting":
            self.state = "selecting"
            self.txt_instructions.setText("<Left Click> Select Objects\n<Right Click> Placement Mode\n<Ctrl+S> Save Map")
            self.cam.enable()

app = MapPlacement(-1)
app.run()
