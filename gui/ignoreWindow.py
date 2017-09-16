import global_vars as g
from gamelogic import *
from objects import *
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Frame, Label
from pyglet_gui.theme import Theme
from pyglet_gui.scrollable import Scrollable
from pyglet_gui.containers import VerticalContainer, HorizontalContainer
from pyglet_gui.buttons import HighlightedButton, Button
from pyglet_gui.constants import HALIGN_LEFT, ANCHOR_LEFT
class IgnoreWindow(Manager):
    def __init__(self):
        g.ignoreWindowOpened = True
        
        label1=Label("Ignore List",bold=True,color=g.loginFontColor)
        closeBtn =HighlightedButton("",on_release=self.delete,width=19,height=19,path='delete')
        title=[label1,None,closeBtn]
        ignores = []
        for c in ignoreList:
            ignores.append(c)
        ignores.sort()
        ignoreCont = []
        for c in ignores:
            label=HighlightedButton(c,width=150,height=24,path='baroutline_btn', on_release=self.constructSelect,argument=c,align=HALIGN_LEFT,font_color=g.guiNameColor)
            ignoreCont.append(label)
            #label=Label(c,bold=True,color=g.nameColorLighter)
            #removeBtn = HighlightedButton("",on_release=self.removeIgnore,width=24,height=24,path='ignoreremove',argument=c)
            #ignoreCont.append(HorizontalContainer(content=[label,removeBtn]))
        addBtn = HighlightedButton("Ignore Player",on_release=addIgnorePopup,width=100,height=24)
        horzCont = HorizontalContainer(content=title)
        frame = Frame(VerticalContainer(content=[horzCont,Scrollable(height=400,width=400,content=VerticalContainer(content=ignoreCont,align=HALIGN_LEFT,padding=0)),addBtn]))
        Manager.__init__(self,
            frame,
            window=g.screen,
            batch=g.guiBatch,
            is_movable=False,
            anchor=ANCHOR_LEFT,
            offset=(40,int(g.SCREEN_HEIGHT*g.WINDOW_POSY_RELATIVE)),
            theme=g.theme)
    def delete(self,event):
        super(Manager,self).delete()
        g.ignoreWindowOpened = False
    def on_mouse_motion(self, x, y, dx, dy):
        Manager.on_mouse_motion(self, x, y, dx, dy)
        g.cursorX=x
        g.cursorY=y
    def constructSelect(self,text):
        content=[]
        content.append({"text":'Unignore','argument':text,'function':removeIgnore})
        content.append({"text":'Close','argument':text,'function':closeSelectWindow})
        g.gameEngine.graphics.initSelectedWindow(text,content,g.cursorX,g.cursorY)