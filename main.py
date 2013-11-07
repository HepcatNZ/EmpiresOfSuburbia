from panda3d.core import NodePath
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from libs.TimCam import TimCam
from libs import TimObjects,TimCol,TimVisuals,TimNetwork,TimXML,TimMenus,TimEconomy,TimCalc
import random

class EmpiresOfSuburbia(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.disableMouse()

        self.client = False
        self.single_player = False
        self.player_name = "Unknown Warrior"
        self.player_kingdom = "Unknown Kingdom"
        self.direct_connect_ip = "192.168.1.12"
        self.player = 2
        base.use_map_factions = False

        self.set_fullscreen(True)

#        TimObjects.MapTable()
#        cam = TimCam()

        self.vis_manager = TimVisuals.VisualManager()
        self.net_manager = TimNetwork.NetworkManager()
        self.xml_manager = TimXML.XMLManager()
        base.xml_manager.load_playerdata()

        self.menu_manager = TimMenus.MenuManager()
        self.calculator = TimCalc.TimCalc()

        #self.net_manager.connection_open()

        #self.start_game()

    def set_fullscreen(self,status):
        wp = WindowProperties()

        self.win_width = base.pipe.getDisplayWidth()
        self.win_height = base.pipe.getDisplayHeight()
        self.screen_width = self.win_width/self.win_height

        if status == True:
            wp.setFullscreen(True)
            #self.win_width = 1366
            #self.win_height = 768
            wp.setSize(self.win_width, self.win_height)
            base.win.requestProperties(wp)

    def start_game(self,map):

        #self.net_manager = TimNetwork.NetworkManager()
        cam = TimCam()

        self.ecn_manager = TimEconomy.EconomyManager(100)
        self.col_manager = TimCol.CollisionManager()
        self.obj_manager = TimObjects.ObjectsManager()
        self.t_msg = self.vis_manager.statbar_create(0.5)

        self.factions = []

        self.armies = []
        self.towers = []
        self.battles = []

        self.xml_manager.map_load("maps/Nepal/map.xml")

        base.ecn_manager.gold = base.factions[base.player].coin
        base.vis_manager.update()

        self.map = TimObjects.Map(self.map_width,self.map_height,"maps/Nepal/"+self.map_tex,self.map_scale)
#        for i in range(10):
#            self.armies.append(TimObjects.Army(1,"Infantry",200+(48*i),500,0))
#        for i in range(10):
#            self.armies.append(TimObjects.Army(2,"Infantry",200+(48*i),550,0))
#
#        for i in range (5):
#            self.towers.append(TimObjects.Tower(1,"Tower",200+(150*i),300,1.0))
#        for i in range (5):
#            self.towers.append(TimObjects.Tower(2,"Tower",200+(150*i),700,1.0))

app = EmpiresOfSuburbia()
app.setFrameRateMeter(True)
app.run()