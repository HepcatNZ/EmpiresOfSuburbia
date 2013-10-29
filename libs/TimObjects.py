from panda3d.core import Geom, GeomVertexData, GeomVertexFormat, GeomVertexWriter, GeomTriangles, GeomNode, NodePath, LineSegs
from pandac.PandaModules import CollisionTube, CollisionTraverser, CollisionHandlerEvent, CollisionSphere, CollisionNode, CardMaker, TransparencyAttrib, deg2Rad
from TimCalc import TimCalc
from direct.task import Task
from direct.interval.IntervalGlobal import *
from direct.showbase.ShowBase import Point3
import random
import TimVisuals
import math

counter_scale = 10
battle_count = 0
gen_count = 0
trait_count = 0
battle_width = 4
army_count = 0
tower_count = 0
tower_scale = 10

TCalc = TimCalc()

class ObjectsManager:
    def __init__(self):
        print "Object Manager Initialised"

class GameObject:
    def __init__(self):
        self.my_id = None
        self.name = ""
        self.x = 0
        self.y = 0
        self.scale = 1.0
        self.model = None
        self.node_path = None
        self.node_col = None
        self.player = 0
        self.selected = True

    def selection_ring_create(self, segments = 16,size = 1.0):
        ls = LineSegs()
        ls.setThickness(2)
        ls.setColor(0.8,0.8,0.8)

        radians = deg2Rad(360)

        for i in range(segments+1):
            a = radians * i / segments
            y = math.sin(a)*size
            x = math.cos(a)*size

            ls.drawTo(x, y, 0.2)

        node = ls.create()

        return NodePath(node)

    def destroy(self):
        self.node_path.removeNode()

    def get_x(self):
        return (self.node_path.getX())

    def get_y(self):
        return (self.node_path.getY())

    def select(self):
        self.selected = True
        try:
            self.selection_ring.show()
        except:
            print "Error showing"

    def deselect(self):
        self.selected = False
        try:
            self.selection_ring.hide()
        except:
            print "Error hiding"

class MapTable(GameObject):
    def __init__(self):
        self.scale = 10

        self.model = loader.loadModel("models/map_table.egg")

        self.node_path = NodePath("map_table_node_path")
        self.model.reparentTo(self.node_path)
        self.node_path.setPos(0,0,0)
        self.node_path.setScale(self.scale,self.scale,self.scale)
        self.node_path.reparentTo(render)

class Army(GameObject):
    def __init__(self,x,y,player,soldiers,general=None):
        global army_count
        self.my_id = army_count
        army_count += 1

        print "ARMY ID IS",self.my_id

        self.name = "Army "+str(self.my_id)
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.scale = counter_scale
        self.range = 50.0

        self.selected = False

        self.general = general
        self.soldiers = soldiers
        self.state = "normal"
        self.speed = 25.0

        self.battle = -1

        self.stat_init = 0.0
        self.stat_hit = 0.0
        self.stat_block = 0.0
        self.stat_delay = 0.0

        self.player = player
        if self.player == 0:
            self.colour = (0.5,0.5,0.5,1)
            self.model = loader.loadModel("models/infantry_counter_grey.egg")
        if self.player == 1:
            self.colour = (1,0,0,1)
            self.model = loader.loadModel("models/infantry_counter_red.egg")
        elif self.player == 2:
            self.colour = (0,1,0,1)
            self.model = loader.loadModel("models/infantry_counter_green.egg")

        self.node_path = NodePath("army"+str(self.my_id)+"_node_path")
        self.model.reparentTo(self.node_path)
        self.node_path.setPos(x,y,0)
        self.node_path.setTag("player","p"+str(player))
        self.node_path.setScale(self.scale,self.scale,self.scale)

        self.node_col = self.node_path.attachNewNode(CollisionNode("army"+str(self.my_id)+"_c_node"))
        self.node_col.setScale((1,1,0.5))
        self.node_col.setPos(0,0,0)
        self.node_col.node().addSolid(CollisionSphere(0,0,0,1))
        self.node_col.setTag("type","army")
        base.cTrav.addCollider(self.node_col,base.col_manager.col_handler)
        #self.node_col.show()
        self.node_path.setTag("id",str(self.my_id))
        self.army_fight_col = self.node_path.attachNewNode(CollisionNode("army"+str(self.my_id)+"_batcol_node"))
        self.army_fight_col.setScale((2,2,0.5))
        self.army_fight_col.setPos(0,0,0)
        self.army_fight_col.node().addSolid(CollisionSphere(0,0,0,1))
        self.army_fight_col.setColor(1,0,0,0.1)
        self.army_fight_col.setTag("player","p"+str(player))
        self.army_fight_col.setTag("state","normal")
        self.army_fight_col.setTag("type","army")
        base.cTrav.addCollider(self.army_fight_col,base.col_manager.col_handler)
        #self.army_fight_col.show()

        self.selection_ring = self.selection_ring_create(size = 1.2)
        self.selection_ring.reparentTo(self.node_path)
        self.selection_ring.hide()

        self.node_path.reparentTo(render)

    def turn_start(self):
        rate = 0.5
        army_scl_up = self.model.scaleInterval(rate, Point3(1.5, 1.5, 1.5))
        army_scl_down = self.model.scaleInterval(rate, Point3(1, 1, 1))
        self.sq_army_bat = Sequence(army_scl_up,army_scl_down)
        self.sq_army_bat.loop()

    def turn_end(self):
        try:
            self.sq_army_bat.finish()
        except:
            print "no sequence to end"

    def die(self):
        if base.single_player == False and base.client == False:
            base.net_manager.server_messager("army_kill",[self.my_id])
        self.state = "dead"
        self.army_fight_col.removeNode()
        self.node_col.removeNode()
        rate = 4
        intvl_shrink = self.model.scaleInterval(rate, Point3(0, 0, 0))
        func_destroy = Func(self.destroy)
        self.sq_die = Sequence(intvl_shrink,func_destroy)
        self.sq_die.start()
        base.battles[self.battle].recenter()
        base.battles[self.battle].shrink()
        if self.selected:
            i = base.col_manager.selecteds.index(self)
            del base.col_manager.selecteds[i]

    def stop(self):
        try:
            self.sq_army_move.pause()
        except:
            print "already stopped"

    def move_to_point(self,tx,ty):
            self.target_x = tx
            self.target_x = ty
            dist = float(TCalc.dist_to_point(self.node_path.getX(),self.node_path.getY(),tx,ty))
            print dist
            #time = dist/speed
            #print dist/speed
            #print time*speed,dist
            try:
                self.sq_army_move.pause()
                self.intvl_army_move = None
            except:
                print "no sequence"

            if dist > 1:
                self.intvl_army_move = self.node_path.posInterval(dist/self.speed, Point3(tx, ty, 0),startPos=Point3(self.node_path.getX(), self.node_path.getY(), 0))
                self.sq_army_move = Sequence(self.intvl_army_move)
                self.sq_army_move.start()
            else:
                try:
                    self.sq_army_move.finish()
                except:
                    print "no sequence"

    def set_target(self,sender,tx,ty):
        if self.state == "normal":
            if base.single_player == False:
                base.net_manager.army_move(self.my_id,tx,ty)
            else:
                self.move_to_point(tx,ty)

class Tower(GameObject):
    def __init__(self,player,name,x,y):
        global tower_count
        self.my_id = tower_count
        tower_count += 1
        self.player = player
        self.name = name
        self.x = x
        self.y = y
        self.state = "normal"
        self.build_progress = 0.0
        self.build_speed = 1.0
        self.gold_inc = 1.0
        base.ecn_manager.gold_inc += self.gold_inc

        if player == 1:
            self.model = loader.loadModel("models/tower_red.egg")
        elif player == 2:
            self.model = loader.loadModel("models/tower_green.egg")

        self.node_path = NodePath("tower"+str(self.my_id)+"_node_path")
        self.model.reparentTo(self.node_path)
        self.node_path.setPos(x,y,0)
        self.node_path.setTag("player","p"+str(player))
        self.node_path.setScale(tower_scale,tower_scale,tower_scale)

        self.node_col = self.node_path.attachNewNode(CollisionNode("tower"+str(self.my_id)+"_c_node"))
        self.node_col.setScale((2,2,1))
        self.node_col.setPos(0,0,0)
        self.node_col.node().addSolid(CollisionSphere(0,0,0,1))
        self.node_col.setTag("type","tower")
        base.cTrav.addCollider(self.node_col,base.col_manager.col_handler)
        #self.node_col.show()
        self.node_path.setTag("id",str(self.my_id))
        self.tower_fight_col = self.node_path.attachNewNode(CollisionNode("tower"+str(self.my_id)+"_batcol_node"))
        self.tower_fight_col.setScale((2,2,0.5))
        self.tower_fight_col.setPos(0,0,0)
        self.tower_fight_col.node().addSolid(CollisionSphere(0,0,0,1))
        self.tower_fight_col.setColor(1,0,0,0.1)
        self.tower_fight_col.setTag("player","p"+str(player))
        self.tower_fight_col.setTag("state","normal")
        #self.tower_fight_col.show()
        base.cTrav.addCollider(self.tower_fight_col,base.col_manager.col_handler)

        self.selection_ring = self.selection_ring_create(size = 1.5)
        self.selection_ring.reparentTo(self.node_path)
        self.selection_ring.hide()

        self.node_path.reparentTo(render)

    def change_owner(self,new_owner):
        if self.player == base.player:
            base.ecn_manager.gold_inc -= self.gold_inc
        elif new_owner == base.player:
            base.ecn_manager.gold_inc += self.gold_inc
        base.vis_manager.update()
        if new_owner == 1:
            self.model.remove()
            self.model = loader.loadModel("models/tower_red.egg")
        elif new_owner == 2:
            self.model.remove()
            self.model = loader.loadModel("models/tower_green.egg")
        self.node_path.setTag("player","p"+str(new_owner))
        self.tower_fight_col.setTag("player","p"+str(new_owner))
        self.player = new_owner
        self.model.reparentTo(self.node_path)

    def build_cancel(self):
        base.ecn_manager.gold += base.ecn_manager.cost_army_gold
        base.vis_manager.update()
        if base.single_player == False and base.client == False:
                base.net_manager.server_messager("build_cancel",[self.my_id])
        taskMgr.remove("task_tower"+str(self.my_id)+"_build")
        self.build_progress = 0.0
        if base.vis_manager.statbar.focus == self:
            base.vis_manager.statbar.show_tower(self.my_id)

    def build_start(self):
        base.ecn_manager.gold -= base.ecn_manager.cost_army_gold
        base.vis_manager.update()
        print "Started Building"
        if base.single_player == False and base.client == False:
                base.net_manager.server_messager("build_start",[self.my_id,self.player,"army"])
        self.build_progress = self.build_speed
        taskMgr.add(self.task_build,"task_tower"+str(self.my_id)+"_build")
        if base.vis_manager.statbar.focus == self:
            base.vis_manager.statbar.show_tower(self.my_id)

    def build_start_request(self):
        base.net_manager.client_messager("build_start_request",[self.my_id,self.player,"army"])

    def build_cancel_request(self):
        base.net_manager.client_messager("build_cancel_request",[self.my_id])

    def task_build(self,task):
        if self.build_progress < 100.00:
            self.build_progress += self.build_speed
            if base.vis_manager.statbar.focus == self:
                base.vis_manager.statbar.bar_build.set_value(self.build_progress)
            return Task.again
        else:
            self.build_progress = 0.0
            if base.vis_manager.statbar.focus == self:
                base.vis_manager.statbar.show_tower(self.my_id)
            if base.single_player == False and base.client == False:
                base.net_manager.server_messager("build_complete",[self.my_id,self.player,"army"])
            if base.client == False:
                self.create_counter()
            return Task.done

    def create_counter(self):
        new_army = Army(self.node_path.getX(),self.node_path.getY(),self.player,"Infantry",1)
        base.armies.append(new_army)
        new_army.state = "new"
        new_army.army_fight_col.setTag("state","new")
        intvl_exit = new_army.node_path.posInterval(2, Point3(self.x, self.y-48, 0),startPos=Point3(self.x, self.y, 0))

        def army_ready():
            new_army.state = "normal"
            new_army.army_fight_col.setTag("state","normal")

        func_armyready = Func(army_ready)
        sq_army_move = Sequence(intvl_exit,func_armyready)
        sq_army_move.start()

class Battle(GameObject):
    def __init__(self,counters,start=-1):
        global battle_count

        self.combatants = counters
        self.my_id = battle_count
        self.turn = 0
        self.chance_range = 100
        self.chance_success = 80

        self.col_scale_orig = 2.0
        self.col_scale = self.col_scale_orig
        self.col_scale_inc = 0.4

        battle_count += 1

        if start != -1:
            self.turn = start
            self.combatants[start].turn_start()

        coords = [(self.combatants[0].get_x(),self.combatants[0].get_y()),(self.combatants[1].get_x(),self.combatants[1].get_y())]
        self.x,self.y = TCalc.midpoint(coords)

        self.node_path = NodePath("battle"+str(self.my_id)+"_node_path")
        self.node_path.setPos(self.x,self.y,0)
        self.node_path.setTag("id",str(self.my_id))
        self.node_path.setTag("type","battle")
        self.node_path.reparentTo(render)

        self.bat_col = self.node_path.attachNewNode(CollisionNode("battle"+str(self.my_id)+"_c_node"))
        self.bat_col.setScale((self.col_scale,self.col_scale,0.2))
        self.bat_col.setPos(0,0,0)
        self.bat_col.node().addSolid(CollisionSphere(0,0,0,10))
        self.bat_col.setTag("type","battle")
        self.bat_col.show()

        self.battle_speed = 1.0

        for a in self.combatants:
            #a.turn_start()
            a.stop()
            a.state = "battle"
            a.army_fight_col.setTag("state","battle")
            a.battle = self.my_id

        if base.client == False:
            taskMgr.add(self.battle_init_rolls, "battle"+str(self.my_id)+"_task_start")

    def recenter(self):
        new_x = 0.0
        new_y = 0.0
        x_list = []
        y_list = []
        counter = 0
        try:
            for a in self.combatants:
                if a.state != "dead":
                    x_list.append(a.node_path.getX())
                    y_list.append(a.node_path.getY())
                    counter += 1
                    new_x += a.node_path.getX()
                    new_y += a.node_path.getY()
        except:
            pass
        new_x /= len(x_list)
        new_y /= len(y_list)

        self.node_path.setPos(new_x,new_y,0)

    def shrink(self):
        if len(self.combatants) <= 10:
            self.col_scale -= self.col_scale_orig*self.col_scale_inc
            self.bat_col.setScale((self.col_scale,self.col_scale,0.2))

    def battle_init_rolls(self,task):
        init_rolls = []
        highest_roll = -1
        counter = 0
        leader = 0
        for a in self.combatants:
            roll = random.randint(0,self.chance_range)+a.stat_init
            print counter,"rolled",roll
            init_rolls.append(roll)
            if roll > highest_roll:
                highest_roll = roll
                leader = counter
            counter += 1
        self.turn = leader
        print leader,"wins!"
        self.combatants[self.turn].turn_start()

        a1 = self.combatants[0]
        a2 = self.combatants[1]

        if base.client == False:
            if base.single_player == False:
                base.net_manager.server_messager("battle_start",[a1.my_id,a1.node_path.getX(),a1.node_path.getY(),
                                                                 a2.my_id,a2.node_path.getX(),a2.node_path.getY(),
                                                                 self.turn])
            taskMgr.doMethodLater(1,self.battle_loop,"battle"+str(self.my_id)+"_task_loop")
        self.get_odds()
        return task.done

    def get_odds(self):
        side1 = []
        side2 = []
        counter = 0
        for a in self.combatants:
            if a.player == 1 and a.state != "dead":
                side1.append(a)
                counter += 1
            elif a.player == 2 and a.state != "dead":
                side2.append(a)
                counter += 1
        self.odds = (100/counter)*len(side1)
        if base.col_manager.selected_node == self.node_path:
            base.vis_manager.statbar.refresh_battle(self.odds)

    def target_recheck(self):
        army = self.combatants[self.turn]
        target_id = random.randint(0,len(self.combatants)-1)
        target = self.combatants[target_id]
        while target == army or target.player == army.player or target.state == "dead":
            target_id = random.randint(0,len(self.combatants)-1)
            target = self.combatants[target_id]
            print "recheck target - aquired",target_id
        return army,target,target_id

    def turn_change(self,new_turn):
        self.combatants[self.turn].turn_end()
        self.combatants[new_turn].turn_start()
        self.turn = new_turn

    def battle_loop(self,task):
        battle_end = False
        army,target,target_id = self.target_recheck()

        task.delayTime = self.battle_speed+army.stat_delay
        roll = random.randint(0,self.chance_range)+army.stat_hit
        if roll >= self.chance_success:
            roll = random.randint(0,self.chance_range)+target.stat_block
            if roll >= self.chance_success:
                result = "block"
            else:
                result = "hit"
                target.state = "dead"
                battle_end = True
                for a in self.combatants:
                    if a.player != army.player and a.state != "dead":
                        battle_end = False
        else:
            result = "fail"

        if base.single_player == False:
            base.net_manager.server_messager("battle_clash",[self.my_id,army.my_id,target.my_id,result])
        self.clash(army,target,result)

        army.turn_end()
        last_turn = self.turn

        if battle_end:
            if base.single_player == False:
                base.net_manager.server_messager("battle_end",[self.my_id])
            self.end()
            return task.done
        else:
            self.get_odds()
            if self.turn < len(self.combatants)-1:
                self.turn += 1
            else:
                self.turn = 0
            while self.combatants[self.turn].state == "dead":
                if self.turn < len(self.combatants)-1:
                    self.turn += 1
                else:
                    self.turn = 0
            if base.single_player == False:
                base.net_manager.server_messager("battle_turn",[self.my_id,self.turn])
            self.combatants[self.turn].turn_start()
            return task.again

    def end(self):
        if base.col_manager.selected_node == self.node_path:
                base.vis_manager.statbar.reset_statbar()
        for a in self.combatants:
            a.turn_end()
            if a.state != "dead":
                a.state = "normal"
                a.battle = -1
                a.army_fight_col.setTag("state","normal")
        self.destroy()

    def clash(self,a1,a2,result):
        if result == "block":
            TimVisuals.BattleText(self.node_path,"BLOCK!",self.x,self.y,a2.colour)
        elif result == "hit":
            TimVisuals.BattleText(self.node_path,"HIT AND KILL!",self.x,self.y,a1.colour)
            a2.state = "dead"
            a2.die()
        else:
            TimVisuals.BattleText(self.node_path,"Attack Failed!",self.x,self.y,a1.colour)

    def add_army(self,army):
        army.stop()
        army.state = "battle"
        army.army_fight_col.setTag("state","battle")
        army.battle = self.my_id
        self.combatants.append(army)
        if len(self.combatants) <= 10:
            self.col_scale += self.col_scale_orig*self.col_scale_inc
            self.bat_col.setScale((self.col_scale,self.col_scale,0.2))

        self.get_odds()
        self.recenter()

    def destroy(self):
        self.node_path.removeNode()

class General:
    def __init__(self,name,texture,skill,traits):
        global gen_count
        self.gen_id = gen_count
        gen_count += 1
        self.name = name
        self.texture = "textures/generals/"+texture+".jpg"
        self.skill = skill
        self.traits = traits

class Trait:
    def __init__(self,name,mod_name,mod_val):
        global trait_count
        self.trait_id = trait_count
        trait_count += 1
        self.name = name
        self.mod_name = mod_name
        self.mod_val = mod_val

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
