import global_vars as g
from gamelogic import *
from objects import *
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Frame, Spacer, Label
from pyglet_gui.theme import Theme
from pyglet_gui.scrollable import Scrollable
from pyglet_gui.containers import VerticalContainer, HorizontalContainer
from pyglet_gui.buttons import HighlightedButton, PartyMemberButton
from pyglet_gui.constants import HALIGN_LEFT, ANCHOR_LEFT, VALIGN_BOTTOM
class PartyWindow(Manager):
    def __init__(self):
        g.partyWindowOpened = True
        #label1=Label("Friends List",bold=True,color=g.loginFontColor)
        #closeBtn =HighlightedButton("",on_release=self.delete,width=19,height=19,path='delete')
        party = []
        for member in g.partyMembers:
            leader=None
            if member.access:
                leader='partyleader'
            party.append(PartyMemberButton(on_press=self.constructSelect,label=member.name,width=64,height=64,argument=member.name,texture=member.texture,outline='partymember',font_valign=VALIGN_BOTTOM,font=g.defaultFont.name,font_color=g.partyColor,font_size=10,leader=leader))
        test = VerticalContainer(content=party)
        Manager.__init__(self,
            test,
            window=g.screen,
            batch=g.guiBatch,
            is_movable=False,
            anchor=ANCHOR_LEFT,
            offset=(g.SCREEN_WIDTH*0.05,int(g.SCREEN_HEIGHT*g.WINDOW_POSY_RELATIVE*1.3)),
            theme=g.theme)
    def delete(self,event):
        super(Manager,self).delete()
        g.partyWindowOpened = False
    def on_mouse_motion(self, x, y, dx, dy):
        Manager.on_mouse_motion(self, x, y, dx, dy)
        g.cursorX=x
        g.cursorY=y
    def constructSelect(self,text):
        print "PARTYLEADER ON", g.mePartyleader
        content=[]
        if text==myPlayer.name:
            content.append({"text":'Leave','argument':text,'function':leaveParty})
        else:
            content.append({"text":'Whisper','argument':text,'function':whisper})
            if isFriend(text):
                content.append({"text":'Unfriend','argument':text,'function':removeFriend})
            else:
                content.append({"text":'Add Friend','argument':text,'function':addFriend})
            if isIgnored(text):
                content.append({"text":'Unignore','argument':text,'function':removeIgnore})
            else:
                content.append({"text":'Ignore','argument':text,'function':addIgnore})
            if g.mePartyleader:
                content.append({"text":'Kick','argument':text,'function':kickFromParty})
        content.append({"text":'Close','argument':text,'function':closeSelectWindow})
        g.gameEngine.graphics.initSelectedWindow(text,content,g.cursorX,g.cursorY)