from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import TransparencyAttrib, NodePath, TextNode
from direct.interval.IntervalGlobal import *
from direct.showbase.ShowBase import Point3
from direct.gui.DirectGui import *
from direct.gui.DirectGuiBase import *
from panda3d.core import Vec3
import sys
import Image

class DetailsBox:
    def __init__(self):#,width,height):
        self.objs = []
        self.width = 0.7
        self.height = 0.240
        frame = DirectFrame(pos = (0,0,0),frameSize=(-self.width,self.width,-self.height,self.height), frameColor=(0,0,0,0.6))
        #image = OnscreenImage("textures/interface/battle.jpg",scale = 0.2, pos = (-width+0.25,0,-0.75))
        self.obj_selected = None
        self.last_state = "placement"

        self.objs.append(frame)
        self.objs.append(OnscreenText(text="Name:",fg=(1,1,1,1),pos=(-self.width+0.05,self.height-0.08),scale=0.05,align=TextNode.ALeft))
        self.objs.append(DirectEntry(pos=(-self.width+0.25,0,self.height-0.08),text = "",scale=.05,width=18,initialText="Tower",numLines=1,focus=0))
        self.objs.append(DirectButton( text = "Save",pos = (self.width-0.25,0,-self.height+0.1),
               text_scale = .05,frameSize=(-0.2,0.2,-0.05,0.05),borderWidth = (.02,.02),
               rolloverSound = None, clickSound = None,command=self.save))
        self.objs.append(DirectButton( text = "Move",pos = (0,0,-self.height+0.1),
               text_scale = .05,frameSize=(-0.2,0.2,-0.05,0.05),borderWidth = (.02,.02),
               rolloverSound = None, clickSound = None,command=self.move))
        self.objs.append(DirectButton( text = "Remove",pos = (-self.width+0.25,0,-self.height+0.1),
               text_scale = .05,frameSize=(-0.2,0.2,-0.05,0.05),borderWidth = (.02,.02),
               rolloverSound = None, clickSound = None,command=self.remove))

    def hide(self):
        for o in self.objs:
            o.hide()

    def save(self):
        self.obj_selected.set_name(self.objs[2].get(plain=True))
        if self.obj_selected.get_type() == "tower":
            base.towers.append(self.obj_selected)
        elif self.obj_selected.get_type() == "army":
            base.armies.append(self.obj_selected)
        base.change_state(self.last_state)

    def move(self):
        self.last_text = base.txt_instructions.getText()
        base.txt_instructions.setText("<Left Click> to place "+self.obj_selected.get_name()+" at mouse location")
        base.change_state("moving")

    def set_object(self,obj, last_state = "placement"):
        self.last_state = last_state
        self.obj_selected = obj
        self.objs[2].enterText(obj.get_name())
        base.txt_instructions.setText("Enter details for "+self.obj_selected.get_name())

    def get_object(self):
        return self.obj_selected

    def remove(self):
        self.obj_selected.node_path.remove()
#        if self.obj_selected.type == "tower"        :
#            base.tower_count -= 1
#        elif self.obj_selected.type == "army":
#            base.army_count -= 1
        del self.obj_selected
        self.obj_selected = None
        base.change_state(self.last_state)

    def show(self):
        for o in self.objs:
            o.show()