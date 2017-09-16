import pyglet
import global_vars as g
from constants import *
from objects import *
import json
import time
import datetime
from twisted.internet import reactor
from pyglet_gui.manager import Manager
from pyglet_gui.text_input import TextInput
from pyglet_gui.theme import Theme
from pyglet_gui.containers import VerticalContainer, Spacer, HorizontalContainer
from pyglet_gui.gui import Label, Frame, Graphic
from pyglet_gui.buttons import HighlightedButton
from pyglet_gui.constants import ANCHOR_BOTTOM_RIGHT

class loginMenu():
    def __init__(self,screen):
        self.screen = screen
        self.username = ""
        self.password = ""
        self.loadedMap=False
        self.charSprite = None
        self.changing=False
        self.naming=False
        self.ready=False
        self.menename=""
        self.bgImg = pyglet.image.load(g.dataPath + '/login/bg_menu.png')
        self.skyImg = pyglet.image.load(g.dataPath+'/login/bg_sky1.png')
        self.ukkeli = pyglet.image.load(g.dataPath+'/login/bg_ukkeli1.png')
        self.ukkeli2 = pyglet.image.load(g.dataPath+'/login/bg_ukkeli2.png')
        self.l1 = pyglet.resource.image(g.dataPath+'/login/logo.png')
        self.ukkeliSprite = pyglet.sprite.Sprite(self.ukkeli,x=0.5*self.screen.width,y=30)
        #self.ukkeliSprite._set_scale(self.screen.width/1920.0)
        
        self.ukkeliSprite2 = pyglet.sprite.Sprite(self.ukkeli2,x=0.5*self.screen.width,y=30)
        #self.ukkeliSprite2._set_scale(self.screen.width/1920.0)
        self.logo = pyglet.sprite.Sprite(self.l1,x=0,y=0)
        #self.logo._set_scale(self.screen.width/1920.0)
        self.initManagers()
        self.startTick = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
        #g.gameEngine.musicManager.queue(pyglet.media.load(g.dataPath+'/sounds/pokemon.mp3'))
        #if g.MUSIC:
        #    g.gameEngine.musicManager.play()
    def exit(self,event):
        g.gameState = GAMESTATE_EXIT
    def tryLogin(self,event):
        if not self.button.disabled:
            #self.username=self.logininput.get_text()
            #self.password=self.passwordinput.get_text()
            #if self.logininput.get_text() != "":
            #    if self.logininput.get_text() == '1':
            #        self.username='test'
            #        self.password='testest'
            #    else:
            self.username=self.logininput.get_text()
            #self.username = "aapinen"
            self.password=self.passwordinput.get_text()
            g.gameEngine.initConnection()
            self.button.disabled = True
            l = reactor.callLater(1,self.f)
    def removeCharCreating(self):
        self.charMan.delete()
        del self.charMan
        self.charSprite=None
        
    def initNameMene(self):
        def sendMeneName(event):
            self.menename=self.nameInput.get_text()
            if len(self.menename)>0:
                self.saveBtn.disabled=True
        self.naming=True
        label = Label("Name Your Mene",color=g.postColor,font_size=18,bold=True)
        #meneTheme = Theme({g.spriteName: {
        #                "image": {
        #                    "source": g.spriteName+'_front.png'
        #                },
        #                "gui_color": [255,255,255,255]
        #            }
        #        },resources_path=g.dataPath+'/menes/'
        #)
        #picture = Graphic(g.spriteName,alternative=meneTheme)
        picture = Graphic(texture=g.gameEngine.resManager.meneSprites[g.spriteName]['front'])
        self.nameInput = TextInput(text="",padding=2,length=12,max_length=12,width=200,font_size=16)
        self.saveBtn = HighlightedButton(label="Save",on_release=sendMeneName,width=100,height=40,font_size=16)
        frame = Frame(VerticalContainer(content=[label,picture,HorizontalContainer([self.nameInput,self.saveBtn])]),path='frame_npc_talk')
        self.meneMan = Manager(frame,
            window=self.screen,
            batch=g.guiBatch,
            theme=g.theme,
            offset=(0,0),
            is_movable=False)
    def removeMenenaming(self):
        self.meneMan.delete()

    def initCreateChar(self):
        def checkClothingOk():
            found=0
            #print g.clothingPairs
            for clothes in g.clothingPairs:
                found=0
                if clothes["type"]=='exclude':
                    if 'shirt' in clothes and clothes['shirt']==myPlayer.shirt:
                        found+=1
                    if 'hat' in clothes and clothes['hat']==myPlayer.hat:
                        found+=1
                    if 'face' in clothes and clothes['face']==myPlayer.face:
                        found+=1
                    if 'shoes' in clothes and clothes['shoes']==myPlayer.shoes:
                        found+=1
                    if found>=2:
                        return False
            return True
        def hatLeft(event):
            myPlayer.hat-=1
            if myPlayer.hat<0:
                myPlayer.hat = g.MAX_HAT-1
            if not checkClothingOk():
                hatLeft(None)
            self.changing=True
        def hatRight(event):
            myPlayer.hat+=1
            if myPlayer.hat>=g.MAX_HAT:
                myPlayer.hat = 0
            if not checkClothingOk():
                hatRight(None)
            self.changing=True
        def faceLeft(event):
            myPlayer.face-=1
            if myPlayer.face<0:
                myPlayer.face = g.MAX_FACE-1
            if not checkClothingOk():
                faceLeft(None)
            self.changing=True
        def faceRight(event):
            myPlayer.face+=1
            if myPlayer.face>=g.MAX_FACE:
                myPlayer.face = 0
            if not checkClothingOk():
                faceRight(None)
            self.changing=True
        def shirtLeft(event):
            myPlayer.shirt-=1
            if myPlayer.shirt<0:
                myPlayer.shirt = g.MAX_SHIRT-1
            if not checkClothingOk():
                shirtLeft(None)
            self.changing=True
        def shirtRight(event):
            myPlayer.shirt+=1
            if myPlayer.shirt>=g.MAX_SHIRT:
                myPlayer.shirt = 0
            if not checkClothingOk():
                shirtRight(None)
            self.changing=True
        def shoesLeft(event):
            myPlayer.shoes-=1
            if myPlayer.shoes<0:
                myPlayer.shoes = g.MAX_SHOES-1
            if not checkClothingOk():
                shoesLeft(None)
            self.changing=True
        def shoesRight(event):
            myPlayer.shoes+=1
            if myPlayer.shoes>=g.MAX_SHOES:
                myPlayer.shoes = 0
            if not checkClothingOk():
                shoesRight(None)
            self.changing=True
        def facingLeft(event):
            myPlayer.dir-=1
            if myPlayer.dir<DIR_DOWN:
                myPlayer.dir=DIR_RIGHT
                myPlayer.tmpPlayer.spriteFacing=8
            elif myPlayer.dir==DIR_UP:
                myPlayer.tmpPlayer.spriteFacing=5
            elif myPlayer.dir==DIR_LEFT:
                myPlayer.tmpPlayer.spriteFacing=3
            elif myPlayer.dir==DIR_DOWN:
                myPlayer.tmpPlayer.spriteFacing=0
            
            #myPlayer.tmpPlayer.spriteFacing-=1
            #if myPlayer.tmpPlayer.spriteFacing<0:
            #    myPlayer.tmpPlayer.spriteFacing=9
        def facingRight(event):
            myPlayer.dir+=1
            if myPlayer.dir>DIR_RIGHT:
                myPlayer.dir=DIR_DOWN
                myPlayer.tmpPlayer.spriteFacing=0
            elif myPlayer.dir==DIR_UP:
                myPlayer.tmpPlayer.spriteFacing=5
            elif myPlayer.dir==DIR_LEFT:
                myPlayer.tmpPlayer.spriteFacing=3
            elif myPlayer.dir==DIR_RIGHT:
                myPlayer.tmpPlayer.spriteFacing=8
        def saveClothes(event):
            self.ready=True
            saveBtn.disabled=True
        self.changing=True
        label = Label("Create Character",color=g.postColor,font_size=18)
        name = Label(myPlayer.name,bold=True,color=g.nameColor,font_size=18)
        hatBtnLeft = HighlightedButton(label="<-",on_release=hatLeft,width=25,height=25,font_size=13)
        hatBtnRight= HighlightedButton(label="->",on_release=hatRight,width=25,height=25,font_size=13)
        hatHorz = HorizontalContainer(content=[hatBtnLeft,Spacer(256-TILESIZE*2,0),hatBtnRight])
        
        faceBtnLeft = HighlightedButton(label="<-",on_release=faceLeft,width=25,height=25,font_size=13)
        faceBtnRight= HighlightedButton(label="->",on_release=faceRight,width=25,height=25,font_size=13)
        faceHorz = HorizontalContainer(content=[faceBtnLeft,Spacer(256-TILESIZE*2,0),faceBtnRight])
        
        shirtBtnLeft = HighlightedButton(label="<-",on_release=shirtLeft,width=25,height=25,font_size=13)
        shirtBtnRight= HighlightedButton(label="->",on_release=shirtRight,width=25,height=25,font_size=13)
        shirtHorz = HorizontalContainer(content=[shirtBtnLeft,Spacer(256-TILESIZE*2,0),shirtBtnRight])
        
        shoesBtnLeft = HighlightedButton(label="<-",on_release=shoesLeft,width=25,height=25,font_size=13)
        shoesBtnRight= HighlightedButton(label="->",on_release=shoesRight,width=25,height=25,font_size=13)
        shoesHorz = HorizontalContainer(content=[shoesBtnLeft,Spacer(256-TILESIZE*2,0),shoesBtnRight])

        facingBtnLeft = HighlightedButton(label="<---",on_release=facingLeft,width=30,height=30,font_size=13)
        facingBtnRight= HighlightedButton(label="--->",on_release=facingRight,width=30,height=30,font_size=13)
        facingHorz = HorizontalContainer(content=[facingBtnLeft,facingBtnRight])

        saveBtn = HighlightedButton(label="Save",on_release=saveClothes,width=100,height=40,font_size=16)
        
        
        frame = Frame(VerticalContainer(content=[label,Spacer(256-TILESIZE,TILESIZE/4),name,Spacer(0,8),hatHorz,faceHorz,shirtHorz,shoesHorz,facingHorz,Spacer(0,8),saveBtn]),path='frame_npc_talk')
        self.charMan = Manager(frame,
            window=self.screen,
            batch=g.guiBatch,
            theme=g.theme,
            offset=(0,0),
            is_movable=False)
    def removeManagers(self):
        self.man1.delete()
        self.man2.delete()
        del self.man1
        del self.man2
        
    def initManagers(self):
        g.gameEngine.changeMusicSong(LOGINMENUSONG)
        g.gameEngine.musicManager.volume=g.MUSICVOLUME
        self.skyHeight = int(0.4592592*g.SCREEN_HEIGHT)
        self.skyWidth = int(1.625*g.SCREEN_WIDTH)
        self.ukkeliSprite._set_scale(self.screen.width/1920.0)
        #self.ukkeliSprite.anchor_x=self.ukkeliSprite.width//2
        #self.ukkeliSprite.anchor_y=self.ukkeliSprite.height//2
        
        self.ukkeliSprite.x=0.5*self.screen.width
        self.ukkeliSprite2._set_scale(self.screen.width/1920.0)
        self.ukkeliSprite2.x=0.5*self.screen.width
        #self.ukkeliSprite2.anchor_x=self.ukkeliSprite2.width//2
        #self.ukkeliSprite2.anchor_y=self.ukkeliSprite2.height//2
        self.logo._set_scale(self.screen.width/1920.0)
        self.logo.x=(self.screen.width-self.l1.width*(self.screen.width/1920.0))/2
        self.logo.y=(self.screen.height-350)*(1080.0/self.screen.height)
        
        
        self.charTick = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
       
        
        label = Label("Username",color=g.loginFontColor,font_size=18)
        label1 = Label("Password",color=g.loginFontColor,font_size=18)
        self.logininput = TextInput(text="",padding=2,length=16,max_length=16,width=220,font_size=18)
        self.passwordinput = TextInput(text="",font=g.defaultPWFont.name,padding=0,length=21.5,width=220,font_size=18)
        
        self.button = HighlightedButton(label="Login",on_release=self.tryLogin,width=210,height=50,font_size=16)
        
        vertCont = VerticalContainer([label,self.logininput,Spacer(min_height=10),label1,self.passwordinput,Spacer(min_height=40),self.button])
        
        versionInfo = Label("Version: " + GAME_VERSION,color=(0,0,0,255),font_size=10)
        self.exitButton = HighlightedButton(label="Exit",on_release=self.exit,width=100,height=40,font_size=14)
        vertCont2 = VerticalContainer([versionInfo,self.exitButton])
        self.man1 = Manager(vertCont,
            window=self.screen,
            batch=g.guiBatch,
            theme=g.theme,
            offset=(0,-50),
            is_movable=False)
        self.man2 = Manager(vertCont2,
            window=self.screen,
            batch=g.guiBatch,
            theme=g.theme,
            anchor=ANCHOR_BOTTOM_RIGHT,
            offset=(-50,50),
            is_movable=False)
        self.man1.set_focus(self.logininput)
    def f(self):
        self.button.disabled = False
    def update(self):
        #print g.dx
        if g.currTick:
            g.dx = int((g.currTick-self.startTick)*0.025)
        if g.dx>=self.skyWidth:
            g.dx=0
            self.startTick = g.currTick
        self.bgImg.blit(0,0,width=self.screen.width,height=self.screen.height)
        self.skyImg.blit(g.dx,self.screen.height-self.skyHeight,width=self.skyWidth, height=self.skyHeight)
        self.skyImg.blit(g.dx-self.skyWidth,self.screen.height-self.skyHeight,width=self.skyWidth, height=self.skyHeight)
        #print self.ukkeliSprite._texture.__dict__
        if g.currTick - self.charTick > 500:
            self.ukkeliSprite.draw()
            if g.currTick - self.charTick > 1000:
                self.charTick = g.currTick
        else:
            self.ukkeliSprite2.draw()
        
        #self.loadedMap = True
        g.FPS=True
        #print g.alertGroup.__dict__
        self.logo.draw()
        g.guiBatch.draw()
        #
        if self.charSprite is not None:
            self.charSprite[myPlayer.tmpPlayer.spriteFacing].blit((g.screen.width-TILESIZE*4)/2,(g.screen.height-TILESIZE*4)/2)
