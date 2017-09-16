import global_vars as g
from constants import *
from pyglet_gui.gui import Graphic

class HpBar(Graphic):
    def __init__(self,maxhp=100,currenthp=100,height=25,width=256,type="hp"):
        self.maxhp=maxhp
        self.currenthp=currenthp
        bar = type+'bar'
        Graphic.__init__(self,path=bar,outline='baroutline',height=height,width=width,bgWidth=int(1.0*currenthp/maxhp*100))
       
    def get_progress(self):
        return self.currenthp/float(self.maxhp)
    def setHP(self,currenthp,maxhp=None):
        self.currenthp=currenthp
        if maxhp is not None:
            self.maxhp=maxhp
        self.bgWidth=int(currenthp/float(self.maxhp)*100)
        self.layout()