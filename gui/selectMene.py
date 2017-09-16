import global_vars as g
from gamelogic import *
import json
from network.packettypes import *
from gui.hpbar import HpBar
from pyglet_gui.buttons import Button, HighlightedButton
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Spacer, Graphic, Frame, Label
from pyglet_gui.containers import HorizontalContainer, VerticalContainer
from pyglet_gui.theme import Theme
from pyglet_gui.hoverbutton import HoverGraphic, HoverButton, AbilityButton
from pyglet_gui.constants import ANCHOR_BOTTOM, VALIGN_BOTTOM

class MeneSelector(Manager):
    def __init__(self, closeButton=True):
        g.selectMeneWindowOpened = True
        self.currentMeneID=g.currMeneID
        self.selectMeneID=None
        self.meneCont=[]
        self.meneButtons = []
        self.closeButton=closeButton
        self.constructMeneButtons()
        selectButton = HighlightedButton("Select Mene",on_release=self.selectMene,width=150,height=30)
        if closeButton:
            closeBtn = HighlightedButton("",on_release=self.delete,width=19,height=19,path='delete')
            cont = VerticalContainer(content=[HorizontalContainer(content=[Spacer(0,0),closeBtn]), HorizontalContainer(content=self.meneCont),Spacer(0,10),selectButton])
        else:
            cont = VerticalContainer(content=[HorizontalContainer(content=self.meneCont),Spacer(0,10),selectButton])
        Manager.__init__(self,
            Frame(cont),
            window=g.screen,
            batch=g.guiBatch,
            is_movable=False,
            offset=(0,0),
            theme=g.theme)
    def setPos(self,x,y):
        self.set_position(x,y)
    def delete(self, arg=None):
        g.selectMeneWindowOpened = False
        super(Manager,self).delete()
    def selectMene(self,argument):
        #sendSelectMene(self.selectMeneID)
        
        if g.gameEngine.fightScreen.myMene.ID==self.selectMeneID:
            if g.gameEngine.fightScreen.myMene.hp==0:
                pass
            else:
                self.delete()
        else:
            packet = json.dumps({"p": ClientPackets.ChangeDefaultMene,'id':self.selectMeneID})
            g.tcpConn.sendData(packet)
        #makeDefaultMene(self.selectMeneID,openMeneWindow=False)
        
    def constructMeneButtons(self):
        for mene in meneList:
            if mene.hp<=0:
                disabled=True
            else:
                disabled=False
            if g.gameEngine.fightScreen.myMene.ID==mene.ID:
                ispressed=True
                self.selectMeneID=mene.ID
            else:
                ispressed=False
            button = Button("",on_press=self.updateWindow,disabled=disabled,width=TILESIZE*2,height=TILESIZE*2, argument=mene.ID,texture=g.gameEngine.resManager.meneSprites[mene.spriteName]["portraitlarge"],is_pressed=ispressed,outline='menewindowbutton')
            nameLabel = Label(mene.name,bold=True,color=g.npcColor)
            lvlLabel = Label("Lvl: %s" % mene.level)
            hpBar = HpBar(height=20,width=64*2,maxhp=mene.maxhp,currenthp=mene.hp)
            self.meneCont.append(VerticalContainer(content=[button,nameLabel,lvlLabel,hpBar],padding=0))
            self.meneButtons.append(button)
    def updateWindow(self, ID):
        self.selectMeneID=ID
        for c in self.meneButtons:
            if c.arg!=ID and c._is_pressed:
                c.changeStateWithoutFnc()
        for c in self.meneButtons:
            if c.arg==ID and not c._is_pressed:
                c.changeStateWithoutFnc()