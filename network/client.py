from twisted.internet.protocol import Protocol, Factory, ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, error
import json
import base64
from constants import *
import global_vars as g
from objects import *
from utils.utils import *
from gamelogic import *
#from database import *
from packettypes import *
from datahandler import *
from gui.popupWindow import popUpWindow

dataHandler = None
def startConnection():
    global dataHandler
    if not g.isConnected:
        g.isConnected = True
        factory = gameClientFactory()
        #g.connectedToLoginServer=True
        g.connector = reactor.connectTCP(g.gameIP,g.gamePORT,factory)
        dataHandler = DataHandler()
    else:
        #print "TAA TAPAHTU"
        g.connector.disconnect()
        #g.connectedToLoginServer=False
        factory = gameClientFactory()
        g.connector = reactor.connectTCP(g.gameIP, g.gamePORT, factory)
        dataHandler = DataHandler()
    return factory.protocol
def closeConnection():
    global dataHandler
    if g.isConnected:
        g.connector.disconnect()
        factory = gameClientFactory()
        g.connector = reactor.connectTCP(g.gameIP, g.gamePORT, factory)
        dataHandler = DataHandler()
    
class gameClientProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        
    
    def connectionMade(self):
        #if g.gameState == GAMESTATE_LOGIN:
        #    g.tcpConn.sendLogin(g.gameEngine.loginMenu.username,g.gameEngine.loginMenu.password)
        self.transport.setTcpNoDelay(True)
        #print self.transport.getTcpNoDelay()
    def lineReceived(self, data):
        global dataHandler
        
            
        decodedData = base64.b64decode(data)
        #log("Received data from server")
        #log(" -> " + decodedData)
        jsonData=decodeJSON(decodedData)
        if g.connectedToLoginServer:
            dataHandler.handleLoginData(jsonData)
        else:
            if type(jsonData) is dict:
                dataHandler.handleData(jsonData)
            elif type(jsonData) is list:
                for d in jsonData:
                    dataHandler.handleData(d)
    def sendData(self, data):
        encodedData = base64.b64encode(data)
        self.sendLine(encodedData)

class gameClientFactory(ClientFactory):
    def __init__(self):
        self.protocol = p = gameClientProtocol(self)
    def startedConnecting(self, connector):
        pass
    def buildProtocol(self, addr):
        return self.protocol
    def clientConnectionFailed(self, connector, reason):
        popUpWindow("Couldn't connect to " + GAME_IP)
        print reason.getErrorMessage()
    def clientConnectionLost(self, connector, reason):
        popping=False
        if g.gameState != GAMESTATE_LOGIN and g.gameState!=GAMESTATE_AUTH:
            popping=True
            changeGameState(GAMESTATE_LOGIN)
        if g.banned is not None:
            popUpWindow(g.banned)
            g.gameIP=GAME_IP
            g.gamePORT=GAME_PORT
            g.connectedToLoginServer=True
        elif popping:
            popUpWindow("Disconnected from the server.")
            g.gameIP=GAME_IP
            g.gamePORT=GAME_PORT
            g.connectedToLoginServer=True
        #elif not g.updateAvailable:
        #    popUpWindow("Username or password wrong!")
        g.banned=None
        g.updateAvailable=False
        print reason.getErrorMessage()
        
class TCPConnection():
    def __init__(self, protocol):
        self.protocol = protocol
    def sendData(self, data):
        self.protocol.sendData(data)
        
    #def sendLogin(self,username,password):
    #    packet = json.dumps([{"p": ClientPackets.Login, "name": username, "password": password,'v':GAME_VERSION}])
    #    self.sendData(packet)
    
    
    #def sendMapRequest(self,)