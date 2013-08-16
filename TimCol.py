from pandac.PandaModules import CollisionTube, CollisionRay, CollisionTraverser, CollisionHandlerEvent,CollisionSphere, CollisionNode, CardMaker, TransparencyAttrib
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import Plane, ShowBase, Vec3, Point3, CardMaker

class CollisionManager:
    def __init__(self):
        base.cTrav = CollisionTraverser()
        self.col_handler = CollisionHandlerEvent()

        self.selected = -1

        picker_node = CollisionNode("mouseRayNode")
        pickerNPos = base.camera.attachNewNode(picker_node)
        self.pickerRay = CollisionRay()
        picker_node.addSolid(self.pickerRay)

        picker_node.setTag("rays","mray")
        base.cTrav.addCollider(pickerNPos, self.col_handler)

        self.col_handler.addInPattern("%(rays)ft-into-%(type)it")
        self.col_handler.addOutPattern("%(rays)ft-out-%(type)it")

        self.col_handler.addAgainPattern("ray_again_all%(""rays"")fh%(""type"")ih")

        self.DO=DirectObject()

        self.DO.accept('mray-into-army', self.col_in_object)
        self.DO.accept('mray-out-army', self.col_out_object)
        self.DO.accept('mray-into-battle', self.col_in_object)
        self.DO.accept('mray-out-battle', self.col_out_object)

        self.DO.accept('ray_again_all', self.col_against_object)

        if base.client == False:
            self.col_handler.addInPattern("%(player)ft-into-%(player)it")
            self.col_handler.addInPattern("%(type)ft-into-%(type)it")
            self.DO.accept('army-into-battle', self.col_army_against_battle)
            self.DO.accept('p1-into-p2', self.col_army_into_army)

        self.pickable=None

        self.DO.accept('mouse1', self.mouse_click, ["down"])
        self.DO.accept('mouse1-up', self.mouse_click, ["up"])
        self.DO.accept('mouse3-up', self.mouse_order)

        taskMgr.add(self.ray_update, "updatePicker")

        taskMgr.add(self.get_mouse_plane_pos, "MousePositionOnPlane")


        z = 0
        self.plane = Plane(Vec3(0, 0, 1), Point3(0, 0, z))

        self.model = loader.loadModel("models/chest.egg")
        self.model.reparentTo(render)
        cm = CardMaker("blah")
        cm.setFrame(-100, 100, -100, 100)
        pnode = render.attachNewNode(cm.generate())#.lookAt(0, 0, -1)
        pnode.hide()

    def col_army_against_battle(self,entry):
        print "Army Joins!"
        #base.net_manager.battle_join(bat,army)
        army = entry.getFromNodePath()
        a_id = int(army.getParent().getTag("id"))
        a = base.armies[a_id]
        if a.state == "normal":
            battle = entry.getIntoNodePath()
            b_id = int(battle.getParent().getTag("id"))
            if base.single_player == False:
                base.net_manager.server_messager("battle_armyadd",[b_id,a_id,a.node_path.getX(),a.node_path.getY()])

            a = base.armies[a_id]
            b = base.battles[b_id]
            b.add_army(a)

    def col_army_into_army(self,entry):
        if entry.getFromNodePath().getTag("state") == "normal" and entry.getIntoNodePath().getTag("state") == "normal":
            #base.net_manager.battle_start(a1,a2)
            army1 = entry.getFromNodePath()
            army2 = entry.getIntoNodePath()
            a1_id = int(army1.getParent().getTag("id"))
            a2_id = int(army2.getParent().getTag("id"))
            a1 = base.armies[a1_id]
            a2 = base.armies[a2_id]
            a1.stop()
            a2.stop()
            base.battles.append(base.obj_manager.create_battle([a1,a2]))

    def col_in_object(self,entry):
        np_into=entry.getIntoNodePath()
        np_into.getParent().setColor(0.5,0.5,0.5,1)
        #self.global_text.setText(np_into.getName())
        if np_into.getTag("type") == "battle":
            print "You're in a battle"

        #print "in"

    def col_out_object(self,entry):
        np_into=entry.getIntoNodePath()
        #print "out"
        try:
            np_into.getParent().clearColor()
        except:
            print "ERROR CLEARING COLOUR"
        #self.global_text.setText("")

        self.pickable = None

    def col_against_object(self,entry):
        if entry.getIntoNodePath().getParent() != self.pickable:
            #print "penetrating"

            np_from=entry.getFromNodePath()
            np_into=entry.getIntoNodePath()
            self.selected_type = np_into.getTag("type")

            self.pickable = np_into.getParent()


    def mouse_click(self,status):
        if self.pickable:
            if status == "down":
                if self.selected_type == "army" and base.armies[int(self.pickable.getTag("id"))].state == "normal":
                    self.pickable.setScale(0.95*10)
                    self.selected = int(self.pickable.getTag("id"))
                    self.selected_node = self.pickable
                    print "You clicked on Army"+str(self.selected)
                    base.vis_manager.statbar.show_army(self.selected)
                elif self.selected_type == "battle":
                    self.selected = int(self.pickable.getTag("id"))
                    self.selected_node = self.pickable
                    print "You clicked on a battle"
                    base.vis_manager.statbar.show_battle(self.selected)
                else:
                    base.vis_manager.statbar.reset_statbar()
            if status == "up":
                if self.selected_type == "army":
                    self.pickable.setScale(1.0*10)
        elif self.pickable == None:
            self.selected = -1
            self.selected_node = None

    def mouse_order(self):
        print "mouse_order"
        if self.selected != -1 and base.armies[self.selected].state == "normal":
            print "orders sent"
            base.armies[self.selected].set_target(True,self.pos3d.getX(),self.pos3d.getY())

    def get_mouse_plane_pos(self, task):
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            self.pos3d = Point3()
            nearPoint = Point3()
            farPoint = Point3()
            base.camLens.extrude(mpos, nearPoint, farPoint)
            if self.plane.intersectsLine(self.pos3d,
                render.getRelativePoint(camera, nearPoint),
                render.getRelativePoint(camera, farPoint)):
                #print "Mouse ray intersects ground plane at ", self.pos3d
                self.model.setPos(render, self.pos3d)
        return task.again

    def ray_update(self,task):
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()

            self.pickerRay.setFromLens(base.camNode, mpos.getX(),mpos.getY())
        return task.cont