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



class VisualManager:
    def __init__(self):
        self.button_counter = 0
        self.buttons = []
        #self.mm = MainMenu()


    def text(self,t,x,y):
        return(OnscreenText(t,style=1, fg=(1,1,1,1), scale = 0.1))

    def statbar_create(self,height):
        self.statbar = GameStatBar(height)
        self.res_bar = ResourceBar(-0.8,0.8,0.1)

    def get_player_col(self,player):
        if player == 0:
            return (.5,.5,.5,1)
        elif player == 1:
            return (1,0,0,1)
        elif player == 2:
            return (0,1,0,1)

    def update(self):
        self.res_bar.update()
        self.statbar.update()

class GameStatBar:
    def __init__(self,height):
        print "stat bar"
        self.focus = None
        self.objs = []
        width = base.screen_width
        self.width = width
        self.height = height
        frame = DirectFrame(pos = (0,0,0),frameSize=(-width,width,-1.0,-1.0+height), frameColor=(0,0,0,0.6))
        image = OnscreenImage("textures/interface/battle.jpg",scale = 0.2, pos = (-width+0.25,0,-0.75))
        self.objs.append(frame)
        self.objs.append(image)
        lbls = []
        #for i in range (6):
        lbl = OnscreenText(text = "Army Name", fg = (1,0,0,1), pos=(-width+0.5,-0.6), scale=0.05, align = TextNode.ALeft)
        self.objs.append(lbl)
        odd_back = DirectFrame(pos = (0,0,0),frameSize=(-width+0.5,-width+0.9,-0.67,-0.62), frameColor=(0,1,0,1))
        odd_front = DirectFrame(pos = (0,0,0),frameSize=(-width+0.5,-width+0.7,-0.67,-0.62), frameColor=(1,0,0,1))
        self.objs.append(odd_back)
        self.objs.append(odd_front)

        self.bar_build = BarProgress(-width+0.5,-0.8,1.0,0.05,50.0,(0.4,0.4,0.4,1),(1,1,0,1))

        self.but_train = DirectButton( text = "Train Infantry",pos = (-width+0.7,0,-0.8),
               text_scale = .05,frameSize=(-0.2,0.2,-0.05,0.05),borderWidth = (.02,.02),
               rolloverSound = None, clickSound = None,command=self.train_unit)
        self.but_cancel = DirectButton( text = "Cancel Training",pos = (-width+0.7,0,-0.9),
               text_scale = .05,frameSize=(-0.2,0.2,-0.05,0.05),borderWidth = (.02,.02),
               rolloverSound = None, clickSound = None,command=self.train_unit)
        self.but_cancel.hide()

    def update(self):
        if base.ecn_manager.gold >= base.ecn_manager.cost_army_gold:
            self.but_train["state"] = 1
            self.but_train["text_fg"] = (0,0,0,1)
        else:
            self.but_train["state"] = 0
            self.but_train["text_fg"] = (1,0,0,1)

    def train_unit(self):
        print "TRAIN UNIT"

    def show_army(self,army_id):
        self.focus = base.armies[army_id]
        col = base.vis_manager.get_player_col(self.focus.player)
        self.reset_statbar()
        self.objs[1].show()
        self.objs[1].setImage("textures/interface/army.jpg")
        self.objs[2].show()
        self.objs[2].setText(base.armies[army_id].get_name())
        self.objs[2].setFg(col)

    def show_battle(self,battle_id):
        self.reset_statbar()
        self.focus = base.battles[battle_id]
        col = base.vis_manager.get_player_col(base.player)
        self.objs[1].show()
        self.objs[1].setImage("textures/interface/battle.jpg")
        base.battles[battle_id].get_odds()
        self.objs[2].show()
        self.objs[2].setText("Battle"+str(battle_id))
        self.objs[2].setFg(col)
        self.objs[3].show()
        self.objs[4].show()

    def show_tower(self,tower_id):
        self.reset_statbar()
        self.focus = base.towers[tower_id]
        col = base.vis_manager.get_player_col(self.focus.player)
        self.objs[1].show()
        self.objs[1].setImage("textures/interface/tower.jpg")
        if base.towers[tower_id].build_progress != 0.0 and self.focus.player == base.player:
            self.bar_build.show()
            self.but_train.hide()
            self.but_cancel.show()
        elif self.focus.player == base.player:
            self.bar_build.hide()
            self.but_train.show()
            self.but_cancel.hide()
        if base.single_player == False and base.client == True:
            self.but_train["command"] = self.focus.build_start_request
            self.but_cancel["command"] = self.focus.build_cancel_request
        else:
            self.but_train["command"] = self.focus.build_start
            self.but_cancel["command"] = self.focus.build_cancel
        self.objs[2].show()
        self.objs[2].setText(base.towers[tower_id].get_name())
        self.objs[2].setFg(col)
        self.objs[3].hide()
        self.objs[4].hide()

    def reset_statbar(self):
        self.focus = None
        #print "BAR RESETTING"
        self.objs[1].hide()
        self.objs[2].hide()
        self.objs[3].hide()
        self.objs[4].hide()
        self.but_train.hide()
        self.but_cancel.hide()
        self.bar_build.hide()

    def refresh_battle(self,odds):
        self.objs[4]["frameSize"]=(-self.width+0.5,-self.width+0.5+(0.4/100)*odds,-0.67,-0.62)

    def mouse_in_bar(self):
        width = self.width
        height = self.height
        m_x,m_y = base.mouseWatcherNode.getMouseX()*base.screen_width,base.mouseWatcherNode.getMouseY()
        print -width,m_x,width,"\n",-1.0,m_y,-1.0+height
        if m_x > -width and m_x < width and m_y > -1.0 and m_y < -1.0+height:
            return True
        else:
            return False

class BarProgress:
    def __init__(self,x,y,w,h,value,back_col,front_col):
        self.my_objs = []
        self.value = value
        self.width = w
        self.height = h
        bar_back = DirectFrame(pos = (x,0,y),frameSize=(0,w,-h/2,h/2), frameColor=back_col)
        bar_front = DirectFrame(pos = (x,0,y),frameSize=(0,w/2,-h/2,h/2), frameColor=front_col)
        self.my_objs.append(bar_back)
        self.my_objs.append(bar_front)
        self.my_objs.append(OnscreenText("Text",pos = (x+(self.width/2),y-self.height/4),scale = 0.05))

    def set_value(self,value):
        self.value = value
        self.my_objs[1]["frameSize"] = (0,(self.width/100)*self.value,-self.height/2,self.height/2)
        self.my_objs[2].setText(str(int(self.value))+"%")

    def hide(self):
        for o in self.my_objs:
            o.hide()

    def show(self):
        for o in self.my_objs:
            o.show()

class BattleText:
    def __init__(self,bat_np,t,x,y,col):
        rate = 2
        z = 20
        scale = 12
        scale_up = 15
        text_node = TextNode("battle_text")
        text_node.setText(t)
        text_node_path = bat_np.attachNewNode(text_node)
        text_node_path.reparentTo(render)
        text_node_path.setPos(x,y,0)
        text_node_path.setHpr(0,-90,0)
        text_node_path.setScale(scale)
        text_node_path.setTransparency(TransparencyAttrib.MAlpha)
        text_node.setTextColor(col)
        text_node.setAlign(TextNode.ACenter)
        node_scl_up = text_node_path.scaleInterval(rate, Point3(scale_up, scale_up, scale_up))
        node_z_up = text_node_path.posInterval(rate, Point3(x, y, z*2))
        node_z_up2 = text_node_path.posInterval(rate, Point3(x, y, z*2))
        node_fade_down = text_node_path.colorScaleInterval(rate, (col[0],col[1],col[2],0))
        node_func_death = Func(self.destroy)
        t_para = Parallel(node_scl_up,node_z_up,node_fade_down)
        t_seq = Sequence(t_para,node_func_death)

        t_seq.start()

        self.tnp = text_node_path

    def destroy(self):
        self.tnp.removeNode()

class ResourceBar:
    def __init__(self,x,y,size):
        self.text = OnscreenText("Gold: "+str(base.ecn_manager.gold)+" +"+str(base.ecn_manager.gold_inc),pos = (x,y),scale = size,fg=base.vis_manager.get_player_col(base.player))
    def update(self):
        self.text.setText("Gold: "+str(int(base.ecn_manager.gold))+" +"+str(base.ecn_manager.gold_inc))