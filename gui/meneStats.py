import global_vars as g
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Spacer, Label
from pyglet_gui.containers import VerticalContainer, HorizontalContainer
from pyglet_gui.constants import ANCHOR_BOTTOM_LEFT,HALIGN_LEFT
from gui.hpbar import HpBar

class MeneStats(Manager):
    def __init__(self,name,level,hp,maxhp):
        self.nameLabel=Label(name,color=g.whiteColor,font_size=g.theme["font_size"]+2,bold=True)
        self.levelLabel=Label('Lvl: ' + str(level),color=g.whiteColor,font_size=g.theme["font_size"]+2,bold=True)
        self.hpBar= HpBar()
        Manager.__init__(self,
            VerticalContainer(content=[HorizontalContainer(content=[self.nameLabel,None,self.levelLabel]),self.hpBar],align=HALIGN_LEFT),
            window=g.screen,
            batch=g.guiBatch,
            is_movable=False,
            anchor=ANCHOR_BOTTOM_LEFT,
            offset=(0,0),
            theme=g.theme)
        self.hpBar.setHP(hp,maxhp)
    def updateLevel(self,level):
        self.levelLabel.set_text("Lvl: "+ str(level))
    def updateInfo(self,name,level,hp,maxhp):
        self.levelLabel.set_text("Lvl: "+ str(level))
        self.nameLabel.set_text(name)
        self.hpBar.setHP(hp,maxhp=maxhp)
        
    def setPos(self,x,y):
        self.set_position(x,y)
    def delete(self):
        super(Manager,self).delete()