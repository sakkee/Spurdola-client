import pyglet
import global_vars as g
from pyglet.gl import *
from constants import *
import datetime
class FightStartAnimation():
    def __init__(self):
        #self.screen = screen
        
        self.icon = pyglet.sprite.Sprite(pyglet.image.load(g.dataPath + '/icons/battleicon.png'),x=(g.SCREEN_WIDTH-163)/2,y=(g.SCREEN_HEIGHT-165)/2)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        self.startTick = None
        self.drawing=False
        self.changeSpeed=100
        self.finished=False
        self.finishTick=40
    def initStartTick(self):
        self.startTick = g.currTick
        self.changeSpeed=100
    def update(self):
        #print g.dx
        if g.currTick>self.changeSpeed+self.startTick:
            if self.drawing:
                self.drawing = False
                self.changeSpeed = self.changeSpeed*0.86
            else:
                self.drawing = True
            self.startTick = g.currTick
        if self.drawing:
            self.icon.draw()
        if self.changeSpeed<=self.finishTick:
            self.finished=True