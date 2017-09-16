import pyglet
import global_vars as g
from gamelogic import *
from constants import *
from objects import *
import datetime
from pyglet.gl import *
from gui.chat import Chat
from gui.escwindow import EscWindow
from gui.settingswindow import SettingsWindow
from gui.gameSettingsWindow import GameSettingsWindow
from gui.friendWindow import FriendWindow
from gui.ignoreWindow import IgnoreWindow
from gui.normalGUI import NormalGUI
#from gui.selectWindow import SelectWindow
from gui.npcTalkWindow import NpcTalkWindow
from gui.adminWindow import AdminWindow
from gui.meneWindow import MeneWindow
from gui.hoverWindow import HoverWindow
from gui.reportWindow import ReportWindow
from gui.reportAnswerWindow import ReportAnswerWindow
from gui.postWindow import PostWindow
from gui.guildWindow import GuildWindow
from gui.selectedWindow import SelectedWindow
from gui.partyWindow import PartyWindow
from gui.keybindingsWindow import KeybindingsWindow
from PIL import Image
import time

class Graphics():
    def __init__(self,screen,sheets,spritesheets,mousesheets):
        self.screen = screen
        self.bgSheets = sheets
        self.realmap = None
        self.fringemap = None
        self.player = None
        self.spriteSheets = spritesheets
        self.mouseSheets = mousesheets
        self.chat = None
        self.escWindow = None
        self.settingsWindow = None
        self.friendWindow = None
        self.ignoreWindow = None
        #self.selectWindow = None
        self.gameSettingsWindow=None
        self.npcTalkWindow=None
        self.adminWindow=None
        self.normalUI = None
        self.meneWindow=None
        self.hoverWindow = None
        self.reportWindow = None
        self.reportAnswerWindow=None
        self.postWindow=None
        self.guildWindow=None
        self.selectedWindow=None
        self.partyWindow=None
        self.keybindingsWindow=None
        #self.dx=0
        #self.dy=0
        g.cursorTile = 0
    def initGUI(self):
        self.normalUI = NormalGUI()
        
    def initKeybindingsWindow(self):
        self.closeAllWindows()
        self.keybindingsWindow = KeybindingsWindow()
    def initSelectedWindow(self,title,content,x,y,type=0):
        if g.selectedWindowOpened:
            self.selectedWindow.delete(None)
        self.selectedWindow = SelectedWindow(title,content,x,y,type)
    def initGuildWindow(self):
        self.closeAllWindows()
        self.guildWindow = GuildWindow()
    def initPostWindow(self):
        self.closeAllWindows()
        self.postWindow = PostWindow()
    def initReportAnswerWindow(self):
        self.closeAllWindows()
        self.reportAnswerWindow = ReportAnswerWindow()
    def initMeneWindow(self):
        self.closeAllWindows()
        self.meneWindow = MeneWindow()
    def initAdminWindow(self):
        self.closeAllWindows()
        self.adminWindow = AdminWindow()
    def initNpcTalkWindow(self,name,text,actionType):
        self.closeAllWindows()
        self.npcTalkWindow = NpcTalkWindow(name,text,actionType)
    def initPartyWindow(self):
        if g.partyWindowOpened:
            self.partyWindow.delete(None)
        self.partyWindow = PartyWindow()
    def deletePartyWindow(self):
        if g.partyWindowOpened:
            self.partyWindow.delete(None)
    def initHoverWindow(self,content,x,y):
        self.hoverWindow = HoverWindow(content,x,y)
    def closeHoverWindow(self):
        try:
            self.hoverWindow.delete(None)
        except:
            pass
    def initSelectWindow(self):
        content=[]
        if g.cursorTarget.playerType == PLAYER_TYPE_PLAYER:
            if g.cursorTarget.name!=myPlayer.name:
                content.append({"text":'Whisper','argument':g.cursorTarget.name,'function':whisper})
                found=False
                for partyMember in g.partyMembers:
                    if partyMember.name==g.cursorTarget.name:
                        found=True
                if g.mePartyleader or len(g.partyMembers)==0:
                    if not found:
                        content.append({"text":'Invite','argument':g.cursorTarget.name,'function':inviteToParty})
                    else:
                        content.append({"text":'Kick','argument':g.cursorTarget.name,'function':kickFromParty})
                if isFriend(g.cursorTarget.name):
                    content.append({"text":'Unfriend','argument':g.cursorTarget.name,'function':removeFriend})
                else:
                    content.append({"text":'Add Friend','argument':g.cursorTarget.name,'function':addFriend})
                if isIgnored(g.cursorTarget.name):
                    content.append({"text":'Unignore','argument':g.cursorTarget.name,'function':removeIgnore})
                else:
                    content.append({"text":'Ignore','argument':g.cursorTarget.name,'function':addIgnore})
                
        elif g.cursorTarget.playerType == PLAYER_TYPE_NPC:
            content.append({"text":'Talk','argument':g.cursorTarget.name,'function':talkNPC})
        self.initSelectedWindow(g.cursorTarget.name,content,g.cursorX,g.cursorY,1)
        #self.selectedWindow = SelectWindow(g.cursorTarget.name,g.cursorTarget.playerType)
        
    def initIgnoreWindow(self):
        self.closeAllWindows()
        self.ignoreWindow = IgnoreWindow()
    def initFriendWindow(self):
        self.closeAllWindows()
        self.friendWindow = FriendWindow()
    def initGraphics(self):
        self.chat = Chat()
        self.initGUI()
    def initEscWindow(self):
        self.escWindow = EscWindow()
    def initSettingsWindow(self):
        self.settingsWindow = SettingsWindow()
    def initGameSettingsWindow(self):
        self.gameSettingsWindow = GameSettingsWindow()
    def initReportWindow(self):
        self.closeAllWindows()
        self.reportWindow = ReportWindow()
    def clearGraphics(self):
        del myPlayer.tmpPlayer.sprite
        del self.fringemap
        del self.realmap
        Map=MapClass()
    def closeAllWindows(self):
        if g.keybindingsWindowOpened:
            self.keybindingsWindow.delete(None)
        if g.npcTalkWindowOpened:
            self.npcTalkWindow.delete(None)
        if g.friendWindowOpened:
            self.friendWindow.delete(None)
        if g.ignoreWindowOpened:
            self.ignoreWindow.delete(None)
        if g.meneWindowOpened:
            self.meneWindow.delete(None)
        if g.reportWindowOpened:
            self.reportWindow.delete(None)
        if g.reportAnswerWindowOpened:
            self.reportAnswerWindow.delete(None)
        if g.adminWindowOpened:
            self.adminWindow.delete(None)
        if g.postWindowOpened:
            self.postWindow.delete(None)
        if g.guildWindowOpened:
            self.guildWindow.delete(None)
    
    def SetupMap(self):
        initMap()
        if g.gameState != GAMESTATE_FIGHTING:
            g.gameEngine.changeMusicSong(Map.song)
        #glEnable(GL_BLEND)
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        map = Image.new("RGBA", (Map.width*TILESHEET_WIDTH, Map.height*TILESHEET_WIDTH), (0,0,0,0))
        fringe = Image.new("RGBA", (Map.width*TILESHEET_WIDTH, Map.height*TILESHEET_WIDTH), (0,0,0,0))
        for x in range(Map.width):
            for y in range(Map.height):
                if Map.tile[x][y].l1 is not None:
                    type = Map.tile[x][y].l1[1]
                    tileset = Map.tile[x][y].l1[0]
                    posx = Map.tile[x][y].l1[2]%TILESHEET_WIDTH
                    posy = Map.tile[x][y].l1[2]//TILESHEET_WIDTH
                    map.paste(self.bgSheets[tileset][type].getTile(posx,posy),(x*TILESHEET_WIDTH,y*TILESHEET_WIDTH),self.bgSheets[tileset][type].getTile(posx,posy).convert('RGBA'))
                if Map.tile[x][y].l2 is not None:
                    type = Map.tile[x][y].l2[1]
                    tileset = Map.tile[x][y].l2[0]
                    posx = Map.tile[x][y].l2[2]%TILESHEET_WIDTH
                    posy = Map.tile[x][y].l2[2]//TILESHEET_WIDTH
                    map.paste(self.bgSheets[tileset][type].getTile(posx,posy),(x*TILESHEET_WIDTH,y*TILESHEET_WIDTH),self.bgSheets[tileset][type].getTile(posx,posy).convert('RGBA'))
                if Map.tile[x][y].l3 is not None:
                    type = Map.tile[x][y].l3[1]
                    tileset = Map.tile[x][y].l3[0]
                    posx = Map.tile[x][y].l3[2]%TILESHEET_WIDTH
                    posy = Map.tile[x][y].l3[2]//TILESHEET_WIDTH
                    map.paste(self.bgSheets[tileset][type].getTile(posx,posy),(x*TILESHEET_WIDTH,y*TILESHEET_WIDTH),self.bgSheets[tileset][type].getTile(posx,posy).convert('RGBA'))
                if Map.tile[x][y].f is not None:
                    type = Map.tile[x][y].f[1]
                    tileset = Map.tile[x][y].f[0]
                    posx = Map.tile[x][y].f[2]%TILESHEET_WIDTH
                    posy = Map.tile[x][y].f[2]//TILESHEET_WIDTH
                    fringe.paste(self.bgSheets[tileset][type].getTile(posx,posy),(x*TILESHEET_WIDTH,y*TILESHEET_WIDTH),self.bgSheets[tileset][type].getTile(posx,posy).convert('RGBA'))

        g.offsetX = (self.screen.width-TILESIZE)/2-myPlayer.x*TILESIZE
        g.offsetY = (self.screen.height+TILESIZE)/2+myPlayer.y*TILESIZE-Map.height*TILESIZE
        map = map.transpose(Image.FLIP_TOP_BOTTOM)
        raw_data = map.tobytes()
        self.realmap = pyglet.image.ImageData(Map.width*TILESHEET_WIDTH,Map.height*TILESHEET_WIDTH,'RGBA',raw_data)
        #self.realmap = self.realmap.get_texture()
        #self.realmap = pyglet.sprite.Sprite(self.realmap)
        #self.realmap._set_scale(2)
        self.realmap.width = self.realmap.width*TILE_SCALE
        self.realmap.height = self.realmap.height*TILE_SCALE
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        fringe = fringe.transpose(Image.FLIP_TOP_BOTTOM)
        raw_data = fringe.tobytes()
        self.fringemap = pyglet.image.ImageData(Map.width*TILESHEET_WIDTH,Map.height*TILESHEET_WIDTH,'RGBA',raw_data)
        #self.fringemap = pyglet.sprite.Sprite(self.fringemap)
        #self.fringemap._set_scale(2)
        #self.fringemap = self.fringemap.get_texture()
        self.fringemap.width = self.fringemap.width*TILE_SCALE
        self.fringemap.height = self.fringemap.height*TILE_SCALE
        myPlayer.tmpPlayer.sprite = loadPlayerSprites(myPlayer,self.spriteSheets)
        
    def drawNPCs(self):
        for i in xrange(len(npcList)):
            offset = checkOffset(npcList[i])
            npcList[i].tmpPlayer.xOffset = -offset[0]
            npcList[i].tmpPlayer.yOffset = -offset[1]
            npcList[i].tmpPlayer.posx = int((npcList[i].x-myPlayer.x)*TILESIZE+(self.screen.width-TILESIZE)/2+npcList[i].tmpPlayer.xOffset+myPlayer.tmpPlayer.xOffset)
            npcList[i].tmpPlayer.posy = int((-npcList[i].y+myPlayer.y)*TILESIZE+(self.screen.height-TILESIZE)/2+npcList[i].tmpPlayer.yOffset+myPlayer.tmpPlayer.yOffset)
            if g.cursorTarget is not None and npcList[i].name==g.cursorTarget.name and g.cursorTarget.playerType==PLAYER_TYPE_NPC and g.selectedWindowOpened and self.selectedWindow.type==1:
                self.selectedWindow.setPos(npcList[i].tmpPlayer.posx-(self.selectedWindow.width-TILESIZE)/2,npcList[i].tmpPlayer.posy+TILESIZE)
            npcList[i].tmpPlayer.sprite[npcList[i].tmpPlayer.spriteFacing].blit(npcList[i].tmpPlayer.posx,npcList[i].tmpPlayer.posy)
            if g.hoverTarget == npcList[i].name:
                npcList[i].tmpPlayer.highlightSprite[npcList[i].tmpPlayer.spriteFacing].blit(npcList[i].tmpPlayer.posx,npcList[i].tmpPlayer.posy)
            if i==g.talkingToNpc:
                if g.npcTalkWindowOpened and ((distance(myPlayer.x,myPlayer.y,npcList[i].x,npcList[i].y)>MAX_NPC_TALK_DISTANCE and myPlayer.tmpPlayer.movePath!=[]) or (npcList[i].name != self.npcTalkWindow.name)):
                    self.npcTalkWindow.delete(None)
                elif not g.npcTalkWindowOpened and distance(myPlayer.x,myPlayer.y,npcList[i].x,npcList[i].y)<=MAX_NPC_TALK_DISTANCE:
                    g.gameEngine.graphics.initNpcTalkWindow(npcList[i].name,npcList[i].text,npcList[i].actionType)
    def drawPlayers(self):
        for i in range(len(Players)):
            offset = checkOffset(Players[i])
            Players[i].tmpPlayer.xOffset = -offset[0]
            Players[i].tmpPlayer.yOffset = -offset[1]
            Players[i].tmpPlayer.posx = int((Players[i].x-myPlayer.x)*TILESIZE+(self.screen.width-TILESIZE)/2+Players[i].tmpPlayer.xOffset+myPlayer.tmpPlayer.xOffset)
            Players[i].tmpPlayer.posy = int((-Players[i].y+myPlayer.y)*TILESIZE+(self.screen.height-TILESIZE)/2+Players[i].tmpPlayer.yOffset+myPlayer.tmpPlayer.yOffset)
            Players[i].tmpPlayer.sprite[Players[i].tmpPlayer.spriteFacing].blit(Players[i].tmpPlayer.posx,Players[i].tmpPlayer.posy)
            if g.cursorTarget is not None and Players[i].name==g.cursorTarget.name and g.cursorTarget.playerType==PLAYER_TYPE_PLAYER and g.selectedWindowOpened:
                self.selectedWindow.setPos(Players[i].tmpPlayer.posx-(self.selectedWindow.width-TILESIZE)/2,Players[i].tmpPlayer.posy+TILESIZE)
            if g.currTick> Players[i].tmpPlayer.chatBubbleTime + Players[i].tmpPlayer.lastMsgTick and Players[i].tmpPlayer.lastMsg is not None:
                Players[i].tmpPlayer.lastMsg.delete()
                Players[i].tmpPlayer.lastMsg=None
            elif (Players[i].tmpPlayer.moving or myPlayer.tmpPlayer.moving) and Players[i].tmpPlayer.lastMsg is not None:
                posx=Players[i].tmpPlayer.posx-Players[i].tmpPlayer.lastMsg._content[0].width/2+TILESIZE/2
                posy=Players[i].tmpPlayer.posy+TILESIZE/16*17
                Players[i].tmpPlayer.lastMsg.setPos(posx,posy)
            if g.hoverTarget == Players[i].name:
                Players[i].tmpPlayer.highlightSprite[Players[i].tmpPlayer.spriteFacing].blit(Players[i].tmpPlayer.posx,Players[i].tmpPlayer.posy)
        if g.cursorTarget is not None and myPlayer.name==g.cursorTarget.name and g.cursorTarget.playerType==PLAYER_TYPE_PLAYER and g.selectedWindowOpened and self.selectedWindow.type==1:
            self.selectedWindow.setPos((g.SCREEN_WIDTH-self.selectedWindow.width)/2,g.SCREEN_HEIGHT/2+TILESIZE/8*4)
    def drawMouse(self):
        redBlockDrawing=False
        if g.currTick - g.redBlockTick < 1000:
            redPosX = g.redBlockX*TILESIZE+g.offsetX
            redPosY = (-g.redBlockY + myPlayer.y)*TILESIZE+(self.screen.height-TILESIZE)/2+myPlayer.tmpPlayer.yOffset
            self.mouseSheets[2+g.redBlockDisabled].blit(redPosX,redPosY)
            redBlockDrawing=True
        x = (g.cursorX-g.offsetX) // TILESIZE
        y = Map.height - (g.cursorY-g.offsetY) // TILESIZE - 1
        g.cursorXTile = x
        g.cursorYTile = y
        if g.selectPaint:
            if g.cursorXTile>=0 and g.cursorXTile <Map.width and g.cursorYTile>=0 and g.cursorYTile < Map.height:
                if g.cursorXTile == g.redBlockX and g.cursorYTile == g.redBlockY and redBlockDrawing:
                    pass
                else:
                    posy = (-g.cursorYTile + myPlayer.y)*TILESIZE+(self.screen.height-TILESIZE)/2+myPlayer.tmpPlayer.yOffset
                    self.mouseSheets[g.cursorTile].blit(g.cursorXTile*TILESIZE+g.offsetX,posy)
            if g.cursorSelectedTile != [-1,-1] and g.cursorSelectedTile[0]>=0 and g.cursorSelectedTile[0] <Map.width and g.cursorSelectedTile[1]>=0 and g.cursorSelectedTile[1] < Map.height:
                if g.cursorTarget is not None:
                    if g.cursorTarget.name != myPlayer.name:
                        offset = checkOffset(g.cursorTarget)
                        g.cursorTarget.tmpPlayer.xOffset = -offset[0]
                        g.cursorTarget.tmpPlayer.yOffset = -offset[1]
                        posx = int((g.cursorTarget.x-myPlayer.x)*TILESIZE+(g.SCREEN_WIDTH-TILESIZE)/2+g.cursorTarget.tmpPlayer.xOffset+myPlayer.tmpPlayer.xOffset)
                        posy = int((-g.cursorTarget.y+myPlayer.y)*TILESIZE+(g.SCREEN_HEIGHT-TILESIZE)/2+g.cursorTarget.tmpPlayer.yOffset+myPlayer.tmpPlayer.yOffset)
                    else:
                        posx=(g.SCREEN_WIDTH-TILESIZE)/2
                        posy=(g.SCREEN_HEIGHT-TILESIZE)/2
                    self.mouseSheets[1].blit(posx,posy)
                #else:
                #    posx = g.cursorSelectedTile[0]*TILESIZE+g.offsetX
                #    posy = (-g.cursorSelectedTile[1] + myPlayer.y)*TILESIZE+(self.screen.height-TILESIZE)/2+myPlayer.tmpPlayer.yOffset
                #print g.mouseoverPaint
            
    def drawNames(self):
        for i in npcList:
            posx=(i.x-myPlayer.x)*TILESIZE+(g.SCREEN_WIDTH-TILESIZE)//2+i.tmpPlayer.xOffset+myPlayer.tmpPlayer.xOffset+TILESIZE/2
            posy=(-i.y+myPlayer.y)*TILESIZE+(g.SCREEN_HEIGHT-TILESIZE)//2+i.tmpPlayer.yOffset+myPlayer.tmpPlayer.yOffset+TILESIZE/4*5-1
            #print posx,posy
            i.tmpPlayer.nameText.blit(posx,posy)
            #moveNameTexts(i,posx,posy)
            
        for i in Players:
            posx=(i.x-myPlayer.x)*TILESIZE+(g.SCREEN_WIDTH-TILESIZE)/2+i.tmpPlayer.xOffset+myPlayer.tmpPlayer.xOffset+TILESIZE/2
            posy=(-i.y+myPlayer.y)*TILESIZE+(g.SCREEN_HEIGHT-TILESIZE)/2+i.tmpPlayer.yOffset+myPlayer.tmpPlayer.yOffset+TILESIZE/4*5-1
            #print i.tmpPlayer.yOffset
            #print posx,posy
            if i.tmpPlayer.battling is not None:
                i.tmpPlayer.battling.blit(posx-TILESIZE/4,posy+i.tmpPlayer.nameText.height/2+1)
            i.tmpPlayer.nameText.blit(posx,posy)
            #moveNameTexts(i,posx,posy)
        myPlayer.tmpPlayer.nameText.blit(g.SCREEN_WIDTH//2,g.SCREEN_HEIGHT//2+TILESIZE/4*3)
        #g.nameBatch.draw()
    def update(self):
        t1=time.time()*1000
        offset = checkOffset(myPlayer)
        myPlayer.tmpPlayer.xOffset = offset[0]
        myPlayer.tmpPlayer.yOffset = offset[1]
        
        g.offsetX = int((self.screen.width-TILESIZE)/2-myPlayer.x*TILESIZE + myPlayer.tmpPlayer.xOffset)
        g.offsetY = int((self.screen.height+TILESIZE)/2+myPlayer.y*TILESIZE-Map.height*TILESIZE + myPlayer.tmpPlayer.yOffset)
        t2=time.time()*1000
        self.realmap.blit(g.offsetX,g.offsetY)
        #self.realmap.x=g.offsetX
        #self.realmap.y=g.offsetY
        #self.realmap.draw()
        t3=time.time()*1000
        tmpTime=time.time()
        self.drawMouse()
        t4=time.time()*1000
        self.drawNPCs()
        t5=time.time()*1000
        self.drawPlayers()
        myPlayer.tmpPlayer.sprite[myPlayer.tmpPlayer.spriteFacing].blit((g.screen.width-TILESIZE)/2,(g.screen.height-TILESIZE)/2)
        if g.hoverTarget == myPlayer.name:
            myPlayer.tmpPlayer.highlightSprite[myPlayer.tmpPlayer.spriteFacing].blit((g.screen.width-TILESIZE)/2,(g.screen.height-TILESIZE)/2)
        t6=time.time()*1000
        #self.fringemap.x=g.offsetX
        #self.fringemap.y=g.offsetY
        #self.fringemap.draw()
        self.fringemap.blit(g.offsetX,g.offsetY)
        t7=time.time()*1000
        self.drawNames()
        t8=time.time()*1000
        #print str(int(t7-t6))
        #print str((time.time()-tmpTime)*1000) + " ms to draw players"
        if g.currTick> myPlayer.tmpPlayer.chatBubbleTime + myPlayer.tmpPlayer.lastMsgTick and myPlayer.tmpPlayer.lastMsg is not None:
            myPlayer.tmpPlayer.lastMsg.delete()
            del myPlayer.tmpPlayer.lastMsg
            myPlayer.tmpPlayer.lastMsg=None
        g.chatBubbleBatch.draw()
        t9=time.time()*1000
        
        #tmpTime=time.time()
        g.guiBatch.draw()
        g.selectWindowBatch.draw()
        t10=time.time()*1000
        
        #print str((t7-t6)) + " ms"
        #print ignoreList
        
        #self.dx-=(g.currTick-g.lastTick)*0.1
        #self.dy+=(g.currTick-g.lastTick)*0.1