import global_vars as g
from gamelogic import *
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Frame, Label, Spacer
from pyglet_gui.theme import Theme
from pyglet_gui.constants import ANCHOR_BOTTOM_LEFT, HALIGN_LEFT
from pyglet_gui.containers import VerticalContainer, HorizontalContainer
from pyglet_gui.buttons import HighlightedButton, Checkbox
from pyglet_gui.option_selectors import Dropdown
import cfg_parser
class KeybindingsWindow(Manager):
    def __init__(self):
        g.keybindingsWindowOpened=True
        self.resW=g.SCREEN_WIDTH
        self.resH=g.SCREEN_HEIGHT
        self.fullscreen = g.FULLSCREEN
        self.vsync = g.VSYNC
        self.screenSelected=g.SCREENSELECTED
        screens = pyglet.window.get_platform().get_default_display().get_screens()
        screenopts=[]
        for i in range(len(screens)):
            screenopts.append(str(i))
        if int(self.screenSelected) >=0 and int(self.screenSelected) < len(screens):
            screenopts.insert(0,str(self.screenSelected))
        options=[]
        modes = pyglet.window.get_platform().get_default_display().get_default_screen().get_modes()
        for i in modes:
            if i.width>=1024 and i.height>=720:
                opt = str(int(i.width))+':'+str(int(i.height))
                if opt not in options:
                    options.append(opt)
        options.insert(0,str(g.SCREEN_WIDTH)+':'+str(g.SCREEN_HEIGHT))
        titleText = Label("Video Settings",color=g.loginFontColor,font_size=g.theme["font_size"]+2)
        windowTypeInfo = Label("Window mode")
        if g.FULLSCREEN:
            windowType = Dropdown(['Fullscreen', 'Windowed'],on_select=self.selection)
        else:
            windowType = Dropdown(['Windowed','Fullscreen'],on_select=self.selection)
        horz = HorizontalContainer([windowTypeInfo,windowType])
        resolutionInfo = Label("Resolution")
        resolutionType = Dropdown(options,on_select=self.resSelect)
        horz1 = HorizontalContainer([resolutionInfo,resolutionType])
        vsyncBtn = Checkbox("VSync",on_press=self.vsyncSelect,is_pressed=self.vsync,align=HALIGN_LEFT)
        resolutionInfo = Label("Monitor")
        resolutionType = Dropdown(screenopts,on_select=self.screenSelect)
        horz3 = HorizontalContainer([resolutionInfo,resolutionType])
        discardBtn = HighlightedButton(label="Discard",on_release=self.delete,width=120,height=30)
        saveBtn = HighlightedButton(label="Save",on_release=self.onSave,width=120,height=30)
        horzBtn = HorizontalContainer([discardBtn,saveBtn])
        Manager.__init__(self,
            Frame(VerticalContainer([titleText,horz,horz1,vsyncBtn,horz3,horzBtn])),
            window=g.screen,
            batch=g.guiBatch,
            theme=g.theme,
            is_movable=False)
    def screenSelect(self,event):   
        self.screenSelected=event
    def vsyncSelect(self,event):
        self.vsync=event
    def delete(self,event):
        g.keybindingsWindowOpened=False
        super(Manager,self).delete()
    def resSelect(self,text):
        self.resW=int(text.split(":")[0])
        self.resH=int(text.split(":")[1])
    def selection(self,text):
        if text == 'Fullscreen':
            self.fullscreen = True
        else:
            self.fullscreen = False
    def onSave(self,event):
        if self.fullscreen!=g.FULLSCREEN:
            g.FULLSCREEN = self.fullscreen
            cfg_parser.saveCfg("Fullscreen",g.FULLSCREEN)
        if g.SCREEN_WIDTH != self.resW or g.SCREEN_HEIGHT != self.resH:
            g.SCREEN_WIDTH = self.resW
            g.SCREEN_HEIGHT = self.resH
            cfg_parser.saveCfg("Resolution",str(g.SCREEN_WIDTH)+':'+str(g.SCREEN_HEIGHT))
            g.gameEngine.fightScreen.scaleBackground()
        if self.vsync != g.VSYNC:
            g.VSYNC = self.vsync
            cfg_parser.saveCfg("Vsync",g.VSYNC)
        if self.screenSelected != g.SCREENSELECTED and g.SCREENSELECTED != -1:
            g.SCREENSELECTED = self.screenSelected
            cfg_parser.saveCfg("Screenselected",g.SCREENSELECTED)
        updateUi()
        self.delete(None)