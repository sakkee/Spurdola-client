from pyglet_gui.extra import PopupInput
from pyglet_gui.theme import Theme
import global_vars as g

class popUpInput(PopupInput):
    def __init__(self,text,ok="Okay",cancel="Cancel",on_ok=None,on_cancel=None,text_color=None,bold=False,max_length=24,offset=(0,g.SCREEN_HEIGHT/6)):
        g.popupWindowOpened=True
        PopupInput.__init__(self,
                            text=text,
                            ok=ok,
                            cancel=cancel,
                            on_ok=on_ok,
                            on_cancel=on_cancel,
                            theme=g.theme,
                            batch=g.guiBatch,
                            window=g.screen,
                            bold=bold,
                            max_length=max_length,
                            text_color=text_color,
                            offset=offset)
        g.popupWindow=self
    def delete(self):
        g.popupWindowOpened=False
        PopupInput.delete(self)
        g.popupWindow=None