import global_vars as g
from gamelogic import *
from objects import *
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Frame, Spacer, Label
from pyglet_gui.theme import Theme
from pyglet_gui.scrollable import Scrollable
from gui.popupInput import popUpInput
from gui.popupConfirm import popUpConfirm
from pyglet_gui.containers import VerticalContainer, HorizontalContainer
from pyglet_gui.buttons import HighlightedButton, Button
from pyglet_gui.constants import HALIGN_LEFT, ANCHOR_LEFT
class GuildWindow(Manager):
    def __init__(self):
        g.guildWindowOpened = True
        closeBtn =HighlightedButton("",on_release=self.delete,width=19,height=19,path='delete')
        if g.guildName is None:
            label1=Label("Guild",bold=True,color=g.loginFontColor)
            horzCont = HorizontalContainer(content=[label1,None,closeBtn])
            label = Label("You are not in a guild",color=g.loginFontColor)
            createBtn = HighlightedButton("Create Guild",on_release=self.createGuild,width=120,height=25)
            frameContent = VerticalContainer(content=[horzCont,label,createBtn])
        else:
            label1=Label(g.guildName,bold=True,color=g.loginFontColor)
            horzCont = HorizontalContainer(content=[label1,None,closeBtn])
            onlineMembers = []
            offlineMembers = []
            for c in guildList:
                if c[2]==1:
                    onlineMembers.append([c[0],c[1]])
                else:
                    offlineMembers.append([c[0],c[1]])
            onlineMembers.sort()
            offlineMembers.sort()
            members = []
            for c in onlineMembers:
                if c[1]==GUILD_MODERATOR:
                    font_color = g.modColor
                elif c[1]==GUILD_ADMIN:
                    font_color = g.adminColorLighter
                else:
                    font_color= g.loginFontColor
                label=HighlightedButton(c[0],width=150,height=24,path='baroutline_btn',font_color=font_color, on_release=self.constructSelect,argument=c[0],align=HALIGN_LEFT)
                #whisperBtn = HighlightedButton("",on_release=self.whisper,width=28,height=24,path='chatwhisper',argument=c[0])
                #if c[1]==GUILD_MODERATOR:
                #    label_extra=Label('#Mod#',color=g.modColor)
                #elif c[1]==GUILD_ADMIN:
                #    label_extra=Label('#Admin#',color=g.adminColorLighter)
                #else:
                label_extra=None
                members.append(HorizontalContainer(content=[label,label_extra]))
            for c in offlineMembers:
                if c[1]==GUILD_MODERATOR:
                    font_color = g.errorColor
                elif c[1]==GUILD_ADMIN:
                    font_color = g.adminColor
                else:
                    font_color= g.npcColorLighter
                label=HighlightedButton(c[0],width=150,height=24,path='baroutline_btn',font_color=font_color, on_release=self.constructSelect,argument=c[0],align=HALIGN_LEFT)
                members.append(label)
                
            buttons=[]
            print g.myGuildAccess
            if g.myGuildAccess>GUILD_MEMBER:
                buttons.append(HighlightedButton("Invite Player",on_release=invitePlayerGuildPopup,width=100,height=24))
            #if g.myGuildAccess==GUILD_ADMIN:
            #    buttons.append(HighlightedButton("Guild Settings",on_release=openSettingsGuild,width=100,height=24))
            #leaveBtn = HighlightedButton("Leave Guild",on_release=self.leaveBtn,width=80,height=24)
            #addBtn = HighlightedButton("",on_release=self.addFriend,width=24,height=24,path='friendadd')
            frameContent=VerticalContainer(content=[horzCont,Scrollable(height=600,width=400,content=VerticalContainer(content=members,align=HALIGN_LEFT,padding=0)),HorizontalContainer(buttons)])
        #horzCont = HorizontalContainer(content=[label1,closeBtn])
        frame = Frame(frameContent)
        Manager.__init__(self,
            frame,
            window=g.screen,
            batch=g.guiBatch,
            is_movable=False,
            anchor=ANCHOR_LEFT,
            offset=(40,int(g.SCREEN_HEIGHT*g.WINDOW_POSY_RELATIVE)),
            theme=g.theme)
    def on_mouse_motion(self, x, y, dx, dy):
        Manager.on_mouse_motion(self, x, y, dx, dy)
        g.cursorX=x
        g.cursorY=y
    def leaveGuild(self,event):
        sendLeaveGuild()
    def leaveBtn(self,event):
        popUpConfirm("Are you sure you want to leave " + g.guildName + "?",on_ok=self.leaveGuild)
        closeSelectWindow(None)
    def newGuild(self,name):
        tmpName=''.join(char for char in name if special_match(char))
        g.tmpName = " ".join(tmpName.split()).lstrip().rstrip()
        if len(g.tmpName)<3:
            constructText(WARNINGS["GUILD_NAME_TOO_SHORT"][0] % (g.tmpName),WARNINGS["GUILD_NAME_TOO_SHORT"][1])
            g.tmpName=None
        else:
            popUpConfirm("Are you sure you want to create a guild named " + g.tmpName + "?",on_ok=createGuild )
        #createGuild(name)
    def createGuild(self,event):
        popUpInput("Name your guild",on_ok=self.newGuild)
   
    def kickGuild(self,event):
        popUpConfirm("Are you sure you want to kick "+event+" from "+g.guildName+"?",on_ok=kickPlayer,argument=event)
        closeSelectWindow(None)
    def delete(self,event):
        super(Manager,self).delete()
        g.guildWindowOpened = False
        
    def promoteGuild(self,event):
        access=GUILD_MEMBER
        for c in guildList:
            if c[0]==event:
                access=c[1]
        text=""
        if g.myGuildAccess==GUILD_ADMIN and access==GUILD_MODERATOR:
            text=" and lose your status as a guild admin"
        popUpConfirm("Are you sure you want to promote "+event+text+"?",on_ok=promotePlayer,argument=event)
        closeSelectWindow(None)
    def demoteGuild(self,event):
        popUpConfirm("Are you sure you want to demote "+event+"?",on_ok=demotePlayer,argument=event)
        closeSelectWindow(None)
    def constructSelect(self,text):
        content=[]
        if text==myPlayer.name:
            content.append({"text":'Leave Guild','argument':'','function':self.leaveBtn})
        else:
            content.append({"text":'Whisper','argument':text,'function':whisper})
            if isFriend(text):
                content.append({"text":'Unfriend','argument':text,'function':removeFriend})
            else:
                content.append({"text":'Add Friend','argument':text,'function':addFriend})
            access=GUILD_MEMBER
            for c in guildList:
                if c[0]==text:
                    access=c[1]
            if g.myGuildAccess>access:
                content.append({"text":'Kick','argument':text,'function':self.kickGuild})
                if g.myGuildAccess==GUILD_ADMIN:
                    content.append({"text":'Promote','argument':text,'function':self.promoteGuild})
                if access==GUILD_MODERATOR:
                    content.append({"text":'Demote','argument':text,'function':self.demoteGuild})
        content.append({"text":'Close','argument':text,'function':closeSelectWindow})
        g.gameEngine.graphics.initSelectedWindow(text,content,g.cursorX,g.cursorY)