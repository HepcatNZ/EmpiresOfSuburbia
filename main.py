from panda3d.core import NodePath
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from libs.TimCam import TimCam
from libs import TimObjects,TimCol,TimVisuals,TimNetwork,TimXML,TimMenus,TimEconomy
import random

class EmpiresOfSuburbia(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.disableMouse()


        self.client = False
        self.single_player = False
        self.player_name = "Unknown Warrior"
        self.player_kingdom = "Unknown Kingdom"
        self.direct_connect_ip = "1.1.1.1"
        self.player = 2

        wp = WindowProperties()
        #wp.setFullscreen(True)

        self.win_width = 1920.0
        self.win_height = 1080.0
        #self.win_width = 1366
        #self.win_height = 768
        self.screen_width = self.win_width/self.win_height
        #wp.setSize(self.win_width, self.win_height)
        base.win.requestProperties(wp)

#        TimObjects.MapTable()
#        cam = TimCam()

        self.vis_manager = TimVisuals.VisualManager()
        self.net_manager = TimNetwork.NetworkManager()
        self.xml_manager = TimXML.XMLManager()
        base.xml_manager.load_playerdata()

        self.menu_manager = TimMenus.MenuManager()

        #self.net_manager.connection_open()

        #self.start_game()

    def start_game(self,map):

        #self.net_manager = TimNetwork.NetworkManager()
        cam = TimCam()

        self.ecn_manager = TimEconomy.EconomyManager(100)
        self.col_manager = TimCol.CollisionManager()
        self.obj_manager = TimObjects.ObjectsManager()
        self.t_msg = self.vis_manager.statbar_create(0.5)

        self.armies = []
        self.towers = []
        self.battles = []
        self.map = TimObjects.Map(500,500,map,4)
        for i in range(10):
            self.armies.append(TimObjects.Army(200+(48*i),500,1,"Infantry",0))
        for i in range(10):
            self.armies.append(TimObjects.Army(200+(48*i),550,2,"Infantry",0))

        for i in range (5):
            self.towers.append(TimObjects.Tower(1,"Tower",200+(150*i),300))
        for i in range (5):
            self.towers.append(TimObjects.Tower(2,"Tower",200+(150*i),700))



app = EmpiresOfSuburbia()
app.setFrameRateMeter(True)
app.run()