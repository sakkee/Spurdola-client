from pyglet_gui.gui import PopupMessage
from pyglet_gui.theme import Theme
import global_vars as g

class popUpWindow(PopupMessage):
    def __init__(self,text):

        # Set up a Manager
        PopupMessage.__init__(self,
                             text=text,
                             textcolor=[255,255,255,200],
                             window=g.screen,
                             width=g.SCREEN_WIDTH/2,
                             batch=g.guiBatch,
                             theme=g.theme)