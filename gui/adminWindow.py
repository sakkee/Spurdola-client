import global_vars as g
from gamelogic import *
from objects import *
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Frame, Spacer, Label
from pyglet_gui.theme import Theme
from pyglet_gui.scrollable import Scrollable
from pyglet_gui.containers import VerticalContainer, HorizontalContainer
from pyglet_gui.buttons import HighlightedButton, Button
from pyglet_gui.constants import HALIGN_LEFT, ANCHOR_LEFT
class AdminWindow(Manager):
    def __init__(self):
        g.adminWindowOpened = True
        label1=Label("Admin Menu",bold=True,color=g.loginFontColor)
        closeBtn = closeBtn =HighlightedButton("",on_release=self.delete,width=19,height=19,path='delete')
        
        adminSayBtn=HighlightedButton("Admin say",on_release=self.adminSay,width=120,height=25)
        muteBtn=HighlightedButton("Mute player",on_release=self.mutePlayer,width=120,height=25)
        unmuteBtn=HighlightedButton("Unmute player",on_release=self.unmutePlayer,width=120,height=25)
        teleportBtn=HighlightedButton("Teleport player",on_release=self.teleportPlayer,width=120,height=25)
        banBtn=HighlightedButton("Ban player",on_release=self.banPlayer,width=120,height=25)
        unbanBtn=HighlightedButton("Unban player",on_release=self.unbanPlayer,width=120,height=25)
        reportBtn=HighlightedButton("Reports",on_release=self.reports,width=120,height=25)
        #addBtn = HighlightedButton("",on_release=self.addFriend,width=24,height=24,path='friendadd')
        
        horzCont = HorizontalContainer(content=[label1,closeBtn])
        frame = Frame(VerticalContainer(content=[horzCont,adminSayBtn,muteBtn,unmuteBtn,teleportBtn,banBtn,unbanBtn,reportBtn]))
        Manager.__init__(self,
            frame,
            window=g.screen,
            batch=g.guiBatch,
            is_movable=False,
            anchor=ANCHOR_LEFT,
            offset=(40,int(g.SCREEN_HEIGHT*g.WINDOW_POSY_RELATIVE)),
            theme=g.theme)
            
    def reports(self,event):
        g.gameEngine.graphics.initReportAnswerWindow()
    def mutePlayer(self,event):
        infoText('/mute <PLAYERNAME> <MINUTES> <REASON>')
        g.gameEngine.graphics.chat.set_focus(g.gameEngine.graphics.chat.chatInput)
        g.gameEngine.graphics.chat.chatInput.set_text("/mute ")
    def unmutePlayer(self,event):
        infoText('/unmute <PLAYERNAME>')
        g.gameEngine.graphics.chat.set_focus(g.gameEngine.graphics.chat.chatInput)
        g.gameEngine.graphics.chat.chatInput.set_text("/unmute ")
    def teleportPlayer(self,event):
        infoText('/teleport <PLAYERNAME> <TARGETPLAYER>|<MAPNAME>,<X>,<Y>')
        g.gameEngine.graphics.chat.set_focus(g.gameEngine.graphics.chat.chatInput)
        g.gameEngine.graphics.chat.chatInput.set_text("/teleport ")
    def banPlayer(self,event):
        infoText('/ban <PLAYERNAME> <MINUTES> <REASON>')
        g.gameEngine.graphics.chat.set_focus(g.gameEngine.graphics.chat.chatInput)
        g.gameEngine.graphics.chat.chatInput.set_text("/ban ")
    def unbanPlayer(self,event):
        infoText('/unban <PLAYERNAME>')
        g.gameEngine.graphics.chat.set_focus(g.gameEngine.graphics.chat.chatInput)
        g.gameEngine.graphics.chat.chatInput.set_text("/unban ")
    def adminSay(self,event):
        g.gameEngine.graphics.chat.set_focus(g.gameEngine.graphics.chat.chatInput)
        g.gameEngine.graphics.chat.chatInput.set_text("/adminsay ")
    def delete(self,event):
        super(Manager,self).delete()
        g.adminWindowOpened = False