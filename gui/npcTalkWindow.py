import global_vars as g
from gamelogic import *
from objects import *
from constants import *
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Frame, Label, Graphic, Spacer
from pyglet_gui.theme import Theme
from pyglet_gui.document import Document
from pyglet_gui.containers import VerticalContainer, HorizontalContainer
from pyglet_gui.buttons import HighlightedButton, Button
from pyglet_gui.hoverbutton import AbilityButton
from pyglet_gui.constants import HALIGN_LEFT, ANCHOR_LEFT, ANCHOR_BOTTOM_LEFT, ANCHOR_CENTER, HALIGN_RIGHT, VALIGN_CENTER
import pyglet.text
class NpcTalkWindow(Manager):
    def __init__(self,name,text,actionType=0):
        g.npcTalkWindowOpened=True
        g.cursorRound=-1
        self.name=name
        sendTalkToNpc(name)
        if actionType == NPC_ACTIONTYPE_SHOP:
            namecolor = g.npcColor
            postcolor = g.whiteColor
            path = 'frame_npc_talk_shop'
        else:
            namecolor = g.npcColorLighter
            postcolor = g.postColor
            path = 'frame_npc_talk'
        label1=Label(name,color=namecolor,bold=True)
        closeBtn =HighlightedButton("",on_release=self.delete,width=19,height=19,path='delete')
        horzCont=HorizontalContainer(content=[label1,None,closeBtn])
        self.yourmoney=None
        w1=int(300*(g.SCREEN_WIDTH/1920.))+50
        h1=int(500*(g.SCREEN_HEIGHT/1080.))
        textArr = text.split('\n\n')
        realText=""

        for c in textArr:
            if c[0]=='>':
                realText+='{color '+str(g.greentextColor)+'}' + c + '\n\n'
            else:
                realText+='{color '+str(postcolor)+'}' + c + '\n\n'
        realText = realText[:-2]
        document = pyglet.text.decode_attributed(realText)
        self.textArea = Document(document,width=w1,height=h1,background=False,font_size=g.chatTheme["font_size"],font_name=g.chatTheme["font"])
        if actionType == NPC_ACTIONTYPE_HEAL:
            healButton = HighlightedButton("Heal my menes",on_release=self.healButton)
            okButton=HighlightedButton("Goodbye",on_release=self.delete)
            cont = VerticalContainer(content=[horzCont,self.textArea,HorizontalContainer([healButton,okButton])])
        elif actionType == NPC_ACTIONTYPE_SHOP:
            #TODO: When more items, do a loop that adds then dynamically instead of statically like this
            disabled=False
            if Items["es"]["cost"]>g.moneyAmount:
            #    print "TAPAHTU"
                disabled=True
            self.esButton = AbilityButton(width=50,height=50,argument=Items["es"]["id"],disabled=disabled,on_press=buyItem,texture=g.gameEngine.resManager.items[Items["es"]["sprite"]],outline='abilityoutline',hover=onHover,hoveringType=HOVERING_ITEM,arguments={'name':Items["es"]["name"],'info':Items["es"]["info"],"args":()})
            nameLabel = Label(Items["es"]["name"],color=g.npcColor)
            esCost = Items["es"]["cost"]/100.0
            costLabel = Label("%.2f" % esCost)
            euroPicture = Graphic("euro")
            costCont = HorizontalContainer(content=[costLabel,euroPicture])
            infoCont = VerticalContainer(content=[Spacer(),nameLabel,costCont],align=HALIGN_LEFT)
            itemCont = HorizontalContainer(content=[self.esButton,infoCont])
            moneyTmp = g.moneyAmount/100.0
            self.yourmoney = Label('%.2f' % moneyTmp)
            yourmoneyCont = HorizontalContainer(content=[self.yourmoney,Graphic("euro")])
            self.yourES = Label('%s' % g.esAmount)
            yourESCont = HorizontalContainer(content=[self.yourES,Graphic("es_icon")])
            okButton=HighlightedButton("Goodbye",on_release=self.delete)
            cont = VerticalContainer(content=[horzCont,self.textArea,itemCont,Spacer(0,20),HorizontalContainer(content=[Spacer(),VerticalContainer(content=[yourmoneyCont,yourESCont],align=HALIGN_RIGHT)]),okButton])
        else:
            okButton=HighlightedButton("Goodbye",on_release=self.delete)
            cont = VerticalContainer(content=[horzCont,self.textArea,okButton])
        frame = Frame(cont,path=path)
        Manager.__init__(self,
            frame,
            window=g.screen,
            batch=g.guiBatch,
            is_movable=False,
            anchor=ANCHOR_LEFT,
            offset=(40,int(g.SCREEN_HEIGHT*g.WINDOW_POSY_RELATIVE)),
            theme=g.theme)
            
    def updateMoney(self,money, es):
        if self.yourmoney is None or self.yourES is None:
            return
        moneyTmp = g.moneyAmount/100.0
        self.yourmoney.set_text("%.2f" % moneyTmp)
        self.yourES.set_text("%s" % es)
        if Items["es"]["cost"] > money and not self.esButton.disabled:
            self.esButton.disabled=True
            self.esButton.reload()
            self.esButton.layout()
        elif Items["es"]["cost"] <= money and self.esButton.disabled:
            self.esButton.disabled=False
            self.esButton.reload()
            self.esButton.layout()
        
    def healButton(self,event):
        sendHealMenes()
        self.delete(None)
    def delete(self,event):
        super(Manager,self).delete()
        g.npcTalkWindowOpened=False
        if g.talkingToNpc is not None:
            if npcList[g.talkingToNpc].name==self.name:
                sendStopTalkToNpc(self.name)
    def setPos(self,x,y):
        self.set_position(x,y)
    