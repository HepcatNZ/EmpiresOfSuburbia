from direct.showbase import DirectObject
from pandac.PandaModules import Vec3,Vec2
from direct.task import Task
import sys


class TimCam(DirectObject.DirectObject):
    def __init__(self):
        self.camera_control()
        self.input_setup()
        taskMgr.add(self.camera_update, "UpdateCameraTask")

    def camera_control(self):
        self.camera = base.camera

        self.disabled = False

        self.camXAngle = 0
        self.camYAngle = -45
        self.camZAngle = 0

        self.camX = 0
        self.camY = 0
        self.camZ = 500

    def camera_update(self,task):
        self.camera.setPos(self.camX, self.camY, self.camZ)
        self.camera.setHpr(self.camXAngle, self.camYAngle, self.camZAngle)
        if base.mouseWatcherNode.hasMouse():
            mx=base.mouseWatcherNode.getMouseX()
            my=base.mouseWatcherNode.getMouseY()
            border = 0.1
            amph = self.camZ/8
            if mx < -1+border:#-base.screen_width+border:
                speed = amph*(mx-(-1+border))
                self.shift((speed,0,0))
            if mx > 1-border:
                speed = amph*(mx-(1-border))
                self.shift((speed,0,0))
            if my < -1+border:#-base.screen_width+border:
                speed = amph*(my-(-1+border))
                self.shift((0,speed,0))
            if my > 1-border:
                speed = amph*(my-(1-border))
                self.shift((0,speed,0))
        return Task.cont

    def input_setup(self):
        self.accept("wheel_down",self.shift,[(0,0,10*(self.camZ/100))])
        self.accept("wheel_up",self.shift,[(0,0,-10*(self.camZ/100))])
        self.accept("escape",self.quit_game)

    def quit_game(self):
        sys.exit()

    def disable(self):
        self.disabled = True

    def enable(self):
        self.disabled = False

    def shift(self,vector):
        self.camX += vector[0]
        self.camY += vector[1]
        self.camZ += vector[2]

    def stop_x( self ):
        self.camera_move("stopX")

    def stop_y( self ):
        self.camera_move("stopY")
