import pyglet.graphics
import pyglet.window
import datetime
#import global_vars as g
import base64
import json
import copy
import os
import sys
import hashlib
from pyglet_gui.containers import VerticalContainer
from pyglet.gl import *
from twisted.internet import reactor, error
from twisted.internet.task import LoopingCall
from twisted.internet.protocol import Protocol, Factory, ClientFactory
from twisted.protocols.basic import LineReceiver
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Frame, Spacer, Label
from pyglet_gui.theme import Theme

theme = Theme({"font": "Segoe UI",
               "font_size":26,
               "text_color":(255,255,255,255)},resources_path=None)
ServerPackets = {
    "SendHashes":1,
    "SendFileInfo":2,
    "DownloadFinished":3,
    "DownloadSize":4
}
ClientPackets = {
    "SendHashes":1,
    "Received":2,
    "Validating":3
}
MODE_INIT=0
MODE_CONNECTING=1
MODE_CONNECTED=2
MODE_DISCONNECTED=3
MODE_CONNECTIONFAILED=4
MODE_CHECKINGINTEGRITY=5
MODE_FOUND_UPDATED=6
MODE_NOTFOUND=7
MODE_RAWMODE=8
MODE_DOWNLOADING=9
MODE_VALIDATING=10
def startConnection():
    factory = gameClientFactory()
    updater.connector = reactor.connectTCP("updater.sakkee.org",2728,factory)
    return factory.protocol
def closeConnection():
    updater.connector.disconnect()
    factory = gameClientFactory()
    updater.connector = reactor.connectTCP("updater.sakkee.org", 2728, factory)
class Updater:

    def loopFunction(self):
        
        self.screen.clear()
        self.currTick = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
        if self.toConnect and self.currTick>self.nextConnect+3000:
            self.initConnection()
            
        if self.screen.has_exit:
            reactor.stop()
        if self.mode==MODE_CONNECTING:
            if self.currTick-self.lastMoveTick>500:
                self.updateConnectText()
                self.lastMoveTick=self.currTick
                
        self.screen.dispatch_events()
        self.guiBatch.draw()
        self.screen.flip()
    def updateConnectText(self):
        if self.animationStep==0:
            self.statusText.set_text("Connecting :D")
            self.animationStep+=1
        elif self.animationStep==1:
            self.statusText.set_text("Connecting :D :D")
            self.animationStep+=1
        elif self.animationStep==2:
            self.statusText.set_text("Connecting :D :D :D")
            self.animationStep+=1
        else:
            self.statusText.set_text("Connecting")
            self.animationStep=0
    
    def removeEmptyDicts(self,dic):
        def removeEmpties(dic2, keys):
            for k, v in dic2.iteritems():
                if isinstance(v, basestring):
                    pass
                elif isinstance(v,dict):
                    if len(v)==0 or k is None:
                        asd=keys+[k]
                        del reduce(lambda a,b:a[b],asd[:-1],dic)[asd[-1]]
                    else:
                        removeEmpties(v,keys+[k])
        n=0
        
        while n < 10:
            removeEmpties(copy.deepcopy(dic),[])
            n+=1
        
    def checkFiles(self,argument,dict,first=False):
        for f1 in os.listdir(argument):
            if f1  not in self.ignores:
                if os.path.isdir(argument+'/'+f1):
                    if not first:
                        dict[f1]={}
                        self.checkFiles(argument+'/'+f1,dict[f1])
                    else:
                        dict[f1]={}
                        self.checkFiles(f1,dict[f1])
                else:
                    dict[f1]=hashlib.md5(open(argument+'/'+f1,'rb').read()).hexdigest()
        return dict
    def myprint(self,t,d,keys):
      for k, v in t.iteritems():
        if isinstance(v, dict):
            if k in d:
                self.myprint(v,d[k],keys+[k])
            else:
                pass
                #print "NO DIRECTORY NAMED", k,keys
        else:
            if k in d:
                if v==d[k]:
                    asd=keys+[k]
                    del reduce(lambda a, b: a[b], asd[:-1], self.copiedList)[asd[-1]] 
                else:
                    filename=''
                    a=0
                    for i in keys+[k]:
                        if a==0:
                            filename=i
                        else:
                            filename+='/'+i
                        a+=1
                    os.remove(filename)
                    #pass
                    #print "WRONG FILE", k, v, d[k]
            else:
                pass
                #print "NO FILE NAMED", k, v, keys
    def initManager(self):
        self.mode=MODE_CONNECTING
        self.guiBatch = pyglet.graphics.Batch()
        self.statusText = Label("Connecting",color=(255,255,255,255))
        self.downloadText=Label("",color=(255,255,255,255))
        self.manager = Manager(VerticalContainer([self.statusText,self.downloadText]),window=self.screen,batch=self.guiBatch,theme=theme)
    def init(self):
        self.mode=MODE_INIT
        self.lastMoveTick=0
        self.animationStep=0
        self.receivedHashes={}
        self.copiedList={}
        self.myHashes={}
        self.downloadSize=0
        self.downloaded=0
        
        self.nextConnect=0
        self.toConnect=False
        self.ignores=['screenshots','temp','test.py','game.cfg','updater.py','pyglet_gui']
        s_width = pyglet.window.get_platform().get_default_display().get_default_screen().width
        s_height = pyglet.window.get_platform().get_default_display().get_default_screen().height
        self.screen = pyglet.window.Window(fullscreen=False,width=550,height=400,style=pyglet.window.Window.WINDOW_STYLE_DIALOG)
        self.screen.set_location((s_width-550)/2,(s_height-400)/2)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        self.initManager()
        tick = LoopingCall(self.loopFunction)
        tick.start(1./300)
        self.initConnection()
        #connectionProtocol = startConnection()
        #self.tcpConn = TCPConnection(connectionProtocol)
        reactor.run()
    def initConnection(self):
        self.toConnect=False
        self.receivedHashes={}
        self.maxRounds=0
        self.currentRound=0
        self.copiedList={}
        self.myHashes={}
        self.downloadSize=0
        self.downloaded=0
        self.animationStep=0
        self.mode=MODE_CONNECTING
        connectionProtocol = startConnection()
        self.tcpConn = TCPConnection(connectionProtocol)
        
    def checkFiles(self,argument,dict,first=False):
        for f1 in os.listdir(argument):
            if f1  not in self.ignores:
                if os.path.isdir(argument+'/'+f1):
                    if not first:
                        dict[f1]={}
                        self.checkFiles(argument+'/'+f1,dict[f1])
                    else:
                        dict[f1]={}
                        self.checkFiles(f1,dict[f1])
                else:
                    dict[f1]=hashlib.md5(open(argument+'/'+f1,'rb').read()).hexdigest()
        return dict
        
    def constructPath(self, args):
        string=""
        first=True
        for arg in args:
            string = string+arg+'/'
            
            #if first:
            #    string=arg
            #    first=False
            #else:
            #    string=string+"/"+arg
        return string
    def myprint1(self, d, args):
        for k, v in d.iteritems():
            if isinstance(v, dict):
                newArgs=args+[k]
                self.myprint1(v,newArgs)
            else:
                path = self.constructPath(args) + k  
                isExisting = os.path.isfile(path)
                if isExisting:
                    md5hash = hashlib.md5(open(path,'rb').read()).hexdigest()[:4]
                    if md5hash!=v:
                        pass
                        #print "vaara tiedosto!" + md5hash + " vs. " + v
                    else:
                        asd=args+[k]
                        del reduce(lambda a, b: a[b], asd[:-1], self.receivedHashes)[asd[-1]] 
                        #print "{0} : {1} in {2}, {3}".format(k, v, path, md5hash)
                else:
                    pass
                    #print k +" ei loytynyt!"
    def checkTesti(self, arguments, dict, first=False):
        path = self.constructPath(arguments)
        for f1 in os.listdir(path):
            #if f1 not in self.ignores:
            newArgs = arguments.append(f1)
            newPath = self.constructPath(arguments)
            #if os.path.isdir(newPath):
            #        self.
            #print f1
        #print path
        return None, None
        #for f1 in os.listdir()
    def checkFilePaskas(self):
        #print self.copiedList
        self.currentFolder=[]
        self.currentDepth=0
        self.testi={}
        self.args=[]
        self.myprint1(self.copiedList, [])
        self.removeEmptyDicts(self.receivedHashes)
        #self.checkTesti(self.args, self.copiedList, True)
        '''
        for i in self.copiedList:
            self.currentDepth=0
            if type(self.copiedList[i]) is dict:
                for j in self.currentFolder[i]:
                    self.currentDepth=1
                    if type(self.copiedList[i]) is dict:
                        for k in self.currentFolder[i][j]:
                            self.currentDepth=2
                            if type(self.copiedList[i][j][k]) is dict:
                                for m in self.currentFolder[i][j][k]:
                                    self.currentDepth=3
            else:'''
                
                
    #def loopFiles():
    def dataHandler(self,data):
        jsonData = json.loads(data)
        packetType = jsonData[0]["p"]
        #print jsonData
        if packetType == ServerPackets["SendHashes"]:
            
            self.receivedHashes=jsonData[0]["d"]
            self.maxRounds=jsonData[0]["r"]
            self.currentRound=jsonData[0]["c"]
            validating=jsonData[0]["v"]
            self.copiedList=copy.deepcopy(self.receivedHashes)
            self.mode=MODE_CHECKINGINTEGRITY
            self.statusText.set_text("Checking for integrity...")
            self.checkFilePaskas();
            if len(self.receivedHashes)>0:
                updater.mode=MODE_FOUND_UPDATED
                updater.statusText.set_text("Found an update!")
                packet = json.dumps([{"p": ClientPackets["SendHashes"], 'd':self.receivedHashes}])
                self.tcpConn.sendData(packet)
            elif self.currentRound==self.maxRounds or validating:
                updater.mode=MODE_NOTFOUND
                updater.statusText.set_text("The game is up to date! Launching the game...")
                self.downloadText.set_text('')
                os.startfile('Spurdola.exe')
                reactor.stop()
            else:
                packet = json.dumps([{"p": ClientPackets["Received"]}])
                updater.tcpConn.sendData(packet)
                #print self.copiedList
            #self.myHashes=self.checkFiles(".",self.myHashes,True)
            
            '''
            self.myprint(self.receivedHashes,self.myHashes,[])
            self.removeEmptyDicts(self.copiedList)
            if len(self.copiedList)>0:
                updater.mode=MODE_FOUND_UPDATED
                updater.statusText.set_text("Found an update!")
                packet = json.dumps([{"p": ClientPackets["SendHashes"], 'd':self.copiedList}])
                self.tcpConn.sendData(packet)
            elif self.currentRound==self.maxRounds or validating:
                updater.mode=MODE_NOTFOUND
                updater.statusText.set_text("The game is up to date! Launching the game...")
                self.downloadText.set_text('')
                os.startfile('Golden ES.exe')
                reactor.stop()
            else:
                packet = json.dumps([{"p": ClientPackets["Received"]}])
                updater.tcpConn.sendData(packet)
                #print self.copiedList
            '''
        elif packetType == ServerPackets["SendFileInfo"]:
            self.file_data=[jsonData[0]["d"],jsonData[0]["h"]]
            self.mode=MODE_RAWMODE
        elif packetType == ServerPackets["DownloadFinished"]:
            self.mode=MODE_VALIDATING
            updater.statusText.set_text("Validating...")
            packet = json.dumps([{"p": ClientPackets["Validating"]}])
            self.tcpConn.sendData(packet)
            #self.mode=MODE_NOTFOUND
            #updater.statusText.set_text("The game is up to date! Launching the game...")
            #self.downloadText.set_text('')
            #os.startfile('goldenes.exe')
            #reactor.stop()
        elif packetType==ServerPackets["DownloadSize"]:
            self.downloadSize=jsonData[0]["d"]
    def updateDownloadText(self):
        downloaded=self.downloaded/1000000.0
        downloadable=self.downloadSize/1000000.0
        self.downloadText.set_text('{}/{} MB'.format("%.2f" % downloaded,'%.2f' %downloadable))
        #print self.receivedData
        
class gameClientProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
    
    def connectionMade(self):
        #print "CONNECTED"
        updater.file_handler = None
        updater.file_data={}
        updater.mode=MODE_CONNECTED
        updater.statusText.set_text("Connected!")
        #if g.gameState == GAMESTATE_LOGIN:
        #    g.tcpConn.sendLogin(g.gameEngine.loginMenu.username,g.gameEngine.loginMenu.password)
        
    def lineReceived(self, data):
        #global dataHandler
        decodedData = base64.b64decode(data)
        #print decodedData
        updater.dataHandler(decodedData)
        if updater.mode==MODE_RAWMODE:
            self.setRawMode()
    def rawDataReceived(self,data):
        updater.mode=MODE_DOWNLOADING
        updater.statusText.set_text("Downloading...")
        filepath = ''
        a=0
        updater.downloaded+=len(data)
        updater.updateDownloadText()
        #print updater.downloaded,updater.downloadSize
        for i in updater.file_data[0]:
            if a==0:
                filepath=i
            else:
                filepath+='/'+i
            if a<len(updater.file_data[0])-1:
                if not os.path.isdir(filepath):
                    os.makedirs(filepath)
            a+=1
        if not updater.file_handler:
            updater.file_handler=open(filepath,'wb')
        if data.endswith('\r\n'):
            data=data[:-2]
            updater.file_handler.write(data)
            self.setLineMode()
            updater.file_handler.close()
            updater.file_handler=None
            packet = json.dumps([{"p": ClientPackets["Received"]}])
            updater.tcpConn.sendData(packet)
        else:
            updater.file_handler.write(data)
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
        updater.mode=MODE_CONNECTIONFAILED
        updater.statusText.set_text("Connection failed ;_; Server down?")
        updater.toConnect=True
        updater.nextConnect=updater.currTick
        #updater.initConnection()
        #print reason.getErrorMessage()
    def clientConnectionLost(self, connector, reason):
        updater.file_handler = None
        updater.file_data={}
        updater.mode=MODE_DISCONNECTED
        updater.statusText.set_text("Connection lost :(")
        updater.toConnect=True
        updater.nextConnect=updater.currTick
        
class TCPConnection():
    def __init__(self, protocol):
        self.protocol = protocol
    def sendData(self, data):
        self.protocol.sendData(data)
updater = Updater()
updater.init()
