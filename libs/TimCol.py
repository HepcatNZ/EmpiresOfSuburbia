from panda3d.core import NodePath, LineSegs, TextNode
from pandac.PandaModules import CollisionTube, CollisionRay, CollisionTraverser, CollisionHandlerEvent,CollisionSphere, CollisionNode, CardMaker, TransparencyAttrib, CollisionPlane
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import Plane, ShowBase, Vec3, Point3, CardMaker
import TimObjects

class CollisionManager:
    def __init__(self):
        base.cTrav = CollisionTraverser()
        self.col_handler = CollisionHandlerEvent()

        self.selected = -1
        self.selected_node = None
        self.selecteds = []
        self.multi_select = False
        self.multi_selecting = False
        self.select_box = NodePath()

        picker_node = CollisionNode("mouseRayNode")
        pickerNPos = base.camera.attachNewNode(picker_node)
        self.pickerRay = CollisionRay()
        picker_node.addSolid(self.pickerRay)

        plane_node = CollisionNode("base_plane")
        plane = base.render.attachNewNode(plane_node)
        self.plane_col = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))
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
        self.DO.accept('mray-into-tower', self.col_in_object)
        self.DO.accept('mray-out-tower', self.col_out_object)

        self.DO.accept('ray_again_all', self.col_against_object)

        if base.client == False:
            self.col_handler.addInPattern("%(player)ft-into-%(player)it")
            self.col_handler.addInPattern("%(type)ft-into-%(type)it")
            self.DO.accept('army-into-battle', self.col_army_against_battle)
            self.DO.accept('army-into-tower', self.col_army_against_tower)
            self.DO.accept('p1-into-p2', self.col_p1_into_p2)

        self.pickable=None

        self.DO.accept('mouse1', self.mouse_click, ["down"])
        self.DO.accept('mouse1-up', self.mouse_click, ["up"])
        self.DO.accept('mouse3-up', self.mouse_order)
        self.DO.accept('lshift', self.set_multiselect, [True])
        self.DO.accept('lshift-up', self.set_multiselect, [False])

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

    def col_p1_into_p2(self,entry):
        if entry.getFromNodePath().getTag("state") == "normal" and entry.getIntoNodePath().getTag("state") == "normal" and entry.getIntoNodePath().getTag("type") == "army" and entry.getFromNodePath().getTag("type") == "army":
            #base.net_manager.battle_start(a1,a2)
            army1 = entry.getFromNodePath()
            army2 = entry.getIntoNodePath()
            a1_id = int(army1.getParent().getTag("id"))
            a2_id = int(army2.getParent().getTag("id"))
            a1 = base.armies[a1_id]
            a2 = base.armies[a2_id]
            a1.stop()
            a2.stop()
            base.battles.append(TimObjects.Battle([a1,a2]))
    def col_army_against_tower(self,entry):
        if entry.getIntoNodePath().getParent().getTag("player") != entry.getFromNodePath().getParent().getTag("player"):
            tower = entry.getIntoNodePath()
            tower_id = int(tower.getParent().getTag("id")[-1])
            invader = int(entry.getFromNodePath().getParent().getTag("player")[-1])
            base.towers[tower_id].change_owner(invader)

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
        self.selected_type = "none"

    def col_against_object(self,entry):
        if entry.getIntoNodePath().getParent() != self.pickable:
            #print "penetrating"

            np_from=entry.getFromNodePath()
            np_into=entry.getIntoNodePath()
            self.selected_type = np_into.getTag("type")

            self.pickable = np_into.getParent()


    def mouse_click(self,status):
        print "click"
        in_statbar = base.vis_manager.statbar.mouse_in_bar()
        if self.multi_select == True:
            print "Multiselect!"
            self.select_all_in_box()
            self.multi_select == False
        elif self.pickable and in_statbar == False:
            if status == "down":
                if self.selected_type == "army" and base.armies[int(self.pickable.getTag("id"))].state == "normal" or base.armies[int(self.pickable.getTag("id"))].state == "new":
                    for obj in self.selecteds:
                        obj.deselect()
                        print obj.my_id,"deselected"
                    self.selecteds = []
                    self.pickable.setScale(0.95*10)
                    self.selected = int(self.pickable.getTag("id"))
                    self.selected_node = self.pickable
                    self.selecteds.append(base.armies[self.selected])
                    base.armies[self.selected].select()
                    print "You clicked on Army"+str(self.selected)
                    base.vis_manager.statbar.show_army(self.selected)
                elif self.selected_type == "tower":
                    for obj in self.selecteds:
                        obj.deselect()
                        print obj.my_id,"deselected"
                    self.selecteds = []
                    self.selected = int(self.pickable.getTag("id"))
                    self.selected_node = self.pickable
                    self.selecteds.append(base.towers[self.selected])
                    base.towers[self.selected].select()
                    print "You clicked on a tower"
                    base.vis_manager.statbar.show_tower(self.selected)
                elif self.selected_type == "battle":
                    self.selected = int(self.pickable.getTag("id"))
                    self.selected_node = self.pickable
                    print "You clicked on a battle"
                    base.vis_manager.statbar.show_battle(self.selected)

            if status == "up":
                if self.selected_type == "army":
                    self.pickable.setScale(1.0*10)
        elif in_statbar == True:
            print "in box"
        elif self.pickable == None:
            for obj in self.selecteds:
                obj.deselect()
                print obj.my_id,"deselected"
            self.selecteds = []
            self.selected = -1
            self.selected_node = None
            base.vis_manager.statbar.reset_statbar()

    def select_all_in_box(self):
        for obj in self.selecteds:
            obj.deselect()
            print obj.my_id,"deselected"
        self.selecteds = []
        print "select units in box"
        for a in base.armies:
            if a.node_col.getTag("type") == "army" and (a.state == "normal" or a.state == "new") and a.player == base.player:
                x = a.get_x()
                y = a.get_y()
                if self.box_x < self.model.getX() and self.box_y > self.model.getY():
                    if x < self.model.getX() and x > self.box_x and y > self.model.getY() and y < self.box_y:
                        self.selecteds.append(a)
                        a.select()
                elif self.box_x < self.model.getX() and self.box_y < self.model.getY():
                    if x < self.model.getX() and x > self.box_x and y < self.model.getY() and y > self.box_y:
                        self.selecteds.append(a)
                        a.select()
                elif self.box_x > self.model.getX() and self.box_y < self.model.getY():
                    if x > self.model.getX() and x < self.box_x and y < self.model.getY() and y > self.box_y:
                        self.selecteds.append(a)
                        a.select()
                elif self.box_x > self.model.getX() and self.box_y > self.model.getY():
                    if x > self.model.getX() and x < self.box_x and y > self.model.getY() and y < self.box_y:
                        self.selecteds.append(a)
                        a.select()

    def set_multiselect(self,state):
        self.multi_select = state
        print "set multiselect to",state
        if state == True:
            self.box_x,self.box_y = self.model.getX(),self.model.getY()
            taskMgr.add(self.draw_multiselect_box, "multibox")

    def draw_multiselect_box(self,task):
        self.select_box.remove()
        ls = LineSegs()
        ls.move_to(self.box_x,self.box_y,1)
        ls.draw_to(self.model.getX(),self.box_y,1)
        ls.draw_to(self.model.getX(),self.model.getY(),1)
        ls.draw_to(self.box_x,self.model.getY(),1)
        ls.draw_to(self.box_x,self.box_y,1)
        node = ls.create()
        text = TextNode('text')
        text.setText(str(self.box_x)+","+str(self.box_y)+"\n"+str(self.model.getX())+","+str(self.model.getY()))
        textnp = NodePath(text)
        textnp.setPos(self.box_x,self.box_y,1)
        textnp.setHpr(0,-90,0)
        textnp.setScale(20.0)
        self.select_box = NodePath(node)
        textnp.reparentTo(self.select_box)
        self.select_box.reparentTo(render)
        if self.multi_select == True:
            return task.cont
        else:
            self.select_box.hide()
            return task.done

    def mouse_order(self):
        print "mouse_order"
#        if self.selected != -1 and base.armies[self.selected].state == "normal":
#            print "orders sent"
        for a in self.selecteds:
            if a.node_col.getTag("type") == "army":
                a.set_target(True,self.pos3d.getX(),self.pos3d.getY())

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