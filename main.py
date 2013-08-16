from panda3d.core import NodePath
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from TimCam import TimCam
import TimObjects
import TimCol
import TimVisuals
import TimNetwork
import TimXML
import random

class EmpiresOfSuburbia(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.disableMouse()


        self.client = False
        self.single_player = False
        self.player_name = "Unknown Warrior"
        self.player_kingdom = "Unknown Kingdom"

        wp = WindowProperties()
        #wp.setFullscreen(True)

        #self.win_width = 1920
        #self.win_height = 1080
        self.win_width = 1366
        self.win_height = 768
        self.screen_width = self.win_width/self.win_height
        #wp.setSize(self.win_width, self.win_height)
        base.win.requestProperties(wp)

        self.vis_manager = TimVisuals.VisualManager()
        self.net_manager = TimNetwork.NetworkManager()
        self.xml_manager = TimXML.XMLManager()
        #self.net_manager.connection_open()
        self.main_menu = TimVisuals.MainMenu()
        #self.start_game()



    def start_game(self,map):

        #self.net_manager = TimNetwork.NetworkManager()
        cam = TimCam()

        self.col_manager = TimCol.CollisionManager()
        self.obj_manager = TimObjects.ObjectsManager()
        self.t_msg = self.vis_manager.statbar_create(0.5)

        self.armies = []
        self.towers = []
        self.battles = []
        self.map = TimObjects.Map(500,500,map,4)
        for i in range(10):
            self.armies.append(TimObjects.Army(1,"Infantry",200+(48*i),500,0,1))
        for i in range(10):
            self.armies.append(TimObjects.Army(2,"Infantry",200+(48*i),550,0,1))

        for i in range (5):
            self.towers.append(TimObjects.Tower(1,"Tower",random.randint(-1000,1000),random.randint(-1000,1000)))
        for i in range (5):
            self.towers.append(TimObjects.Tower(2,"Tower",random.randint(-1000,1000),random.randint(-1000,1000)))

    def update_camera(self,task):
        base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)

    def toggle_host(self):
        if self.client == True:
            self.client = False
            self.t_msg.setText("Server")
        else:
            self.client = True
            self.t_msg.setText("Client")

    def connection_setup(self):
        if self.client == True:
            self.net_manager.client_connect("192.168.0.2")
        else:
            self.net_manager.msgAllClients()

app = EmpiresOfSuburbia()
app.setFrameRateMeter(True)
app.run()