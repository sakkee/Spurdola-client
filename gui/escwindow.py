import global_vars as g
from gamelogic import *
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Frame, Spacer
from pyglet_gui.theme import Theme

from pyglet_gui.containers import VerticalContainer
from pyglet_gui.buttons import HighlightedButton
class EscWindow(Manager):
    def __init__(self):
        gameSettingsButton = HighlightedButton(label="Game Settings",on_release=self.gameSettings,width=120,height=30)
        settingsButton = HighlightedButton(label="Video Settings",on_release=self.settings,width=120,height=30)
        keybindingsButton = HighlightedButton(label="Keybindings",on_release=self.keybindings,width=120,height=30)
        helpButton = HighlightedButton(label="Help",on_release=self.help,width=120,height=30)
        disconnectButton = HighlightedButton(label="Disconnect",on_release=self.disconnect,width=120,height=30)
        closeButton = HighlightedButton(label="Close",on_release=self.delete,width=120,height=30)
        quitButton = HighlightedButton(label="Quit",on_release=self.onQuit,width=120,height=30)
        Manager.__init__(self,
            Frame(VerticalContainer(content=[gameSettingsButton,settingsButton,keybindingsButton,helpButton,disconnectButton,quitButton,Spacer(0,20),closeButton])),
            window=g.screen,
            batch=g.guiBatch,
            is_movable=False,
            theme=g.theme)
            
    def keybindings(self,event):
        g.gameEngine.graphics.initKeybindingsWindow()
        self.delete(None)
    def onQuit(self,event):
        changeGameState(GAMESTATE_EXIT)
    def delete(self,event):
        g.escWindowOpened=False
        super(Manager,self).delete()
    def disconnect(self,event):
        g.gameEngine.disconnect()
        
    def help(self,event):
        g.gameEngine.graphics.initReportWindow()
        self.delete(None)
    def settings(self,event):
        g.gameEngine.graphics.initSettingsWindow()
        self.delete(None)
        g.settingsWindowOpened=True
        
    def gameSettings(self,event):
        g.gameEngine.graphics.initGameSettingsWindow()
        self.delete(None)