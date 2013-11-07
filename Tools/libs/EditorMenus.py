from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import TransparencyAttrib, NodePath, TextNode
from direct.interval.IntervalGlobal import *
from direct.showbase.ShowBase import Point3
from direct.gui.DirectGui import *
from direct.gui.DirectGuiBase import *
from panda3d.core import Vec3
import sys, os
import Image

class MenuManager:
    def __init__(self):
        print "Menu Manager Initialised"
        self.menu = None

        self.menu_map_create = MenuMapCreate()
        self.menu_factions = MenuFactions()
        self.menu_factions.hide()
        self.menu_map_create.hide()

    def menu_goto(self,menu):
        menu.show()
        if self.menu != None:
            self.menu.hide()
        self.menu = menu

class MenuBase:
    def hide(self):
        for i in self.items:
            i.hide()

    def show(self):
        for i in self.items:
            i.show()

class MenuMapCreate(MenuBase):
    def __init__(self):
        self.create_components()

    def create_components(self):
        self.items = []
        self.items.append(OnscreenText(text="Map Name:",fg=(1,1,1,1),pos=(-base.screen_width+0.05,0.9),scale=0.05,align=TextNode.ALeft))#0
        self.items.append(DirectEntry(pos=(-base.screen_width+0.61,0,0.9),scale=0.05,width=20,initialText="New Map",numLines=1,focus=1))#1
        self.items.append(OnscreenText(text="Map Folder: data/maps/",fg=(1,1,1,1),pos=(-base.screen_width+0.05,0.8),scale=0.05,align=TextNode.ALeft))#2
        self.items.append(DirectEntry(pos=(-base.screen_width+0.61,0,0.8),scale=0.05,width=20,initialText="new_map",numLines=1,focus=0))#3
        self.items.append(OnscreenText(text="Warning folder already exists!",fg=(1,1,0,1),pos=(-base.screen_width+1.65,0.8),scale=0.05,align=TextNode.ALeft))#4

        self.items.append(OnscreenText(text="Map Texture:",fg=(1,1,1,1),pos=(-base.screen_width+0.05,0.7),scale=0.05,align=TextNode.ALeft))#5
        self.items.append(DirectEntry(pos=(-base.screen_width+0.61,0,0.7),scale=0.05,width=20,initialText="untitled.jpg",numLines=1,focus=0))#6
        self.items.append(OnscreenText(text="Invalid Texture!",fg=(1,0,0,1),pos=(-base.screen_width+1.65,0.7),scale=0.05,align=TextNode.ALeft))#7

        self.items.append(OnscreenText(text="Preview Image:",fg=(1,1,1,1),pos=(-base.screen_width+0.05,0.6),scale=0.05,align=TextNode.ALeft))#8
        self.items.append(DirectEntry(pos=(-base.screen_width+0.61,0,0.6),scale=0.05,width=20,initialText="untitled.jpg",numLines=1,focus=0))#9
        self.items.append(OnscreenText(text="Invalid Image!",fg=(1,0,0,1),pos=(-base.screen_width+1.65,0.6),scale=0.05,align=TextNode.ALeft))#10

        self.items.append(OnscreenText(text="Map Size:",fg=(1,1,1,1),pos=(-base.screen_width+0.05,0.5),scale=0.05,align=TextNode.ALeft))#11
        self.items.append(DirectEntry(pos=(-base.screen_width+0.61,0,0.5),scale=0.05,width=5,initialText="1024",numLines=1,focus=0))#12
        self.items.append(DirectEntry(pos=(-base.screen_width+0.91,0,0.5),scale=0.05,width=5,initialText="687",numLines=1,focus=0))#13
        self.items.append(OnscreenText(text="Invalid Size!",fg=(1,0,0,1),pos=(-base.screen_width+1.2,0.5),scale=0.05,align=TextNode.ALeft))#14

        self.items.append(DirectButton( text = "Check Details",pos = (-base.screen_width+0.3,0,0.3),
               text_scale = .05,frameSize=(-0.25,0.25,-0.08,0.08),borderWidth = (.02,.02),
               rolloverSound = None, clickSound = None,command=self.check_items))#15

        self.items.append(OnscreenImage(image = 'sample_pre.jpg', pos = (-base.screen_width+0.45, 0, -0.55), scale = 0.4))#16
        self.items.append(OnscreenImage(image = 'sample_tex.jpg', pos = (base.screen_width-0.85, 0, -0.2), scale = 0.6))#17
        self.items.append(OnscreenText(text="Preview Image",fg=(1,1,1,1),pos=(-base.screen_width+0.45, -0.1),scale=0.1,align=TextNode.ACenter))#18
        self.items.append(OnscreenText(text="Map Texture",fg=(1,1,1,1),pos=(base.screen_width-0.85,0.45),scale=0.1,align=TextNode.ACenter))#19
        self.items.append(DirectButton( text = "Continue",pos = (-base.screen_width+0.3,0,0.1),
               text_scale = .05,frameSize=(-0.25,0.25,-0.08,0.08),borderWidth = (.02,.02),
               rolloverSound = None, clickSound = None,command=self.next_menu))#20

        self.items.append(OnscreenText(text="Map Scale:",fg=(1,1,1,1),pos=(-base.screen_width+0.05,0.4),scale=0.05,align=TextNode.ALeft))#21
        self.items.append(DirectEntry(pos=(-base.screen_width+0.61,0,0.4),scale=0.05,width=5,initialText="2.00",numLines=1,focus=0))#22
        self.items.append(OnscreenText(text="Invalid Scale!",fg=(1,0,0,1),pos=(-base.screen_width+1.2,0.4),scale=0.05,align=TextNode.ALeft))#23

    def check_items(self):
        problem = False

        base.map_name = self.items[1].get()

        ent_fldr = self.items[3]
        ent_tex = self.items[6]
        ent_pre = self.items[9]
        ent_w = self.items[12]
        ent_h = self.items[13]
        ent_scl = self.items[22]

        base.tex_name = ent_tex.get()
        base.pre_name = ent_pre.get()

        txt_fldr = self.items[4]
        txt_tex = self.items[7]
        txt_pre = self.items[10]
        txt_size = self.items[14]
        txt_scl = self.items[23]

        map_path = "../maps/"+ent_fldr.get(plain=True)+"/"
        tex_file = map_path+ent_tex.get(plain=True)
        pre_file = map_path+ent_pre.get(plain=True)

        if os.path.exists(map_path):
            txt_fldr.setText("Good!")
            txt_fldr["fg"] = (0,1,0,1)
            base.map_path = map_path
        else:
            txt_fldr.setText("Directory Doesn't Exist!")
            txt_fldr["fg"] = (1,0,0,1)
            problem = True
        if os.path.exists(tex_file):
            txt_tex.setText("Good!")
            txt_tex["fg"] = (0,1,0,1)
        else:
            txt_tex.setText("File Doesn't Exist!")
            txt_tex["fg"] = (1,0,0,1)
            problem = True

        if os.path.exists(pre_file):
            txt_pre.setText("Good!")
            txt_pre["fg"] = (0,1,0,1)
        else:
            txt_pre.setText("File Doesn't Exist!")
            txt_pre["fg"] = (1,0,0,1)
            problem = True
        try:
            size = (int(ent_w.get(plain=True)),int(ent_h.get(plain=True)))
            if size[0] > 256 and size[1] > 256:
                txt_size.setText("Good!")
                txt_size["fg"] = (0,1,0,1)
            else:
                problem = True
                txt_size.setText("Map too small!")
                txt_size["fg"] = (1,0,0,1)
        except:
            problem = True
            txt_size.setText("Invalid Size!")
            txt_size["fg"] = (1,0,0,1)

        try:
            scale = float(ent_scl.get(plain=True))
            if scale >= 0.5:
                txt_scl.setText("Good!")
                txt_scl["fg"] = (0,1,0,1)
            else:
                txt_scl.setText("Scale too small!")
                txt_scl["fg"] = (1,0,0,1)
                problem = True
        except:
            txt_scl.setText("Invalid Scale!")
            txt_scl["fg"] = (1,0,0,1)
            problem = True

        if problem == False:
            self.save_details(pre_file,tex_file)
            return True
        else:
            return False

    def save_details(self,pre,tex):
        img_pre = self.items[16]
        img_tex = self.items[17]

        img_pre.setImage(pre)
        img_tex.setImage(tex)

        base.map_texture = tex
        base.map_preview = pre
        base.map_width = int(self.items[12].get())
        base.map_height = int(self.items[13].get())
        base.map_scale = float(self.items[22].get())

    def next_menu(self):
        if self.check_items() == True:
            base.menu_manager.menu_goto(base.menu_manager.menu_factions)

class MenuFactions(MenuBase):
    def __init__(self):
        self.create_components()

    def create_components(self):
        self.items = []
        self.items.append(OnscreenText(text="(0) Neutral Faction:",fg=(0,0,0,1),pos=(-base.screen_width+0.05,0.9),scale=0.05,align=TextNode.ALeft))#0
        self.items.append(DirectEntry(pos=(-base.screen_width+0.61,0,0.9),scale=0.05,width=20,initialText="Neutrals",numLines=1,focus=1))#1

        self.items.append(OnscreenText(text="(1) Red Faction:",fg=(1,0,0,1),pos=(-base.screen_width+0.05,0.65),scale=0.05,align=TextNode.ALeft))#2
        self.items.append(DirectEntry(pos=(-base.screen_width+0.61,0,0.65),scale=0.05,width=20,initialText="Reds",numLines=1,focus=0))#3
        self.items.append(OnscreenText(text="Coin:",fg=(1,0,0,1),pos=(-base.screen_width+0.25,0.55),scale=0.05,align=TextNode.ALeft))#4
        self.items.append(DirectEntry(pos=(-base.screen_width+0.41,0,0.55),scale=0.05,width=5,initialText="100",numLines=1,focus=0))#5
        self.items.append(OnscreenText(text="Invalid Number",fg=(1,1,0,1),pos=(-base.screen_width+0.7,0.55),scale=0.05,align=TextNode.ALeft))#6

        self.items.append(OnscreenText(text="(2) Green Faction:",fg=(0,1,0,1),pos=(-base.screen_width+0.05,0.4),scale=0.05,align=TextNode.ALeft))#7
        self.items.append(DirectEntry(pos=(-base.screen_width+0.61,0,0.4),scale=0.05,width=20,initialText="Greens",numLines=1,focus=0))#8
        self.items.append(OnscreenText(text="Coin:",fg=(0,1,0,1),pos=(-base.screen_width+0.25,0.3),scale=0.05,align=TextNode.ALeft))#9
        self.items.append(DirectEntry(pos=(-base.screen_width+0.41,0,0.3),scale=0.05,width=5,initialText="100",numLines=1,focus=0))#10
        self.items.append(OnscreenText(text="Invalid Number",fg=(1,1,0,1),pos=(-base.screen_width+0.7,0.3),scale=0.05,align=TextNode.ALeft))#11

        self.items.append(DirectButton( text = "Place Objects",pos = (-base.screen_width+0.3,0,0.1),
               text_scale = .05,frameSize=(-0.25,0.25,-0.08,0.08),borderWidth = (.02,.02),
               rolloverSound = None, clickSound = None,command=self.done))#12

        base.faction0 = self.items[1].get()
        base.faction0_gold = 0
        base.faction1 = self.items[3].get()
        base.faction1_gold = self.items[5].get()
        base.faction2 = self.items[8].get()
        base.faction2_gold = self.items[10].get()

    def done(self):
        self.hide()
        base.start_map()