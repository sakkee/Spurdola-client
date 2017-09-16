import pyglet.window

from pyglet_gui.override import Label

from pyglet_gui.constants import HALIGN_LEFT, HALIGN_RIGHT, HALIGN_CENTER, VALIGN_BOTTOM, VALIGN_CENTER

from pyglet_gui.controllers import TwoStateController
from pyglet_gui.core import Viewer
from pyglet_gui.mixins import FocusMixin, HighlightMixin
from pyglet_gui.theme import templates
class Button(TwoStateController, Viewer):
    def __init__(self, label="", is_pressed=False, on_press=None,width=0,height=0,font_size=None,path=None,alternative=None,argument=None,outline=None,disabled=False,align=HALIGN_CENTER,font_color=None,texture=None,outlinePressingEnabled=True,font=None,font_valign=VALIGN_CENTER,on_right_press=None):
        TwoStateController.__init__(self, is_pressed=is_pressed, on_press=on_press)
        Viewer.__init__(self,width=width,height=height)
       
        self._width=width
        self._height=height
        self.label = label
        self._outlineGraphic=None
        # graphics
        self._label = None
        self._button = None
        self._fn=font
        if path is not None:
            self._path = [path]
        else:
            self._path = ['button']
        self._alt=alternative
        self.font_size=font_size
        self.arg=argument
        self._outline=outline
        self.disabled=disabled
        self._al=align
        self._fl=font_color
        self._textureZ=texture
        self._olPressing=outlinePressingEnabled
        self._fontvalign=font_valign
        self.on_right_press=on_right_press
    def changeStateWithoutFnc(self):
        self._is_pressed = not self._is_pressed
        self.reload()
        self.reset_size()
    def change_state(self):
        self._is_pressed = not self._is_pressed
        self.reload()
        self.reset_size()
        if self.arg is None:
            self._on_press(self._is_pressed)
        else:
            self._on_press(self.arg)

    def hit_test(self, x, y):
        return self.is_inside(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.disabled:
            print button
            if self.on_right_press is None or button==1:
                self.change_state()
            elif self.on_right_press is not None and button==4:
                self.on_right_press(self.arg)
    
    def get_path(self):
        path = self._path
        path.append(self.getPressedPath())
        return path
    def getPressedPath(self):
        if self.is_pressed:
            return 'down'
        else:
            return 'up'
    def load_graphics(self):
        if self._alt is not None:
            theme = self._alt['button']
        else:
            #print self.theme, self.get_path()
            theme = self.theme[self.get_path()]
        if self._textureZ is None:
            self._button = theme['image'].generate(theme['gui_color'], **self.get_batch('background'))
        else:
            self._button = theme = templates.TextureTemplate(self._textureZ).generate([255,255,255,255], **self.get_batch('background'))
        if self._outline is not None:
            if self._olPressing:
                outlineTheme = self.theme[self._outline][self.getPressedPath()]
            else:
                outlineTheme = self.theme[self._outline]
            self._outlineGraphic = outlineTheme["image"].generate([255,255,255,255],**self.get_batch('foreground'))
        if self.label != "":
            if self.font_size is None:
                self.font_size = theme['font_size']
            if self._fl is None:
                self._fl = theme['text_color']
            if self._fn is None:
                self._fn = theme['font']
            self._label = Label(self.label,
                                font_name=self._fn,
                                font_size=self.font_size,
                                color=self._fl,
                                **self.get_batch('foreground'))

    def unload_graphics(self):
        if self._outlineGraphic is not None:
            self._outlineGraphic.unload()
        self._button.unload()
        if self._label is not None:
            self._label.unload()

    def compute_size(self):
        # Treat the height of the label as ascent + descent
        if self._label is not None:
            font = self._label.document.get_font()
            if not self._width and not self._height:
                height = font.ascent - font.descent
                return self._button.get_needed_size(self._label.content_width, height)
            elif self._width and not self._height:
                height = font.ascent - font.descent
                return self._button.get_needed_size(self._width, height)
            elif self._height and not self._width:
                return self._button.get_needed_size(self._label.content_width, self._height)
            else:
                return self._button.get_needed_size(self._width, self._height)
        else:
            return self._button.get_needed_size(self._width, self._height)
    def layout(self):
        self._button.update(self.x, self.y, self.width, self.height)
        if self._outlineGraphic is not None:
            self._outlineGraphic.update(self.x, self.y, self.width, self.height)
        # centers the label on the middle of the button
        x, y, width, height = self._button.get_content_region()
        if self._label is not None:
            font = self._label.document.get_font()
            if self._al==HALIGN_CENTER:
                self._label.x = x + width/2 - self._label.content_width/2
            else:
                self._label.x=x + 4
            if self._fontvalign==VALIGN_BOTTOM:
                self._label.y=y+font.ascent/2 + font.descent + 2
            else:
                self._label.y = y + height/2 - font.ascent/2 - font.descent - 2
            self._label.update()
    def delete(self):
        TwoStateController.delete(self)
        Viewer.delete(self)


class GroupButton(Button):
    button_groups = {}

    def __init__(self, group_id="", label="", is_pressed=False, on_press=None):
        Button.__init__(self, label=label, is_pressed=is_pressed, on_press=on_press)
        self.button_groups.setdefault(group_id, []).append(self)
        self.group_id = group_id

    def change_state(self):
        for button in self.button_groups[self.group_id]:
            if button._is_pressed and button is not self:
                button.change_state()
        super(GroupButton, self).change_state()


class OneTimeButton(Button):
    def __init__(self, label="", on_release=None,width=0,height=0,font_size=None,path=None,argument=None,align=HALIGN_CENTER,font_color=None):
        Button.__init__(self, label=label,width=width,height=height,font_size=font_size,path=path,align=align,font_color=font_color)
        self.disabled = False
        self.arg=argument
        self.on_release = lambda x: x
        if on_release is not None:
            self.on_release = on_release

    def on_mouse_release(self, x, y, button, modifiers):
        if self.is_pressed:
            self.change_state()

            # If mouse is still hovering us, signal on_release
            if self.hit_test(x, y) and not self.disabled:
                if self.arg is not None:
                    self.on_release(self.arg)
                else:
                    self.on_release(self._is_pressed)


class Checkbox(Button):
    def __init__(self, label="", is_pressed=False, on_press=None, align=HALIGN_RIGHT, padding=4,width=None,height=None):

        assert align in [HALIGN_LEFT, HALIGN_RIGHT]
        Button.__init__(self, label=label, is_pressed=is_pressed, on_press=on_press,width=width,height=height)

        self.align = align  # where the label is positioned.
        self.w=width
        self.h=height
        # private
        self._padding = padding

    def get_path(self):
        path = ['checkbox']
        if self.is_pressed:
            path.append('checked')
        else:
            path.append('unchecked')
        return path

    def layout(self):
        if self.align == HALIGN_RIGHT:  # label goes on right
            self._button.update(self.x,
                                self.y + self.height/2 - self.h/2,
                                self.w,
                                self.h)
            self._label.x = self.x + self.w + self._padding
        else:  # label goes on left
            self._label.x = self.x
            self._button.update(self.x + self._label.content_width + self._padding,
                                self.y + self.height/2 - self.h/2,
                                self.w,
                                self.h)

        font = self._label.document.get_font()
        height = font.ascent - font.descent
        self._label.y = self.y + self.height/2 - height/2 - font.descent

    def compute_size(self):
        if self._width is not None and self._height is not None:
            self.w=self._width
            self.h=self._height
        else:
            self.w=self._button.width
            self.h=self._button.height
        # Treat the height of the label as ascent + descent
        if self._label is not None:
            font = self._label.document.get_font()
            height = font.ascent - font.descent

            return self.w + self._padding + self._label.content_width, max(self.h, height)
        else:
            return self.w + self._padding, self.h


class FocusButton(Button, FocusMixin):
    """
    Button that is focusable and thus can be selected with TAB.
    """
    def __init__(self, label="", is_pressed=False, on_press=None,width=0,height=0,path=None):
        Button.__init__(self, label, is_pressed, on_press,width,height,path=path)
        FocusMixin.__init__(self)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ENTER:
            self.change_state()

    
class HighlightedButton(OneTimeButton, HighlightMixin):
    """
    An example of a Button that changes behavior when is mouse-hovered.
    We mix the behavior of button with HighlightMixin.
    """
    def __init__(self, label="", on_release=None,width=0,height=0,font_size=None,path=None,argument=None,align=HALIGN_CENTER,font_color=None):
        OneTimeButton.__init__(self, label, on_release,width,height,font_size,path=path,argument=argument,align=align,font_color=font_color)
        HighlightMixin.__init__(self)

    def load_graphics(self):
        OneTimeButton.load_graphics(self)
        HighlightMixin.load_graphics(self)

    def layout(self):
        OneTimeButton.layout(self)
        HighlightMixin.layout(self)
        
    def on_mouse_press(self, x, y, button, modifiers):
        OneTimeButton.change_state(self)
        HighlightMixin.unload_graphics(self)
    def unload_graphics(self):
        OneTimeButton.unload_graphics(self)
        HighlightMixin.unload_graphics(self)
        
class PartyMemberButton(TwoStateController, Viewer):
    def __init__(self, label="", on_press=None,width=0,height=0,font_size=None,argument=None,outline=None,font_color=None,texture=None,font=None,font_valign=VALIGN_CENTER,leader=None):
        TwoStateController.__init__(self, is_pressed=False, on_press=on_press)
        Viewer.__init__(self,width=width,height=height)
       
        self._width=width
        self._height=height
        self.label = label
        self._outlineGraphic=None
        self._label = None
        self._button = None
        self._fn=font
        self._path = ['button']
        self._leader=leader
        self.leaderGraphic=None
        self.font_size=font_size
        self.arg=argument
        self._outline=outline
        self._fl=font_color
        self._textureZ=texture
        self._fontvalign=font_valign
    def change_state(self):
        self._is_pressed = not self._is_pressed
        if self.arg is None:
            self._on_press(self._is_pressed)
        else:
            self._on_press(self.arg)

    def hit_test(self, x, y):
        return self.is_inside(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        self.change_state()

    
    def get_path(self):
        return self._path
    def load_graphics(self):
        theme = self.theme[self.get_path()]
        self._button = templates.TextureTemplate(self._textureZ).generate([255,255,255,255], **self.get_batch('background'))
        self._outlineGraphic = self.theme[self._outline]["image"].generate([255,255,255,255],**self.get_batch('highlight'))
        if self._leader is not None:
            print self.theme[self._leader]
            self.leaderGraphic = self.theme[self._leader]["image"].generate([255,255,255,255],**self.get_batch('foreground'))
        if self.label != "":
            if self.font_size is None:
                self.font_size = theme['font_size']
            if self._fl is None:
                self._fl = theme['text_color']
            if self._fn is None:
                self._fn = theme['font']
            self._label = Label(self.label,
                                font_name=self._fn,
                                font_size=self.font_size,
                                color=self._fl,
                                **self.get_batch('foreground'))

    def unload_graphics(self):
        if self._outlineGraphic is not None:
            self._outlineGraphic.unload()
        self._button.unload()
        if self._label is not None:
            self._label.unload()
        if self._leader is not None:
            self.leaderGraphic.unload()

    def compute_size(self):
        # Treat the height of the label as ascent + descent
        if self._label is not None:
            font = self._label.document.get_font()
            if not self._width and not self._height:
                height = font.ascent - font.descent
                return self._button.get_needed_size(self._label.content_width, height)
            elif self._width and not self._height:
                height = font.ascent - font.descent
                return self._button.get_needed_size(self._width, height)
            elif self._height and not self._width:
                return self._button.get_needed_size(self._label.content_width, self._height)
            else:
                return self._button.get_needed_size(self._width, self._height)
        else:
            return self._button.get_needed_size(self._width, self._height)
    def layout(self):
        self._button.update(self.x, self.y, self.width, self.height)
        if self._outlineGraphic is not None:
            self._outlineGraphic.update(self.x, self.y, self.width, self.height)
        # centers the label on the middle of the button
        x, y, width, height = self._button.get_content_region()
        if self._leader is not None:
            self.leaderGraphic.update(x+4,y+height-16-4,16,16)
        if self._label is not None:
            font = self._label.document.get_font()
            self._label.x = x + width/2 - self._label.content_width/2
            if self._fontvalign==VALIGN_BOTTOM:
                self._label.y=y+font.ascent/2 + font.descent + 2
            else:
                self._label.y = y + height/2 - font.ascent/2 - font.descent - 2
            self._label.update()
    def delete(self):
        TwoStateController.delete(self)
        Viewer.delete(self)