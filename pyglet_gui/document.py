import pyglet
import time
from pyglet_gui.scrollbars import VScrollbar
from pyglet_gui.core import Viewer, Rectangle
from pyglet_gui.controllers import Controller


class Document(Controller, Viewer):
    """
    Allows you to embed a document within the GUI, which includes a
    vertical scrollbar.
    """
    def __init__(self, document, width=0, height=0, is_fixed_size=False,background=False,font_size=13,font_name='Segoe UI',font_color=None,chat=False):
        Viewer.__init__(self, width, height)
        Controller.__init__(self)

        self.max_height = height
        if isinstance(document, str):
            self._document = pyglet.text.document.UnformattedDocument(document)
        else:
            self._document = document
        self.h1=height
        self.w1=width
        self.chat=chat
        self.fontSize=font_size
        self.fontName=font_name
        self.fontColor=font_color
        self._bgcolor = background
        self._bg = None
        self._content = None
        self.content_width = width
        self._scrollbar = None
        self.set_document_style = False
        self.firstTimeLoad=True
        self.is_fixed_size = is_fixed_size

    def hit_test(self, x, y):
        if self._content is not None:
            return Rectangle(self._content.x,
                             self._content.y,
                             self._content.width,
                             self._content.height).is_inside(x, y)
        else:
            return False

    def _load_scrollbar(self, height):
        if self._content.content_height > height:
            if self._scrollbar is None:
                self._scrollbar = VScrollbar(self.max_height)
                self._scrollbar.set_manager(self._manager)
                self._scrollbar.parent = self
                self._scrollbar.load()
                self._scrollbar.set_knob_size(self.height, self._content.content_height)
        # if smaller, we unload it if it is loaded
        elif self._scrollbar is not None:
            self._scrollbar.unload()
            self._scrollbar = None

    def load_graphics(self):
        if self._bgcolor is True: 
            self._bg = self.theme[['document']]['image'].generate(self.theme[['document']]['gui_color'],**self.get_batch("background"))
        
        if not self.set_document_style and not self.chat:
            self.do_set_document_style(self._manager)
        self._content = pyglet.text.layout.IncrementalTextLayout(self._document,
                                                                 self.content_width, self.max_height,
                                                                 multiline=True, **self.get_batch('foreground'))


    def unload_graphics(self):
        if self._bg is not None:
            self._bg.unload()
        self._content.delete()
        if self._scrollbar is not None:
            self._scrollbar.unload()
            self._scrollbar = None
        
    def do_set_document_style(self, dialog):
        self.set_document_style = True
        # Check the style runs to make sure we don't stamp on anything
        # set by the user
        self._do_set_document_style('color', dialog.theme['text_color'])
        self._do_set_document_style('font_name', dialog.theme['font'])
        self._do_set_document_style('font_size', dialog.theme['font_size'])
    def _do_set_document_style(self, attr, value):
        length = len(self._document.text)
        runs = [(start, end, doc_value) for start, end, doc_value in
                self._document.get_style_runs(attr).ranges(0, length)
                if doc_value is not None]
        if not runs:
            terminator = len(self._document.text)
        else:
            terminator = runs[0][0]
        self._document.set_style(0, terminator, {attr: value})

    def get_text(self):
        return self._document.text

    def layout(self):
        if self._bgcolor is True:
            self._bg.update(self.x,self.y,self.w1+2,self.h1)
        if self._scrollbar is not None:
            self._scrollbar.set_position(self.x + self._content.content_width+2, self.y)
            pos = self._scrollbar.get_knob_pos()
            if pos != -self._content.view_y:
                self._content.view_y = -pos

        self._content.begin_update()
        self._content.x = self.x+2
        self._content.y = self.y
        self._content.end_update()
        if self._scrollbar is not None:
            self._scrollbar.set_position(self.x + self.content_width+2, self.y)

    def on_gain_highlight(self):
        if self._scrollbar is not None:
            self._manager.set_wheel_target(self._scrollbar)

    def on_lose_highlight(self):
        self._manager.set_wheel_target(None)

    def compute_size(self):
        if self.is_fixed_size or (self.max_height and self._content.content_height > self.max_height):
            height = self.max_height
        else:
            height = self._content.content_height
        self._content.height = height
        self._load_scrollbar(height)
        if self._scrollbar is not None:
            
            self._scrollbar.set_knob_size(height, self._content.content_height)
            if self.firstTimeLoad:
                self._scrollbar.set_knob_pos(0)
                self.firstTimeLoad=False
            else:
                self._scrollbar.set_knob_pos(1)
            self._scrollbar.compute_size()
            
            width = self.content_width + self._scrollbar.width
            #print self._scrollbar.get_knob_pos()
        else:
            width = self.content_width
        return width, height

    def set_text(self, text):
        self._document.text = text
        self.compute_size()
        self.layout()
    def update_text(self,text):
        realtext = '{font_size '+str(self.fontSize)+'}{font_name "'+self.fontName+'"}{wrap "char"}'+text
        t1 = time.time()*1000
        #self._document = pyglet.text.decode_attributed(realtext)
        
        #self._document.insert_text(0,text)
        #print len(self._document._text)
        #print self._document.__dict__
        t2 = time.time()*1000
        #self._content.begin_update()
        #self._content._set_document(self._document)
        t3 = time.time()*1000
        #self._content.end_update()
        #self.compute_size()
        t4 = time.time()*1000
        #self.layout()
        t5 = time.time()*1000
        print "Total: " + str(int(t5-t1)) + " ms. t2-t1: " + str(int(t2-t1)) + " and t3-t2: " + str(int(t3-t2)) + " and t4-t3: " + str(int(t4-t3)) + " and t5-t4: " + str(int(t5-t4))
    def delete(self):
        Controller.delete(self)
        Viewer.delete(self)
