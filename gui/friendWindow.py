import global_vars as g
from gamelogic import *
from objects import *
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Frame, Spacer, Label
from pyglet_gui.theme import Theme
from pyglet_gui.scrollable import Scrollable
from pyglet_gui.containers import VerticalContainer, HorizontalContainer
from pyglet_gui.buttons import HighlightedButton, Button
from pyglet_gui.constants import HALIGN_LEFT, ANCHOR_LEFT
class FriendWindow(Manager):
    def __init__(self):
        g.friendWindowOpened = True
        label1=Label("Friends List",bold=True,color=g.loginFontColor)
        closeBtn =HighlightedButton("",on_release=self.delete,width=19,height=19,path='delete')
        onlineFriends = []
        offlineFriends = []
        for c in friendList:
            if c[1]==1:
                onlineFriends.append(c[0])
            else:
                offlineFriends.append(c[0])
        onlineFriends.sort()
        offlineFriends.sort()
        friends = []
        for c in onlineFriends:
            label=HighlightedButton(c,width=150,height=24,path='baroutline_btn', on_release=self.constructSelect,argument=c,align=HALIGN_LEFT,font_color=g.loginFontColor)
            friends.append(label)
        for c in offlineFriends:
            label=HighlightedButton(c,width=150,height=24,path='baroutline_btn', on_release=self.constructSelect,argument=c,align=HALIGN_LEFT,font_color=g.npcColorLighter)
            friends.append(label)
        addBtn = HighlightedButton("Add Friend",on_release=addFriendPopup,width=100,height=24)
        
        horzCont = HorizontalContainer(content=[label1,None,closeBtn])
        frame = Frame(VerticalContainer(content=[horzCont,Scrollable(height=400,width=400,content=VerticalContainer(content=friends,align=HALIGN_LEFT,padding=0)),addBtn]))
        Manager.__init__(self,
            frame,
            window=g.screen,
            batch=g.guiBatch,
            is_movable=False,
            anchor=ANCHOR_LEFT,
            offset=(40,int(g.SCREEN_HEIGHT*g.WINDOW_POSY_RELATIVE)),
            theme=g.theme)
    def delete(self,event):
        super(Manager,self).delete()
        g.friendWindowOpened = False
    def on_mouse_motion(self, x, y, dx, dy):
        Manager.on_mouse_motion(self, x, y, dx, dy)
        g.cursorX=x
        g.cursorY=y
    def constructSelect(self,text):
        content=[]
        if isFriendOnline(text):
            content.append({"text":'Whisper','argument':text,'function':whisper})
        content.append({"text":'Unfriend','argument':text,'function':removeFriend})
        content.append({"text":'Close','argument':text,'function':closeSelectWindow})
        g.gameEngine.graphics.initSelectedWindow(text,content,g.cursorX,g.cursorY)