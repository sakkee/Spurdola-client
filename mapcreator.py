import pygame
from objects import *
from constants import *
from pgu import gui
import pickle
import os
from utils import undo
import ntpath
import json
import re
import pyglet
import time
pyglet.lib.load_library('data/avbin')
pyglet.have_avbin=True
background_colour = (60,60,60)
fontcolor=(255,255,255)
(width, height) = (1800, 960)
screen = pygame.display.set_mode((width, height),pygame.DOUBLEBUF)
surface = pygame.Surface((32,32))
surface.fill((255,255,255))
surface.set_colorkey((255,255,255))
surface.blit(pygame.image.load('data/icons/favico.png').convert_alpha(),(0,0))
pygame.display.set_icon(surface)
pygame.display.set_caption('Kultainen ES Map Editor')
pygame.display.flip()



class MenuObjects(gui.Menus):
    def __init__(self,**params):
        self.saved=False
        def fnc_open(argument):
            a = gui.FileDialog(path="data/maps/")
            a.connect(gui.CHANGE,selectFile1,a)
            self.engine.engine.dialogOpened=True
            a.open()
            
        def fnc(x):
            if x=='New':
                self.engine.engine.Map = MapClass()
                self.engine.engine.Map.tile = [[TileClass() for i in range(self.engine.engine.Map.height)] for i in range(self.engine.engine.Map.width)]
                self.engine.engine.mapProps.mapNameInput._setvalue(self.engine.engine.mapName)
                self.engine.engine.mapProps.musicNameInput._setvalue(self.engine.engine.Map.song)
                self.engine.engine.mapProps.deathTeleportInput._setvalue(self.engine.engine.Map.death[0])
                self.engine.engine.mapProps.deathXInput._setvalue(str(self.engine.engine.Map.death[1]))
                self.engine.engine.mapProps.deathYInput._setvalue(str(self.engine.engine.Map.death[2]))
                self.engine.engine.mapProps.mapWidthInput._setvalue(str(self.engine.engine.Map.width))
                self.engine.engine.mapProps.mapHeightInput._setvalue(str(self.engine.engine.Map.height))
                self.engine.engine.mapSurface = pygame.transform.scale(self.engine.engine.mapSurface,(TILESIZE*self.engine.engine.Map.width,TILESIZE*self.engine.engine.Map.height))
                
                self.engine.engine.map.updateScroll()
                self.engine.engine.buttons.switchDisabled()
                self.engine.engine.oldFile=None
                self.engine.engine.mapLoaded = True
                #self.fncSave()
                #self.selectFile(self.engine.engine.openedFile)
                self.saved=True
            elif x=='Save':
                self.fncSave()
                self.engine.engine.oldFile = 'data/maps/'+self.engine.engine.mapName + '.map'
        data = [
            ('File/Open', fnc_open,None),
            ('File/Save', fnc, 'Save'),
            ('File/New', fnc, "New")
        ]
        gui.Menus.__init__(self,data,**params)
        self.engine = None
        def selectFile1(object):
            self.selectFile(object.value)
            self.engine.engine.dialogOpened=False
            self.engine.engine.oldFile = object.value
    def fncSave(self):
        if self.engine.engine.error==2:
            self.engine.engine.error=0
        tmpMap = self.engine.engine.Map.__dict__
        tiles=[]
        for x in range(tmpMap["width"]):
            tilesX=[]
            for y in range(tmpMap["height"]):
                tmpTile = TileClass()
                tmpTile.l1 = tmpMap["tile"][x][y].l1
                tmpTile.l2 = tmpMap["tile"][x][y].l2
                tmpTile.l3 = tmpMap["tile"][x][y].l3
                tmpTile.f = tmpMap["tile"][x][y].f
                tmpTile.d1 = tmpMap["tile"][x][y].d1
                tmpTile.d2 = tmpMap["tile"][x][y].d2
                tmpTile.t = tmpMap["tile"][x][y].t
                tmpTile.d3 = tmpMap["tile"][x][y].d3
                tilesX.append(tmpTile.__dict__)
            tiles.append(tilesX)
        tmpMap["tile"]=tiles
        #print tiles
        try:
            os.rename(self.engine.engine.oldFile, "data/maps/temp/"+os.path.basename(os.path.normpath(self.engine.engine.oldFile)))
        except Exception, e:
            try:
                os.remove("data/maps/temp/"+os.path.basename(os.path.normpath(self.engine.engine.oldFile)))
                os.rename(self.engine.engine.oldFile, "data/maps/temp/"+os.path.basename(os.path.normpath(self.engine.engine.oldFile)))
            except Exception, e:
                self.engine.engine.error=8
                self.engine.engine.header.updateErrorMsg()
        with open('data/maps/'+self.engine.engine.mapName+'.map','w') as fp:
            json.dump(tmpMap, fp)
        
        self.selectFile('data/maps/'+self.engine.engine.mapName+'.map')
        #else:
        #    self.engine.engine.error=2
        #    self.engine.updateErrorMsg()
        #print str(e)
        
    def selectFile(self,text):
        self.engine.engine.openedFile=text
        #try:
        if text:
            with open(self.engine.engine.openedFile,'r') as fp:
                tempMap = json.load(fp)
            self.engine.engine.Map.width = tempMap["width"]
            self.engine.engine.Map.height = tempMap["height"]
            self.engine.engine.Map.song = tempMap["song"]
            self.engine.engine.Map.menes = tempMap["menes"]
            try:
                self.engine.engine.Map.death[:] = tempMap["death"] 
            except Exception, e:
                self.engine.engine.Map.death[:] = ["",0,0]
            self.engine.engine.Map.tile = [[TileClass() for i in range(tempMap["height"])] for i in range(tempMap["width"])]
            tmpTiles = []
            for x in range(tempMap["width"]):
                tmpTilesW=[]
                for y in range(tempMap["height"]):
                    tmpTile = TileClass()
                    tmpTile.l1 = tempMap['tile'][x][y]["l1"]
                    tmpTile.l2 = tempMap['tile'][x][y]["l2"]
                    tmpTile.l3 = tempMap['tile'][x][y]["l3"]
                    tmpTile.f = tempMap['tile'][x][y]["f"]
                    tmpTile.t = tempMap['tile'][x][y]["t"]
                    
                    tmpTile.d1 = tempMap['tile'][x][y]["d1"]
                    tmpTile.d2= tempMap['tile'][x][y]["d2"]
                    tmpTile.d3 = tempMap['tile'][x][y]["d3"]
                    tmpTilesW.append(tmpTile)
                tmpTiles.append(tmpTilesW)
            self.engine.engine.Map.tile = tmpTiles
            
        else:
            self.engine.engine.openedFile='data/maps/.map'
        self.engine.engine.error=0
        
        tmpStr = os.path.basename(os.path.normpath(self.engine.engine.openedFile))
        tmpStr = tmpStr.split('.')[0]
        self.engine.engine.mapName = tmpStr
        self.engine.engine.mapProps.deathTeleportInput._setvalue(self.engine.engine.Map.death[0])
        self.engine.engine.mapProps.deathXInput._setvalue(str(self.engine.engine.Map.death[1]))
        self.engine.engine.mapProps.deathYInput._setvalue(str(self.engine.engine.Map.death[2]))
        self.engine.engine.mapProps.mapNameInput._setvalue(self.engine.engine.mapName)
        self.engine.engine.mapProps.musicNameInput._setvalue(str(self.engine.engine.Map.song))
        self.engine.engine.mapProps.mapWidthInput._setvalue(str(self.engine.engine.Map.width))
        self.engine.engine.mapProps.mapHeightInput._setvalue(str(self.engine.engine.Map.height))
        #if len(self.engine.engine.Map.menes)>0:
        self.engine.engine.mapProps.populateTypeList2()
        #    #self.engine.engine.mapProps.typeList2.value=self.engine.engine.Map.menes[0][0]
        self.engine.engine.mapSurface = pygame.transform.scale(self.engine.engine.mapSurface,(TILESIZE*self.engine.engine.Map.width,TILESIZE*self.engine.engine.Map.height))
        self.engine.engine.map.updateScroll()
        self.engine.engine.buttons.switchDisabled()
        self.engine.engine.mapLoaded = True
        

class LayerButtons(gui.Container):
    def __init__(self,**params):
        gui.Container.__init__(self,**params)
        self.engine=None
        def fnc1(self):
            self.engine.selectedLayer = 0
            self.engine.showTileTypes = False
        def fnc2(self):
            self.engine.selectedLayer = 1
        def fnc3(self):
            self.engine.selectedLayer = 2
        def fnc4(self):
            self.engine.selectedLayer = 3
        def fnc5(self):
            self.engine.selectedLayer = 4
        def fnc6(self):
            if self.engine.showTileTypes:
                self.engine.showTileTypes = False
            else:
                self.engine.showTileTypes = True
        
        self.button1 = gui.Button("Default view", width=125,height=40,disabled=True)
        self.button1.connect(gui.CLICK,fnc1,self)
        
        self.button2 = gui.Button("Layer 1", width=125,height=40,disabled=True)
        self.button2.connect(gui.CLICK,fnc2,self)
        
        self.button3 = gui.Button("Layer 2", width=125,height=40,disabled=True)
        self.button3.connect(gui.CLICK,fnc3,self)
        
        self.button4 = gui.Button("Layer 3", width=125,height=40,disabled=True)
        self.button4.connect(gui.CLICK,fnc4,self)
        
        self.button5 = gui.Button("Layer fringe", width=125,height=40,disabled=True)
        self.button5.connect(gui.CLICK,fnc5,self)
        
        self.button6 = gui.Button("Show tile types", width=125,height=40,disabled=True)
        self.button6.connect(gui.CLICK,fnc6,self)
        
        """
        self.group = gui.Group(name='Insert tool', value='Nothing')
        
        self.radiobutton1 = gui.Radio(self.group,'0')
        self.radiobutton2 = gui.Radio(self.group,'1')
        """
        def fnc7(self):
            if self.g.value == 'block' or self.g.value == 'npcavoid' or self.g.value == 'teleport' or self.g.value=='fight':
                self.engine.selectedLayer = 0
                self.engine.showTileTypes = True
        self.g = gui.Group(name='Tool',value='default')
        self.g.connect(gui.CHANGE,fnc7,self)
        t = gui.Table()
        t.tr()
        t.td(gui.Label('Select',color=fontcolor),height=40,align=-1,width=120)
        t.td(gui.Radio(self.g,'default'),height=40,align=1)
        t.tr()
        t.td(gui.Label('Remove',color=fontcolor),height=40,align=-1,width=120)
        t.td(gui.Radio(self.g,'remove'),height=40,align=1)
        t.tr()
        t.td(gui.Label('Paint',color=fontcolor),height=40,align=-1,width=120)
        t.td(gui.Radio(self.g,'paint'),height=40,align=1)
        t.tr()
        t.td(gui.Label('Block',color=fontcolor),height=40,align=-1,width=120)
        t.td(gui.Radio(self.g,'block'),height=40,align=1)
        t.tr()
        t.td(gui.Label('NPC avoid',color=fontcolor),height=40,align=-1,width=120)
        t.td(gui.Radio(self.g,'npcavoid'),height=40,align=1)
        t.tr()
        t.td(gui.Label('Teleport',color=fontcolor),height=40,align=-1,width=120)
        t.td(gui.Radio(self.g,'teleport'),height=40,align=1)
        t.tr()
        t.td(gui.Label('Fight',color=fontcolor),height=40,align=-1,width=120)
        t.td(gui.Radio(self.g,'fight'),height=40,align=1)
        
        
        def fnc8(self):
            undo.stack().undo()
        self.button7 = gui.Button("Undo (Ctrl+Z)", width=125,height=40)
        self.button7.connect(gui.CLICK,fnc8,self)
        def fnc9(self):
            undo.stack().redo()
            
        self.button8 = gui.Button("Redo (Ctrl+Y)", width=125,height=40)
        self.button8.connect(gui.CLICK,fnc9,self)
        
        self.btnPlay = gui.Button("Play",width=125,height=40)
        self.btnPlay.connect(gui.CLICK,self.fncPlay)
        
        @undo.undoable
        def fnc10(argument):
            if argument=='right':
                empty=[]
                for i in xrange(len(self.engine.Map.tile[0])):
                    empty.append(TileClass())
                self.engine.Map.tile.insert(0,empty)
                yield
                del self.engine.Map.tile[0]
            elif argument=='down':
                for x in xrange(len(self.engine.Map.tile)):
                    self.engine.Map.tile[x].insert(0,TileClass())
                yield
                for x in xrange(len(self.engine.Map.tile)):
                    del self.engine.Map.tile[x][0]
            elif argument=='left':
                tmpTiles=self.engine.Map.tile[0]
                empty=[]
                for i in xrange(len(self.engine.Map.tile[0])):
                    empty.append(TileClass())
                del self.engine.Map.tile[0]
                self.engine.Map.tile.append(empty)
                yield
                self.engine.Map.tile.insert(0,tmpTiles)
                del self.engine.Map.tile[-1]
            elif argument=='up':
                tmpTiles=[]
                for x in xrange(len(self.engine.Map.tile)):
                    tmpTiles.append(self.engine.Map.tile[x][0])
                    del self.engine.Map.tile[x][0]
                    self.engine.Map.tile[x].append(TileClass())
                yield
                for x in xrange(len(self.engine.Map.tile)):
                    self.engine.Map.tile[x].insert(0,tmpTiles[x])
                    del self.engine.Map.tile[x][-1]
                    
        self.btnUp = gui.Button("Up",width=40,height=40)
        self.btnDown=gui.Button("Down",width=40,height=40)
        self.btnRight = gui.Button("Right",width=40,height=40)
        self.btnLeft = gui.Button("Left",width=40,height=40)
        self.btnUp.connect(gui.CLICK,fnc10,"up")
        self.btnDown.connect(gui.CLICK,fnc10,"down")
        self.btnLeft.connect(gui.CLICK,fnc10,"left")
        self.btnRight.connect(gui.CLICK,fnc10,"right")
        
        t1=gui.Table()
        t1.td(gui.Spacer(0, 0))
        t1.td(self.btnUp)
        t1.td(gui.Spacer(0,0))
        t1.tr()
        t1.td(self.btnLeft)
        t1.td(gui.Spacer(0,0))
        t1.td(self.btnRight)
        t1.tr()
        t1.td(gui.Spacer(0,0))
        t1.td(self.btnDown)
        self.add(self.button1,0,0)
        self.add(self.button2,0,self.button1.style.height+10)
        self.add(self.button3,0,(self.button1.style.height+10)*2)
        self.add(self.button4,0,(self.button1.style.height+10)*3)
        self.add(self.button5,0,(self.button1.style.height+10)*4)
        self.add(self.button6,0,(self.button1.style.height+10)*5)
        self.add(t,0,(self.button1.style.height+10)*6)
        self.add(self.button7,0,(self.button1.style.height+10)*12)
        self.add(self.button8,0,(self.button1.style.height+10)*13)
        self.add(self.btnPlay,0,(self.button1.style.height+10)*14.5)
        self.add(t1,0,(self.button1.style.height+10)*15.5)
    def fncPlay(self):
        if self.engine.playing:
            self.engine.playing = False
        else:
            self.engine.testPlay.initatePlay()
            self.engine.playing = True
            
    def switchDisabled(self):
        if self.button1.disabled and self.engine.Map.tile != []:
            self.button1.disabled = False
            self.button2.disabled = False
            self.button3.disabled = False
            self.button4.disabled = False
            self.button5.disabled = False
            self.button6.disabled = False
        elif self.engine.Map.tile==[]:
            self.button1.disabled = True
            self.button2.disabled = True
            self.button3.disabled = True
            self.button4.disabled = True
            self.button5.disabled = True
            self.button6.disabled = True
        
class Header(gui.Container):
    def __init__(self,**params):
        gui.Container.__init__(self,**params)
        self.engine = None
        self.w = MenuObjects()
        self.w.engine = self
        self.add(self.w,0,0)
        self.d = gui.Label("Please open a file...",color=fontcolor)
        self.add(self.d,(width-self.d.style.width)/2,(25-self.d.style.height)/2)
        
    def changeText(self,value):
        if self.engine.error==0:
            self.d.set_text(value)
            self.d.style.x=(width-self.d.font.size(value)[0])/2
        else:
            self.updateErrorMsg()
            
    def updateErrorMsg(self):
        if self.engine.error!=0:
            self.d.set_text(self.engine.errorMessages[self.engine.error-1])
            self.d.style.x=(width-self.d.font.size(self.engine.errorMessages[self.engine.error-1])[0])/2
            
class TileScroller(gui.ScrollArea):
    def __init__(self,**params):
        self.engine = None
        self.hovering = True
        self.mousex=0
        self.mousey=0
        self.selectedX=-1
        self.selectedY=-1
        self.tileSurface = pygame.Surface((9*64,10*64))
        
    def drawTileScroller(self):
        self.tileSurface.fill((0,0,0))
        self.tileSurface.blit(self.engine.map.groundSurface,(0,0))
        self.mapping = gui.Image(self.tileSurface)
        gui.ScrollArea.__init__(self,self.mapping,width=9*64+16,height=10*64+16,step=TILESIZE)
    def updateScrollSize(self):
        if self.engine.map.tileSheets[self.engine.tilePicker.typeList.value][self.engine.tilePicker.typeList1.value].get_width()<9*64 and self.engine.map.tileSheets[self.engine.tilePicker.typeList.value][self.engine.tilePicker.typeList1.value].get_height() < 10*64:
            self.tileSurface = pygame.Surface((9*64,10*64))
        elif self.engine.map.tileSheets[self.engine.tilePicker.typeList.value][self.engine.tilePicker.typeList1.value].get_width()<9*64:
            self.tileSurface = pygame.Surface((9*64,self.engine.map.tileSheets[self.engine.tilePicker.typeList.value][self.engine.tilePicker.typeList1.value].get_height()))
        elif self.engine.map.tileSheets[self.engine.tilePicker.typeList.value][self.engine.tilePicker.typeList1.value].get_height()<10*64:
            self.tileSurface = pygame.Surface((self.engine.map.tileSheets[self.engine.tilePicker.typeList.value][self.engine.tilePicker.typeList1.value].get_width(),10*64))
        else:
            self.tileSurface = pygame.Surface((self.engine.map.tileSheets[self.engine.tilePicker.typeList.value][self.engine.tilePicker.typeList1.value].get_width(),self.engine.map.tileSheets[self.engine.tilePicker.typeList.value][self.engine.tilePicker.typeList1.value].get_height()))
        self.tileSurface.blit(self.engine.map.tileSheets[self.engine.tilePicker.typeList.value][self.engine.tilePicker.typeList1.value],(0,0))
        
        self.mapping.style.width=self.tileSurface.get_width()
        self.mapping.style.height=self.tileSurface.get_height()

        self.resize()
        
    def updateTileScroller(self):
        self.tileSurface.fill((0,0,0))
        self.tileSurface.blit(self.engine.map.tileSheets[self.engine.tilePicker.typeList.value][self.engine.tilePicker.typeList1.value],(0,0))
        if self.hovering:
            self.tileSurface.blit(self.engine.map.hoverSprite,(self.mousex*TILESIZE,self.mousey*TILESIZE))
        if self.selectedX!=-1 and self.selectedY!=-1:
            self.tileSurface.blit(self.engine.map.selectedSprite,(self.selectedX*TILESIZE,self.selectedY*TILESIZE))
        self.mapping.repaint(self.tileSurface)
    def drawHover(self,x,y,checker):
        self.mousex = x//TILESIZE
        self.mousey = y//TILESIZE
        if checker:
            self.selectedX=self.mousex
            self.selectedY=self.mousey
            try:
                self.engine.map.paintSurface.fill((0,0,0))
                self.engine.map.paintSurface.set_colorkey((0,0,0))
                self.engine.map.paintSurface.blit(self.engine.map.tileSheets[self.engine.tilePicker.typeList.value][self.engine.tilePicker.typeList1.value],(0,0),(self.selectedX*TILESIZE,self.selectedY*TILESIZE,TILESIZE,TILESIZE))
                self.engine.error=0
            except:
                self.engine.error=7
                self.engine.header.updateErrorMsg()
        
class TilePicker(gui.Container):
    def __init__(self,**params):
        gui.Container.__init__(self,**params)
        self.engine=None
        self.hovering=True
        label1 = gui.Label("Select tilesheet: ",color=fontcolor,width=125)
        self.add(label1,0,7)
        self.typeList = gui.Select(value=0)
        self.typeList.add("Ground",0)
        self.typeList.add("Wall",1)
        self.typeList.add("Trees",2)
        self.typeList.add("Props",3)
        self.typeList.add("Buildings",4)
        self.typeList.add("Other",5)
        self.add(self.typeList,label1.style.width+10,5)
        
        label2=gui.Label("Select sheet type: ",color=fontcolor,width=150)
        self.typeList1 = gui.Select(value=0)
        self.typeList.connect(gui.CHANGE,self.populateTypeList)
        self.typeList1.connect(gui.CHANGE,self.changeTiles)
        self.add(label2,275,7)
        self.add(self.typeList1,275+label2.style.width+10,5)
        
        refreshBtn = gui.Button("Refresh Tilesets",color=fontcolor,height=40,width=120)
        self.add(refreshBtn,0,40)
        def refreshTiles():
            self.engine.map.createSheets()
        refreshBtn.connect(gui.CLICK,refreshTiles)
    
    def changeTiles(self):
        self.engine.tileScroller.updateScrollSize()
        
    def populateTypeList(self):
        x=len(self.typeList1.options.widgets)-1
        while x>=0:
            self.typeList1._remove(x)
            x-=1
        for i in range(len(self.engine.map.tileSheets[self.typeList.value])):
            self.typeList1.add(str(i),i)
        if self.typeList1.value==0:
            self.changeTiles()
        self.typeList1.value=0
        
class MapProperties(gui.Container):
    def __init__(self,**params):
        gui.Container.__init__(self,**params)
        self.engine = None
        
        label1 = gui.Label("Map name: ",color=fontcolor)
        self.add(label1,0,0)
        self.mapNameInput = gui.Input(value="",width=(1280-1000-label1.style.width-30))
        self.add(self.mapNameInput,label1.style.width+10,0)
        
        musicLabel = gui.Label("Song: ", color=fontcolor)
        self.musicNameInput = gui.Input(value="",width=(1280-1000-musicLabel.style.width-30))
        self.add(musicLabel,0,(label1.style.height+10)*2)
        self.add(self.musicNameInput,260-self.musicNameInput.style.width,(label1.style.height+10)*2)
        
        def special_match(strg, search=re.compile(r'[^a-zA-Z0-9 -]').search):
            if bool(search(strg)):
                if strg=='\xe4' or strg=='\xc4' or strg=='\xf6' or strg=='\xd6':
                    return True
                return False
            return True
        def fncNameChange(self):
            if len(self.mapNameInput.value)>0:
                if not special_match(self.mapNameInput.value[len(self.mapNameInput.value)-1]):
                    self.mapNameInput.value = self.mapNameInput.value[:-1]
        
            if len(self.mapNameInput.value)>0 and self.engine.Map.tile!=[]:
                self.engine.mapName = self.mapNameInput.value
                self.engine.openedFile='data/maps/'+self.engine.mapName+'.map'
               
                if self.engine.error==3:
                    self.engine.error=0
            elif self.engine.Map.tile!=[]:
                self.engine.error=3
                self.engine.header.updateErrorMsg()
        self.mapNameInput.connect(gui.CHANGE,fncNameChange,self)
        def fncMusicChange(object):
            self.musicNameInput.value=os.path.basename(os.path.normpath(object.value))[:-4]
            self.engine.Map.song = self.musicNameInput.value
            self.engine.dialogOpened=False
        def fnc_open(self):
            a = gui.FileDialog(path="data/sounds/")
            a.connect(gui.CHANGE,fncMusicChange,a)
            self.engine.dialogOpened=True
            a.open()
        self.musicNameInput.connect(gui.CLICK,fnc_open,self)
        #label2 = gui.Label("Map number: ",color=fontcolor)
        #self.add(label2,0,label1.style.height+10)
        #self.mapNumberInput = gui.Input(value=None,width=30,disabled=True)
        #self.add(self.mapNumberInput,280-50,label1.style.height+10)
        
        
        label4 = gui.Label("Width: ",color=fontcolor)
        self.add(label4,0,label1.style.height*3+30)
        self.mapWidthInput = gui.Input(value=Map.width,width=30)
        self.add(self.mapWidthInput,280-50,label1.style.height*3+30)
        
        
        label5 = gui.Label("Height: ",color=fontcolor)
        self.add(label5,0,label1.style.height*4+40)
        self.mapHeightInput = gui.Input(value=Map.height,width=30)
        self.add(self.mapHeightInput,280-50,label1.style.height*4+40)
        
       
        
        label7 = gui.Label("Tile type: ",color=fontcolor)
        self.add(label7,300,0)
        self.typeList = gui.Select(value=0)
        self.typeList.add("TILE_TYPE_WALKABLE",0)
        self.typeList.add("TILE_TYPE_BLOCKED",1)
        self.typeList.add("TILE_TYPE_TELEPORT",2)
        #self.typeList.add("TILE_TYPE_FIGHTTRIGGER",3)
        self.typeList.add("TILE_TYPE_NPCAVOID",4)
        self.typeList.add("TILE_TYPE_FIGHT",5)
        self.add(self.typeList,label5.style.width+10+300+4,0)
        def typeChange(self):
            if self.typeList.value==2:
                self.tileDataInput1.disabled = False
                self.tileDataInput2.disabled = False
                self.tileDataInput3.disabled = False
            else:
                self.tileDataInput1.disabled = True
                self.tileDataInput2.disabled = True
                self.tileDataInput3.disabled = True
            self.engine.Map.tile[self.engine.selectionX][self.engine.selectionY].t = self.typeList.value
        self.typeList.connect(gui.CHANGE,typeChange,self)
        
        def selectTeleportMap(object):
            tmpName=object.value.replace('/','\\').split('\\')
            self.engine.Map.tile[self.engine.selectionX][self.engine.selectionY].d1= tmpName[-1][:-4]
            self.tileDataInput1.value=self.engine.Map.tile[self.engine.selectionX][self.engine.selectionY].d1
            self.engine.dialogOpened=False
        def fncTeleportChange1():
            a = gui.FileDialog(path="data/maps/")
            a.connect(gui.CHANGE,selectTeleportMap,a)
            self.engine.dialogOpened=True
            a.open()
            #if self.tileDataInput1.value and self.engine.Map.tile[self.engine.selectionX][self.engine.selectionY].d1 != self.tileDataInput1.value and len(self.tileDataInput1.value)<20:
            #    self.engine.Map.tile[self.engine.selectionX][self.engine.selectionY].d1 = self.tileDataInput1.value
            #print self.tileDataInput1.value
        def fncTeleportChange2(self):
            if self.tileDataInput2.value and self.tileDataInput2.value.isdigit() and self.engine.Map.tile[self.engine.selectionX][self.engine.selectionY].d2 != int(self.tileDataInput2.value) and int(self.tileDataInput2.value)>=0 and int(self.tileDataInput2.value)<10000:
                self.engine.Map.tile[self.engine.selectionX][self.engine.selectionY].d2 = int(self.tileDataInput2.value)
        def fncTeleportChange3(self):
            if self.tileDataInput3.value and self.tileDataInput3.value.isdigit() and self.engine.Map.tile[self.engine.selectionX][self.engine.selectionY].d3 != int(self.tileDataInput3.value) and int(self.tileDataInput3.value)>=0 and int(self.tileDataInput3.value)<1000:
                self.engine.Map.tile[self.engine.selectionX][self.engine.selectionY].d3 = int(self.tileDataInput3.value)
        def selectDeathMap(object):
            tmpName=object.value.replace('/','\\').split('\\')
            self.engine.Map.death[0] = tmpName[-1][:-4]
            self.deathTeleportInput.value=self.engine.Map.death[0]
            self.engine.dialogOpened=False
        def fncDeathMap():
            a = gui.FileDialog(path="data/maps/")
            a.connect(gui.CHANGE,selectDeathMap,a)
            self.engine.dialogOpened=True
            a.open()
        label8 = gui.Label("Teleport to Map(name): ",color=fontcolor)
        self.add(label8,300,label5.style.height+10)
        self.tileDataInput1 = gui.Input(value=0,width=120,disabled=True)
        self.add(self.tileDataInput1,label5.style.width+10+300+130+41,label1.style.height+10)
        self.tileDataInput1.connect(gui.CLICK,fncTeleportChange1)
        #self.tileDataInput1.connect(gui.CHANGE,fncTeleportChange1,self)
        
        label9 = gui.Label("Teleport to X (in Map(name)): ",color=fontcolor)
        self.add(label9,300,label5.style.height*2+20)
        self.tileDataInput2 = gui.Input(value="",width=30,disabled=True)
        self.add(self.tileDataInput2,label5.style.width+10+300+130+41,label1.style.height*2+20)
        self.tileDataInput2.connect(gui.CHANGE,fncTeleportChange2,self)
        
        label10 = gui.Label("Teleport to Y (in Map(name)): ",color=fontcolor)
        self.add(label10,300,label5.style.height*3+30)
        self.tileDataInput3 = gui.Input(value=0,width=30, disabled=True)
        self.add(self.tileDataInput3,label5.style.width+10+300+130+41,label1.style.height*3+30)
        self.tileDataInput3.connect(gui.CHANGE,fncTeleportChange3,self)
        
        
        label11 = gui.Label("TileX: ",color=fontcolor)
        self.add(label11,0,label1.style.height*5+50)
        label12 = gui.Label("TileY: ",color=fontcolor)
        self.add(label12,(1280-1000-label1.style.width-30+label1.style.width+10)/2,label1.style.height*5+50)
        self.mapTileXInput = gui.Input(value=-1,width=30)
        self.add(self.mapTileXInput,(1280-1000-30+10)/2-50,label1.style.height*5+50)
        self.mapTileYInput = gui.Input(value=-1,width=30)
        self.add(self.mapTileYInput,280-50,label1.style.height*5+50)
        
        label_deathteleport = gui.Label("On death, teleport to Map: ",color=fontcolor)
        self.add(label_deathteleport,300,label11.style.height*4+40)
        self.deathTeleportInput = gui.Input(value="",width=120)
        self.add(self.deathTeleportInput,label5.style.width+10+300+130+41,label1.style.height*4+40)
        self.deathTeleportInput.connect(gui.CLICK,fncDeathMap)
        
        labelDeathX = gui.Label("DeathX: ",color=fontcolor)
        self.add(labelDeathX,300,label1.style.height*5+50)
        self.deathXInput = gui.Input(value=-1,width=30)
        self.add(self.deathXInput,300+labelDeathX.style.width+10,label1.style.height*5+50)
        
        labelDeathY = gui.Label("DeathY: ",color=fontcolor)
        self.add(labelDeathY,300+125,label1.style.height*5+50)
        self.deathYInput = gui.Input(value=-1,width=30)
        self.add(self.deathYInput,300+125+10+labelDeathY.style.width,label1.style.height*5+50)
        
        def deathXChange(input):
            if self.deathXInput.value and self.deathXInput.value.isdigit():
                self.engine.Map.death[1]=int(self.deathXInput.value)
        def deathYChange(input):
            if self.deathYInput.value and self.deathYInput.value.isdigit():
                self.engine.Map.death[2]=int(self.deathYInput.value)
        self.deathXInput.connect(gui.CHANGE,deathXChange,self)
        self.deathYInput.connect(gui.CHANGE,deathYChange,self)
        
        #label12 = gui.Label("DeathY: ",color=fontcolor)
        #self.add(label12,(1280-1000-label1.style.width-30+label1.style.width+10)/2,label1.style.height*5+50)
        #self.mapTileXInput = gui.Input(value=-1,width=30)
        #self.add(self.mapTileXInput,(1280-1000-30+10)/2-50,label1.style.height*5+50)
        #self.mapTileYInput = gui.Input(value=-1,width=30)
        #self.add(self.mapTileYInput,280-50,label1.style.height*5+50)
        def meneChange():
            getValue=None
            for i in self.engine.Map.menes:
                if i[0]==self.typeList2.value:
                    getValue=i
            self.menenameinput._setvalue(getValue[0])
            self.typeList1.value=getValue[1]
            self.lvlMin._setvalue(str(getValue[2]))
            self.lvlMax._setvalue(str(getValue[3]))
            self.typeList1.disabled=False
            self.insertBtn.disabled=False
            self.removeBtn.disabled=False
            self.lvlMin.disabled=False
            self.lvlMax.disabled=False
            
        def selectMene(object):
            tmpName=object.value.replace('/','\\').split('\\')
            self.menenameinput._setvalue(tmpName[-1][:-4].split('_')[0])
            #self.typeList.disabled=False
            self.typeList1.disabled=False
            self.insertBtn.disabled=False
            self.removeBtn.disabled=False
            self.lvlMin.disabled=False
            self.lvlMax.disabled=False
            self.engine.dialogOpened=False
            
        def menenameget():
            a = gui.FileDialog(path="data/menes/")
            a.connect(gui.CHANGE,selectMene,a)
            self.engine.dialogOpened=True
            a.open()
        label13=gui.Label("Menes",color=fontcolor)
        self.add(label13,800,0)
        self.typeList2 = gui.Select(disabled=True)
        #self.typeList.add("No menes")
        self.typeList2.connect(gui.CHANGE,meneChange)
        self.add(self.typeList2,700,label1.style.height+10)
        label14=gui.Label("Mene: ",color=fontcolor)
        self.add(label14,700,label1.style.height*2+30)
        self.menenameinput=gui.Input(width=120)
        self.add(self.menenameinput,700+label4.style.width+10,label1.style.height*2+30)
        self.menenameinput.connect(gui.CLICK,menenameget)
        self.typeList1 = gui.Select(disabled=True)
        self.typeList1.add("SHOWUP_NORMAL",SHOWUP_NORMAL)
        self.typeList1.add("SHOWUP_UNCOMMON",SHOWUP_UNCOMMON)
        self.typeList1.add("SHOWUP_RARE",SHOWUP_RARE)
        self.typeList1.value=1
        self.add(self.typeList1,700,label1.style.height*3+40)
        self.insertBtn=gui.Button("Insert",width=60,height=40,disabled=True)
        self.removeBtn=gui.Button("Delete",width=60,height=40,disabled=True)
        self.add(self.insertBtn,700,label1.style.height*4+50)
        self.add(self.removeBtn,700+self.insertBtn.style.width+20,label1.style.height*4+50)
        label15=gui.Label("Lvl Min",color=fontcolor)
        self.lvlMin=gui.Input(width=40,disabled=True)
        self.lvlMax=gui.Input(width=40,disabled=True)
        label16=gui.Label("Lvl Max",color=fontcolor)
        self.add(label15,910,label1.style.height*2+30)
        self.add(self.lvlMin,910,label1.style.height*3+40)
        self.add(label16,910,label1.style.height*4+50)
        self.add(self.lvlMax,910,label1.style.height*5+60)
        
        
        def fncInsertMene():
            found=False
            for i in xrange(len(self.engine.Map.menes)):
                if self.engine.Map.menes[i][0]==self.menenameinput.value:
                    self.engine.Map.menes[i][1]=self.typeList1.value
                    self.engine.Map.menes[i][2]=int(''.join(x for x in self.lvlMin.value if x.isdigit()))
                    self.engine.Map.menes[i][3]=int(''.join(x for x in self.lvlMax.value if x.isdigit()))
                    found=True
            if not found:
                self.engine.Map.menes.append([self.menenameinput.value,self.typeList1.value,int(self.lvlMin.value),int(self.lvlMax.value)])
                self.typeList2.add(self.menenameinput.value,self.menenameinput.value)
            self.typeList2.disabled=False
            self.typeList2.value=self.engine.Map.menes[-1][0]
        
        def fncRemoveMene():
            #print self.engine.Map.menes
            for i in xrange(len(self.engine.Map.menes)):
                if self.engine.Map.menes[i][0]==self.menenameinput.value:
                    del self.engine.Map.menes[i]
                    break
            self.populateTypeList2()
        self.insertBtn.connect(gui.CLICK,fncInsertMene)
        self.removeBtn.connect(gui.CLICK,fncRemoveMene)
        def tileXChange(self):
            if self.mapTileXInput.value and self.mapTileXInput.value.isdigit() and self.engine.selectionX != self.mapTileXInput.value and int(self.mapTileXInput.value)>=0 and int(self.mapTileXInput.value)<self.engine.Map.width:
                self.engine.selectionX = int(self.mapTileXInput.value)
                self.refreshTile(self.engine.selectionX,self.engine.selectionY,0)
        def tileYChange(self):
            if self.mapTileYInput.value and self.mapTileXInput.value.isdigit() and self.engine.selectionY != self.mapTileYInput.value and int(self.mapTileYInput.value)>=0 and int(self.mapTileYInput.value)<self.engine.Map.width:
                self.engine.selectionY = int(self.mapTileYInput.value)
                self.refreshTile(self.engine.selectionX,self.engine.selectionY,0)
        self.mapTileXInput.connect(gui.CHANGE,tileXChange,self)
        self.mapTileYInput.connect(gui.CHANGE,tileYChange,self)
        
        @undo.undoable
        def changeMapWidth():
            self.engine.mapLoaded = False
            tmpWidth = self.engine.Map.width
            self.engine.Map.width = int(self.mapWidthInput.value)
            if self.engine.Map.width > len(self.engine.Map.tile):
                for y in range(self.engine.Map.width-tmpWidth):
                    tiles = []
                    for x in range(self.engine.Map.height):
                        tiles.append(TileClass())
                    self.engine.Map.tile.append(tiles)
            
            self.engine.map.changed = True
            self.engine.mapLoaded = True
            yield
            self.engine.map.changed = True
            self.engine.Map.width = tmpWidth
            self.mapWidthInput.value = tmpWidth
            
        def mapWidthChange(self):
            if self.mapWidthInput.value and self.mapWidthInput.value.isdigit() and self.engine.mapLoaded and self.engine.Map.width != self.mapWidthInput.value and int(self.mapWidthInput.value)>=0 and int(self.mapWidthInput.value)<9999:
                changeMapWidth()
                
        self.mapWidthInput.connect(gui.CHANGE,mapWidthChange,self)
        
        @undo.undoable
        def changeMapHeight():
            self.engine.mapLoaded = False
            tmpHeight = self.engine.Map.height
            self.engine.Map.height = int(self.mapHeightInput.value)
            if self.engine.Map.height > len(self.engine.Map.tile[0]):
                for x in range(len(self.engine.Map.tile)):
                    for y in range(self.engine.Map.height+1-len(self.engine.Map.tile[x])):
                        self.engine.Map.tile[x].append(TileClass())
            self.engine.map.changed = True
            self.engine.mapLoaded = True
            yield
            self.engine.map.changed = True
            self.engine.Map.height = tmpHeight
            self.mapHeightInput.value = tmpHeight
            
        def mapHeightChange(self):
            if self.mapHeightInput.value and self.mapHeightInput.value.isdigit() and self.engine.mapLoaded and self.engine.Map.height != self.mapHeightInput.value and int(self.mapHeightInput.value)>=0 and int(self.mapHeightInput.value)<9999:
                changeMapHeight()
        self.mapHeightInput.connect(gui.CHANGE,mapHeightChange,self)
        
        def selectFile(object):
            try:
                tmpStr = object.value.split('/')[3]
                tmpStr = tmpStr.split('.')
                tmpStr1 = tmpStr[0]
                if (tmpStr[1]!='png'):
                    self.engine.error=2
                    self.engine.header.updateErrorMsg()
                elif tmpStr1[:5] != 'Tiles':
                    self.engine.error=3
                    self.engine.header.updateErrorMsg()
                elif not isinstance(int(tmpStr[0][5:]),int):
                    self.engine.error=5
                    self.engine.header.updateErrorMsg()
                else:
                    self.engine.error=0
            except:
                self.engine.error=4
                self.engine.header.updateErrorMsg()
    def populateTypeList2(self):
        x=len(self.typeList2.options.widgets)-1
        while x>=0:
            self.typeList2._remove(x)
            x-=1
        
        for i in xrange(len(self.engine.Map.menes)):
            self.typeList2.add(self.engine.Map.menes[i][0].encode('ascii','ignore'),self.engine.Map.menes[i][0])
        if len(self.engine.Map.menes)==0:
            self.typeList2.disabled=True
            self.typeList1.disabled=True
            self.insertBtn.disabled=True
            self.removeBtn.disabled=True
            self.lvlMin.disabled=True
            self.lvlMax.disabled=True
            self.lvlMin._setvalue('')
            self.lvlMax._setvalue('')
            self.menenameinput._setvalue('')
        else:
            self.typeList2.disabled=False
            self.typeList2.value=self.engine.Map.menes[-1][0]
    def refreshTile(self,x,y,action):
        if x>=self.engine.Map.width or y>=self.engine.Map.height:
            return
        @undo.undoable
        def handleTeleport(x,y):
            if self.engine.Map.tile[x][y].t == 2:
                self.engine.Map.tile[x][y].t = 0
                yield
                self.engine.Map.tile[x][y].t = 2
            else:
                tmpType = self.engine.Map.tile[x][y].t
                self.engine.Map.tile[x][y].t = 2
                yield
                self.engine.Map.tile[x][y].t = tmpType
        @undo.undoable
        def handleNPCAvoid(x,y):
            if self.engine.Map.tile[x][y].t == 4:
                self.engine.Map.tile[x][y].t = 0
                yield
                self.engine.Map.tile[x][y].t = 4
            else:
                tmpType = self.engine.Map.tile[x][y].t
                self.engine.Map.tile[x][y].t = 4
                yield
                self.engine.Map.tile[x][y].t = tmpType
                
        @undo.undoable
        def handleFight(x,y):
            if self.engine.Map.tile[x][y].t==TILE_TYPE_FIGHT and not self.engine.painting:
                self.engine.Map.tile[x][y].t=TILE_TYPE_WALKABLE
                yield
                self.engine.Map.tile[x][y].t=TILE_TYPE_FIGHT
            else:
                tmpType = self.engine.Map.tile[x][y].t
                self.engine.Map.tile[x][y].t=TILE_TYPE_FIGHT
                yield
                self.engine.Map.tile[x][y].t = tmpType
        @undo.undoable
        def handleBlock(x,y):
            if self.engine.Map.tile[x][y].t == 1 and not self.engine.painting:
                self.engine.Map.tile[x][y].t = 0
                yield
                self.engine.Map.tile[x][y].t = 1
            else:
                tmpType = self.engine.Map.tile[x][y].t
                self.engine.Map.tile[x][y].t = 1
                yield
                self.engine.Map.tile[x][y].t = tmpType
        @undo.undoable
        def handleRemove(x,y):
            if self.engine.showTileTypes:
                tmp1 = self.engine.Map.tile[x][y].t
                tmp2 = self.engine.Map.tile[x][y].d1
                tmp3 = self.engine.Map.tile[x][y].d2
                tmp4 = self.engine.Map.tile[x][y].d3
                self.engine.Map.tile[x][y].t = 0
                self.engine.Map.tile[x][y].d1 = None
                self.engine.Map.tile[x][y].d2 = 0
                self.engine.Map.tile[x][y].d3 = 0
                yield
                self.engine.Map.tile[x][y].t = tmp1
                self.engine.Map.tile[x][y].d1 = tmp2
                self.engine.Map.tile[x][y].d2 = tmp3
                self.engine.Map.tile[x][y].d3 = tmp4
            elif self.engine.selectedLayer == 0:
                tmp1 = self.engine.Map.tile[x][y].l1
                tmp2 = self.engine.Map.tile[x][y].l2
                tmp3 = self.engine.Map.tile[x][y].l3
                tmp4 = self.engine.Map.tile[x][y].f
                self.engine.Map.tile[x][y].l1 = None
                self.engine.Map.tile[x][y].l2 = None
                self.engine.Map.tile[x][y].l3 = None
                self.engine.Map.tile[x][y].f = None
                yield
                self.engine.Map.tile[x][y].l1 = tmp1
                self.engine.Map.tile[x][y].l2 = tmp2
                self.engine.Map.tile[x][y].l3 = tmp3
                self.engine.Map.tile[x][y].f = tmp4
            elif self.engine.selectedLayer == 1:
                tmp1 = self.engine.Map.tile[x][y].l1
                self.engine.Map.tile[x][y].l1 = None
                yield
                self.engine.Map.tile[x][y].l1 = tmp1
            elif self.engine.selectedLayer == 2:
                tmp1 = self.engine.Map.tile[x][y].l2
                self.engine.Map.tile[x][y].l2 = None
                yield
                self.engine.Map.tile[x][y].l2 = tmp1
            elif self.engine.selectedLayer == 3:
                tmp1 = self.engine.Map.tile[x][y].l3
                self.engine.Map.tile[x][y].l3 = None
                yield
                self.engine.Map.tile[x][y].l3 = tmp1
            elif self.engine.selectedLayer == 4:
                tmp1 = self.engine.Map.tile[x][y].f
                self.engine.Map.tile[x][y].f = None
                yield
                self.engine.Map.tile[x][y].f = tmp1
        @undo.undoable
        def handlePaint(x,y):
            if self.engine.selectedLayer==1 or self.engine.selectedLayer==0:
                tmp1 = self.engine.Map.tile[x][y].l1
                self.engine.Map.tile[x][y].l1 = [self.engine.tilePicker.typeList.value,self.engine.tilePicker.typeList1.value,self.engine.tileScroller.selectedX+self.engine.tileScroller.selectedY*32]
                yield
                self.engine.Map.tile[x][y].l1 = tmp1
            elif self.engine.selectedLayer==2:
                tmp1 = self.engine.Map.tile[x][y].l2
                self.engine.Map.tile[x][y].l2 = [self.engine.tilePicker.typeList.value,self.engine.tilePicker.typeList1.value,self.engine.tileScroller.selectedX+self.engine.tileScroller.selectedY*32]
                yield
                self.engine.Map.tile[x][y].l2 = tmp1
            elif self.engine.selectedLayer==3:
                tmp1 = self.engine.Map.tile[x][y].l3
                self.engine.Map.tile[x][y].l3 = [self.engine.tilePicker.typeList.value,self.engine.tilePicker.typeList1.value,self.engine.tileScroller.selectedX+self.engine.tileScroller.selectedY*32]
                yield
                self.engine.Map.tile[x][y].l3 = tmp1
            elif self.engine.selectedLayer==4:
                tmp1 = self.engine.Map.tile[x][y].f
                self.engine.Map.tile[x][y].f = [self.engine.tilePicker.typeList.value,self.engine.tilePicker.typeList1.value,self.engine.tileScroller.selectedX+self.engine.tileScroller.selectedY*32]
                yield
                self.engine.Map.tile[x][y].f = tmp1
        if action:
            if self.engine.buttons.g.value == 'block':
                handleBlock(x,y)
            elif self.engine.buttons.g.value == 'remove':
                handleRemove(x,y)
            elif self.engine.buttons.g.value == 'npcavoid':
                handleNPCAvoid(x,y)
            elif self.engine.buttons.g.value == 'teleport':
                handleTeleport(x,y)
            elif self.engine.buttons.g.value == 'fight':
                handleFight(x,y)
            elif self.engine.buttons.g.value =='paint':
                if self.engine.tileScroller.selectedX!=-1 and self.engine.tileScroller.selectedY!=-1:
                    handlePaint(x,y)
        self.typeList.value = self.engine.Map.tile[x][y].t
        self.tileDataInput1.value = self.engine.Map.tile[x][y].d1
        self.tileDataInput2.value = self.engine.Map.tile[x][y].d2
        self.tileDataInput3.value = self.engine.Map.tile[x][y].d3
        self.mapTileXInput.value = x
        self.mapTileYInput.value = y
        
class MapArea(gui.ScrollArea):
    def __init__(self,**params):
        self.engine = None
        self.hovering = True
        self.changed = False
        self.mousex = 0
        self.mousey = 0
       
        self.selectedSprite = pygame.image.load("data/gui/selected.png").convert_alpha()
        #self.selectedSprite.set_colorkey(COLOR_KEY,pygame.RLEACCEL)
        self.hoverSprite = pygame.image.load("data/gui/select.png").convert_alpha()
        #self.hoverSprite.set_colorkey(COLOR_KEY,pygame.RLEACCEL)
        self.fadeTile = pygame.image.load("data/gui/fadetile.png").convert_alpha()
        self.blockTile = pygame.image.load("data/gui/fadeblock.png").convert_alpha()
        self.npcAvoidTile = pygame.image.load("data/gui/fadenpcavoid.png").convert_alpha()
        self.teleportTile = pygame.image.load("data/gui/fadeteleport.png").convert_alpha()
        self.fightTile = pygame.image.load("data/gui/fadefight.png").convert_alpha()
        self.removeTile = pygame.image.load("data/gui/delete.png").convert_alpha()
        self.tileSheets=[]
        self.groundSurface = pygame.image.load("data/tilesets/ground/0.png").convert_alpha()
        self.groundSurface = pygame.transform.scale(self.groundSurface, (self.groundSurface.get_rect().width*TILE_SCALE,self.groundSurface.get_rect().height*TILE_SCALE))
        self.createSheets()
    def createSheets(self):
        self.tileSheets[:] = []
        groundSheets=[]
        for x in range(999):
            try:
                tmpSurface = pygame.image.load('data/tilesets/ground/'+str(x)+'.png').convert_alpha()
                groundSheets.append(pygame.transform.scale(tmpSurface, (tmpSurface.get_rect().width*TILE_SCALE,tmpSurface.get_rect().height*TILE_SCALE)))
            except:
                break
        self.tileSheets.append(groundSheets)
        
        wallSheets = []
        for x in range(999):
            try:
                tmpSurface = pygame.image.load('data/tilesets/wall/'+str(x)+'.png').convert_alpha()
                #tmpSurface.set_colorkey(COLOR_KEY,pygame.RLEACCEL)
                wallSheets.append(pygame.transform.scale(tmpSurface, (tmpSurface.get_rect().width*TILE_SCALE,tmpSurface.get_rect().height*TILE_SCALE)))
            except:
                break
        self.tileSheets.append(wallSheets)
        
        treesSheets = []
        for x in range(999):
            try:
                tmpSurface = pygame.image.load('data/tilesets/trees/'+str(x)+'.png').convert_alpha()
                treesSheets.append(pygame.transform.scale(tmpSurface, (tmpSurface.get_rect().width*TILE_SCALE,tmpSurface.get_rect().height*TILE_SCALE)))
            except Exception, e:
                #print Exception, e
                break
        self.tileSheets.append(treesSheets)
        propsSheets = []
        for x in range(999):
            try:
                tmpSurface = pygame.image.load('data/tilesets/props/'+str(x)+'.png').convert_alpha()
                propsSheets.append(pygame.transform.scale(tmpSurface, (tmpSurface.get_rect().width*TILE_SCALE,tmpSurface.get_rect().height*TILE_SCALE)))
            except:
                break
        self.tileSheets.append(propsSheets)
        
        buildingSheets = []
        for x in range(999):
            try:
                tmpSurface = pygame.image.load('data/tilesets/building/'+str(x)+'.png').convert_alpha()
                buildingSheets.append(pygame.transform.scale(tmpSurface, (tmpSurface.get_rect().width*TILE_SCALE,tmpSurface.get_rect().height*TILE_SCALE)))
            except:
                break
        self.tileSheets.append(buildingSheets)
        
        otherSheets = []
        for x in range(999):
            try:
                tmpSurface = pygame.image.load('data/tilesets/other/'+str(x)+'.png').convert_alpha()
                otherSheets.append(pygame.transform.scale(tmpSurface, (tmpSurface.get_rect().width*TILE_SCALE,tmpSurface.get_rect().height*TILE_SCALE)))
            except:
                break
        self.tileSheets.append(otherSheets)
        
        self.paintSurface = pygame.Surface((TILESIZE,TILESIZE))
        self.paintSurface.blit(self.tileSheets[0][0],(0,0),(0,0,TILESIZE,TILESIZE))
        
    def drawMap(self):
        self.mapping = gui.Image(self.engine.mapSurface)
        gui.ScrollArea.__init__(self,self.mapping,width=15*64+16,height=11*64+16,step=TILESIZE)
    def updateScroll(self):
        self.mapping.style.width=self.engine.mapSurface.get_width()
        self.mapping.style.height=self.engine.mapSurface.get_height()
        self.resize()
    def redrawMap(self):
        self.engine.mapSurface.fill((0,0,0))
        if self.engine.Map.tile != [] and self.engine.mapLoaded:
            if self.engine.mapSurface.get_height() != self.engine.Map.height*TILESIZE or self.engine.mapSurface.get_width() != self.engine.Map.width*TILESIZE:
                if self.engine.Map.height<22 and self.engine.Map.width<30:
                    self.engine.mapSurface = pygame.Surface((15*64,11*64))
                elif self.engine.Map.height<22:
                    self.engine.mapSurface = pygame.Surface((self.engine.Map.width*TILESIZE,11*64))
                elif self.engine.Map.width<30:
                    self.engine.mapSurface = pygame.Surface((15*64,self.engine.Map.height*TILESIZE))
                else:
                    self.engine.mapSurface = pygame.Surface((self.engine.Map.width*TILESIZE,self.engine.Map.height*TILESIZE))
            tmpRect = pygame.Rect(0,0,TILESIZE,TILESIZE)
            for x in range(self.engine.Map.width):
                for y in range(self.engine.Map.height):
                    if self.engine.Map.tile[x][y].l1 is not None:
                        tmpRect.top = (self.engine.Map.tile[x][y].l1[2] // 32) * TILESIZE
                        tmpRect.left = (self.engine.Map.tile[x][y].l1[2] % 32) * TILESIZE
                        self.engine.mapSurface.blit(self.tileSheets[self.engine.Map.tile[x][y].l1[0]][self.engine.Map.tile[x][y].l1[1]], (x*TILESIZE,y*TILESIZE),tmpRect)
                        if self.engine.selectedLayer>1:
                            self.engine.mapSurface.blit(self.fadeTile,(x*TILESIZE,y*TILESIZE),pygame.Rect(0,0,TILESIZE,TILESIZE))
                    else:
                        self.engine.mapSurface.fill((0,0,0),((x)*TILESIZE,(y)*TILESIZE,TILESIZE,TILESIZE))
                    
                    if self.engine.Map.tile[x][y].l2 is not None and (self.engine.selectedLayer>=2 or self.engine.selectedLayer==0):
                        tmpRect.top = (self.engine.Map.tile[x][y].l2[2] // 32) * TILESIZE
                        tmpRect.left = (self.engine.Map.tile[x][y].l2[2] % 32) * TILESIZE
                        self.engine.mapSurface.blit(self.tileSheets[self.engine.Map.tile[x][y].l2[0]][self.engine.Map.tile[x][y].l2[1]], (x*TILESIZE,y*TILESIZE),tmpRect)
                        if self.engine.selectedLayer>2:
                            self.engine.mapSurface.blit(self.fadeTile,(x*TILESIZE,y*TILESIZE),pygame.Rect(0,0,TILESIZE,TILESIZE))
                    if self.engine.Map.tile[x][y].l3 is not None and (self.engine.selectedLayer>=3 or self.engine.selectedLayer==0):
                        tmpRect.top = (self.engine.Map.tile[x][y].l3[2] // 32) * TILESIZE
                        tmpRect.left = (self.engine.Map.tile[x][y].l3[2] % 32) * TILESIZE
                        self.engine.mapSurface.blit(self.tileSheets[self.engine.Map.tile[x][y].l3[0]][self.engine.Map.tile[x][y].l3[1]], (x*TILESIZE,y*TILESIZE),tmpRect)
                        if self.engine.selectedLayer>3:
                            self.engine.mapSurface.blit(self.fadeTile,(x*TILESIZE,y*TILESIZE),pygame.Rect(0,0,TILESIZE,TILESIZE))
                    if self.engine.Map.tile[x][y].f is not None and (self.engine.selectedLayer>=4 or self.engine.selectedLayer==0):
                        tmpRect.top = (self.engine.Map.tile[x][y].f[2] // 32) * TILESIZE
                        tmpRect.left = (self.engine.Map.tile[x][y].f[2] % 32) * TILESIZE
                        self.engine.mapSurface.blit(self.tileSheets[self.engine.Map.tile[x][y].f[0]][self.engine.Map.tile[x][y].f[1]], (x*TILESIZE,y*TILESIZE),tmpRect)
                        if self.engine.selectedLayer>4:
                            self.engine.mapSurface.blit(self.fadeTile,(x*TILESIZE,y*TILESIZE),pygame.Rect(0,0,TILESIZE,TILESIZE))
                    if self.engine.showTileTypes:
                        if self.engine.Map.tile[x][y].t == 1:
                            self.engine.mapSurface.blit(self.blockTile, (x*TILESIZE,y*TILESIZE),pygame.Rect(0,0,TILESIZE,TILESIZE))
                        elif self.engine.Map.tile[x][y].t == 2:
                            self.engine.mapSurface.blit(self.teleportTile, (x*TILESIZE,y*TILESIZE),pygame.Rect(0,0,TILESIZE,TILESIZE))
                        elif self.engine.Map.tile[x][y].t == 4:
                            self.engine.mapSurface.blit(self.npcAvoidTile, (x*TILESIZE,y*TILESIZE),pygame.Rect(0,0,TILESIZE,TILESIZE))
                        elif self.engine.Map.tile[x][y].t==TILE_TYPE_FIGHT:
                            self.engine.mapSurface.blit(self.fightTile, (x*TILESIZE,y*TILESIZE),pygame.Rect(0,0,TILESIZE,TILESIZE))
            if self.changed == True:
                self.updateScroll()
                self.changed = False
        if self.hovering:
            if self.engine.buttons.g.value == 'block':
                self.engine.mapSurface.blit(self.blockTile,(self.mousex*TILESIZE,self.mousey*TILESIZE))
            elif self.engine.buttons.g.value == 'remove':
                self.engine.mapSurface.blit(self.removeTile,(self.mousex*TILESIZE+8,self.mousey*TILESIZE+8))
            elif self.engine.buttons.g.value == 'npcavoid':
                self.engine.mapSurface.blit(self.npcAvoidTile,(self.mousex*TILESIZE,self.mousey*TILESIZE))
            elif self.engine.buttons.g.value == 'teleport':
                self.engine.mapSurface.blit(self.teleportTile,(self.mousex*TILESIZE,self.mousey*TILESIZE))
            elif self.engine.buttons.g.value == 'fight':
                self.engine.mapSurface.blit(self.fightTile,(self.mousex*TILESIZE,self.mousey*TILESIZE))
            elif self.engine.buttons.g.value =='paint':
                self.engine.mapSurface.blit(self.paintSurface,(self.mousex*TILESIZE,self.mousey*TILESIZE))
            else:
                self.engine.mapSurface.blit(self.hoverSprite,(self.mousex*TILESIZE,self.mousey*TILESIZE))
        if self.engine.selectionX != -1 and self.engine.selectionY != -1 and self.engine.buttons.g.value != 'block' and self.engine.buttons.g.value != 'npcavoid' and self.engine.buttons.g.value != 'teleport' and self.engine.buttons.g.value != 'remove' and self.engine.buttons.g.value != 'paint' and self.engine.buttons.g.value!='fight':
            self.engine.mapSurface.blit(self.selectedSprite,(self.engine.selectionX*TILESIZE,self.engine.selectionY*TILESIZE))
        self.mapping.repaint(self.engine.mapSurface)
        
    def drawHover(self,mouseX,mouseY):
        self.mousex = (mouseX-50)//TILESIZE
        self.mousey = (mouseY-40)//TILESIZE
        
class TestPlay():
    def __init__(self):
        self.surface = pygame.Surface((15*64,11*64))
        self.hovering=False
        self.moving=False
        self.moved=False
        self.loading=False
        self.map=MapClass()
        self.nextMove=-1
        self.playerPos = [-1,-1]
        self.mousePos= [-1,-1]
        self.facing=0
        self.musicManager = pyglet.media.Player()
        self.musicManager.volume=0.5
        self.musicManager.eos_action = pyglet.media.Player.EOS_LOOP
        self.playerSprite = pygame.image.load('data/sprites/char.png').convert_alpha()
        #self.playerSprite.set_colorkey(COLOR_KEY,pygame.RLEACCEL)
        self.playerSprite = pygame.transform.scale(self.playerSprite,(self.playerSprite.get_width()*TILE_SCALE,self.playerSprite.get_height()*TILE_SCALE))
        self.posx=(1800-self.surface.get_width())/2
        self.posy=(960-self.surface.get_height())/2
        self.playerOffsetX=0
        self.playerOffsetY=0
        self.tick=0
        font=pygame.font.Font(None,36)
        self.text=font.render("Press ESC to quit the demo.",1,(255,255,255))
        self.textpos=self.text.get_rect()
        self.textpos.y=50
        self.textpos.centerx=screen.get_rect().centerx
        
    def initatePlay(self):
        self.map.tile = [[TileClass() for i in range(self.engine.Map.height)] for i in range(self.engine.Map.width)]
        self.map.tile = self.engine.Map.tile
        self.map.width = self.engine.Map.width
        self.map.height = self.engine.Map.height
        self.playMusic(self.engine.Map.song)
    def playMusic(self,song):
        self.musicManager.next_source()
        if song!="":
            self.musicManager.queue(pyglet.media.load('data/sounds/'+song+'.mp3'))
            self.musicManager.play()
        
    def playUpdate(self):
        screen.fill((60,60,60))
        self.surface.fill((0,0,0))
        #tmpTick=pygame.time.get_ticks()
        tmpTick = int(time.clock()*1000)
        tmpRect = pygame.Rect(0,0,TILESIZE,TILESIZE)
        if self.moving:
            #print "MOVEEE"
            if tmpTick-self.tick>=640/2 and not self.moved:
                self.facing+=1
                self.moved=True
            elif tmpTick-self.tick>=640:
                if self.map.tile[self.playerPos[0]][self.playerPos[1]].t==2:
                    self.loading=True
                    tmp1=self.playerPos[0]
                    tmp2=self.playerPos[1]
                    self.playerPos[0]=self.map.tile[tmp1][tmp2].d2
                    self.playerPos[1]=self.map.tile[tmp1][tmp2].d3
                    with open('data/maps/'+self.map.tile[tmp1][tmp2].d1+'.map','r') as fp:
                        tempMap = json.load(fp)
                    self.map.width = tempMap["width"]
                    self.map.height = tempMap["height"]
                    self.map.tile = [[TileClass() for i in range(tempMap["height"])] for i in range(tempMap["width"])]
                    tmpTiles = []
                    for x in range(tempMap["width"]):
                        tmpTilesW=[]
                        for y in range(tempMap["height"]):
                            tmpTile = TileClass()
                            tmpTile.l1 = tempMap['tile'][x][y]["l1"]
                            tmpTile.l2 = tempMap['tile'][x][y]["l2"]
                            tmpTile.l3 = tempMap['tile'][x][y]["l3"]
                            tmpTile.f = tempMap['tile'][x][y]["f"]
                            tmpTile.t = tempMap['tile'][x][y]["t"]
                            tmpTile.d1 = tempMap['tile'][x][y]["d1"]
                            tmpTile.d2= tempMap['tile'][x][y]["d2"]
                            tmpTile.d3 = tempMap['tile'][x][y]["d3"]
                            tmpTilesW.append(tmpTile)
                        tmpTiles.append(tmpTilesW)
                    self.map.tile = tmpTiles
                    self.loading=False
                    self.playMusic(tempMap["song"])
                    return
                self.facing-=1
                if self.nextMove>=0:
                    self.facing=self.nextMove
                    self.tick = tmpTick
                    stopped=False
                    if self.nextMove==1:
                        if self.canMove(self.playerPos[0],self.playerPos[1]+1):
                            self.playerPos[1]+=1
                        else:
                            stopped=True
                    elif self.nextMove==3:
                        if self.canMove(self.playerPos[0]+1,self.playerPos[1]):
                            self.playerPos[0]+=1
                        else:
                            stopped=True
                    elif self.nextMove==6:
                        if self.canMove(self.playerPos[0],self.playerPos[1]-1):
                            self.playerPos[1]-=1
                        else:
                            stopped=True
                    elif self.nextMove==8:
                        if self.canMove(self.playerPos[0]-1,self.playerPos[1]):
                            self.playerPos[0]-=1
                        else:
                            stopped=True
                    self.nextMove=-1
                    self.moved=False
                    if stopped:
                        self.moving=False
                else:
                    self.moving=False
                    self.moved=False
                    self.nextMove=-1
                    if self.facing==1:
                        self.facing=0
                    elif self.facing==6:
                        self.facing=5
                self.playerOffsetX=0
                self.playerOffsetY=0
            if (self.facing==3 or self.facing==4):
                self.playerOffsetX=(TILESIZE-(tmpTick-self.tick)//20)
            elif (self.facing==8 or self.facing==9):
                self.playerOffsetX=-(TILESIZE-(tmpTick-self.tick)//20)
            elif (self.facing==1 or self.facing==2):
                self.playerOffsetY=(TILESIZE-(tmpTick-self.tick)//20)
            elif (self.facing==6 or self.facing==7):
                self.playerOffsetY=-(TILESIZE-(tmpTick-self.tick)//20)
            
        else:
            self.playerOffsetX=0
            self.playerOffsetY=0
        if self.map.tile != []:
            for i in range(-1,self.map.width):
                for j in range(-1,self.map.height):
                    if self.playerPos[0]!=-1 and self.playerPos[1]!=-1:
                        x = self.playerPos[0]-15+i
                        y= self.playerPos[1]-10+j
                    else:
                        x=i
                        y=j
                    if x>=self.map.width or y>=self.map.height or x<0 or y<0:
                        if x>=self.map.width or y>=self.map.height:
                            self.surface.fill((0,0,0),((i)*TILESIZE+self.playerOffsetX,(j)*TILESIZE+self.playerOffsetY,TILESIZE,TILESIZE))
                    else:
                        if self.map.tile[x][y].l1 is not None:
                            tmpRect.top = (self.map.tile[x][y].l1[2] // 32) * TILESIZE
                            tmpRect.left = (self.map.tile[x][y].l1[2] % 32) * TILESIZE
                            self.surface.blit(self.engine.map.tileSheets[self.map.tile[x][y].l1[0]][self.map.tile[x][y].l1[1]], (i*TILESIZE+self.playerOffsetX,j*TILESIZE+self.playerOffsetY),tmpRect)
                        if self.map.tile[x][y].l2 is not None:
                            tmpRect.top = (self.map.tile[x][y].l2[2] // 32) * TILESIZE
                            tmpRect.left = (self.map.tile[x][y].l2[2] % 32) * TILESIZE
                            self.surface.blit(self.engine.map.tileSheets[self.map.tile[x][y].l2[0]][self.map.tile[x][y].l2[1]], (i*TILESIZE+self.playerOffsetX,j*TILESIZE+self.playerOffsetY),tmpRect)
                        if self.map.tile[x][y].l3 is not None:
                            tmpRect.top = (self.map.tile[x][y].l3[2] // 32) * TILESIZE
                            tmpRect.left = (self.map.tile[x][y].l3[2] % 32) * TILESIZE
                            self.surface.blit(self.engine.map.tileSheets[self.map.tile[x][y].l3[0]][self.map.tile[x][y].l3[1]], (i*TILESIZE+self.playerOffsetX,j*TILESIZE+self.playerOffsetY),tmpRect)
                        
                        if self.playerPos==[-1,-1]:
                            if x==self.mousePos[0] and y==self.mousePos[1]:
                                self.surface.blit(self.playerSprite,(i*TILESIZE,j*TILESIZE),(0,0,TILESIZE,TILESIZE))
                        
                        elif x==self.playerPos[0] and y==self.playerPos[1]:
                            self.surface.blit(self.playerSprite,(i*TILESIZE,j*TILESIZE),(self.facing*TILESIZE,0,TILESIZE,TILESIZE))
                        
                        elif x==self.playerPos[0]+1 and y==self.playerPos[1] and self.moving and (self.facing==8 or self.facing==9):
                            self.surface.blit(self.playerSprite,(i*TILESIZE-TILESIZE,j*TILESIZE),(self.facing*TILESIZE,0,TILESIZE,TILESIZE))
                            
                        elif x==self.playerPos[0] and y==self.playerPos[1]+1 and self.moving and (self.facing==6 or self.facing==7):
                            self.surface.blit(self.playerSprite,(i*TILESIZE,j*TILESIZE-TILESIZE),(self.facing*TILESIZE,0,TILESIZE,TILESIZE))
                        if x>0 and x < self.map.width and y>=0 and y <= self.map.height-1:
                            if self.map.tile[x-1][y].f is not None:
                                tmpRect.top = (self.map.tile[x-1][y].f[2] // 32) * TILESIZE
                                tmpRect.left = (self.map.tile[x-1][y].f[2] % 32) * TILESIZE
                                self.surface.blit(self.engine.map.tileSheets[self.map.tile[x-1][y].f[0]][self.map.tile[x-1][y].f[1]], (i*TILESIZE+self.playerOffsetX-TILESIZE,j*TILESIZE+self.playerOffsetY),tmpRect)
                        if x>=0 and x < self.map.width and y>0 and y < self.map.height:
                            if self.map.tile[x][y-1].f is not None:
                                tmpRect.top = (self.map.tile[x][y-1].f[2] // 32) * TILESIZE
                                tmpRect.left = (self.map.tile[x][y-1].f[2] % 32) * TILESIZE
                                self.surface.blit(self.engine.map.tileSheets[self.map.tile[x][y-1].f[0]][self.map.tile[x][y-1].f[1]], (i*TILESIZE+self.playerOffsetX,j*TILESIZE+self.playerOffsetY-TILESIZE),tmpRect)
                        if self.map.tile[x][y].f is not None:
                            tmpRect.top = (self.map.tile[x][y].f[2] // 32) * TILESIZE
                            tmpRect.left = (self.map.tile[x][y].f[2] % 32) * TILESIZE
                            self.surface.blit(self.engine.map.tileSheets[self.map.tile[x][y].f[0]][self.map.tile[x][y].f[1]], (i*TILESIZE+self.playerOffsetX,j*TILESIZE+self.playerOffsetY),tmpRect)
                    
        else:
            if self.playerPos==[-1,-1]:
                if self.mousePos[0]<=self.map.width-1 and self.mousePos[1]<=self.map.height-1:
                    self.surface.blit(self.playerSprite,(self.mousePos[0]*TILESIZE+self.playerOffsetX,self.mousePos[1]*TILESIZE+self.playerOffsetY),(0,0,TILESIZE,TILESIZE))
            else:
                self.surface.blit(self.playerSprite,(self.playerPos[0]*TILESIZE+self.playerOffsetX,self.playerPos[1]*TILESIZE+self.playerOffsetY),(32*self.facing,0,TILESIZE,TILESIZE))
        
        screen.blit(self.surface,(self.posx,self.posy))
        screen.blit(self.text,self.textpos)
        pygame.display.update()
    def canMove(self,x,y):
        if x < 0 or y < 0 or x >= self.map.width or y >= self.map.height or self.map.tile[x][y].t==1:
            return False
        else:
            return True
    def _handleEvents(self,event):
        if event.type == pygame.MOUSEMOTION:
            if self.playerPos==[-1,-1]:
                self.mousePos[0] = (event.pos[0]-self.posx)//TILESIZE
                self.mousePos[1] = (event.pos[1]-self.posy)//TILESIZE
        
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1 and self.playerPos==[-1,-1]:
            if self.canMove((event.pos[0]-self.posx)//TILESIZE,(event.pos[1]-self.posy)//TILESIZE):
                self.playerPos[0] = (event.pos[0]-self.posx)//TILESIZE
                self.playerPos[1] = (event.pos[1]-self.posy)//TILESIZE
        if event.type == pygame.KEYDOWN:
            
            k= pygame.key.get_pressed()
            if k[pygame.K_ESCAPE]:
                self.hovering=False
                self.moving=False
                self.moved=False
                self.nextMove=-1
                self.playerPos = [-1,-1]
                self.mousePos= [-1,-1]
                self.facing=0
                self.loading=False
                self.engine.playing=False
                self.musicManager.pause()
            elif k[pygame.K_a] and self.playerPos!=[-1,-1]:
                if self.canMove(self.playerPos[0]-1,self.playerPos[1]):
                    if not self.moving:
                        self.moving=True
                        self.facing=8
                        self.tick = int(time.clock()*1000)
                        self.playerPos[0]-=1
                    #else:
                    self.nextMove=8
                elif not self.moving:
                    self.facing=8
            elif k[pygame.K_d] and self.playerPos!=[-1,-1]:
                if self.canMove(self.playerPos[0]+1,self.playerPos[1]):
                    if not self.moving:
                        self.moving=True
                        self.facing=3
                        self.tick = int(time.clock()*1000)
                        self.playerPos[0]+=1
                    #else:
                    self.nextMove = 3
                elif not self.moving:
                    self.facing=3
            elif k[pygame.K_w] and self.playerPos!=[-1,-1]:
                if self.canMove(self.playerPos[0],self.playerPos[1]-1):
                    if not self.moving:
                        self.moving=True
                        self.facing=6
                        self.tick = int(time.clock()*1000)
                        self.playerPos[1]-=1
                    #else:
                    self.nextMove = 6
                elif not self.moving:
                    self.facing=5
            elif k[pygame.K_s] and self.playerPos!=[-1,-1]:
                if self.canMove(self.playerPos[0],self.playerPos[1]+1):
                    if not self.moving:
                        self.moving=True
                        self.facing=1
                        self.tick = int(time.clock()*1000)
                        self.playerPos[1]+=1
                    #else:
                    self.nextMove = 1
                elif not self.moving:
                    self.facing=0
        elif event.type==pygame.KEYUP:
            self.nextMove=-1
    
class MapEditor():
    def __init__(self):
        self.openedFile = None
        self.oldFile=None
        self.selectionX = -1
        self.selectionY = -1
        self.selectedLayer = 0
        self.playing = False
        self.showTileTypes = False
        self.mapLoaded = False
        self.painting=False
        self.dialogOpened=False
        self.error = 0
        self.mapName = ""
        self.songName = ""
        self.errorMessages = [
            "Couldn't read the map file properly!",
            "Error with saving. Please make sure the map name is proper (a to z)",
            "THE MAP MUST HAVE A TITLE",
            "There's some serious trouble in opening the file. The file needs to be in data/tilesets/ and be a .png",
            "Please open a map file",
            "The file must end with numbers, i.e. Tiles5.png or Tiles16.png",
            "Can't paint blank!",
            "A VERY BAD ERROR HAS OCCURED. TRY TO GO ONE STEP BACK IN WHAT YOU JUST DID!"
            ]
        self.Map = MapClass()
        self.mapSurface = pygame.Surface((TILESIZE*self.Map.width,TILESIZE*self.Map.height))
        self.header = Header()
        self.header.engine = self
        self.mapProps = MapProperties()
        self.mapProps.engine = self
        self.buttons = LayerButtons()
        self.buttons.engine = self
        
        self.map = MapArea()
        self.map.engine = self
        self.map.drawMap()
        
        
        self.tileScroller = TileScroller()
        self.tileScroller.engine = self
        self.tileScroller.drawTileScroller()
        
        self.tilePicker = TilePicker()
        self.tilePicker.engine = self
        self.tilePicker.populateTypeList()
        
        self.testPlay = TestPlay()
        self.testPlay.engine = self
        #self.tileScroller.updateScrollSize()
        c = gui.Container(align=-1,valign=-1)
        c.add(self.header,0,0)
        c.add(self.mapProps,20,40+64*11+25)
        c.add(self.map,50,40)
        c.add(self.buttons,70+64*15,40)
        c.add(self.tilePicker,230+64*15+15,40)
        c.add(self.tileScroller,230+64*15+15,200)
        self.app = gui.App()
        self.app.init(c)
        
    def update(self):
        screen.fill(background_colour)
        self.map.redrawMap()
        self.tileScroller.updateTileScroller()
        pygame.event.pump()
        self.app.paint()
        pygame.display.update()
        if self.error==0 and self.openedFile is not None:
            self.header.changeText(self.openedFile)
        elif self.error==0:
            self.header.changeText("Please open a file...")
        
    def _handleEvents(self,event):
        self.app.event(event)
        if event.type == pygame.MOUSEMOTION:
            if event.pos[0] >= 50 and event.pos[0] < (50+self.map.style.width-16) and event.pos[1] >= 40 and event.pos[1] < (40+self.map.style.height-16) and not self.dialogOpened:
                self.map.hovering=True
                self.map.drawHover(event.pos[0]+self.map.sbox.offset[0],event.pos[1]+self.map.sbox.offset[1])
                if self.painting:
                    self.selectionX = (event.pos[0]-50+self.map.sbox.offset[0])//TILESIZE
                    self.selectionY = (event.pos[1]-40+self.map.sbox.offset[1])//TILESIZE
                    self.mapProps.refreshTile(self.selectionX,self.selectionY,1)
            elif event.pos[0]>=230+64*15+16 and event.pos[0]<(64*15+230+9*64+16) and event.pos[1] >=200 and event.pos[1] < 200+10*64:
                self.tileScroller.hovering = True
                self.tileScroller.drawHover(event.pos[0]+self.tileScroller.sbox.offset[0]-230-64*15-16,event.pos[1]+self.tileScroller.sbox.offset[1]-200,0)
            else:
                self.map.hovering=False
                self.tileScroller.hovering=False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.dialogOpened:
            if event.pos[0] >= 50 and event.pos[0] < (50+self.map.style.width-16) and event.pos[1] >= 40 and event.pos[1] < (40+self.map.style.height-16):
                if self.selectionX == (event.pos[0]-50+self.map.sbox.offset[0])//TILESIZE and self.selectionY == (event.pos[1]-40+self.map.sbox.offset[1])//TILESIZE or self.openedFile==None:
                    if self.openedFile != None:
                        self.mapProps.refreshTile(self.selectionX,self.selectionY,1)
                        self.painting=True
                    self.selectionX = -1
                    self.selectionY = -1
                else:
                    self.selectionX = (event.pos[0]-50+self.map.sbox.offset[0])//TILESIZE
                    self.selectionY = (event.pos[1]-40+self.map.sbox.offset[1])//TILESIZE
                    self.mapProps.refreshTile(self.selectionX,self.selectionY,1)
                    self.painting=True
            elif event.pos[0]>=230+64*15+16 and event.pos[0]<(64*15+230+9*64+16) and event.pos[1] >=200 and event.pos[1] < 200+10*64:
                if self.tileScroller.selectedX == (event.pos[0]+self.tileScroller.sbox.offset[0]-230-64*15-16)//TILESIZE and self.tileScroller.selectedY == (event.pos[1]+self.tileScroller.sbox.offset[1]-200)//TILESIZE:
                    self.tileScroller.selectedX=-1
                    self.tileScroller.selectedY=-1
                else:
                    self.tileScroller.drawHover(event.pos[0]+self.tileScroller.sbox.offset[0]-230-64*15-16,event.pos[1]+self.tileScroller.sbox.offset[1]-200,1)
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL] and keys[pygame.K_z]:
                undo.stack().undo()
            elif keys[pygame.K_LCTRL] and keys[pygame.K_y]:
                undo.stack().redo()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.painting=False

mapEdit = MapEditor()
running = True
while running:
    try:
        if mapEdit.playing:
            if not mapEdit.testPlay.loading:
                mapEdit.testPlay.playUpdate()
        else:
            mapEdit.update()
        if mapEdit.error==8:
            mapEdit.error=0
            
    except Exception, e:
        print Exception, e
        mapEdit.error=8
        mapEdit.header.updateErrorMsg()
        mapEdit.app.paint()
        pygame.display.update()
    #clock.tick()
    #print "fps:", clock.get_fps()
    for event in pygame.event.get():
        #try:
        if mapEdit.playing:
            mapEdit.testPlay._handleEvents(event)
        else:
            mapEdit._handleEvents(event)
        #except Exception, e:
        #    mapEdit.error=8
        #    mapEdit.header.updateErrorMsg()
    if event.type == pygame.QUIT:
        running = False