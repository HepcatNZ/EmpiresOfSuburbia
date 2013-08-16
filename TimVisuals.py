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


class GameStatBar:
    def __init__(self,height):
        print "stat bar"
        self.objs = []
        width = 1.78
        frame = DirectFrame(pos = (0,0,0),frameSize=(-width,width,-1.0,-1.0+height), frameColor=(0,0,0,0.6))
        image = OnscreenImage("textures/interface/battle.jpg",scale = 0.2, pos = (-width+0.25,0,-0.75))
        self.objs.append(frame)
        self.objs.append(image)
        lbls = []
        #for i in range (6):
        lbl = OnscreenText(text = "Army Name", fg = (1,0,0,1), pos=(-width+0.5,-0.6), scale=0.05, align = TextNode.ALeft)
        self.objs.append(lbl)

    def show_army(self,army_id):
        self.objs[1].show()
        self.objs[1].setImage("textures/interface/army.jpg")
        self.objs[2].setText(base.armies[army_id].name)

    def show_battle(self,battle_id):
        self.objs[1].show()
        self.objs[1].setImage("textures/interface/battle.jpg")
        self.objs[2].setText("Battle")

    def reset_statbar(self):
        print "BAR RESETTING"
        self.objs[1].hide()
        self.objs[2].setText("Battle")


class MainMenu:
    def __init__(self):
        self.mm_buts = []
        self.menu_sp_buts = []
        self.menu_stage = "main"
        self.mm_buts.append(self.MenuBackground("textures/menu/scenes/scene5.jpg",1.24))
        mm_but_text = ["Single Player","Multiplayer","Options","Quit"]
        mm_but_func = [self.start_sp,self.start_mp,self.start_options,self.quit]
        lbl_title = DirectLabel(text = "Empires of Suburbia", text_fg = (1,0,0,1), pos=(0,0,0.6), scale=0.28, frameColor=(1,1,1,0), text_align = TextNode.ACenter)
        self.mm_buts.append(lbl_title)
        mm_but_w = 0.8
        mm_but_h = 0.2
        mm_but_space = 0.01
        mm_but_y = -0.1
        for i in range(len(mm_but_text)):
            self.mm_buts.append(self.MenuButton(mm_but_text[i],0,mm_but_y-(mm_but_h*i+(mm_but_space*i)),mm_but_w,mm_but_h,mm_but_func[i]))

        self.menu_multiplay_create()
        self.menu_options_create()

    def MenuBackground(self,img,scl = 1.0):
#        self.app_path = os.path.dirname(os.path.realpath(__file__))
#        os.chdir(self.app_path)
#        img_total = self.app_path+"/"+img
        img_real = Image.open(img)
        w = float(img_real.size[0])
        h = float(img_real.size[1])
        w_multiplier = w/h
        print w_multiplier
        image = OnscreenImage(img, scale=(scl*w_multiplier,0,scl))
        return image

    def MenuMapImage(self,img,pos,scl):
        img_real = Image.open(img)
        image = OnscreenImage(img,pos=pos, scale=(scl,0,scl))
        return image

    def MenuScrollList(self,x,y,width,height,items_vis=6):
        numItemsVisible = items_vis
        itemHeight = height/numItemsVisible#0.08
#                                    (0.0, 0.7, -0.05, 0.59)
        bor_w = 0.05
        myScrolledList = DirectScrolledList(
            decButton_pos= (0, 0, (height/5)),
            decButton_text = "Up",
            decButton_text_scale = 0.04,
            decButton_borderWidth = (0.005, 0.005),
            decButton_frameSize=(-0.08,0.08,-0.03,0.03),

            incButton_pos= (0, 0,-height),
            incButton_text = "Down",
            incButton_text_scale = 0.04,
            incButton_borderWidth = (0.005, 0.005),
            incButton_frameSize=(-0.08,0.08,-0.03,0.03),

            frameSize = (0-(width/2), (width/2), -height, (height/5)),
            frameColor = (1,0,0,0.5),
            pos = (x, 0, y),
            items = [],
            numItemsVisible = numItemsVisible,
            forceHeight = itemHeight,
            itemFrame_frameSize = (0-(width/2)+bor_w, (width/2)-bor_w, -height+bor_w, (height/5)-bor_w),
            itemFrame_pos = (0, 0, 0),
            )

        return myScrolledList

    def MenuButton(self,t,x,y,w,h,func=None,extra_arg=None):
        bor_size = .03
        txt_scl = .08
        if func == None:
            button = DirectButton( text = t,pos = (x,0,y),
               text_scale = txt_scl,frameSize=(-(w/2),(w/2),-(h/2),(h/2)),borderWidth = (bor_size,bor_size),
               rolloverSound = None, clickSound = None)#command=self.report_pos, extraArgs=[self.button_counter])

        elif func != None and extra_arg == None:
            button = DirectButton( text = t,pos = (x,0,y),
               text_scale = txt_scl,frameSize=(-(w/2),(w/2),-(h/2),(h/2)),borderWidth = (bor_size,bor_size),
               rolloverSound = None, clickSound = None,command=func)# extraArgs=[self.button_counter])
        else:
            button = DirectButton( text = t,pos = (x,0,y),
               text_scale = txt_scl,frameSize=(-(w/2),(w/2),-(h/2),(h/2)),borderWidth = (bor_size,bor_size),
               rolloverSound = None, clickSound = None, command=func, extraArgs=[extra_arg])
        return button

    def SmallMenuButton(self,t,x,y,w,h,func,extra_arg=None):
        if extra_arg == None:
            button = DirectButton( text = t,pos = (x,0,y),
               text_scale = .05,frameSize=(-(w/2),(w/2),-(h/2),(h/2)),borderWidth = (.02,.02),
               rolloverSound = None, clickSound = None,command=func)# extraArgs=[self.button_counter])
        else:
            button = DirectButton( text = t,pos = (x,0,y),
               text_scale = .05,frameSize=(-(w/2),(w/2),-(h/2),(h/2)),borderWidth = (.02,.02),
               rolloverSound = None, clickSound = None, command=func, extraArgs=[extra_arg])
        return button

    def start_sp(self):
        base.client = False
        base.single_player = True
        self.menu_showhide(self.mm_buts,False)
        base.start_game("wellington")
        self.menu_state = "singleplayer"

    def start_mp(self):
        base.single_player = False
        self.menu_showhide(self.mm_buts,False)
        self.menu_showhide(self.menu_mp_objs["main"],True)
        self.menu_state = "multiplayer"

    def start_options(self):
        self.menu_showhide(self.mm_buts,False)
        self.menu_showhide(self.menu_op_objs,True)
        self.menu_state = "options"

    def quit(self):
        sys.exit()

    def menu_showhide(self,button_group,show,dict=False):
        if show == True:
            for i in button_group:
                if dict == False:
                    i.show()
                else:
                    for o in button_group[i]:
                        o.show()
        else:
            for i in button_group:
                if dict == False:
                    i.hide()
                else:
                    for o in button_group[i]:
                        o.hide()

    def mm_back(self,menu_from):
        if self.menu_state == "options":
            menu_from[2].enterText(base.player_name)
            menu_from[4].enterText(base.player_kingdom)
            self.menu_showhide(menu_from,False)
        if self.menu_state == "multiplayer":
            self.menu_showhide(menu_from,False,True)
        elif self.menu_state == "multiplayer-game":
            self.menu_showhide(menu_from,False)
            base.net_manager.connection_close()
            self.menu_showhide(self.menu_mp_objs["main"],True)
            self.chat_destroy()
            self.menu_state = "multiplayer"
            return 1
        else:
            self.menu_showhide(menu_from,False)
        self.menu_showhide(self.mm_buts,True)
        self.menu_state = "main"

    def menu_multiplay_create(self):
        self.maplist = base.xml_manager.load_maplist()
        self.map_selected = 0

        self.selected_server = -1
        self.menu_mp_objs = {}
        self.menu_mp_objs["main"] = []
        self.menu_mp_objs["game"] = []

        self.menu_mp_objs["main"].append(self.MenuBackground("textures/menu/scenes/scene6.jpg",1.2))
        self.menu_mp_objs["main"].append(self.SmallMenuButton("Back",-0.8,-0.7,0.4,0.2,self.mm_back,self.menu_mp_objs))
        scroll_width = 1.0
        server_scroll = self.MenuScrollList(-0.8,0.8,1.0,0.8)
        self.menu_mp_objs["main"].append(server_scroll)
        txt_scl = 0.06
        #ss_but = DirectButton(text = ("Currently Broken", "Server selected", "Broken Button", "disabled"),
        #          text_scale=txt_scl, borderWidth = (0.01, 0.01),
        #          relief=2,frameSize=(-scroll_width/2+0.06,scroll_width/2-0.06,-0.04,0.06),command=self.server_select,extraArgs=[0])
        #server_scroll.addItem(ss_but)
        self.menu_mp_objs["main"].append(self.SmallMenuButton("Join Game",-0.08,0.85,0.4,0.15,self.menu_multiplay_join))
        self.menu_mp_objs["main"][3]["state"] = 0
        self.menu_mp_objs["main"][3]["text"] = ("Join Server","Join Server","Join Server","------")
        self.menu_mp_objs["main"].append(self.SmallMenuButton("Host Game",-0.08,0.7,0.4,0.15,self.menu_multiplay_host))
        self.menu_mp_objs["main"].append(self.SmallMenuButton("Direct Connect",-0.08,0.4,0.4,0.15,self.menu_multiplay_direct))


        host_txt_col = (1,0,0,1)
        clnt_txt_col = (0,1,0,1)
        txt_scl = 0.05
        p1_y = 0.8
        p2_y = 0.65
        txt_x = -1.05
        txt_x2 = -0.4

        self.menu_mp_objs["game"].append(self.MenuBackground("textures/menu/scenes/scene6.jpg",1.2))
        self.menu_mp_objs["game"].append(DirectFrame(pos = (0,0,0),frameSize=(-1.1,1.1,-0.9,0.9), frameColor=(0,0,0,0.6)))
        self.menu_mp_objs["game"].append(self.SmallMenuButton("<Players Not Ready>",0.7,-0.7,0.6,0.2,self.menu_multiplay_startgame))
        self.menu_mp_objs["game"][2]["text_fg"] = (1,0,0,1)
        self.menu_mp_objs["game"][2]["state"] = 0
        self.menu_mp_objs["game"].append(self.SmallMenuButton("Back to Lobby",-0.8,-0.7,0.4,0.2,self.mm_back,self.menu_mp_objs["game"]))
        lbl_p1 = DirectLabel(text = "Player Name Unknown", text_fg = host_txt_col, pos=(txt_x,0,p1_y), scale=txt_scl, frameColor=(1,1,1,0), text_align = TextNode.ALeft)
        lbl_k1 = DirectLabel(text = "Player Kingdom Unknown", text_fg = host_txt_col, pos=(txt_x2,0,p1_y), scale=txt_scl, frameColor=(1,1,1,0), text_align = TextNode.ALeft)
        lbl_p2 = DirectLabel(text = "Player Name Unknown", text_fg = clnt_txt_col, pos=(txt_x,0,p2_y), scale=txt_scl, frameColor=(1,1,1,0), text_align = TextNode.ALeft)
        lbl_k2 = DirectLabel(text = "Player Kingdom Unknown", text_fg = clnt_txt_col, pos=(txt_x2,0,p2_y), scale=txt_scl, frameColor=(1,1,1,0), text_align = TextNode.ALeft)
        self.menu_mp_objs["game"].append(lbl_p1)#5
        self.menu_mp_objs["game"].append(lbl_k1)#6
        self.menu_mp_objs["game"].append(lbl_p2)#7
        self.menu_mp_objs["game"].append(lbl_k2)#8

        def toggle_ready(state):
            if base.client == True:
                base.net_manager.client_messager("ready_button",[9,chk_p2["indicatorValue"]])
            else:
                base.net_manager.server_messager("ready_button",[8,chk_p1["indicatorValue"]])



        chk_p1 = DirectCheckButton(pos=(txt_x2+0.8,0,p1_y),text = "Ready" ,scale=.05,command=toggle_ready)
        self.menu_mp_objs["game"].append(chk_p1)#8
        chk_p2 = DirectCheckButton(pos=(txt_x2+0.8,0,p2_y),text = "Ready" ,scale=.05,command=toggle_ready)
        self.menu_mp_objs["game"].append(chk_p2)#9
        self.menu_mp_objs["game"].append(self.MenuMapImage(self.maplist[self.map_selected]["preview"],(-0.6,0,0),0.4))#10
        lbl_map = DirectLabel(text = self.maplist[self.map_selected]["fullname"], text_fg = (1,1,1,1), pos=(-0.6,0,0.45), scale=0.06, frameColor=(1,1,1,0), text_align = TextNode.ACenter)
        self.menu_mp_objs["game"].append(lbl_map)#11
        bor = 0.05



        def map_change(dir):
            if dir == "back":
                if self.map_selected > 0:
                    self.map_selected -= 1
                else:
                    self.map_selected = len(self.maplist)-1
            elif dir == "next":
                if self.map_selected != len(self.maplist)-1:
                    self.map_selected += 1
                else:
                    self.map_selected = 0
            self.menu_mp_objs["game"][11]["text"] = self.maplist[self.map_selected]["fullname"]
            self.menu_mp_objs["game"][10].setImage(self.maplist[self.map_selected]["preview"])
            base.net_manager.server_messager("map_set",[self.map_selected])

        b_left = DirectButton( text = "<",pos = (-1,0,0.45),
               text_scale = .05,frameSize=(-bor,bor,-bor,bor),borderWidth = (.015,.015),
               rolloverSound = None, clickSound = None,command=map_change,extraArgs=["back"])
        b_right = DirectButton( text = ">",pos = (-0.2,0,0.45),
               text_scale = .05,frameSize=(-bor,bor,-bor,bor),borderWidth = (.015,.015),
               rolloverSound = None, clickSound = None,command=map_change,extraArgs=["next"])
        self.menu_mp_objs["game"].append(b_left)#12
        self.menu_mp_objs["game"].append(b_right)#13

        self.menu_mp_objs["game"].append(DirectFrame(pos = (0.5,0,0),frameSize=(-0.5,0.5,-0.5,0.6), frameColor=(0,0,0,0.6)))

        def send_chat(text):
            if text != "":
                if base.client == True:
                    base.net_manager.client_messager("chat_send",[(0,1,0,1),self.menu_mp_objs["game"][15].get()])
                else:
                    base.net_manager.server_messager("chat_send",[(1,0,0,1),self.menu_mp_objs["game"][15].get()])
                self.menu_mp_objs["game"][15].set("")
            self.menu_mp_objs["game"][15]["focus"]=1

        entry_chat = DirectEntry(pos = (0.05,0,-0.4),text = "" ,scale=.05, width = 18,
                    initialText="", numLines = 1,focus=1,command=send_chat)

        self.menu_mp_objs["game"].append(entry_chat)#15
        self.menu_showhide(self.menu_mp_objs,False,True)

    def start_game_check(self):
        if self.menu_mp_objs["game"][8]["indicatorValue"] == True and self.menu_mp_objs["game"][9]["indicatorValue"] == True:
            self.menu_mp_objs["game"][2]["text"] = "Start Game"
            self.menu_mp_objs["game"][2]["text_fg"] = (0,0,0,1)
            self.menu_mp_objs["game"][2]["state"] = 1
        else:
            self.menu_mp_objs["game"][2]["text"] = "<Players not ready>"
            self.menu_mp_objs["game"][2]["text_fg"] = (1,0,0,1)
            self.menu_mp_objs["game"][2]["state"] = 0

    def chat_add(self,col,text):
        i = len(self.chat_labels)-1
        while i != 0:
            self.chat_labels[i].setText(self.chat_labels[i-1].getText())
            self.chat_nps[i].setColor(self.chat_nps[i-1].getColor())
            #self.chat_labels[i]["text_fg"] = self.chat_labels[i-1]["text_fg"]
            i-=1
        self.chat_labels[i].setText(text)
        self.chat_nps[i].setColor(col[0],col[1],col[2],1)

    def chat_create(self,n,scl):
        self.chat_labels = []
        self.chat_nps = []
        gap = 0.00
        for l in range(n):
            #lbl = DirectLabel(text = "chatline"+str(l), text_fg = (1,1,1,1),text_mayChange = True,
            #                  pos=(0.05,0,-0.3+(0.5*l*(scl+0.08))), scale=scl, frameColor=(1,1,1,0), text_align = TextNode.ALeft)
            lbl = TextNode('node name')
            lbl.setText("")
            textNodePath = aspect2d.attachNewNode(lbl)
            textNodePath.setScale(scl)
            textNodePath.setColor(1,1,1,1)
            textNodePath.setPos(0.05,0,-0.3+(0.5*l*(scl+0.08)))
            self.chat_nps.append(textNodePath)
            self.chat_labels.append(lbl)
        print "CHAT MADE"

    def chat_destroy(self):
        for l in self.chat_nps:
            l.remove()

    def server_select(self,server_id):
        return 1

    def menu_multiplay_host(self):
        self.menu_showhide(self.menu_mp_objs["main"],False)
        base.client = False
        base.net_manager.connection_open()
        self.chat_create(14,0.05)
        self.menu_mp_objs["game"][4]["text"] = base.player_name
        self.menu_mp_objs["game"][5]["text"] = base.player_kingdom
        self.menu_showhide(self.menu_mp_objs["game"],True)
        self.menu_state = "multiplayer-game"
        self.menu_mp_objs["game"][8]["state"]=1
        self.menu_mp_objs["game"][9]["state"]=0

    def menu_multiplay_join(self):
        return 1

    def menu_multiplay_direct(self):
        base.client = True
        base.net_manager.connection_open()
        if base.net_manager.client_connect("192.168.0.2"):
            self.menu_state = "multiplayer-game"
            self.menu_showhide(self.menu_mp_objs["main"],False)
            self.chat_create(14,0.05)
            self.menu_showhide(self.menu_mp_objs["game"],True)
            self.menu_mp_objs["game"][8]["state"]=0
            self.menu_mp_objs["game"][9]["state"]=1
            self.menu_mp_objs["game"][12].hide()
            self.menu_mp_objs["game"][13].hide()
            base.net_manager.client_messager("game_init_request",[base.player_name,base.player_kingdom])
            self.menu_mp_objs["game"][6]["text"]=base.player_name
            self.menu_mp_objs["game"][7]["text"]=base.player_kingdom

        else:
            base.net_manager.connection_close()

    def client_update(self,p1_name,p1_kingdom,p1_ready,game_map):
        self.menu_mp_objs["game"][4]["text"] = p1_name
        self.menu_mp_objs["game"][5]["text"] = p1_kingdom
        self.menu_mp_objs["game"][8]["indicatorValue"] = p1_ready
        self.menu_mp_objs["game"][11]["text"] = self.maplist[game_map]["fullname"]
        self.menu_mp_objs["game"][10].setImage(self.maplist[game_map]["preview"])
        self.selected_map = game_map

    def menu_multiplay_startgame(self):
        base.main_menu.menu_destroy()
        base.start_game(self.maplist[self.map_selected]["name"])

    def menu_destroy(self):
        for o in self.mm_buts:
            try:
                o.destroy()
            except:
                print o,"undestroyed"
        for o in self.menu_mp_objs["game"]:
            try:
                o.destroy()
            except:
                print o,"undestroyed"
        self.chat_destroy()
        for o in self.menu_mp_objs["main"]:
            try:
                o.destroy()
            except:
                print o,"undestroyed"
        for o in self.menu_op_objs:
            try:
                o.destroy()
            except:
                print o,"undestroyed"

    def menu_options_create(self):
        self.menu_op_objs = []
        self.menu_op_objs.append(self.MenuBackground("textures/menu/scenes/scene7.jpg",1.34))
        self.menu_op_objs.append(self.SmallMenuButton("Cancel",-0.8,-0.8,0.4,0.2,self.mm_back,self.menu_op_objs))
        entry_name = DirectEntry(pos = (-0.76,0,0.9),text = "" ,scale=.05, width = 15,
                    initialText=base.player_name, numLines = 1,focus=0)
        self.menu_op_objs.append(entry_name)#command=setText,#focusInCommand=self.clear_entry)
        self.menu_op_objs.append(OnscreenText("Character Name:",pos=(-1,0.9),style=1, fg=(1,1,1,1), scale = 0.05))
        entry_kgdm = DirectEntry(pos = (-0.76,0,0.8),text = "" ,scale=.05, width = 15,
                    initialText=base.player_kingdom, numLines = 1,focus=0)
        self.menu_op_objs.append(entry_kgdm)#command=setText,#focusInCommand=self.clear_entry)
        self.menu_op_objs.append(OnscreenText("Kingdom Name:",pos=(-1,0.8),style=1, fg=(1,1,1,1), scale = 0.05))
        self.menu_op_objs.append(self.SmallMenuButton("Save Changes",0.8,-0.8,0.6,0.2,self.menu_options_save))
        self.menu_showhide(self.menu_op_objs,False)

    def menu_options_save(self):
        base.player_name = self.menu_op_objs[2].get()
        base.player_kingdom = self.menu_op_objs[4].get()
        self.mm_back(self.menu_op_objs)

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