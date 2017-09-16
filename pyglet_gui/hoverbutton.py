from pyglet_gui.buttons import Button
from pyglet_gui.core import Controller, Viewer
from pyglet_gui.controllers import TwoStateController
from pyglet_gui.constants import VALIGN_BOTTOM
from pyglet_gui.gui import Label, Frame, Graphic
from pyglet_gui.theme import templates, elements
from threading import Timer
import global_vars as g
from constants import *
from templates import *

'''
class HoverButton(Button):
    def __init__(self, label="", is_pressed=False, on_press=None,width=0,height=0,font_size=None,path=None,alternative=None,argument=None,outline=None,disabled=False,hover=None,hoveringType=None,arguments=None):
        Button.__init__(self,label=label,is_pressed=is_pressed,on_press=on_press,width=width,height=height,font_size=font_size,path=path,alternative=alternative,argument=argument,outline=outline,disabled=disabled)
        self.hover=hover
        self.args=arguments
        #self.hoverContent=hoverContent
        self.hoveringType = hoveringType
    #def on_mouse_motion(self,x,y,dx,dy):
    #    self.hover(None,False,x,y)
    def on_gain_highlight(self):
        self.hover(abilityHoverTemplate(args=self.args),True,self.x+self.width/2,self.y+self.height+8,hoveringType=self.hoveringType)
    def on_lose_highlight(self):
        self.hover(None,False)'''
        
#,width=0,height=0,path=None,alternative=None,outline=None,hover=None,hoveringType=None,arguments=None
class AbilityButton(TwoStateController, Viewer):
    def __init__(self, on_press=None,width=0,height=0,hover=None,argument=None,outline=None,disabled=False,arguments=None,texture=None,hoveringType=None,path=None):
        TwoStateController.__init__(self, is_pressed=False, on_press=on_press)
        Viewer.__init__(self,width=width,height=height)
        self.disabled=disabled
        self._width=width
        self._height=height
        self._outlineGraphic=None
        self._button = None
        self.hover=hover
        self._path=path
        self.leaderGraphic=None
        self.arg=argument
        self.args=arguments
        self._outline=outline
        self._painting=None
        self._textureZ=texture
        self.pressing=False
        self.hovering=False
        self.hoveringType = hoveringType
        self.paintingLoaded=False
    def change_state(self):
        self._is_pressed = not self._is_pressed
        self._on_press(self.arg)

    def hit_test(self, x, y):
        return self.is_inside(x, y)

    def release_mouse(self):
        if not self.hovering and not self.disabled:
            self.unload_painting()
        self.pressing=False
    def on_mouse_press(self, x, y, button, modifiers):
        if not self.disabled:
            self.change_state()
            if not self.pressing:
                self.pressing=True
                self.load_painting((255,255,255,100))
                t = Timer(0.075,self.release_mouse)
                t.start()
            
    def changeHover(self,hovering):
        self.hovering=hovering
        if self.disabled:
            return
        if self.hovering:
            self.load_painting((255,255,255,100))
        else:
            self.unload_painting()
    def on_gain_highlight(self):
        if self.hoveringType == HOVERING_ABILITY:
            cont = abilityHoverTemplate(args=self.args)
            x=self.x+self.width/2
            y=self.y+self.height+8
        elif self.hoveringType == HOVERING_ITEM:
            cont = itemHoverTemplate(args=self.args)
            x=self.x+self.width+8
            y=self.y+self.height/2
        self.hover(cont,True,x,y,hoveringType=self.hoveringType)
        self.changeHover(True)
    def on_lose_highlight(self):
        self.changeHover(False)
        self.hover(None,False)
    def get_path(self):
        return self._path
    def load_graphics(self):
        theme = self.theme[self.get_path()]
        if self._path is not None:
            self._button = theme['image'].generate(theme['gui_color'], **self.get_batch('background'))
        else:
            self._button = templates.TextureTemplate(self._textureZ).generate([255,255,255,255], **self.get_batch('background'))
        if self.disabled:
            self.load_painting((0,0,0,170))
            #self._painting = elements.TestGraphicElement((0,0,0,170),**self.get_batch('highlight'))
        self._outlineGraphic = self.theme[self._outline]["image"].generate([255,255,255,255],**self.get_batch('foreground'))
        
    def load_painting(self,color):
        if self.paintingLoaded:
            return
        self._painting = elements.TestGraphicElement(color,**self.get_batch('highlight'))
        self._painting.update(self.x,self.y,self.width,self.height)
        self.paintingLoaded=True
    def unload_painting(self):
        if self.paintingLoaded:
            self._painting.unload()
            self.paintingLoaded=False
    def unload_graphics(self):
        self._outlineGraphic.unload()
        if self.disabled and self._painting is not None:
            self.unload_painting()
        
        self._button.unload()

    def compute_size(self):
        return self._button.get_needed_size(self._width, self._height)
    def layout(self):
        self._button.update(self.x, self.y, self.width, self.height)
        if self.disabled and self._painting is not None:
            self._painting.update(self.x,self.y,self.width,self.height)
        self._outlineGraphic.update(self.x, self.y, self.width, self.height)
    def delete(self):
        TwoStateController.delete(self)
        Viewer.delete(self)
class HoverGraphic(Graphic,Controller):
    def __init__(self,width=0,height=0,path=None,alternative=None,outline=None,hover=None,hoveringType=None,arguments=None,showHighlight=False,texture=None):
        Graphic.__init__(self,path=path, width=width,height=height, alternative=alternative,outline=outline,texture=texture)
        Controller.__init__(self)
        self.hover=hover
        self.args=arguments
        self.path=path
        self.showHighlight=showHighlight
        self.hoveringType = hoveringType
    def hit_test(self, x, y):
        return self.is_inside(x, y)
    def delete(self):
        Controller.delete(self)
        Graphic.delete(self)
        
    def on_gain_highlight(self):
        if self.showHighlight:
            Graphic.change_path(self,self.path+'highlighted')
            Graphic.unload_graphics(self)
            Graphic.load_graphics(self)
            Graphic.layout(self)
        if g.gameState == GAMESTATE_FIGHTING and self.hoveringType != HOVERING_ABILITY:
            y = self.y-8
        else:
            y = self.y+self.height+8
        if self.hoveringType==HOVERING_PING:
            self.hover(pingHoverTemplate(g.latency),True,self.x+self.width/2,y,hoveringType=self.hoveringType)
        elif self.hoveringType==HOVERING_ABILITY:
            self.hover(abilityHoverTemplate(args=self.args),True,self.x+self.width/2,y,hoveringType=self.hoveringType)
        elif self.hoveringType == HOVERING_BAG:
            self.hover(bagHoverTemplate(g.moneyAmount,g.esAmount),True,self.x+self.width/2,y,hoveringType=self.hoveringType)
        
    def on_lose_highlight(self):
        self.hover(None,False)
        if self.showHighlight:
            Graphic.change_path(self,self.path)
            Graphic.unload_graphics(self)
            Graphic.load_graphics(self)
            Graphic.layout(self)
class HoverButton(Graphic,TwoStateController,Label):
    def __init__(self,width=0,height=0,path=None,alternative=None,outline=None,hover=None,hoveringType=None,arguments=None,is_pressed=False,on_press=None,disabled=False,argument=None,buttonNumber=None):
        Graphic.__init__(self,path=path, width=width,height=height, alternative=alternative,outline=outline)
        TwoStateController.__init__(self,is_pressed=is_pressed,on_press=on_press)
        Label.__init__(self,str(buttonNumber),color=(255,255,255,255))
        self.ol=outline
        self.hover=hover
        self.args=arguments
        self.arg=argument
        self.disabled=disabled
        #self.hoverContent=hoverContent
        self.hovering=False
        self.hoveringType = hoveringType
        self.bN=buttonNumber
        self.pressing=False
    def hit_test(self, x, y):
        return self.is_inside(x, y)
    def on_gain_highlight(self):
        if self.hoveringType==HOVERING_PING:
            self.hover(pingHoverTemplate(g.latency),True,self.x+self.width/2,self.y+self.height+8,hoveringType=self.hoveringType)
        elif self.hoveringType==HOVERING_ABILITY:
            self.hover(abilityHoverTemplate(args=self.args),True,self.x+self.width/2,self.y+self.height+8,hoveringType=self.hoveringType)
        self.changeHover(True)
    def on_lose_highlight(self):
        self.changeHover(False)
        self.hover(None,False)
    def change_state(self):
        self._is_pressed = not self._is_pressed
        self.reload()
        self.reset_size()
        if self.arg is None:
            self._on_press(self._is_pressed)
        else:
            self._on_press(self.arg)
    def release_mouse(self):
        self._outline=self.ol
        Graphic.unload_graphics(self)
        Graphic.load_graphics(self)
        Graphic.layout(self)
        self.pressing=False
    def on_mouse_press(self, x, y, button, modifiers):
        if not self.disabled:
            self.change_state()
        if not self.pressing:
            self.pressing=True
            self._outline=self.ol+'_highlighted'
            Graphic.unload_graphics(self)
            Graphic.load_graphics(self)
            Graphic.layout(self)
            t = Timer(0.075,self.release_mouse)
            t.start()
    def changeDisable(self,disabled):
        self.disabled=disabled
        if self.disabled:
            self._outline=self.ol+'_disabled'
        else:
            if self.hovering:
                self.changeHover(True)
                return
            self._outline=self.ol
        Graphic.unload_graphics(self)
        Graphic.load_graphics(self)
        Graphic.layout(self)
    def changeHover(self,hovering):
        self.hovering=hovering
        if self.disabled:
            return
        if self.hovering:
            self._outline=self.ol+'_highlighted'
        else:
            self._outline=self.ol
        Graphic.unload_graphics(self)
        Graphic.load_graphics(self)
        Graphic.layout(self)