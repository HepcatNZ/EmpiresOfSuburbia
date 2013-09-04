import math


class MapInterpreter:
    def __init__(self):
        print "Interpreter Initialised"
        
    def deg2num(lat_deg, lon_deg, zoom):
      lat_rad = math.radians(lat_deg)
      n = 2.0 ** zoom
      xtile = int((lon_deg + 180.0) / 360.0 * n)
      ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
      return (xtile, ytile)

class Map:
    def __init__(self,width,height,texture,scale):
        self.width = width*scale
        self.height = height*scale
        self.texture = loader.loadTexture("textures/map/"+texture+".jpg")

        cm = CardMaker("CardMaker")
        cm.setFrame((self.width/2,self.height/2,0),(-self.width/2,self.height/2,0),(-self.width/2,-self.height/2,0),(self.width/2,-self.height/2,0))
        card = render.attachNewNode(cm.generate())
        card.clearColor()
        card.setBin("background", 10)
        card.setHpr(180,0,0)
        card.setTransparency(TransparencyAttrib.MAlpha)

        card.setTexture(self.texture)