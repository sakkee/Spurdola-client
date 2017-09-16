import global_vars as g
from gamelogic import *
from objects import *
from constants import *
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Frame, Label
from pyglet_gui.theme import Theme
from pyglet_gui.containers import VerticalContainer, HorizontalContainer
from pyglet_gui.buttons import HighlightedButton
from pyglet_gui.constants import HALIGN_LEFT
class SelectedWindow(Manager):
    def __init__(self,title,content=None,x=0,y=0,type=0):
        g.selectedWindowOpened=True
        cont = []
        self.type=type
        cont.append(Label(title,color=g.loginFontColor))
        for c in content:
            cont.append(HighlightedButton(c["text"],on_release=c["function"],width=120,height=24,path='empty',argument=c["argument"],align=HALIGN_LEFT))
        frame = Frame(VerticalContainer(content=cont,padding=0,align=HALIGN_LEFT),path='frame_alternative')
        Manager.__init__(self,
            frame,
            window=g.screen,
            batch=g.selectWindowBatch,
            is_movable=False,
            offset=(0,0),
            theme=g.theme)
        self.set_position(x,y-self.height)
    def delete(self,event):
        super(Manager,self).delete()
        g.selectedWindowOpened=False
        g.cursorTarget=None
    def setPos(self,x,y):
        self.set_position(x,y)