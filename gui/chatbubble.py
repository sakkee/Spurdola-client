import global_vars as g
from constants import *
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Frame, Label
from pyglet_gui.theme import Theme
from pyglet_gui.constants import ANCHOR_BOTTOM_LEFT
from pyglet_gui.containers import HorizontalContainer

class ChatBubble(Manager):
    def __init__(self,name,text,a=0):
        if text[0]=='>':
            color=g.greentextColor
        else:
            color=g.postColor
        if a>0:
            if a==ADMIN_MODERATOR:
                nameColor=g.modColor
                appendix='#Mod#'
            elif a==ADMIN_ADMIN:
                nameColor=g.adminColor
                appendix='#Admin#'
            else:
                nameColor=g.adminColor
                appendix='#Owner#'
        else:
            nameColor=g.nameColor
            appendix=''
        if appendix:
            horz=HorizontalContainer(content=[Label(name,bold=True,color=nameColor),Label(appendix+':',color=nameColor),Label(text,color=color)])
        else:
            horz=HorizontalContainer(content=[Label(name+':',bold=True,color=nameColor),Label(text,color=color)])
        Manager.__init__(self,
            Frame(horz),
            window=g.screen,
            batch=g.chatBubbleBatch,
            anchor=ANCHOR_BOTTOM_LEFT,
            is_movable=False,
            offset=(0,0),
            theme=g.chatTheme)
            
    def setPos(self,x,y):
        self.set_position(x,y)
    
    def delete(self):
        super(Manager,self).delete()