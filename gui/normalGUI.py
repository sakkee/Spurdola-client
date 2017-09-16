import global_vars as g
from gamelogic import *
from constants import *
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Frame, Label
from pyglet_gui.theme import Theme
from pyglet_gui.containers import VerticalContainer, HorizontalContainer
from pyglet_gui.buttons import HighlightedButton, Button
from pyglet_gui.hoverbutton import HoverButton, HoverGraphic
from pyglet_gui.constants import HALIGN_LEFT, ANCHOR_BOTTOM, VALIGN_BOTTOM


class NormalGUI(Manager):
    def __init__(self):
        friendBtn = HighlightedButton("",on_release=self.openFriends,width=32,height=32,path='btn_friendwindow')
        ignoreBtn = HighlightedButton("",on_release=self.openIgnores,width=32,height=32,path='btn_ignorewindow')
        #meneBtn = HighlightedButton("",on_release=self.openMenes,width=50,height=50,path='es')
        meneBtn = HighlightedButton("",on_release=self.openMenes,width=50,height=50,path='menes')
        fightBtn = HighlightedButton("",on_release=self.openMenes,width=50,height=50,path='es')
        if g.latencyType == PING_TYPE_GREEN:
            path='ping_green'
        elif g.latencyType == PING_TYPE_YELLOW:
            path='ping_yellow'
        else:
            path='ping_red'
        self.latencyBtn = HoverGraphic(width=15,height=32,path=path,hover=onHover,hoveringType=HOVERING_PING)
        guildBtn = HighlightedButton("",on_release=self.openGuild,width=32,height=32,path='guild')
        settingsBtn = HighlightedButton("",on_release=self.openSettings,width=32,height=32,path='settings')
        
        self.mailBtn = HighlightedButton("",on_release=self.openMail,width=32,height=32,path='mail')
        bagBtn = HoverGraphic(width=32,height=32,path='bag',hover=onHover,hoveringType=HOVERING_BAG,showHighlight=True)
        self.horzCont = HorizontalContainer(content=[friendBtn,ignoreBtn,meneBtn,fightBtn,guildBtn,self.latencyBtn,settingsBtn,bagBtn],align=VALIGN_BOTTOM)
        Manager.__init__(self,
            self.horzCont,
            window=g.screen,
            batch=g.guiBatch,
            is_movable=False,
            anchor=ANCHOR_BOTTOM,
            offset=(0,20),
            theme=g.theme)
        if len(g.mails)>0:
            self.addMail()
            
    def setPos(self,x,y):
        self.set_position(x,y)
    def openGuild(self,event):
        if g.guildWindowOpened:
            g.gameEngine.graphics.guildWindow.delete(None)
        else:
            g.gameEngine.graphics.initGuildWindow()
    def openMail(self,event):
        if g.postWindowOpened:
            g.gameEngine.graphics.postWindow.delete(None)
        else:
            g.gameEngine.graphics.initPostWindow()
    def addMail(self):
        found=False
        for c in self.horzCont._content:
            if c._path[0]=='mail':
                found=True
        if not found:
            self.horzCont.add(self.mailBtn)
    def removeMail(self):
        found=False
        for c in self.horzCont._content:
            if c._path[0]=='mail':
                found=True
        if found:
            self.horzCont.remove(self.mailBtn)
    def refreshLatencybar(self):
        if g.latencyType == PING_TYPE_GREEN:
            self.latencyBtn._path='ping_green'
        elif g.latencyType == PING_TYPE_YELLOW:
            self.latencyBtn._path='ping_yellow'
        else:
            self.latencyBtn._path='ping_red'
        self.latencyBtn.reload()
        self.latencyBtn.reset_size()
    def delete(self):
        super(Manager,self).delete()
    def openMenes(self,event):
        if g.meneWindowOpened:
             g.gameEngine.graphics.meneWindow.delete(None)
        else:
             g.gameEngine.graphics.initMeneWindow()
    def openSettings(self,event):
        g.gameEngine.graphics.closeAllWindows()
        if g.escWindowOpened:
            g.gameEngine.graphics.escWindow.delete(None)
            g.escWindowOpened=False
        else:
            if g.settingsWindowOpened:
                g.settingsWindowOpened=False
                g.gameEngine.graphics.settingsWindow.delete(None)
            g.escWindowOpened=True
            g.gameEngine.graphics.initEscWindow()
    def printLatency(self,event):
        pass
        #constructText("Ping is "+str(int(g.latency))+' ms.',g.helpColor)
        #g.chatLog+='\n{background_color '+str(g.postBgColor)+'}{color '+str(g.helpColor)+'}'
        #g.chatLog+="Ping is "+str(int(g.latency))+' ms.'
        #g.chatLog+='\n'
        #checkChatLogLength()
        #g.gameEngine.graphics.chat.textArea.update_text(g.chatLog)
    def openFriends(self,event):
        if g.friendWindowOpened:
            g.gameEngine.graphics.friendWindow.delete(None)
        else:
            g.gameEngine.graphics.initFriendWindow()
    def openIgnores(self,event):
        if g.ignoreWindowOpened:
            g.gameEngine.graphics.ignoreWindow.delete(None)
        else:
            g.gameEngine.graphics.initIgnoreWindow()