from pandac.PandaModules import CollisionTube, CollisionRay, CollisionTraverser, CollisionHandlerEvent,CollisionSphere, CollisionNode, CardMaker, TransparencyAttrib, CollisionPlane
from direct.showbase.ShowBase import Plane, ShowBase, Vec3, Point3, CardMaker
from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath, LineSegs, TextNode, MouseButton
import math
import EditorObjects

class CollisionManager:
    def __init__(self):
        self.line_dir = NodePath()

        base.cTrav = CollisionTraverser()
        self.col_handler = CollisionHandlerEvent()

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

        self.model = loader.loadModel("../models/chest.egg")
        self.model_node = NodePath("sdfafd")
        self.model.reparentTo(self.model_node)
        self.model_node.reparentTo(render)
#
#        self.text_node = TextNode("battle_text")
#        self.text_node.setText("TEXTYTEXTYTEXTTEXT")
#        self.text_node_path = render.attachNewNode(self.text_node)
#        self.text_node_path.reparentTo(render)
#        self.text_node_path.setPos(0,0,4)
#        self.text_node_path.setHpr(0,0,0)
#        self.text_node_path.setScale(1)
#        #self.text_node_path.setTransparency(TransparencyAttrib.MAlpha)
#        self.text_node.setTextColor((1,1,1,1))
#        self.text_node.setAlign(TextNode.ALeft)

        self.placement_ghost = EditorObjects.PlacementGhost(0,"tower",base.object_scale)

        z=0
        self.plane = Plane(Vec3(0, 0, 1), Point3(0, 0, z))

        taskMgr.add(self.ray_update, "updatePicker")
        taskMgr.add(self.get_mouse_plane_pos, "MousePositionOnPlane")
        taskMgr.add(self.task_mouse_press_check, "checkMousePress")

        self.input_init()

        self.pickable=None

    def input_init(self):
        self.DO=DirectObject()

        self.DO.accept('mouse1', self.mouse_click, ["1-down"])
        self.DO.accept('mouse1-up', self.mouse_click, ["1-up"])
        self.DO.accept('mouse3', self.mouse_click, ["3-down"])

        self.DO.accept('0', self.placement_ghost.change_player, [0])
        self.DO.accept('1', self.placement_ghost.change_player, [1])
        self.DO.accept('2', self.placement_ghost.change_player, [2])

        self.DO.accept('a', self.placement_ghost.change_type, ["army"])
        self.DO.accept('t', self.placement_ghost.change_type, ["tower"])

        self.DO.accept('control-s', base.xml_manager.save)

        self.DO.accept('mray-into-army', self.col_in_object)
        self.DO.accept('mray-out-army', self.col_out_object)
        self.DO.accept('mray-into-tower', self.col_in_object)
        self.DO.accept('mray-out-tower', self.col_out_object)

        self.DO.accept('ray_again_all', self.col_against_object)

    def col_against_object(self,entry):
        if entry.getIntoNodePath().getParent() != self.pickable:

            np_from=entry.getFromNodePath()
            np_into=entry.getIntoNodePath()
            self.selected_type = np_into.getTag("type")

            self.pickable = np_into.getParent()

    def col_in_object(self,entry):
        if base.state == "selecting":
            np_into=entry.getIntoNodePath()
            np_into.getParent().setColor(0.5,0.5,0.5,1)

    def col_out_object(self,entry):
        np_into=entry.getIntoNodePath()
        try:
            np_into.getParent().clearColor()
        except:
            print "ERROR CLEARING COLOUR"

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
                self.model_node.setPos(render, self.pos3d)
                self.placement_ghost.set_position(self.pos3d[0],self.pos3d[1])
        return task.again

    def ray_update(self,task):
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()

            self.pickerRay.setFromLens(base.camNode, mpos.getX(),mpos.getY())
        return task.cont

    def task_mouse_place(self,task):
        if base.mouseWatcherNode.isButtonDown(MouseButton.one()):
            self.placing_object = True
            self.place_pos = (self.anchor_x,self.anchor_y)
            self.line_dir.remove()
            ls = LineSegs()
            ls.move_to(self.anchor_x,self.anchor_y,1)
            ls.draw_to(self.model.getX(),self.model.getY(),1)
            node = ls.create()
            angle1 = math.atan2(self.anchor_y - self.anchor_y,self.anchor_x - self.anchor_x+50)
            angle2 = math.atan2(self.anchor_y - self.model.getY(),self.anchor_x - self.model.getY());
            final_angle = angle1-angle2;
            self.model.setHpr(final_angle,0,0)
            self.line_dir = NodePath(node)
            self.line_dir.reparentTo(render)
            return task.again
        else:
            self.line_dir.hide()
            taskMgr.add(self.task_mouse_press_check, "checkMousePress")
            return task.done

    def task_mouse_press_check(self,task):
        if base.mouseWatcherNode.isButtonDown(MouseButton.one()):
            #if self.multi_select == True:
                self.anchor_x,self.anchor_y = self.model.getX(),self.model.getY()
                taskMgr.add(self.task_mouse_place, "multibox")
                return task.done
        return task.again

    def mouse_click(self,status):
        print base.state
        if status == "1-down":
            if base.state == "placement":
                if self.placement_ghost.get_type() == "tower":
                    obj = self.placement_ghost.place("tower",self.model.getX(),self.model.getY())
                elif self.placement_ghost.get_type() == "army":
                    obj = self.placement_ghost.place("army",self.model.getX(),self.model.getY())
                base.details_box.set_object(obj)
                base.change_state("modifying")
            elif base.state == "moving":
                obj = base.details_box.get_object()
                obj.set_position(self.pos3d[0],self.pos3d[1])
                base.change_state("modifying")
            elif base.state == "selecting" and self.pickable != None:
                obj = base.get_obj_from_node(self.pickable)
                base.details_box.set_object(obj,"selecting")
                base.change_state("modifying")
        elif status == "1-up":
            print "Mouse",status
        elif status == "3-down":
            if base.state == "placement":
                base.change_state("selecting")
            elif base.state == "selecting":
                base.change_state("placement")
