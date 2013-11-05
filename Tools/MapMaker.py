from panda3d.core import NodePath
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from libs import EditorCam, EditorDrawer, EditorCol, EditorVis, EditorInterface
#from libs import TimObjects,TimCol,TimVisuals,TimNetwork,TimXML,TimMenus,TimEconomy
import random
import Image

import pygtk
import gtk
import gtk.glade

class MapEditor:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("EditorUI.glade")

        self.window = self.builder.get_object("window")
        self.window.connect("destroy", lambda w: gtk.main_quit())
        self.window.show()

        self.import_widgets(self.builder)

    def import_widgets(self,builder):
        self.map = ""
        self.image = ""

        self.towers = {}
        self.armies = {}

        #MAIN PAGE
        self.btn_map_load = builder.get_object("btn_map_load")
        self.ent_map_name = builder.get_object("ent_map_name")
        self.btn_image_load = builder.get_object("btn_map_image")
        self.btn_image_load.connect("clicked",self.load_image)
        self.adj_map_width = builder.get_object("adj_map_width")
        self.adj_map_height = builder.get_object("adj_map_height")
        self.img_map = builder.get_object("img_map")
        self.btn_place_things = builder.get_object("btn_place_things")
        self.btn_place_things.connect("clicked",self.open_p3d)

        #FACTIONS PAGE
        self.ent_faction0 = builder.get_object("ent_faction0")
        self.ent_faction1 = builder.get_object("ent_faction1")
        self.ent_faction2 = builder.get_object("ent_faction2")
        self.ent_faction0.connect("changed",self.set_factions)
        self.ent_faction1.connect("changed",self.set_factions)
        self.ent_faction2.connect("changed",self.set_factions)

        #TOWERS PAGE
        self.tv_towers = builder.get_object("tv_towers")
        self.ls_towers = builder.get_object("lst_towers")
        self.ent_tower_name = builder.get_object("ent_tower_name")
        self.adj_tower_income = builder.get_object("adj_tower_income")
        self.cmb_tower_faction = builder.get_object("cmb_tower_faction")
        self.lbl_tower_pos = builder.get_object("lbl_tower_pos")
        self.btn_tower_del = builder.get_object("btn_tower_del")

        #ARMIES PAGE
        self.tv_armies = builder.get_object("tv_armies")
        self.ls_armies = builder.get_object("lst_armies")
        self.ent_army_name = builder.get_object("ent_army_name")
        self.cmb_army_faction = builder.get_object("cmb_army_faction")
        self.lbl_army_pos = builder.get_object("lbl_army_pos")
        self.btn_army_del = builder.get_object("btn_army_del")

        #FINAL PAGE
        self.btn_map_save = builder.get_object("btn_map_save")

        #LOAD IMAGE
        self.load_image_box = builder.get_object("file_image_load")
        self.btn_image_open = builder.get_object("btn_image_open")
        self.btn_image_open.connect("clicked",self.load_image_open)
        self.btn_image_cancel = builder.get_object("btn_image_open")
        self.btn_image_cancel.connect("clicked",self.load_image_cancel)

    def set_factions(self,widget):
        self.faction0 = self.ent_faction0.get_text()
        self.faction1 = self.ent_faction1.get_text()
        self.faction2 = self.ent_faction2.get_text()

    def load_image(self,widget):
        self.window.hide()
        self.load_image_box.show()

    def load_image_cancel(self,widget):
        self.load_image_box.hide()
        self.window.show()

    def load_image_open(self,widget):
        self.load_image_box.hide()
        self.window.show()
        self.image = str(self.load_image_box.get_filename())
        im = Image.open(self.image)
        self.pix = im.load()
        img_width,img_height = im.size
        print "LOAD IMAGE:",self.image
        self.img_map.set_size_request(img_width,img_height)
        self.img_map.set_from_file()

    def open_p3d(self,widget):
        self.map_width = self.adj_map_width.get_value()
        self.map_height = self.adj_map_height.get_value()
        self.image = "images/rotorua.jpg"
        if self.image != "":
            app = MapPlacement(self)
            app.run()

class MapPlacement(ShowBase):
    def __init__(self,editor):
        ShowBase.__init__(self)
        base.disableMouse()

        wp = WindowProperties()
        #wp.setFullscreen(True)

        self.interfacer = EditorInterface.Interfacer(editor,self)

        self.win_width = 1920.0
        self.win_height = 1080.0
        #self.win_width = 1366
        #self.win_height = 768
        self.screen_width = self.win_width/self.win_height
        #wp.setSize(self.win_width, self.win_height)
        base.win.requestProperties(wp)

        self.cam = EditorCam.Camera()
        self.game_vars()

        self.state = "placement"

        self.details_box = EditorVis.DetailsBox()
        self.details_box.hide()

        self.draw_manager = EditorDrawer.Map(2048,1024,"images/rotorua.jpg",1)#editor.map_width,editor.map_height,editor.image,1.0)
        self.col_manager = EditorCol.CollisionManager()

    def game_vars(self):
        self.object_scale = 10.0
        self.tower_count = 0

        self.towers = []
        self.armies = []

    def change_state(self,new_state):
        old_state = self.state
        if old_state == "placement":
            self.col_manager.placement_ghost.hide()
        elif old_state == "modifying":
            self.details_box.hide()

        if new_state == "placement":
            self.state = "placement"
            self.cam.enable()
            self.col_manager.placement_ghost.show()
        elif new_state == "modifying":
            self.state = "modifying"
            self.cam.disable()
            self.details_box.show()
        elif new_state == "moving":
            self.state = "moving"
            self.cam.enable()

#app = MapPlacement(-1)
#app.run()

if __name__ == "__main__":
    app = MapEditor()
    gtk.main()