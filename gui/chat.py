from pyglet_gui.text_input import TextInput
from pyglet_gui.manager import Manager
from pyglet_gui.containers import VerticalContainer,HorizontalContainer
from pyglet_gui.theme import Theme
from pyglet_gui.document import Document
from pyglet_gui.constants import ANCHOR_BOTTOM_LEFT, HALIGN_LEFT
from pyglet_gui.buttons import HighlightedButton
import pyglet.text
import global_vars as g
import time
from constants import *
from gamelogic import *

class Chat(Manager):
    def __init__(self):
        w1=int(350*(g.SCREEN_WIDTH/1920.))
        h1=int(300*(g.SCREEN_HEIGHT/1080.))
        if w1>300:
            g.chatTheme["font_size"]=11
            g.theme["font_size"]=11
            g.theme["button"]["font_size"]=11
        elif w1>250:
            g.chatTheme["font_size"]=12
            g.theme["font_size"]=12
            g.theme["button"]["font_size"]=12
            w1=int(w1*1.1)
        elif w1>200:
            g.chatTheme["font_size"]=11
            g.theme["font_size"]=11
            g.theme["button"]["font_size"]=11
            w1=int(w1*1.2)
        elif w1>175:
            g.chatTheme["font_size"]=10
            g.theme["font_size"]=10
            g.theme["button"]["font_size"]=10
            w1=int(w1*1.3)
        else:
            g.chatTheme["font_size"]=9
            g.theme["font_size"]=9
            g.theme["button"]["font_size"]=9
            w1=int(w1*1.3)
        self.chatInput = TextInput(text="",padding=0,length=16,max_length=MAX_CHAT_INPUT,width=w1-5-50)
        sendButton = HighlightedButton(label="Send",on_release=self.sendMessage,width=50,height=35)
        realtext = '{font_size '+str(g.chatTheme["font_size"])+'}{background_color '+str(g.postBgColor)+'}{font_name "'+g.chatTheme["font"]+'"}{wrap "char"} '
        document = pyglet.text.decode_attributed(realtext)
        self.textArea = Document(document,width=w1,height=h1,background=True,font_size=g.chatTheme["font_size"],font_name=g.chatTheme["font"],chat=True)

        vertCont = VerticalContainer(content=[self.textArea,HorizontalContainer(content=[self.chatInput,sendButton])],align=HALIGN_LEFT)
        Manager.__init__(self,
                        vertCont,
                        window=g.screen,
                        batch = g.guiBatch,
                        theme=g.chatTheme,
                        anchor=ANCHOR_BOTTOM_LEFT,
                        offset=(g.SCREEN_WIDTH*0.05,g.SCREEN_HEIGHT*0.1),
                        is_movable=False)
        #print self.__dict__
    def setPos(self,x,y):
        self.set_position(x,y)
    def sendMessage(self,event):
        g.chatReloaded=False
        text = self.chatInput.get_text()
        
        if text!="":
            sendChatMsg(text)
        else:
            g.chatting = None
        if not g.chatReloaded:
            self.chatInput.set_text("")
            if self._focus == self.chatInput:
                self._focus=None
                self.chatInput.on_lose_focus()
        self.chatInput.focused=False
    def delete(self):
        super(Manager,self).delete()
    def addText(self,constructedText):
        len1=len(self.textArea._document.text)
        attributes={}
        for c in constructedText._style_runs:
            for d in constructedText._style_runs[c]:
                if d[2] is not None:
                    attributes.update({str(c):d[2]})
        self.textArea._document.insert_text(len1,constructedText._text,attributes)
        
        