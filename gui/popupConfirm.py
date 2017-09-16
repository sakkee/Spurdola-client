from pyglet_gui.gui import PopupConfirm
from pyglet_gui.theme import Theme
import global_vars as g

class popUpConfirm(PopupConfirm):
    def __init__(self,text,ok="Okay",cancel="Cancel",on_ok=None,on_cancel=None, argument=None,offset=(0,g.SCREEN_HEIGHT/6)):
        
        PopupConfirm.__init__(self,
                            text=text,
                            ok=ok,
                            cancel=cancel,
                            on_ok=on_ok,
                            on_cancel=on_cancel,
                            theme=g.theme,
                            batch=g.guiBatch,
                            window=g.screen,
                            argument=argument,
                            offset=offset)
        g.popupWindow=self
    def delete(self):
        g.popupWindow=None
        PopupConfirm.delete(self)