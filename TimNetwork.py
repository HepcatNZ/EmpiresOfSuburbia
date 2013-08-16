from panda3d.core import QueuedConnectionManager, QueuedConnectionListener, QueuedConnectionReader, ConnectionWriter, PointerToConnection, NetAddress, NetDatagram
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
import TimObjects

PRINT_MESSAGE = 1

SERVER_CHAT = 2
CLIENT_CHAT = 3
SERVER_READY = 4
CLIENT_READY = 5
CLIENT_JOIN_GAME = 6
MAP_SET = 7
CLIENT_INIT_UPDATE = 8
CLIENT_INIT_REQUEST = 9
SERVER_LOADED = 10
CLIENT_LOADED = 11

ARMY_MOVE = 20
ARMY_MOVE_REQUEST = 21
ARMY_KILL = 22

TOWER_TRAIN = 50

BATTLE_START = 100
BATTLE_TURN = 101
BATTLE_CLASH = 102
BATTLE_ARMYADD = 103
BATTLE_END = 110

REQUEST_MOVE_COUNTER = 120
REQUEST_TOWER_TRAIN = 150

class NetworkManager:
    def __init__(self):
        print "Network Manager Started"


    def connection_open(self):
        self.cManager = QueuedConnectionManager()
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager,0)

        self.activeConnections=[] # We'll want to keep track of these later

        self.cListener = QueuedConnectionListener(self.cManager, 0)
        port_address=9099 #No-other TCP/IP services are using this port
        backlog=1000 #If we ignore 1,000 connection attempts, something is wrong!
        self.tcpSocket = self.cManager.openTCPServerRendezvous(port_address,backlog)
        self.cListener.addConnection(self.tcpSocket)
        print "Network Connection Opened"
        taskMgr.add(self.tskListenerPolling,"Poll the connection listener",-39)
        taskMgr.add(self.tskReaderPolling,"Poll the connection reader",-40)

    def connection_close(self):
        for aClient in self.activeConnections:
            self.cReader.removeConnection(aClient)
        self.activeConnections=[]

         # close down our listener
        self.cManager.closeConnection(self.tcpSocket)
        print "Network Connection Closed"

    def tskListenerPolling(self, taskdata):
        if self.cListener.newConnectionAvailable():
            rendezvous = PointerToConnection()
            netAddress = NetAddress()
            newConnection = PointerToConnection()
            if self.cListener.getNewConnection(rendezvous,netAddress,newConnection):
                newConnection = newConnection.p()
                self.activeConnections.append(newConnection) # Remember connection
                self.cReader.addConnection(newConnection)     # Begin reading connection
        return Task.cont

    def tskReaderPolling(self, taskdata):
        if self.cReader.dataAvailable():
            datagram=NetDatagram()  # catch the incoming data in this instance
    # Check the return value; if we were threaded, someone else could have
    # snagged this data before we did
            if self.cReader.getData(datagram):
                if base.client == True:
                    self.client_processing(datagram)
                else:
                    self.server_processing(datagram)
        return Task.cont



    def server_messager(self,msg,args=[]):
        if msg == "map_set":
            order = PyDatagram()
            order.addUint8(MAP_SET)
            order.addInt8(args[0])
            self.send_package(order)
        elif msg == "client_update":
            order = PyDatagram()
            order.addUint8(CLIENT_INIT_UPDATE)
            order.addString(args[0])
            order.addString(args[1])
            order.addInt8(args[2])
            order.addInt8(args[3])
            self.send_package(order)
        elif msg == "chat_send":
            r = args[0][0]
            g = args[0][1]
            b = args[0][2]
            order = PyDatagram()
            order.addUint8(SERVER_CHAT)
            order.addInt8(r)
            order.addInt8(g)
            order.addInt8(b)
            order.addString(args[1])
            self.send_package(order)
            base.main_menu.chat_add((r,g,b,1),args[1])
        elif msg == "ready_button":
            order = PyDatagram()
            order.addUint8(SERVER_READY)
            order.addInt8(args[0])
            order.addInt8(args[1])
            self.send_package(order)
            base.main_menu.menu_mp_objs["game"][args[0]]["indicatorValue"]=args[1]
            base.main_menu.start_game_check()
        elif msg == "army_kill":
            order = PyDatagram()
            order.addUint8(ARMY_KILL)
            order.addInt8(args[0])
            self.send_package(order)
        elif msg == "battle_start":
            order = PyDatagram()
            order.addUint8(BATTLE_START)
            order.addInt8(args[0])
            order.addFloat32(args[1])
            order.addFloat32(args[2])
            order.addInt8(args[3])
            order.addFloat32(args[4])
            order.addFloat32(args[5])
            order.addInt8(args[6])
            self.send_package(order)
        elif msg == "battle_clash":
            order = PyDatagram()
            order.addUint8(BATTLE_CLASH)
            order.addInt8(args[0])
            order.addInt8(args[1])
            order.addInt8(args[2])
            order.addString(args[3])
            self.send_package(order)
        elif msg == "battle_turn":
            order = PyDatagram()
            order.addUint8(BATTLE_TURN)
            order.addInt8(args[0])
            order.addInt8(args[1])
            self.send_package(order)
        elif msg == "battle_end":
            order = PyDatagram()
            order.addUint8(BATTLE_END)
            order.addInt8(args[0])
            self.send_package(order)
        elif msg == "battle_armyadd":
            order = PyDatagram()
            order.addUint8(BATTLE_ARMYADD)
            order.addInt8(args[0])
            order.addInt8(args[1])
            order.addFloat32(args[2])
            order.addFloat32(args[3])
            self.send_package(order)


    def client_messager(self,msg,args=[]):
        if msg == "chat_send":
            order = PyDatagram()
            order.addUint8(CLIENT_CHAT)
            order.addInt8(args[0][0])
            order.addInt8(args[0][1])
            order.addInt8(args[0][2])
            order.addString(args[1])
            self.send_package(order)
        elif msg == "ready_button":
            order = PyDatagram()
            order.addUint8(CLIENT_READY)
            order.addInt8(args[0])
            order.addInt8(args[1])
            self.send_package(order)
        elif msg == "game_init_request":
            order = PyDatagram()
            order.addUint8(CLIENT_INIT_REQUEST)
            order.addString(args[0])
            order.addString(args[1])
            self.send_package(order)

    def client_processing(self,datagram):
        data_iter = PyDatagramIterator(datagram)
        msgID = data_iter.getUint8()
        if msgID == PRINT_MESSAGE:
            messageToPrint = data_iter.getString()
            print messageToPrint
        if msgID == ARMY_MOVE:
            army_id = data_iter.getInt16()
            ax = data_iter.getFloat64()
            ay = data_iter.getFloat64()
            tx = data_iter.getFloat64()
            ty = data_iter.getFloat64()
            base.armies[army_id].node_path.setX(ax)
            base.armies[army_id].node_path.setY(ay)
            base.armies[army_id].move_to_point(tx,ty)
        if msgID == CLIENT_INIT_UPDATE:
            p1_name = data_iter.getString()
            p1_kingdom = data_iter.getString()
            p1_ready = data_iter.getInt8()
            game_map = data_iter.getInt8()
            base.main_menu.client_update(p1_name,p1_kingdom,p1_ready,game_map)
        if msgID == SERVER_CHAT:
            r = data_iter.getInt8()
            g = data_iter.getInt8()
            b = data_iter.getInt8()
            text = data_iter.getString()
            base.main_menu.chat_add((r,g,b),text)
        if msgID == SERVER_READY:
            but_id = data_iter.getInt8()
            state = data_iter.getInt8()
            base.main_menu.menu_mp_objs["game"][but_id]["indicatorValue"]=state
            base.main_menu.start_game_check()
        if msgID == MAP_SET:
            map = data_iter.getInt8()
            base.main_menu.map_selected = map
            base.main_menu.menu_mp_objs["game"][11]["text"]=base.main_menu.maplist[map]["fullname"]
            base.main_menu.menu_mp_objs["game"][10].setImage(base.main_menu.maplist[map]["preview"])
        if msgID == BATTLE_TURN:
            a1 = data_iter.getInt8()
            a2 = data_iter.getInt8()
            base.armies[a1].turn_end()
            base.armies[a2].turn_start()
        if msgID == BATTLE_START:
            a1 = data_iter.getInt8()
            a1_x = data_iter.getFloat32()
            a1_y = data_iter.getFloat32()
            a2 = data_iter.getInt8()
            a2_x = data_iter.getFloat32()
            a2_y = data_iter.getFloat32()
            army_start = data_iter.getInt8()
            base.armies[a1].stop()
            base.armies[a2].stop()
            base.armies[a1].node_path.setPos(a1_x,a1_y,0)
            base.armies[a2].node_path.setPos(a2_x,a2_y,0)
            base.battles.append(TimObjects.Battle([base.armies[a1],base.armies[a2]],army_start))
        if msgID == BATTLE_CLASH:
            battle = data_iter.getInt8()
            a1 = data_iter.getInt8()
            a2 = data_iter.getInt8()
            result = data_iter.getString()
            base.battles[battle].clash(base.armies[a1],base.armies[a2],result)
        if msgID == BATTLE_ARMYADD:
            battle = data_iter.getInt8()
            bat = data_iter.getInt8()
            army = data_iter.getInt8()
            a_x = data_iter.getFloat32()
            a_y = data_iter.getFloat32()
            base.battles[bat].add_army(army)
        if msgID == BATTLE_END:
            bat = data_iter.getInt8()
            for a in base.battles[bat].combatants:
                if a.state != "dead":
                    a.state = "normal"
                    a.army_fight_col.setTag("state","normal")

    def server_processing(self,datagram):
        data_iter = PyDatagramIterator(datagram)
        msgID = data_iter.getUint8()
        if msgID == PRINT_MESSAGE:
            messageToPrint = data_iter.getString()
            print messageToPrint
        if msgID == ARMY_MOVE_REQUEST:
            army_id = data_iter.getInt16()
            ax = data_iter.getFloat64()
            ay = data_iter.getFloat64()
            tx = data_iter.getFloat64()
            ty = data_iter.getFloat64()
            base.armies[army_id].set_target(False,tx,ty)
        if msgID == CLIENT_CHAT:
            r = data_iter.getInt8()
            g = data_iter.getInt8()
            b = data_iter.getInt8()
            text = data_iter.getString()
            self.server_messager("chat_send",[(r,g,b),text])
            #base.main_menu.chat_add((r,g,b,1),text)
        if msgID == CLIENT_READY:
            but_id = data_iter.getInt8()
            state = data_iter.getInt8()
            self.server_messager("ready_button",[but_id,state])
            #base.main_menu.chat_add((r,g,b,1),text)
        if msgID == CLIENT_INIT_REQUEST:
            pn = data_iter.getString()
            pk = data_iter.getString()
            base.main_menu.menu_mp_objs["game"][6]["text"] = pn
            base.main_menu.menu_mp_objs["game"][7]["text"] = pk
            self.server_messager("client_update",[base.main_menu.menu_mp_objs["game"][4]["text"],
                                                 base.main_menu.menu_mp_objs["game"][5]["text"],
                                                 base.main_menu.menu_mp_objs["game"][8]["indicatorValue"],
                                                 base.main_menu.map_selected])

    def msgAllClients(self):
        myPyDatagram=self.myNewPyDatagram()  # build a datagram to send
        for aClient in self.activeConnections:
            self.cWriter.send(myPyDatagram,aClient)

    def send_package(self,package):
#        print "packaged"
        for aClient in self.activeConnections:
            print "Package",package,"sent"
            self.cWriter.send(package,aClient)

    def army_move(self,army_id,tx,ty):
        order = PyDatagram()
        if base.client == True:
            order.addUint8(ARMY_MOVE_REQUEST)
        else:
            order.addUint8(ARMY_MOVE)
        ax = base.armies[army_id].node_path.getX()
        ay = base.armies[army_id].node_path.getY()
        order.addInt16(army_id)
        order.addFloat64(ax)
        order.addFloat64(ay)
        order.addFloat64(tx)
        order.addFloat64(ty)
        if base.client == True:
            self.cWriter.send(order,base.server_connection)
        else:
            self.send_package(order)
            base.armies[army_id].move_to_point(tx,ty)

    def tower_train(self,tower_id,build_object):
        order = PyDatagram()
        if base.client == True:
            order.addUint8(REQUEST_TOWER_TRAIN)
        else:
            order.addUint8(TOWER_TRAIN)
        order.addInt16(army_id)
        order.addFloat64(tx)
        order.addFloat64(ty)
        if base.client == True:
            self.cWriter.send(order,base.server_connection)
        else:
            self.send_package(order)
            base.towers[tower_id].train_counter()

#    def request_army_move(self,army_id,tx,ty):
#        order = PyDatagram()
#        order.addUint8(REQUEST_MOVE_COUNTER)
#        order.addInt16(army_id)
#        order.addFloat64(tx)
#        order.addFloat64(ty)
#        self.cWriter.send(order,base.server_connection)

    def myNewPyDatagram(self):
        # Send a test message
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(PRINT_MESSAGE)
        myPyDatagram.addString("You got ze message!")
        return myPyDatagram

    def client_connect(self,ip):
        port_address=9099  # same for client and server

         # a valid server URL. You can also use a DNS name
         # if the server has one, such as "localhost" or "panda3d.org"
        ip_address=ip

         # how long until we give up trying to reach the server?
        timeout_in_miliseconds=3000  # 3 seconds

        base.server_connection=self.cManager.openTCPClientConnection(ip_address,port_address,timeout_in_miliseconds)

        if base.server_connection:
            self.cReader.addConnection(base.server_connection)  # receive messages from server
            self.activeConnections.append(base.server_connection)
            print "Connected to server",ip
            return True
        print "Connection failed"
        return False