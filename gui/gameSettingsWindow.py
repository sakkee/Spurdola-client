import global_vars as g
from gamelogic import *
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Frame, Label, Spacer
from pyglet_gui.theme import Theme
from pyglet_gui.constants import ANCHOR_BOTTOM_LEFT,HALIGN_LEFT
from pyglet_gui.containers import VerticalContainer, HorizontalContainer
from pyglet_gui.buttons import HighlightedButton, Checkbox
from pyglet_gui.sliders import HorizontalSlider
from pyglet_gui.option_selectors import Dropdown
import cfg_parser
class GameSettingsWindow(Manager):
    def __init__(self):
        g.gameSettingsWindowOpened=True
        self.mouseoverPaint = g.selectPaint
        self.hoverPaint = g.hoverPaint
        self.musicEnabled=g.MUSIC
        self.musicVolume=g.MUSICVOLUME
        self.soundEnabled=g.SOUND
        self.soundVolume=g.SOUNDVOLUME
        titleText = Label("Game Settings",color=g.loginFontColor,font_size=g.theme["font_size"]+2)
        mouseoverBtn = Checkbox("Paint tile select",on_press=self.mouseoverSelect,is_pressed=self.mouseoverPaint,align=HALIGN_LEFT,width=24,height=24)
        hoverBtn = Checkbox("Paint hover players",on_press=self.hoverSelect,is_pressed=self.hoverPaint,align=HALIGN_LEFT)
        audioEnabled=Checkbox("Enable music",on_press=self.musicSelect,is_pressed=self.musicEnabled,align=HALIGN_LEFT)
        musicVolume = Label("Music volume")
        musicSlider = HorizontalSlider(on_set=self.musicVolumeChange,value=self.musicVolume)
        self.musicVolumeNumber = Label('%.2f' % self.musicVolume)
        soundEnabled=Checkbox("Enable sounds",on_press=self.soundSelect,is_pressed=self.soundEnabled,align=HALIGN_LEFT)
        soundVolume = Label("Sound volume")
        soundSlider = HorizontalSlider(on_set=self.soundVolumeChange,value=self.soundVolume)
        self.soundVolumeNumber = Label('%.2f' % self.soundVolume)
        horz2 = HorizontalContainer([musicVolume,musicSlider,self.musicVolumeNumber],padding=0)
        horz3 = HorizontalContainer([soundVolume,soundSlider,self.soundVolumeNumber],padding=0)
        discardBtn = HighlightedButton(label="Discard",on_release=self.delete,width=120,height=30)
        saveBtn = HighlightedButton(label="Save",on_release=self.onSave,width=120,height=30)
        horzBtn = HorizontalContainer([discardBtn,saveBtn])
        Manager.__init__(self,
            Frame(VerticalContainer([titleText,mouseoverBtn,hoverBtn,audioEnabled,horz2,soundEnabled,horz3,horzBtn])),
            window=g.screen,
            batch=g.guiBatch,
            theme=g.theme,
            is_movable=False)
    def soundSelect(self,event):
        self.soundEnabled=event
    
    def soundVolumeChange(self,volume):
        g.SOUNDVOLUME=volume
        #self.musicVolume=volume
        self.soundVolumeNumber.set_text('%.2f' %volume)
    def musicVolumeChange(self,volume):
        g.gameEngine.musicManager.volume=volume
        self.musicVolume=volume
        self.musicVolumeNumber.set_text('%.2f' %volume)
    def musicSelect(self,event):
        self.musicEnabled=event
        if not event and g.gameEngine.musicManager.playing:
            g.gameEngine.musicManager.pause()
        elif event and not g.gameEngine.musicManager.playing:
            g.gameEngine.musicManager.play()
    def hoverSelect(self,event):
        self.hoverPaint=event
    def mouseoverSelect(self,event):
        self.mouseoverPaint=event
    def delete(self,event):
        if g.gameEngine.musicManager.playing and not g.MUSIC:
            g.gameEngine.musicManager.pause()
        elif not g.gameEngine.musicManager.playing and g.MUSIC:
            g.gameEngine.musicManager.play()
        g.gameEngine.musicManager.volume=g.MUSICVOLUME
        g.SOUNDVOLUME=self.soundVolume
        g.settingsWindowOpened=False
        super(Manager,self).delete()
    def onSave(self,event):
        if self.mouseoverPaint!=g.selectPaint:
            g.selectPaint = self.mouseoverPaint
            cfg_parser.saveCfg("selectpaint",g.selectPaint)
        if self.hoverPaint!=g.hoverPaint:
            g.hoverPaint = self.hoverPaint
            cfg_parser.saveCfg("hoverpaint",g.hoverPaint)
        if self.musicEnabled != g.MUSIC:
            g.MUSIC = self.musicEnabled
            cfg_parser.saveCfg("MUSIC",g.MUSIC)
        if self.musicVolume != g.MUSICVOLUME:
            g.MUSICVOLUME = self.musicVolume
            cfg_parser.saveCfg("MUSICVOLUME",g.MUSICVOLUME)
        if self.soundVolume != g.SOUNDVOLUME:
            self.soundVolume=g.SOUNDVOLUME
            cfg_parser.saveCfg("SOUNDVOLUME",g.SOUNDVOLUME)
        if self.soundEnabled != g.SOUND:
            g.SOUND=self.soundEnabled
            cfg_parser.saveCfg("SOUND",g.SOUND)
        self.delete(None)
        g.gameSettingsWindowOpened=False