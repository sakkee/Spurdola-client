import global_vars as g
from constants import *
import pyglet.graphics
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Frame
from pyglet_gui.theme import Theme
from pyglet_gui.constants import ANCHOR_BOTTOM_LEFT
class HoverWindow(Manager):
    def __init__(self,content,x,y):
        self.frame = Frame(content,path='frame_alternative')
        #print content.__dict__
        #print "CONTENTHEIGHT",content.height
        #print content.__dict__
        #frame.expand(content.width,content.label.content_height)
        #print content.__dict__
        Manager.__init__(self,
            self.frame,
            window=g.screen,
            batch=g.guiBatch,
            is_movable=False,
            offset=(x,y),
            theme=g.theme,
            anchor=ANCHOR_BOTTOM_LEFT)
        #frame.layout()
        #try:
        #    #print frame.content.label.content_height
        #    frame.expand(frame._content.width,frame._content.height)
        #    #print frame.content.label.content_height
        #except Exception, e:
        #    print Exception, e, frame.content.__dict__
        #print self._content[0]._content[0].label.content_height
        #frame.layout()
        #self.setPos(x-self.width/2,y)
        #g.selectWindowOpened=True
    def delete(self,event):
        g.hoveringType=None
        super(Manager,self).delete()
        #g.selectWindowOpened=False
        #g.cursorTarget=None
    def setPos(self,x,y):
        self.set_position(x,y)
        
    def updateContent(self,content):
        oldWidth=self.width
        oldX=self.x
        #if type==HOVERING_PING:
        #    self._content[0]._content[0].set_text(text)
        self.frame.content.delete()

        self.frame._content[0] = content
        self.frame.content.set_manager(self)
        self.frame.content.parent = self.frame
        self.frame.content.load()
        self.frame.reset_size()
        self.frame.layout()
        self.setPos(oldX+(oldWidth-self.width)/2,self.y)