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

class MenuManager:
    def __init__(self):
        self.button_counter = 0
        self.buttons = []
        #self.mm = MainMenu()
        print "Menu Manager Initialised"
        self.create_menus()


    def create_menus(self):
        self.menu_state = "main"
        self.menus = {"main":MenuMain(),"mp":MenuMulti(),"mp-game":MenuMultiGame(),"mp-load":MenuMultiLoad(),"options":MenuOptions()}#,"options":MenuOptions()}

        for m in self.menus:
            self.menus[m].hide()

        self.menus["main"].show()

    def menu_goto(self,new_menu):
        old_menu = self.menu_state
        if new_menu == "sp":
            self.menus["main"].hide()
            self.menu_state = "sp"
            base.start_game("wellington")
        else:
            self.menus[old_menu].hide()
            self.menus[new_menu].show()
            self.menu_state = new_menu


class MenuType:
    def __init__(self):
        self.name = None
        self.menu_state = None
        self.obj_list = []
        self.obj_dict = {}

    def hide(self):
        obj_group = self.obj_list
        dict = False
        for i in obj_group:
            if dict == False:
                i.hide()
            else:
                for o in obj_group[i]:
                    o.hide()

    def show(self):
        obj_group = self.obj_list
        dict = False
        for i in obj_group:
            if dict == False:
                i.show()
            else:
                for o in obj_group[i]:
                    o.show()


    def back(self,menu_objs):
        if self.back_menu == "main":
            base.menu_manager.menu_goto("main")
        elif self.back_menu == "mp":
            base.menu_manager.menu_goto("mp")
            base.net_manager.connection_close()

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

class MenuMain(MenuType):
    def __init__(self):
        self.obj_list = []
        self.obj_list.append(self.MenuBackground("textures/menu/scenes/scene5.jpg",1.24))
        mm_but_text = ["Single Player","Multiplayer","Options","Quit"]
        mm_but_func = [self.start_sp,self.start_mp,self.start_options,self.quit]
        lbl_title = DirectLabel(text = "Empires of Suburbia", text_fg = (1,0,0,1), pos=(0,0,0.6), scale=0.28, frameColor=(1,1,1,0), text_align = TextNode.ACenter)
        self.obj_list.append(lbl_title)
        mm_but_w = 0.8
        mm_but_h = 0.2
        mm_but_space = 0.01
        mm_but_y = -0.1
        for i in range(len(mm_but_text)):
            self.obj_list.append(self.MenuButton(mm_but_text[i],0,mm_but_y-(mm_but_h*i+(mm_but_space*i)),mm_but_w,mm_but_h,mm_but_func[i]))

    def start_sp(self):
        base.client = False
        base.single_player = True
        base.menu_manager.menu_goto("sp")

    def start_mp(self):
        base.single_player = False
        base.menu_manager.menu_goto("mp")

    def start_options(self):
        base.menu_manager.menu_goto("options")

    def quit(self):
        sys.exit()

class MenuSingle(MenuType):
    def __init__(self):
        self.back_menu = "main"
        self.obj_list = []
        self.obj_list.append(self.MenuBackground("textures/menu/scenes/scene5.jpg",1.24))

class MenuMulti(MenuType):
    def __init__(self):
        self.back_menu = "main"

        self.selected_server = -1
        self.obj_dict = {}
        self.obj_list = []

        self.obj_list.append(self.MenuBackground("textures/menu/scenes/scene6.jpg",1.2))
        self.obj_list.append(self.SmallMenuButton("Back",-0.8,-0.7,0.4,0.2,self.back,self.obj_dict))
        scroll_width = 1.0
        server_scroll = self.MenuScrollList(-0.8,0.8,1.0,0.8)
        self.obj_list.append(server_scroll)
        txt_scl = 0.06
        #ss_but = DirectButton(text = ("Currently Broken", "Server selected", "Broken Button", "disabled"),
        #          text_scale=txt_scl, borderWidth = (0.01, 0.01),
        #          relief=2,frameSize=(-scroll_width/2+0.06,scroll_width/2-0.06,-0.04,0.06),command=self.server_select,extraArgs=[0])
        #server_scroll.addItem(ss_but)
        self.obj_list.append(self.SmallMenuButton("Join Game",-0.08,0.85,0.4,0.15,self.menu_join_game))
        self.obj_list[3]["state"] = 0
        self.obj_list[3]["text"] = ("Join Server","Join Server","Join Server","------")
        self.obj_list.append(self.SmallMenuButton("Host Game",-0.08,0.7,0.4,0.15,self.menu_host_game))
        self.obj_list.append(self.SmallMenuButton("Direct Connect",-0.08,0.4,0.4,0.15,self.menu_join_direct))


    def server_select(self,server_id):
        return 1

    def menu_host_game(self):
        base.client = False
        base.net_manager.connection_open()
        base.menu_manager.menus["mp-game"].host_init()
        base.menu_manager.menu_goto("mp-game")

    def menu_join_game(self):
        return 1

    def menu_join_direct(self):
        base.client = True
        base.player = 2
        base.net_manager.connection_open()
        if base.net_manager.client_connect(base.direct_connect_ip):
            base.menu_manager.menus["mp-game"].join_init()
            base.menu_manager.menu_goto("mp-game")
        else:
            base.net_manager.connection_close()

class MenuMultiGame(MenuType):
    def __init__(self):
        self.back_menu = "mp"

        self.maplist = base.xml_manager.load_maplist()
        self.map_selected = 0

        host_txt_col = (1,0,0,1)
        clnt_txt_col = (0,1,0,1)
        txt_scl = 0.05
        p1_y = 0.8
        p2_y = 0.65
        txt_x = -1.05
        txt_x2 = -0.4

        self.obj_list = []

        self.obj_list.append(self.MenuBackground("textures/menu/scenes/scene6.jpg",1.2))
        self.obj_list.append(DirectFrame(pos = (0,0,0),frameSize=(-1.1,1.1,-0.9,0.9), frameColor=(0,0,0,0.6)))
        self.obj_list.append(self.SmallMenuButton("<Players Not Ready>",0.7,-0.7,0.6,0.2,self.menu_startgame))
        self.obj_list[2]["text_fg"] = (1,0,0,1)
        self.obj_list[2]["state"] = 0
        self.obj_list.append(self.SmallMenuButton("Back to Lobby",-0.8,-0.7,0.4,0.2,self.back,self.obj_list))
        lbl_p1 = DirectLabel(text = "Player Name Unknown", text_fg = host_txt_col, pos=(txt_x,0,p1_y), scale=txt_scl, frameColor=(1,1,1,0), text_align = TextNode.ALeft)
        lbl_k1 = DirectLabel(text = "Player Kingdom Unknown", text_fg = host_txt_col, pos=(txt_x2,0,p1_y), scale=txt_scl, frameColor=(1,1,1,0), text_align = TextNode.ALeft)
        lbl_p2 = DirectLabel(text = "Player Name Unknown", text_fg = clnt_txt_col, pos=(txt_x,0,p2_y), scale=txt_scl, frameColor=(1,1,1,0), text_align = TextNode.ALeft)
        lbl_k2 = DirectLabel(text = "Player Kingdom Unknown", text_fg = clnt_txt_col, pos=(txt_x2,0,p2_y), scale=txt_scl, frameColor=(1,1,1,0), text_align = TextNode.ALeft)
        self.obj_list.append(lbl_p1)#5
        self.obj_list.append(lbl_k1)#6
        self.obj_list.append(lbl_p2)#7
        self.obj_list.append(lbl_k2)#8

        def toggle_ready(state):
            if base.client == True:
                base.net_manager.client_messager("ready_button",[9,chk_p2["indicatorValue"]])
            else:
                base.net_manager.server_messager("ready_button",[8,chk_p1["indicatorValue"]])

        chk_p1 = DirectCheckButton(pos=(txt_x2+0.8,0,p1_y),text = "Ready" ,scale=.05,command=toggle_ready)
        self.obj_list.append(chk_p1)#8
        chk_p2 = DirectCheckButton(pos=(txt_x2+0.8,0,p2_y),text = "Ready" ,scale=.05,command=toggle_ready)
        self.obj_list.append(chk_p2)#9
        self.obj_list.append(self.MenuMapImage(self.maplist[self.map_selected]["preview"],(-0.6,0,0),0.4))#10
        lbl_map = DirectLabel(text = self.maplist[self.map_selected]["fullname"], text_fg = (1,1,1,1), pos=(-0.6,0,0.45), scale=0.06, frameColor=(1,1,1,0), text_align = TextNode.ACenter)
        self.obj_list.append(lbl_map)#11

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
            self.obj_list[11]["text"] = self.maplist[self.map_selected]["fullname"]
            self.obj_list[10].setImage(self.maplist[self.map_selected]["preview"])
            base.net_manager.server_messager("map_set",[self.map_selected])

        b_left = DirectButton( text = "<",pos = (-1,0,0.45),
               text_scale = .05,frameSize=(-bor,bor,-bor,bor),borderWidth = (.015,.015),
               rolloverSound = None, clickSound = None,command=map_change,extraArgs=["back"])
        b_right = DirectButton( text = ">",pos = (-0.2,0,0.45),
               text_scale = .05,frameSize=(-bor,bor,-bor,bor),borderWidth = (.015,.015),
               rolloverSound = None, clickSound = None,command=map_change,extraArgs=["next"])
        self.obj_list.append(b_left)#12
        self.obj_list.append(b_right)#13

        self.obj_list.append(DirectFrame(pos = (0.5,0,0),frameSize=(-0.5,0.5,-0.5,0.6), frameColor=(0,0,0,0.6)))

        def send_chat(text):
            if text != "":
                if base.client == True:
                    base.net_manager.client_messager("chat_send",[(0,1,0,1),self.obj_list[15].get()])
                else:
                    base.net_manager.server_messager("chat_send",[(1,0,0,1),self.obj_list[15].get()])
                self.obj_list[15].set("")
            self.obj_list[15]["focus"]=1

        entry_chat = DirectEntry(pos = (0.05,0,-0.4),text = "" ,scale=.05, width = 18,
                    initialText="", numLines = 1,focus=1,command=send_chat)

        self.obj_list.append(entry_chat)#15

        self.chat_create(14,0.05)
        #self.obj_list[4]["text"] = base.player_name
        #self.obj_list[5]["text"] = base.player_kingdom
        self.obj_list[8]["state"]=1
        self.obj_list[9]["state"]=0

    def host_init(self):
        self.obj_list[4]["text"] = base.player_name
        self.obj_list[5]["text"] = base.player_kingdom

    def join_init(self):
        self.obj_list[8]["state"]=0
        self.obj_list[9]["state"]=1
        self.obj_list[12].hide()
        self.obj_list[13].hide()
        base.net_manager.client_messager("game_init_request",[base.player_name,base.player_kingdom])
        self.obj_list[6]["text"]=base.player_name
        self.obj_list[7]["text"]=base.player_kingdom

    def start_game_check(self):
        if self.obj_list[8]["indicatorValue"] == True and self.obj_list[9]["indicatorValue"] == True:
            self.obj_list[2]["text_fg"] = (0,0,0,1)
            if base.client == False:
                self.obj_list[2]["text"] = "Start Game"
                self.obj_list[2]["state"] = 1
            else:
                self.obj_list[2]["text"] = "<Waiting to Start>"
        else:
            self.obj_list[2]["text"] = "<Players Not Ready>"
            self.obj_list[2]["text_fg"] = (1,0,0,1)
            self.obj_list[2]["state"] = 0

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
        print "Chatbox created"

    def chat_destroy(self):
        print "Chatbox destroyed"
        for l in self.chat_nps:
            l.remove()

    def menu_startgame(self):
        #base.main_menu.menu_destroy()
        #base.start_game(self.maplist[self.map_selected]["name"])
        base.menu_manager.menu_goto("mp-load")
        if base.client == False:
            base.net_manager.server_messager("game_start")
            base.menu_manager.menus["mp-load"].load()
        print "Game Loading"

    def client_update(self,p1_name,p1_kingdom,p1_ready,game_map):
        self.obj_list[4]["text"] = p1_name
        self.obj_list[5]["text"] = p1_kingdom
        self.obj_list[8]["indicatorValue"] = p1_ready
        self.obj_list[11]["text"] = self.maplist[game_map]["fullname"]
        self.obj_list[10].setImage(self.maplist[game_map]["preview"])
        self.selected_map = game_map

    def show(self):
        self.chat_create(14,0.05)
        obj_group = self.obj_list
        dict = False
        for i in obj_group:
            if dict == False:
                i.show()
            else:
                for o in obj_group[i]:
                    o.show()
        if base.client == True:
            self.obj_list[12].hide()
            self.obj_list[13].hide()

    def hide(self):
        self.chat_destroy()
        obj_group = self.obj_list
        dict = False
        for i in obj_group:
            if dict == False:
                i.hide()
            else:
                for o in obj_group[i]:
                    o.hide()

class MenuOptions(MenuType):
    def __init__(self):
        self.back_menu = "main"

        self.obj_list = []
        self.obj_list.append(self.MenuBackground("textures/menu/scenes/scene7.jpg",1.34))
        self.obj_list.append(self.SmallMenuButton("Cancel",-0.8,-0.8,0.4,0.2,self.back,self.obj_list))
        entry_name = DirectEntry(pos = (-0.76,0,0.9),text = "" ,scale=.05, width = 15,
                    initialText=base.player_name, numLines = 1,focus=0)
        self.obj_list.append(entry_name)#command=setText,#focusInCommand=self.clear_entry)
        self.obj_list.append(OnscreenText("Character Name:",pos=(-1,0.9),style=1, fg=(1,1,1,1), scale = 0.05))
        entry_kgdm = DirectEntry(pos = (-0.76,0,0.8),text = "" ,scale=.05, width = 15,
                    initialText=base.player_kingdom, numLines = 1,focus=0)
        self.obj_list.append(entry_kgdm)#command=setText,#focusInCommand=self.clear_entry)
        self.obj_list.append(OnscreenText("Kingdom Name:",pos=(-1,0.8),style=1, fg=(1,1,1,1), scale = 0.05))

        entry_ip = DirectEntry(pos = (-0.76,0,0.7),text = "" ,scale=.05, width = 15,
                    initialText=base.direct_connect_ip, numLines = 1,focus=0)
        self.obj_list.append(entry_ip)#command=setText,#focusInCommand=self.clear_entry)
        self.obj_list.append(OnscreenText("Direct Connect IP:",pos=(-1,0.7),style=1, fg=(1,1,1,1), scale = 0.05))

        self.obj_list.append(self.SmallMenuButton("Save Changes",0.8,-0.8,0.6,0.2,self.menu_options_save))

    def menu_options_save(self):
        base.player_name = self.obj_list[2].get()
        base.player_kingdom = self.obj_list[4].get()
        base.xml_manager.save_playerdata()
        self.back(self.obj_list)

class MenuMultiLoad(MenuType):
    def __init__(self):
        self.obj_list = []

        self.obj_list.append(self.MenuBackground("textures/menu/scenes/scene7.jpg",1.34))
        if base.client == True:
            self.obj_list.append(OnscreenText("Waiting for Server...",scale = 1.0))
        else:
            self.obj_list.append(OnscreenText("Loading...",scale = 1.0))

    def load(self):
        self.obj_list[1].setText("Loading...")
        base.start_game(base.menu_manager.menus["mp-game"].maplist[base.menu_manager.menus["mp-game"].map_selected]["name"])
        if base.client == True:
            base.net_manager.client_messager("client_loaded",[])
        else:
            base.net_manager.server_messager("server_loaded",[])

    def load_complete(self):
        self.hide()