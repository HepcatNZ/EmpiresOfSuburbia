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
ALL_LOADED = 12
GAME_START = 13

ARMY_MOVE = 20
ARMY_MOVE_REQUEST = 21
ARMY_KILL = 22

BUILD_START = 50
BUILD_CANCEL = 51
BUILD_COMPLETE = 52
BUILD_START_REQUEST = 53
BUILD_CANCEL_REQUEST = 54

BATTLE_START = 100
BATTLE_TURN = 101
BATTLE_CLASH = 102
BATTLE_ARMYADD = 103
BATTLE_END = 110

TOWER_CAPTURE = 40

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
            order.addUint16(MAP_SET)
            order.addInt32(args[0])
            self.send_package(order)
        elif msg == "client_update":
            order = PyDatagram()
            order.addUint16(CLIENT_INIT_UPDATE)
            order.addString(args[0])
            order.addString(args[1])
            order.addInt32(args[2])
            order.addInt32(args[3])
            self.send_package(order)
        elif msg == "chat_send":
            r = args[0][0]
            g = args[0][1]
            b = args[0][2]
            order = PyDatagram()
            order.addUint16(SERVER_CHAT)
            order.addInt32(r)
            order.addInt32(g)
            order.addInt32(b)
            order.addString(args[1])
            self.send_package(order)
            base.menu_manager.menus["mp-game"].chat_add((r,g,b,1),args[1])
        elif msg == "ready_button":
            order = PyDatagram()
            order.addUint16(SERVER_READY)
            order.addInt32(args[0])
            order.addInt32(args[1])
            self.send_package(order)
            base.menu_manager.menus["mp-game"].obj_list[args[0]]["indicatorValue"]=args[1]
            base.menu_manager.menus["mp-game"].start_game_check()
        elif msg == "server_loaded":
            order = PyDatagram()
            order.addUint16(SERVER_LOADED)
            self.send_package(order)
        elif msg == "all_loaded":
            order = PyDatagram()
            order.addUint16(ALL_LOADED)
            self.send_package(order)
        elif msg == "game_start":
            order = PyDatagram()
            order.addUint16(GAME_START)
            self.send_package(order)
        elif msg == "army_kill":
            order = PyDatagram()
            order.addUint16(ARMY_KILL)
            order.addInt32(args[0])
            self.send_package(order)
        elif msg == "build_start":
            order = PyDatagram()
            order.addUint16(BUILD_START)
            order.addInt32(args[0])
            order.addInt8(args[1])
            order.addString(args[2])
            self.send_package(order)
        elif msg == "tower_capture":
            order = PyDatagram()
            order.addUint16(TOWER_CAPTURE)
            order.addInt32(args[0])
            order.addInt8(args[1])
            self.send_package(order)
        elif msg == "build_complete":
            order = PyDatagram()
            order.addUint16(BUILD_COMPLETE)
            order.addInt32(args[0])
            order.addInt8(args[1])
            order.addString(args[2])
            self.send_package(order)
        elif msg == "build_cancel":
            order = PyDatagram()
            order.addUint16(BUILD_CANCEL)
            order.addInt32(args[0])
            self.send_package(order)
        elif msg == "battle_start":
            order = PyDatagram()
            order.addUint16(BATTLE_START)
            order.addInt32(args[0])
            order.addFloat32(args[1])
            order.addFloat32(args[2])
            order.addInt32(args[3])
            order.addFloat32(args[4])
            order.addFloat32(args[5])
            order.addInt32(args[6])
            self.send_package(order)
        elif msg == "battle_clash":
            order = PyDatagram()
            order.addUint16(BATTLE_CLASH)
            order.addInt32(args[0])
            order.addInt32(args[1])
            order.addInt32(args[2])
            order.addString(args[3])
            order.addInt8(args[4])
            self.send_package(order)
        elif msg == "battle_turn":
            order = PyDatagram()
            order.addUint16(BATTLE_TURN)
            order.addInt32(args[0])
            order.addInt32(args[1])
            self.send_package(order)
        elif msg == "battle_end":
            order = PyDatagram()
            order.addUint16(BATTLE_END)
            order.addInt32(args[0])
            self.send_package(order)
        elif msg == "battle_armyadd":
            order = PyDatagram()
            order.addUint16(BATTLE_ARMYADD)
            order.addInt32(args[0])
            order.addInt32(args[1])
            order.addFloat32(args[2])
            order.addFloat32(args[3])
            self.send_package(order)


    def client_messager(self,msg,args=[]):
        if msg == "chat_send":
            order = PyDatagram()
            order.addUint16(CLIENT_CHAT)
            order.addInt32(args[0][0])
            order.addInt32(args[0][1])
            order.addInt32(args[0][2])
            order.addString(args[1])
            self.send_package(order)
        elif msg == "ready_button":
            order = PyDatagram()
            order.addUint16(CLIENT_READY)
            order.addInt32(args[0])
            order.addInt32(args[1])
            self.send_package(order)
        elif msg == "client_loaded":
            order = PyDatagram()
            order.addUint16(CLIENT_LOADED)
            self.send_package(order)
        elif msg == "game_init_request":
            order = PyDatagram()
            order.addUint16(CLIENT_INIT_REQUEST)
            order.addString(args[0])
            order.addString(args[1])
            self.send_package(order)
        elif msg == "build_start_request":
            order = PyDatagram()
            order.addUint16(BUILD_START_REQUEST)
            order.addInt32(args[0])
            order.addInt32(args[1])
            order.addString(args[2])
            self.send_package(order)
        elif msg == "build_cancel_request":
            order = PyDatagram()
            order.addUint16(BUILD_CANCEL_REQUEST)
            order.addInt32(args[0])
            self.send_package(order)

    def client_processing(self,datagram):
        data_iter = PyDatagramIterator(datagram)
        msgID = data_iter.getUint16()
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
            p1_ready = data_iter.getInt32()
            game_map = data_iter.getInt32()
            base.menu_manager.menus["mp-game"].client_update(p1_name,p1_kingdom,p1_ready,game_map)
        if msgID == SERVER_CHAT:
            r = data_iter.getInt32()
            g = data_iter.getInt32()
            b = data_iter.getInt32()
            text = data_iter.getString()
            base.menu_manager.menus["mp-game"].chat_add((r,g,b),text)
        if msgID == SERVER_READY:
            but_id = data_iter.getInt32()
            state = data_iter.getInt32()
            base.menu_manager.menus["mp-game"].obj_list[but_id]["indicatorValue"]=state
            base.menu_manager.menus["mp-game"].start_game_check()
        if msgID == SERVER_LOADED:
            base.menu_manager.menus["mp-load"].load()
        if msgID == ALL_LOADED:
            base.menu_manager.menus["mp-load"].load_complete()
        if msgID == GAME_START:
            base.menu_manager.menu_goto("mp-load")
        if msgID == MAP_SET:
            map = data_iter.getInt32()
            base.menu_manager.menus["mp-game"].map_selected = map
            mapname = base.menu_manager.menus["mp-game"].maplist[map]["fullname"]
            mapimage = base.menu_manager.menus["mp-game"].maplist[map]["preview"]
            base.menu_manager.menus["mp-game"].obj_list[11]["text"]=mapname
            base.menu_manager.menus["mp-game"].obj_list[10].setImage(mapimage)
        if msgID == BATTLE_TURN:
            bat = data_iter.getInt32()
            turn = data_iter.getInt32()
            base.battles[bat].turn_change(turn)
        if msgID == BATTLE_START:
            a1 = data_iter.getInt32()
            a1_x = data_iter.getFloat32()
            a1_y = data_iter.getFloat32()
            a2 = data_iter.getInt32()
            a2_x = data_iter.getFloat32()
            a2_y = data_iter.getFloat32()
            army_start = data_iter.getInt32()
            base.armies[a1].stop()
            base.armies[a2].stop()
            base.armies[a1].node_path.setPos(a1_x,a1_y,0)
            base.armies[a2].node_path.setPos(a2_x,a2_y,0)
            base.battles.append(TimObjects.Battle([base.armies[a1],base.armies[a2]],army_start))
        if msgID == BATTLE_CLASH:
            battle = data_iter.getInt32()
            a1 = data_iter.getInt32()
            a2 = data_iter.getInt32()
            result = data_iter.getString()
            buff = data_iter.getInt8()
            base.battles[battle].clash(base.armies[a1],base.armies[a2],result,buff)
        if msgID == BATTLE_ARMYADD:
            bat = data_iter.getInt32()
            army = data_iter.getInt32()
            a_x = data_iter.getFloat32()
            a_y = data_iter.getFloat32()
            base.battles[bat].add_army(base.armies[army])
            base.armies[army].node_path.setPos(a_x,a_y,0)
        if msgID == BATTLE_END:
            bat = data_iter.getInt32()
            base.battles[bat].end()
        if msgID == BUILD_START:
            t_id = data_iter.getInt32()
            player = data_iter.getInt8()
            type = data_iter.getString()
            base.towers[t_id].build_start()
        if msgID == TOWER_CAPTURE:
            t_id = data_iter.getInt32()
            player = data_iter.getInt8()
            base.towers[t_id].change_owner(player)
        if msgID == BUILD_CANCEL:
            t_id = data_iter.getInt32()
            base.towers[t_id].build_cancel()
        if msgID == BUILD_COMPLETE:
            t_id = data_iter.getInt32()
            player = data_iter.getInt8()
            type = data_iter.getString()
            base.towers[t_id].create_counter()

    def server_processing(self,datagram):
        data_iter = PyDatagramIterator(datagram)
        msgID = data_iter.getUint16()
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
            r = data_iter.getInt32()
            g = data_iter.getInt32()
            b = data_iter.getInt32()
            text = data_iter.getString()
            self.server_messager("chat_send",[(r,g,b),text])
            #base.main_menu.chat_add((r,g,b,1),text)
        if msgID == CLIENT_READY:
            but_id = data_iter.getInt32()
            state = data_iter.getInt32()
            self.server_messager("ready_button",[but_id,state])
            #base.main_menu.chat_add((r,g,b,1),text)
        if msgID == CLIENT_LOADED:
            self.server_messager("all_loaded",[])
            base.menu_manager.menus["mp-load"].load_complete()
        if msgID == CLIENT_INIT_REQUEST:
            pn = data_iter.getString()
            pk = data_iter.getString()
            base.menu_manager.menus["mp-game"].obj_list[6]["text"] = pn
            base.menu_manager.menus["mp-game"].obj_list[7]["text"] = pk
            self.server_messager("client_update",[base.menu_manager.menus["mp-game"].obj_list[4]["text"],
                                                 base.menu_manager.menus["mp-game"].obj_list[5]["text"],
                                                 base.menu_manager.menus["mp-game"].obj_list[8]["indicatorValue"],
                                                 base.menu_manager.menus["mp-game"].map_selected])
        if msgID == BUILD_START_REQUEST:
            t_id = data_iter.getInt32()
            player = data_iter.getInt32()
            type = data_iter.getString()
            base.towers[t_id].build_start()
        if msgID == BUILD_CANCEL_REQUEST:
            t_id = data_iter.getInt32()
            player = data_iter.getInt32()
            type = data_iter.getString()
            base.towers[t_id].build_cancel()

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
            order.addUint16(ARMY_MOVE_REQUEST)
        else:
            order.addUint16(ARMY_MOVE)
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
            order.addUint16(REQUEST_TOWER_TRAIN)
        else:
            order.addUint16(TOWER_TRAIN)
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
#        order.addUint16(REQUEST_MOVE_COUNTER)
#        order.addInt16(army_id)
#        order.addFloat64(tx)
#        order.addFloat64(ty)
#        self.cWriter.send(order,base.server_connection)

    def myNewPyDatagram(self):
        # Send a test message
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint16(PRINT_MESSAGE)
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