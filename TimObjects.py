from panda3d.core import Geom, GeomVertexData, GeomVertexFormat, GeomVertexWriter, GeomTriangles, GeomNode, NodePath
from pandac.PandaModules import CollisionTube, CollisionTraverser, CollisionHandlerEvent, CollisionSphere, CollisionNode, CardMaker, TransparencyAttrib
from TimCalc import TimCalc
from direct.task import Task
from direct.interval.IntervalGlobal import *
from direct.showbase.ShowBase import Point3
import random
import TimVisuals

counter_scale = 10
army_count = 0
battle_count = 0
gen_count = 0
trait_count = 0
battle_width = 4
tower_count = 0
tower_scale = 10

TCalc = TimCalc()

class ObjectsManager:
    def __init__(self):
        print "Object Manager Initialised"

    def create_army(self,player,name,x,y,gen,soldiers):
        return(Army(player,name,x,y,gen,soldiers))

    def create_battle(self,counters):
        return(Battle(counters))

class Army:
    def __init__(self,player,name,x,y,gen,soldiers):
        global army_count
        self.army_id = army_count
        army_count += 1
        self.range = 50
        self.player = player

        if player == 1:
            self.colour = (1,0,0,1)
        else:
            self.colour = (0,1,0,1)

        self.name = name
        self.tx = x
        self.ty = y
        self.gen = gen
        self.soldiers = soldiers
        self.state = "normal"
        self.speed = 25.0

        self.stat_init = 0.0
        self.stat_hit = 0.0
        self.stat_block = 0.0
        self.stat_delay = 0.0

        if player == 1:
            self.model = loader.loadModel("models/infantry_counter_red.egg")
        elif player == 2:
            self.model = loader.loadModel("models/infantry_counter_green.egg")

        self.node_path = NodePath("army"+str(self.army_id)+"_node_path")
        self.model.reparentTo(self.node_path)
        self.node_path.setPos(x,y,0)
        self.node_path.setScale(counter_scale,counter_scale,counter_scale)

        self.army_col = self.node_path.attachNewNode(CollisionNode("army"+str(self.army_id)+"_c_node"))
        self.army_col.setScale((1,1,0.5))
        self.army_col.setPos(0,0,0)
        self.army_col.node().addSolid(CollisionSphere(0,0,0,1))
        self.army_col.setTag("type","army")
        base.cTrav.addCollider(self.army_col,base.col_manager.col_handler)
        #base.col_traverser.addCollider(self.army_col, base.col_handler)
        #self.army_col.show()
        self.node_path.setTag("id",str(self.army_id))
        self.army_fight_col = self.node_path.attachNewNode(CollisionNode("army"+str(self.army_id)+"_batcol_node"))
        self.army_fight_col.setScale((2,2,0.5))
        self.army_fight_col.setPos(0,0,0)
        self.army_fight_col.node().addSolid(CollisionSphere(0,0,0,1))
        self.army_fight_col.setColor(1,0,0,0.1)
        self.army_fight_col.setTag("player","p"+str(player))
        self.army_fight_col.setTag("state","normal")
        base.cTrav.addCollider(self.army_fight_col,base.col_manager.col_handler)
        #self.army_fight_col.show()

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
            base.net_manager.server_messager("army_kill",[self.army_id])
        self.state = "dead"
        self.army_fight_col.removeNode()
        self.army_col.removeNode()
        rate = 4
        intvl_shrink = self.model.scaleInterval(rate, Point3(0, 0, 0))
        func_destroy = Func(self.destroy)
        self.sq_die = Sequence(intvl_shrink,func_destroy)
        self.sq_die.start()

    def destroy(self):
        self.node_path.removeNode()

    def stop(self):
        try:
            self.sq_army_move.pause()
        except:
            print "already stopped"

    def move_to_point(self,tx,ty):
            self.tx = tx
            self.ty = ty
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
                base.net_manager.army_move(self.army_id,tx,ty)
            else:
                self.move_to_point(tx,ty)

    def get_x(self):
        return (self.node_path.getX())

    def get_y(self):
        return (self.node_path.getY())

class Tower:
    def __init__(self,player,name,x,y):
        global tower_count
        self.tower_id = tower_count
        tower_count += 1
        self.player = player
        self.name = name
        self.x = x
        self.y = y
        self.state = "normal"

        if player == 1:
            self.model = loader.loadModel("models/tower_red.egg")
        elif player == 2:
            self.model = loader.loadModel("models/tower_green.egg")

        self.node_path = NodePath("tower"+str(self.tower_id)+"_node_path")
        self.model.reparentTo(self.node_path)
        self.node_path.setPos(x,y,0)
        self.node_path.setScale(tower_scale,tower_scale,tower_scale)

        self.selection_ring = loader.loadModel("models/selection_ring.egg")
        self.selection_ring.setPos(x,y,20)
        self.selection_ring.setScale(tower_scale*2,tower_scale*2,tower_scale)
        self.selection_ring.reparentTo(render)


        self.node_path.reparentTo(render)


    def create_counter(self):
        new_army = Army(self.player,"Infantry",self.node_path.getX(),self.node_path.getY(),None,1)
        base.armies.append(new_army)
        new_army.state = "newborn"
        new_army.army_fight_col.setTag("state","newborn")
        intvl_exit = new_army.node_path.posInterval(2, Point3(self.x, self.y-48, 0),startPos=Point3(self.x, self.y, 0))

        def army_ready():
            new_army.state = "normal"
            new_army.army_fight_col.setTag("state","normal")

        func_armyready = Func(army_ready)
        sq_army_move = Sequence(intvl_exit,func_armyready)
        sq_army_move.start()


class Battle:
    def __init__(self,counters,start=-1):
        global battle_count

        self.combatants = counters
        self.bat_id = battle_count
        self.turn = 0
        self.chance_range = 100
        self.chance_success = 80

        battle_count += 1

        if start != -1:
            self.turn = start
            base.armies[start].turn_start()

        coords = [(self.combatants[0].get_x(),self.combatants[0].get_y()),(self.combatants[1].get_x(),self.combatants[1].get_y())]
        self.x,self.y = TCalc.midpoint(coords)

        self.node_path = NodePath("battle"+str(self.bat_id)+"_node_path")
        self.node_path.setPos(self.x,self.y,0)
        self.node_path.setTag("id",str(self.bat_id))
        self.node_path.setTag("type","battle")
        self.node_path.reparentTo(render)

        self.bat_col = self.node_path.attachNewNode(CollisionNode("battle"+str(self.bat_id)+"_c_node"))
        self.bat_col.setScale((2,2,0.2))
        self.bat_col.setPos(0,0,0)
        self.bat_col.node().addSolid(CollisionSphere(0,0,0,10))
        self.bat_col.setTag("type","battle")
        self.bat_col.show()

        self.battle_speed = 2.0

        for a in self.combatants:
            #a.turn_start()
            a.stop()
            a.state = "battle"
            a.army_fight_col.setTag("state","battle")

        if base.client == False and base.single_player == False:
            taskMgr.add(self.battle_init_rolls, "battle"+str(self.bat_id)+"_task_start")
        elif base.single_player == True:
            taskMgr.add(self.battle_init_rolls, "battle"+str(self.bat_id)+"_task_start")

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

        if base.single_player == False:
            base.net_manager.server_messager("battle_start",[a1.army_id,a1.node_path.getX(),a1.node_path.getX(),
                                                             a2.army_id,a2.node_path.getX(),a2.node_path.getX(),
                                                             self.turn])

        taskMgr.doMethodLater(1,self.battle_loop,"battle"+str(self.bat_id)+"_task_loop")

        return task.done


    def target_recheck(self):
        army = self.combatants[self.turn]
        target_id = random.randint(0,len(self.combatants)-1)
        target = self.combatants[target_id]
        while target == army or target.player == army.player or target.state == "dead":
            target_id = random.randint(0,len(self.combatants)-1)
            target = self.combatants[target_id]
            print "recheck target - aquired",target_id
        return army,target,target_id

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
            base.net_manager.server_messager("battle_clash",[self.bat_id,army.army_id,target.army_id,result])
        self.clash(army,target,result)

        army.turn_end()
        last_turn = self.turn

        if battle_end:
            if base.single_player == False:
                base.net_manager.server_messager("battle_end",self.bat_id)
            for a in self.combatants:
                if a.state != "dead":
                    a.state = "normal"
                    a.army_fight_col.setTag("state","normal")
            self.destroy()
            return task.done
        else:
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
                base.net_manager.server_messager("battle_turn",[last_turn,self.turn])
            self.combatants[self.turn].turn_start()
            return task.again

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
        self.combatants.append(army)

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