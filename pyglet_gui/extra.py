from pyglet_gui.buttons import HighlightedButton
from pyglet_gui.core import Controller
from pyglet_gui.gui import Label, Frame
from pyglet_gui.containers import HorizontalContainer, VerticalContainer
from pyglet_gui.manager import Manager
from pyglet_gui.text_input import TextInput

class PopupInput(Manager):
    def __init__(self, text="", ok="Ok", cancel="Cancel",
                 window=None, batch=None, group=None, theme=None,
                 on_ok=None, on_cancel=None, text_color=None,bold=False,max_length=24,offset=(0,0)):
                 
        self.input = TextInput(text="",padding=0,length=24,max_length=max_length)
        def on_ok_click(_):
            if on_ok is not None:
                on_ok(self.input.get_text())
            self.delete()

        def on_cancel_click(_):
            if on_cancel is not None:
                on_cancel(self)
            self.delete()
        
        Manager.__init__(self, content=Frame(
            VerticalContainer([
                Label(text,color=text_color,bold=bold),
                self.input,
                HorizontalContainer([HighlightedButton(ok, on_release=on_ok_click),
                                     None,
                                     HighlightedButton(cancel, on_release=on_cancel_click)]
                )])
        ), window=window, batch=batch, group=group, theme=theme, is_movable=True, offset=offset)