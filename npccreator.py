import pygame
from objects import *
from constants import *
from pgu import gui
import re
import global_vars as g
import os
import json
import random
import time

background_colour = (60,60,60)
fontcolor=(255,255,255)
nameColor=(255,255,0)
(width, height) = (512, 832)
screen = pygame.display.set_mode((width, height),pygame.DOUBLEBUF)
surface = pygame.Surface((32,32))
surface.fill((255,255,255))
surface.set_colorkey((255,255,255))
COLOR_KEY=((255,255,255))
surface.blit(pygame.image.load('data/icons/char.png').convert_alpha(),(0,0))
pygame.display.set_icon(surface)
pygame.display.set_caption('Kultainen ES NPC Editor')
pygame.display.flip()

class charControl(gui.Table):
    def __init__(self):
        gui.Table.__init__(self)
        self.engine=None
        def btnNextHat(btn):
            if self.engine.hat < 3:
                self.engine.hat+=1
            else:
                self.engine.hat=0
            self.engine.updateCharSprite()
        def btnPrevHat(btn):
            if self.engine.hat > 0:
                self.engine.hat-=1
            else:
                self.engine.hat=3
            self.engine.updateCharSprite()
            
        def btnNextFace(btn):
            if self.engine.face < 3:
                self.engine.face+=1
            else:
                self.engine.face=0
            self.engine.updateCharSprite()
        def btnPrevFace(btn):
            if self.engine.face > 0:
                self.engine.face-=1
            else:
                self.engine.face=3
            self.engine.updateCharSprite()
            
        def btnNextShoes(btn):
            if self.engine.shoes < 1:
                self.engine.shoes+=1
            else:
                self.engine.shoes=0
            self.engine.updateCharSprite()
        def btnPrevShoes(btn):
            if self.engine.shoes > 0:
                self.engine.shoes-=1
            else:
                self.engine.shoes=1
            self.engine.updateCharSprite()
            
        def btnNextShirt(btn):
            if self.engine.shirt < 2:
                self.engine.shirt+=1
            else:
                self.engine.shirt=0
            self.engine.updateCharSprite()
        def btnPrevShirt(btn):
            if self.engine.shirt > 0:
                self.engine.shirt-=1
            else:
                self.engine.shirt=2
            self.engine.updateCharSprite()


        
        self.tr()
        self.td(gui.Spacer(0,30))
        self.tr()
        self.td(gui.Spacer(64,0))
        self.td(gui.Spacer(64,0))
        self.td(gui.Spacer(256,0))
        self.td(gui.Spacer(64,0))
        self.td(gui.Spacer(64,0))
        self.tr()
        
        self.td(gui.Spacer(0, 0))
        btn = gui.Button("<-", width=24, height=24)
        btn.connect(gui.CLICK, btnPrevHat, None)
        self.td(btn)
        self.td(gui.Spacer(0, 0))
        btn = gui.Button("->", width=24, height=24)
        btn.connect(gui.CLICK, btnNextHat, None)
        self.td(btn)
        self.tr()
        self.td(gui.Spacer(0,8))
        self.tr()
        self.td(gui.Spacer(0, 0))
        btn = gui.Button("<-", width=24, height=24)
        btn.connect(gui.CLICK, btnPrevFace, None)
        self.td(btn)
        self.td(gui.Spacer(0, 0))
        btn = gui.Button("->", width=24, height=24)
        btn.connect(gui.CLICK, btnNextFace, None)
        self.td(btn)
        self.tr()
        self.td(gui.Spacer(0,8))
        self.tr()
        
        self.td(gui.Spacer(0, 0))
        btn = gui.Button("<-", width=24, height=24)
        btn.connect(gui.CLICK, btnPrevShirt, None)
        self.td(btn)
        self.td(gui.Spacer(0, 0))
        btn = gui.Button("->", width=24, height=24)
        btn.connect(gui.CLICK, btnNextShirt, None)
        self.td(btn)
        self.tr()
        self.td(gui.Spacer(0,8))
        self.tr()
        
        self.td(gui.Spacer(0, 0))
        btn = gui.Button("<-", width=24, height=24)
        btn.connect(gui.CLICK, btnPrevShoes, None)
        self.td(btn)
        self.td(gui.Spacer(0, 0))
        btn = gui.Button("->", width=24, height=24)
        btn.connect(gui.CLICK, btnNextShoes, None)
        self.td(btn)
        self.tr()
        self.td(gui.Spacer(0,18))
        self.tr()
        
        self.td(gui.Spacer(0,0))
        btn = gui.Button("<--", width=24, height=24)
        btn.connect(gui.CLICK, self.btnPrevClass, None)
        self.td(btn)
        self.td(gui.Spacer(0,0))
        btn = gui.Button("-->", width=24, height=24)
        btn.connect(gui.CLICK, self.btnNextClass, None)
        self.td(btn)
    def btnNextClass(self,btn):
        if self.engine.Facing <9:
            self.engine.Facing+=1
        else:
            self.engine.Facing =0
        self.engine.updateCharSprite()

    def btnPrevClass(self,btn):
        if self.engine.Facing >0:
            self.engine.Facing-=1
        else:
            self.engine.Facing =9
        self.engine.updateCharSprite()
class textarea(gui.Container):
    def __init__(self):
        gui.Container.__init__(self)
        label=gui.Label("Text: ",color=fontcolor)
        self.textArea = gui.TextArea(value="",width=512-label.style.width-32,height=64,size=16)
        self.add(label,0,(self.textArea.style.height-label.style.height)/2)
        self.add(self.textArea,label.style.width,0)
        self.engine=None
class Buttons(gui.Container):
    def __init__(self):
        gui.Container.__init__(self)
        self.engine=None
        
        #regex=r'[^a-zA-Z0-9 -]'
        def special_match(strg, search=re.compile(r'[^a-zA-Z0-9 -]').search):
            if bool(search(strg)):
                if strg=='\xe4' or strg=='\xc4' or strg=='\xf6' or strg=='\xd6':
                    return True
                return False
            return True
        def intMatch(str,search=re.compile(r'[^0-9]').search):
            if bool(search(str)):
                return False
            return True
        def fnc1(self):
            self.input1.value=""
            self.input2.value="0"
            self.typeList.value = NPC_WALKTYPE_STOPPED
            self.engine.maps[:]=[]
            self.engine.mapButtons.label2.set_text("")
            self.engine.mapButtons.xInput._setvalue("0")
            self.engine.mapButtons.yInput._setvalue("0")
            self.engine.mapButtons.dirList.value=DIR_DOWN
            self.engine.mapButtons.populateTypeList()
            self.engine.mapButtons.xInput.disabled=True
            self.engine.mapButtons.yInput.disabled=True
            self.engine.mapButtons.dirList.disabled=True
            self.engine.mapButtons.btn1.disabled=True
            self.engine.mapButtons.btn3.disabled=True
            self.engine.textarea.textArea._setvalue("")
            self.engine.Facing=0
            self.engine.hat = 1
            self.engine.shirt=0
            self.engine.shoes=0
            self.engine.face=1
            self.engine.updateCharSprite()
        def fnc2():
            if self.typeList.value == NPC_WALKTYPE_RESTRICTED:
                self.input2.disabled = False
            else:
                self.input2.disabled = True
                self.input2.value="0"
        def fnc3():
            if len(self.input2.value)>0:
                if not intMatch(self.input2.value[len(self.input2.value)-1]):
                    self.input2.value = self.input2.value[:-1]
        def fnc4():
            if len(self.input1.value)>0:
                if not special_match(self.input1.value[len(self.input1.value)-1]):
                    self.input1.value = self.input1.value[:-1]
            if len(self.input1.value)==0:
                self.button2.disabled=True
            else:
                self.button2.disabled=False
        def fnc5():
            npc = {"t":self.typeList.value, 'r':int(self.input2.value),'f':self.engine.Facing,'h':self.engine.hat,'s':self.engine.shirt,'sh':self.engine.shoes,'fa':self.engine.face,'te':self.engine.textarea.textArea.value,'m':self.engine.maps,'type':self.npcTypeList.value}
            with open(g.dataPath+'/npc/'+self.input1.value+'.npc','w') as fp:
                json.dump(npc, fp)
        def selectFile(object):
            self.openFile(object.value)
        def fnc6():
            a = gui.FileDialog(path=g.dataPath+"/npc/")
            a.connect(gui.CHANGE,selectFile,a)
            a.open()
        button1 = gui.Button("New", width=75,height=30)
        button1.connect(gui.CLICK,fnc1,self)
        self.button2 = gui.Button("Save", width=75,height=30,disabled=True)
        self.button2.connect(gui.CLICK,fnc5)
        self.button3 = gui.Button("Open", width=75,height=30)
        self.button3.connect(gui.CLICK,fnc6)
        label1=gui.Label("NPC name:",color=fontcolor)
        label2=gui.Label("Walk type:",color=fontcolor)
        label3=gui.Label("Walking area radius:",color=fontcolor)
        label4=gui.Label("NPC type:",color=fontcolor)
        self.input1 = gui.Input(value="",width=200)
        self.input1.connect(gui.CHANGE,fnc4)
        self.input2 = gui.Input(value="0",width=50,disabled=True)
        self.input2.connect(gui.CHANGE,fnc3)
        self.typeList = gui.Select(value=0)
        self.typeList.add("WALKTYPE_STOPPED",0)
        self.typeList.add("WALKTYPE_RESTRICTED",1)
        self.typeList.add("WALKTYPE_FREEWALK",2)
        self.typeList.connect(gui.CHANGE,fnc2)
        
        self.npcTypeList=gui.Select(value=0)
        self.npcTypeList.add("NPC_ACTIONTYPE_TALK",0)
        self.npcTypeList.add("NPC_ACTIONTYPE_HEAL",1)
        self.npcTypeList.add("NPC_ACTIONTYPE_SHOP",2)
        self.add(label1,10,20)
        self.add(self.input1,20+label1.style.width,20)
        self.add(label2,10,30+label1.style.height)
        self.add(label3,10,40+label1.style.height+label2.style.height)
        self.add(label4,10,50+label1.style.height+label2.style.height+label3.style.height)
        self.add(self.input2,20+label3.style.width,40+label1.style.height+label2.style.height)
        self.add(self.typeList,20+label1.style.width,30+label1.style.height)
        self.add(button1,width-100,15)
        self.add(self.button2,width-100,55)
        self.add(self.button3,width-100,95)
        self.add(self.npcTypeList,20+label1.style.width,50+label1.style.height+label2.style.height+label3.style.height)
        
    def openFile(self,fileName):
        with open(fileName,'r') as fp:
            npc = json.load(fp)
        tmpName = fileName.replace('/','\\').split('\\')
        self.input1.value=tmpName[len(tmpName)-1][:-4]
        self.input2.value=str(npc["r"])
        self.typeList.value = npc["t"]
        try:
            self.npcTypeList.value=npc["type"]
        except:
            self.npcTypeList.value=0
        self.engine.maps[:]=[]
        self.engine.maps=npc["m"]
        for c in self.engine.maps:
            c[0]=str(c[0])
        self.engine.mapButtons.populateTypeList()
        if len(self.engine.maps)>0:
            self.engine.mapButtons.label2.set_text(self.engine.maps[0][0])
            self.engine.mapButtons.xInput._setvalue(str(self.engine.maps[0][1]))
            self.engine.mapButtons.yInput._setvalue(str(self.engine.maps[0][2]))
            self.engine.mapButtons.dirList.value=self.engine.maps[0][3]
            self.engine.mapButtons.xInput.disabled=False
            self.engine.mapButtons.yInput.disabled=False
            self.engine.mapButtons.dirList.disabled=False
            self.engine.mapButtons.btn1.disabled=False
            self.engine.mapButtons.btn3.disabled=False
        else:
            self.engine.mapButtons.label2.set_text("")
            self.engine.mapButtons.xInput._setvalue("0")
            self.engine.mapButtons.yInput._setvalue("0")
            self.engine.mapButtons.dirList.value=0
            self.engine.mapButtons.xInput.disabled=True
            self.engine.mapButtons.yInput.disabled=True
            self.engine.mapButtons.dirList.disabled=True
            self.engine.mapButtons.btn1.disabled=True
            self.engine.mapButtons.btn3.disabled=True
        self.engine.Facing=npc["f"]
        self.engine.hat = npc["h"]
        self.engine.shirt=npc["s"]
        self.engine.shoes=npc["sh"]
        self.engine.face=npc["fa"]
        self.engine.textarea.textArea._setvalue(npc["te"])
        self.engine.updateCharSprite()
class mapButtons(gui.Container):
    def __init__(self):
        gui.Container.__init__(self)
        self.engine=None
        def selectFile(object):
            self.reset()
            tmpName = object.value.replace('/','\\').split('\\')
            self.label2.set_text(tmpName[len(tmpName)-1][:-4])
            self.xInput.disabled=False
            self.yInput.disabled=False
            self.dirList.disabled=False
            self.btn1.disabled=False
            self.btn3.disabled=False
            
            #self.btn2.disabled=False
        def fnc1():
            a = gui.FileDialog(path=g.dataPath+"/maps/")
            a.connect(gui.CHANGE,selectFile,a)
            a.open()
        def fnc2():
            if len(self.engine.maps)>0:
                self.label2.set_text(self.engine.maps[self.typeList.value][0])
                self.xInput._setvalue(str(self.engine.maps[self.typeList.value][1]))
                self.yInput._setvalue(str(self.engine.maps[self.typeList.value][2]))
                self.dirList.value=self.engine.maps[self.typeList.value][3]
            self.xInput.disabled=False
            self.yInput.disabled=False
            self.dirList.disabled=False
            self.btn1.disabled=False
            self.btn2.disabled=False
            self.btn3.disabled=False
        def fnc3():
            if self.dirList.value == DIR_DOWN:
                self.engine.Facing=0
            elif self.dirList.value == DIR_LEFT:
                self.engine.Facing=8
            elif self.dirList.value == DIR_UP:
                self.engine.Facing=5
            elif self.dirList.value == DIR_RIGHT:
                self.engine.Facing=3
            self.engine.updateCharSprite()
        def fnc4():
            found=False
            for i in xrange(len(self.engine.maps)):
                if self.engine.maps[i][0]==self.label2.value:
                    self.engine.maps[i][1]=int(self.xInput.value)
                    self.engine.maps[i][2]=int(self.yInput.value)
                    self.engine.maps[i][3]=self.dirList.value
                    found=True
                    break
            if not found:
                self.engine.maps.append([self.label2.value,int(self.xInput.value),int(self.yInput.value),self.dirList.value])
            self.populateTypeList()
            self.typeList.disabled=False
            

        def fnc6():
            if self.engine.playing:
                self.engine.playing = False
            else:
                self.engine.testPlay.initatePlay()
                self.engine.playing = True
        def intMatch(str,search=re.compile(r'[^0-9]').search):
            if bool(search(str)):
                return False
            return True
        def fnc7():
            if len(self.xInput.value)>0:
                if not intMatch(self.xInput.value[len(self.xInput.value)-1]):
                    self.xInput.value = self.xInput.value[:-1]
        def fnc8():
            if len(self.yInput.value)>0:
                if not intMatch(self.yInput.value[len(self.yInput.value)-1]):
                    self.yInput.value = self.yInput.value[:-1]
        
        btn=gui.Button("Select map")
        btn.connect(gui.CLICK,fnc1)
        self.add(btn,0,30)
        self.typeList = gui.Select(disabled=True)
        self.typeList.add("Please insert a map")
        self.typeList.connect(gui.CHANGE,fnc2)
        self.add(self.typeList,0,0)
        label1=gui.Label("Map name: ",color=fontcolor)
        self.add(label1,width/9*4,0)
        self.label2 = gui.Label("",color=nameColor)
        self.add(self.label2,width/9*4+label1.style.width,0)
        label3=gui.Label("X: ",color=fontcolor)
        label4=gui.Label("Y: ",color=fontcolor)
        self.add(label3,width/9*4,label1.style.height+10)
        self.add(label4,width/9*4,(label1.style.height+10)*2)
        self.xInput=gui.Input(value="0",width=30,disabled=True)
        self.xInput.connect(gui.CHANGE,fnc7)
        self.yInput=gui.Input(value="0",width=30,disabled=True)
        self.yInput.connect(gui.CHANGE,fnc8)
        self.add(self.xInput,width/9*4+label3.style.width,label1.style.height+10)
        self.add(self.yInput,width/9*4+label3.style.width,(label1.style.height+10)*2)
        label5=gui.Label("Direction: ",color=fontcolor)
        self.add(label5,width/9*4,(label1.style.height+10)*3)
        self.dirList = gui.Select(value=DIR_DOWN,disabled=True)
        self.dirList.add("DIR_DOWN",DIR_DOWN)
        self.dirList.add("DIR_LEFT",DIR_LEFT)
        self.dirList.add("DIR_UP",DIR_UP)
        self.dirList.add("DIR_RIGHT",DIR_RIGHT)
        self.dirList.connect(gui.CHANGE,fnc3)
        self.add(self.dirList,width/9*4+label5.style.width,(label1.style.height+10)*3)
        self.btn1=gui.Button("Insert",width=100,height=30,disabled=True)
        self.btn1.connect(gui.CLICK,fnc4)
        self.add(self.btn1,width/9*4,(label1.style.height+10)*4)
        self.btn2=gui.Button("Remove",width=100,height=30,disabled=True)
        self.btn2.connect(gui.CLICK,self.fnc5)
        self.add(self.btn2,width/9*4+120,(label1.style.height+10)*4)
        self.btn3=gui.Button("Test play",width=100,height=30,disabled=True)
        self.btn3.connect(gui.CLICK,fnc6)
        self.add(self.btn3,width/9*4,(label1.style.height+12)*5)
    def fnc5(self):
        for i in xrange(len(self.engine.maps)):
            if self.engine.maps[i][0]==self.label2.value:
                del self.engine.maps[i]
                break
        self.populateTypeList()
        if len(self.engine.maps)>0:
            self.label2.set_text(self.engine.maps[self.typeList.value][0])
            self.xInput._setvalue(str(self.engine.maps[self.typeList.value][1]))
            self.yInput._setvalue(str(self.engine.maps[self.typeList.value][2]))
            self.dirList.value=self.engine.maps[self.typeList.value][3]
        else:
            self.reset()
            self.xInput.disabled=True
            self.yInput.disabled=True
            self.dirList.disabled=True
            self.btn1.disabled=True
            self.btn3.disabled=True
    def reset(self):
        self.label2.set_text("")
        self.xInput._setvalue("0")
        self.yInput._setvalue("0")
        self.dirList.value=DIR_DOWN
    def populateTypeList(self):
        x=len(self.typeList.options.widgets)-1
        while x>=0:
            self.typeList._remove(x)
            x-=1
        for i in xrange(len(self.engine.maps)):
            self.typeList.add(self.engine.maps[i][0],i)
        found=False
        for i in xrange(len(self.engine.maps)):
            if self.engine.maps[i][0]==self.label2.value:
                self.typeList.value=i
                found=True
        if not found:
            self.typeList.value=0
        x=len(self.typeList.options.widgets)-1
        if x>=0:
            self.btn2.disabled=False
        else:
            self.btn2.disabled=True
            
class TestPlay():
    def __init__(self):
        self.surface = pygame.Surface((8*64,8*64))
        self.hovering=False
        self.moving=False
        self.moved=False
        self.loading=False
        self.engine=None
        self.map=MapClass()
        self.nextMove=-1
        self.playerPos = [-1,-1]
        self.mousePos= [-1,-1]
        self.facing=0
        self.type=0
        #self.playerSprite = pygame.image.load('data/sprites/char.png').convert()
        #self.playerSprite.set_colorkey(COLOR_KEY,pygame.RLEACCEL)
        #self.playerSprite = pygame.transform.scale(self.playerSprite,(self.playerSprite.get_width()*2,self.playerSprite.get_height()*2))
        
        
        self.posx=(width-self.surface.get_width())/2
        self.posy=(height-self.surface.get_height())/2
        self.playerOffsetX=0
        self.playerOffsetY=0
        self.tick=0
        font=pygame.font.Font(None,36)
        self.text=font.render("Press ESC to quit the demo.",1,(255,255,255))
        self.textpos=self.text.get_rect()
        self.textpos.y=50
        self.textpos.centerx=screen.get_rect().centerx
        
    def initatePlay(self):
        self.loading=True
        self.engine.initMap()
        self.map.tile = [[TileClass() for i in range(self.engine.Map.height)] for i in range(self.engine.Map.width)]
        self.map.tile = self.engine.Map.tile
        self.map.width = self.engine.Map.width
        self.map.height = self.engine.Map.height
        self.playerSprite=pygame.Surface((32*10,32),pygame.SRCALPHA)
        self.spriteImageRect = pygame.Rect(0,0,32,32)
        
        self.playerSprite.blit(self.engine.tempImage, (0,0),(0,0,32*10,32))
        self.playerSprite.blit(self.engine.tempHatImage, (0,0),(0,self.engine.hat*32,32*10,32))
        self.playerSprite.blit(self.engine.tempShirtImage, (0,0),(0,self.engine.shirt*32,32*10,32))
        self.playerSprite.blit(self.engine.tempShoesImage, (0,0),(0,self.engine.shoes*32,32*10,32))
        self.playerSprite.blit(self.engine.tempFaceImage, (0,0),(0,self.engine.face*32,32*10,32))
        self.playerSprite = pygame.transform.scale(self.playerSprite,(64*10,64)).convert_alpha()
        self.type=self.engine.buttons.typeList.value
        self.loading=False

    def posChange(self,direction):
        if direction == DIR_DOWN:
            return [0,1]
        elif direction == DIR_LEFT:
            return [-1,0]
        elif direction == DIR_UP:
            return [0,-1]
        elif direction == DIR_RIGHT:
            return [1,0]
    def playUpdate(self):
        screen.fill((60,60,60))
        self.surface.fill((0,0,0))
        tmpTick=time.time()*1000
        tmpRect = pygame.Rect(0,0,64,64)
        if self.moving:
            if (self.facing==3 or self.facing==4):
                self.playerOffsetX=(64-(tmpTick-self.tick)//10)
            elif (self.facing==8 or self.facing==9):
                self.playerOffsetX=-(64-(tmpTick-self.tick)//10)
            elif (self.facing==1 or self.facing==2):
                self.playerOffsetY=(64-(tmpTick-self.tick)//10)
            elif (self.facing==6 or self.facing==7):
                self.playerOffsetY=-(64-(tmpTick-self.tick)//10)
            if tmpTick-self.tick>=WALKSPEED/2 and not self.moved:
                self.facing-=1
                self.moved=True
            elif tmpTick-self.tick>=WALKSPEED:
                self.moving=False
                self.moved=False
                self.nextMove=-1
                if self.facing==1:
                    self.facing=0
                elif self.facing==6:
                    self.facing=5
                elif self.facing==9:
                    self.facing=8
                elif self.facing==4:
                    self.facing=3
                self.playerOffsetX=0
                self.playerOffsetY=0

            
        else:
            self.playerOffsetX=0
            self.playerOffsetY=0
            if tmpTick-self.tick>=4000 and self.type != 0 and not self.loading:
                r=[DIR_DOWN,DIR_LEFT,DIR_UP,DIR_RIGHT]
                posChg=[-1,-1]
                dir=DIR_DOWN
                while 1 and len(r)>0:
                    dir=random.choice(r)
                    posChg=self.posChange(dir)
                    if int(self.engine.buttons.input2.value)==0 and self.type==NPC_WALKTYPE_RESTRICTED:
                        posChg=[0,0]
                        break
                    if self.canMove(self.playerPos[0]+posChg[0],self.playerPos[1]+posChg[1]):
                        if self.type==NPC_WALKTYPE_RESTRICTED and abs(self.playerPos[0]+posChg[0]-int(self.engine.mapButtons.xInput.value))<=int(self.engine.buttons.input2.value) and abs(self.playerPos[1]+posChg[1]-int(self.engine.mapButtons.yInput.value))<=int(self.engine.buttons.input2.value):
                            break
                        elif self.type==NPC_WALKTYPE_FREEWALK:
                            break
                    else:
                        r.remove(dir)
                #print dir, posChg
                if posChg!=[-1,-1]:
                    self.tick =  time.time()*1000
                    if posChg!=[0,0]:
                        self.moving=True
                        self.playerPos[0]+=posChg[0]
                        self.playerPos[1]+=posChg[1]
                        if dir==DIR_DOWN:
                            self.facing=2
                        elif dir==DIR_UP:
                            self.facing=7
                        elif dir==DIR_RIGHT:
                            self.facing=4
                        elif dir==DIR_LEFT:
                            self.facing=9
                    else:
                        if dir==DIR_DOWN:
                            self.facing=0
                        elif dir==DIR_UP:
                            self.facing=5
                        elif dir==DIR_RIGHT:
                            self.facing=3
                        elif dir==DIR_LEFT:
                            self.facing=8
                
        if self.map.tile != []:
            for i in range(-1,16):
                for j in range(-1,12):
                    if self.playerPos[0]!=-1 and self.playerPos[1]!=-1:
                        x = self.playerPos[0]-3+i
                        y= self.playerPos[1]-3+j
                    else:
                        x=i
                        y=j
                    if x>=self.map.width or y>=self.map.height or x<0 or y<0:
                        if x>=self.map.width or y>=self.map.height:
                            self.surface.fill((0,0,0),((i)*64+self.playerOffsetX,(j)*64+self.playerOffsetY,64,64))
                    else:
                        if self.map.tile[x][y].l1 is not None:
                            tmpRect.top = (self.map.tile[x][y].l1[2] // 32) * 64
                            tmpRect.left = (self.map.tile[x][y].l1[2] % 32) * 64
                            print self.engine.tileSheets[self.map.tile[x][y].l1[0]][self.map.tile[x][y].l1[1]]
                           
                            self.surface.blit(self.engine.tileSheets[self.map.tile[x][y].l1[0]][self.map.tile[x][y].l1[1]], (i*64+self.playerOffsetX,j*64+self.playerOffsetY),tmpRect)
                        if self.map.tile[x][y].l2 is not None:
                            tmpRect.top = (self.map.tile[x][y].l2[2] // 32) * 64
                            tmpRect.left = (self.map.tile[x][y].l2[2] % 32) * 64
                            self.surface.blit(self.engine.tileSheets[self.map.tile[x][y].l2[0]][self.map.tile[x][y].l2[1]], (i*64+self.playerOffsetX,j*64+self.playerOffsetY),tmpRect)
                        if self.map.tile[x][y].l3 is not None:
                            tmpRect.top = (self.map.tile[x][y].l3[2] // 32) * 64
                            tmpRect.left = (self.map.tile[x][y].l3[2] % 32) * 64
                            print self.engine.tileSheets
                            print self.map.tile[x][y].l3[0]
                            print self.map.tile[x][y].l3[1]
                            print self.engine.tileSheets[self.map.tile[x][y].l3[0]][self.map.tile[x][y].l3[1]]
                            self.surface.blit(self.engine.tileSheets[self.map.tile[x][y].l3[0]][self.map.tile[x][y].l3[1]], (i*64+self.playerOffsetX,j*64+self.playerOffsetY),tmpRect)
                        
                        if self.playerPos==[-1,-1]:
                            if x==self.mousePos[0] and y==self.mousePos[1]:
                                self.surface.blit(self.playerSprite,(i*64,j*64),(0,0,64,64))
                        
                        elif x==self.playerPos[0] and y==self.playerPos[1]:
                            self.surface.blit(self.playerSprite,(i*64,j*64),(self.facing*64,0,64,64))
                        
                        elif x==self.playerPos[0]+1 and y==self.playerPos[1] and self.moving and (self.facing==8 or self.facing==9):
                            self.surface.blit(self.playerSprite,(i*64-64,j*64),(self.facing*64,0,64,64))
                            
                        elif x==self.playerPos[0] and y==self.playerPos[1]+1 and self.moving and (self.facing==6 or self.facing==7):
                            self.surface.blit(self.playerSprite,(i*64,j*64-64),(self.facing*64,0,64,64))
                        if x>0 and x < self.map.width and y>=0 and y <= self.map.height-1:
                            if self.map.tile[x-1][y].f is not None:
                                tmpRect.top = (self.map.tile[x-1][y].f[2] // 32) * 64
                                tmpRect.left = (self.map.tile[x-1][y].f[2] % 32) * 64
                                self.surface.blit(self.engine.tileSheets[self.map.tile[x-1][y].f[0]][self.map.tile[x-1][y].f[1]], (i*64+self.playerOffsetX-64,j*64+self.playerOffsetY),tmpRect)
                        if x>=0 and x < self.map.width and y>0 and y < self.map.height:
                            if self.map.tile[x][y-1].f is not None:
                                tmpRect.top = (self.map.tile[x][y-1].f[2] // 32) * 64
                                tmpRect.left = (self.map.tile[x][y-1].f[2] % 32) * 64
                                self.surface.blit(self.engine.tileSheets[self.map.tile[x][y-1].f[0]][self.map.tile[x][y-1].f[1]], (i*64+self.playerOffsetX,j*64+self.playerOffsetY-64),tmpRect)
                        if self.map.tile[x][y].f is not None:
                            tmpRect.top = (self.map.tile[x][y].f[2] // 32) * 64
                            tmpRect.left = (self.map.tile[x][y].f[2] % 32) * 64
                            self.surface.blit(self.engine.tileSheets[self.map.tile[x][y].f[0]][self.map.tile[x][y].f[1]], (i*64+self.playerOffsetX,j*64+self.playerOffsetY),tmpRect)
                    
        else:
            if self.playerPos==[-1,-1]:
                if self.mousePos[0]<=self.map.width-1 and self.mousePos[1]<=self.map.height-1:
                    self.surface.blit(self.playerSprite,(self.mousePos[0]*64+self.playerOffsetX,self.mousePos[1]*64+self.playerOffsetY),(0,0,64,64))
            else:
                self.surface.blit(self.playerSprite,(self.playerPos[0]*64+self.playerOffsetX,self.playerPos[1]*64+self.playerOffsetY),(32*self.facing,0,64,64))
        
        screen.blit(self.surface,(self.posx,self.posy))
        screen.blit(self.text,self.textpos)
        pygame.display.update()
    def canMove(self,x,y):
        if x < 0 or y < 0 or x >= self.map.width or y >= self.map.height or self.map.tile[x][y].t==TILE_TYPE_BLOCKED or self.map.tile[x][y].t==TILE_TYPE_WARP or self.map.tile[x][y].t==TILE_TYPE_NPCAVOID:
            return False
        else:
            return True
    def _handleEvents(self,event):
        #if event.type == pygame.MOUSEMOTION:
        #    if self.playerPos==[-1,-1]:
        #        self.mousePos[0] = (event.pos[0]-self.posx)//64
        #        self.mousePos[1] = (event.pos[1]-self.posy)//64
        
        #if event.type==pygame.MOUSEBUTTONDOWN and event.button==1 and self.playerPos==[-1,-1]:
        #    if self.canMove((event.pos[0]-self.posx)//64,(event.pos[1]-self.posy)//64):
        #        self.playerPos[0] = (event.pos[0]-self.posx)//64
        #        self.playerPos[1] = (event.pos[1]-self.posy)//64
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
        elif event.type==pygame.KEYUP:
            self.nextMove=-1
class NPCEditor():
    def __init__(self):
        self.npcSurface = pygame.Surface((16*32,16*32))
        self.buttons = Buttons()
        self.buttons.engine = self
        self.bgBox = pygame.Rect(width/2-128, height/3-128, 256, 256)
        self.surfaceNormal = pygame.Surface((256,256))
        self.surfaceNormal.fill((249,221,138))
        self.Facing=0
        self.hat = 1
        self.shirt=0
        self.shoes=0
        self.face=1
        self.playing=False
        self.Map=MapClass()
        self.maps=[]
        self.tempImage = pygame.image.load(g.dataPath + "/sprites/char.png").convert_alpha()
        self.tempHatImage = pygame.image.load(g.dataPath + "/sprites/hat.png").convert_alpha()
        self.tempShirtImage = pygame.image.load(g.dataPath + "/sprites/shirt.png").convert_alpha()
        self.tempShoesImage = pygame.image.load(g.dataPath + "/sprites/shoes.png").convert_alpha()
        self.tempFaceImage = pygame.image.load(g.dataPath + "/sprites/face.png").convert_alpha()
        self.tempSprite = pygame.Surface((32, 32),pygame.SRCALPHA)
        self.tempHatSprite = pygame.Surface((32,32),pygame.SRCALPHA)
        self.tempShirtSprite = pygame.Surface((32,32),pygame.SRCALPHA)
        self.tempShoesSprite = pygame.Surface((32,32),pygame.SRCALPHA)
        self.tempFaceSprite = pygame.Surface((32,32),pygame.SRCALPHA)
        self.spriteScale = 2
        self.spriteImage = pygame.Surface((TILESIZE * self.spriteScale, TILESIZE * self.spriteScale))
        self.spriteHatImage = pygame.Surface((TILESIZE * self.spriteScale,TILESIZE * self.spriteScale))
        self.spriteShirtImage = pygame.Surface((TILESIZE * self.spriteScale, TILESIZE * self.spriteScale))
        self.spriteShoesImage = pygame.Surface((TILESIZE * self.spriteScale, TILESIZE * self.spriteScale))
        self.spriteFaceImage = pygame.Surface((TILESIZE * self.spriteScale, TILESIZE * self.spriteScale))
        self.spriteImageRect = self.spriteImage.get_rect()
        self.spriteImageRect.centerx = width/2
        self.spriteImageRect.centery = height/3
        self.testPlay = TestPlay()
        self.testPlay.engine=self
        self.spriteButtons=charControl()
        self.spriteButtons.engine=self
        self.textarea = textarea()
        self.textarea.engine=self
        self.mapButtons = mapButtons()
        self.mapButtons.engine=self
        c = gui.Container(align=-1,valign=-1)
        c.add(self.buttons,0,0)
        c.add(self.spriteButtons,0,160+32)
        c.add(self.textarea,6,256+160+32)
        c.add(self.mapButtons,6,544)
        self.app = gui.App()
        self.app.init(c)
        self.updateCharSprite()
        self.tileSheets = []
        groundSheets=[]
        for x in range(999):
            try:
                tmpSurface = pygame.image.load('data/tilesets/ground/'+str(x)+'.png').convert_alpha()
                groundSheets.append(pygame.transform.scale(tmpSurface, (tmpSurface.get_rect().width*2,tmpSurface.get_rect().height*2)))
            except:
                break
        self.tileSheets.append(groundSheets)
        
        wallSheets = []
        for x in range(999):
            try:
                tmpSurface = pygame.image.load('data/tilesets/wall/'+str(x)+'.png').convert_alpha()
                wallSheets.append(pygame.transform.scale(tmpSurface, (tmpSurface.get_rect().width*2,tmpSurface.get_rect().height*2)))
            except:
                break
        self.tileSheets.append(wallSheets)
        
        treesSheets = []
        for x in range(999):
            try:
                tmpSurface = pygame.image.load('data/tilesets/trees/'+str(x)+'.png').convert_alpha()
                treesSheets.append(pygame.transform.scale(tmpSurface, (tmpSurface.get_rect().width*2,tmpSurface.get_rect().height*2)))
            except:
                break
        self.tileSheets.append(treesSheets)
        
        propsSheets = []
        for x in range(999):
            try:
                tmpSurface = pygame.image.load('data/tilesets/props/'+str(x)+'.png').convert_alpha()
                propsSheets.append(pygame.transform.scale(tmpSurface, (tmpSurface.get_rect().width*2,tmpSurface.get_rect().height*2)))
            except:
                break
        self.tileSheets.append(propsSheets)
        
        buildingSheets = []
        for x in range(999):
            try:
                tmpSurface = pygame.image.load('data/tilesets/building/'+str(x)+'.png').convert_alpha()
                buildingSheets.append(pygame.transform.scale(tmpSurface, (tmpSurface.get_rect().width*2,tmpSurface.get_rect().height*2)))
            except:
                break
        self.tileSheets.append(buildingSheets)
        
        otherSheets = []
        for x in range(999):
            try:
                tmpSurface = pygame.image.load('data/tilesets/other/'+str(x)+'.png').convert_alpha()
                otherSheets.append(pygame.transform.scale(tmpSurface, (tmpSurface.get_rect().width*2,tmpSurface.get_rect().height*2)))
            except:
                break
        self.tileSheets.append(otherSheets)
    def initMap(self):
        self.testPlay.playerPos = [int(self.mapButtons.xInput.value),int(self.mapButtons.yInput.value)]
        with open(g.dataPath+'/maps/'+self.mapButtons.label2.value+'.map','r') as fp:
            tempMap = json.load(fp)
        self.Map.width = tempMap["width"]
        self.Map.height = tempMap["height"]
        self.Map.tile = [[TileClass() for i in range(tempMap["height"])] for i in range(tempMap["width"])]
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
        self.Map.tile = tmpTiles
    def update(self):
        screen.fill(background_colour)
        screen.blit(self.surfaceNormal,self.bgBox)
        screen.blit(self.spriteImage, self.spriteImageRect)
        
        screen.blit(self.spriteShoesImage, self.spriteImageRect)
        screen.blit(self.spriteShirtImage, self.spriteImageRect)
        screen.blit(self.spriteFaceImage, self.spriteImageRect)
        screen.blit(self.spriteHatImage, self.spriteImageRect)
        #self.buttons.draw()
        pygame.event.pump()
        self.app.paint()
        pygame.display.update()
    def updateCharSprite(self):
        self.tempSprite = pygame.Surface((32, 32),pygame.SRCALPHA)
        self.tempHatSprite = pygame.Surface((32,32),pygame.SRCALPHA)
        self.tempShirtSprite = pygame.Surface((32,32),pygame.SRCALPHA)
        self.tempShoesSprite = pygame.Surface((32,32),pygame.SRCALPHA)
        self.tempFaceSprite = pygame.Surface((32,32),pygame.SRCALPHA)
        self.tempSprite.blit(self.tempImage, (0, 0), (32*self.Facing, 0, 32, 32))
        self.tempHatSprite.blit(self.tempHatImage, (0, 0), (32*self.Facing, self.hat*32, 32, 32))
        self.tempShirtSprite.blit(self.tempShirtImage, (0, 0), (32*self.Facing, self.shirt*32, 32, 32))
        self.tempShoesSprite.blit(self.tempShoesImage, (0, 0), (32*self.Facing, self.shoes*32, 32, 32))
        self.tempFaceSprite.blit(self.tempFaceImage, (0, 0), (32*self.Facing, self.face*32, 32, 32))
        self.spriteShirtImage = pygame.transform.scale(self.tempShirtSprite, (TILESIZE * self.spriteScale, TILESIZE * self.spriteScale))
        self.spriteHatImage = pygame.transform.scale(self.tempHatSprite, (TILESIZE * self.spriteScale, TILESIZE * self.spriteScale))
        self.spriteImage = pygame.transform.scale(self.tempSprite, (TILESIZE * self.spriteScale, TILESIZE * self.spriteScale))
        self.spriteShoesImage = pygame.transform.scale(self.tempShoesSprite, (TILESIZE * self.spriteScale, TILESIZE * self.spriteScale))
        self.spriteFaceImage = pygame.transform.scale(self.tempFaceSprite, (TILESIZE * self.spriteScale, TILESIZE * self.spriteScale))
npcEditor = NPCEditor()
running = True
while running:
    if npcEditor.playing:
        if not npcEditor.testPlay.loading:
            npcEditor.testPlay.playUpdate()
    else:
        npcEditor.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if npcEditor.playing:
            npcEditor.testPlay._handleEvents(event)
        else:
            npcEditor.app.event(event)
            
            if event.type == pygame.KEYDOWN and not npcEditor.buttons.myfocus == npcEditor.buttons.input1 and not npcEditor.textarea.myfocus == npcEditor.textarea.textArea:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    npcEditor.spriteButtons.btnPrevClass(None)
                elif keys[pygame.K_d]:
                    npcEditor.spriteButtons.btnNextClass(None)