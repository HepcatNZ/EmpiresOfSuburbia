from pandac.PandaModules import CardMaker, TransparencyAttrib

class DrawingManager:
    def __init__(self):
        print "Drawing Manager Initialised"

class Map:
    def __init__(self,width,height,texture,scale):
        self.width = width*scale
        self.height = height*scale
        self.texture = loader.loadTexture(texture)#"textures/map/"+texture+".jpg")

        cm = CardMaker("CardMaker")
        cm.setFrame((self.width/2,self.height/2,0),(-self.width/2,self.height/2,0),(-self.width/2,-self.height/2,0),(self.width/2,-self.height/2,0))
        card = render.attachNewNode(cm.generate())
        card.clearColor()
        card.setBin("background", 10)
        card.setHpr(180,0,0)
        card.setTransparency(TransparencyAttrib.MAlpha)

        card.setTexture(self.texture)