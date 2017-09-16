import time
import pyglet

import sys
import global_vars as g
pyglet.lib.load_library(g.dataPath+'/avbin')
pyglet.have_avbin=True
import datetime
from loginmenu import loginMenu
from constants import *
import fightstartanimation
from objects import *
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from network.client import *
from gamelogic import *
import resourcemanager
import graphics
from pyglet.gl import *
import cfg_parser
from fightscreen import FightScreen
#from network.database import *

class Engine:
    def __init__(self):
        getSmallestResolution()
        #g.SCREEN_WIDTH = pyglet.window.get_platform().get_default_display().get_default_screen().width
        #g.SCREEN_HEIGHT=pyglet.window.get_platform().get_default_display().get_default_screen().height
        #print pyglet.window.get_platform().get_default_display().get_default_screen().get_modes()
        g.SCREENSELECTED = pyglet.window.get_platform().get_default_display().get_default_screen()._handle
        cfg_parser.readCfg()
        if int(g.SCREENSELECTED)<len(pyglet.window.get_platform().get_default_display().get_screens()) and int(g.SCREENSELECTED)>=0:
            defaultMonitor = pyglet.window.get_platform().get_default_display().get_screens()[int(g.SCREENSELECTED)]
        else:
            defaultMonitor = pyglet.window.get_platform().get_default_display().get_default_screen()
        
        g.screen = pyglet.window.Window(fullscreen=g.FULLSCREEN,vsync=g.VSYNC,width=g.SCREEN_WIDTH,height=g.SCREEN_HEIGHT,screen=defaultMonitor) #,screen=pyglet.window.get_platform().get_default_display().get_screens()[1]
        g.SCREEN_WIDTH = g.screen.width
        g.SCREEN_HEIGHT = g.screen.height
        g.gameEngine = self
        g.screen.set_mouse_cursor(g.cursorUp)
        g.screen.set_caption(GAME_NAME)
        g.screen.set_icon(g.gameIcon)
        self.soundManager = pyglet.media.Player()
        self.soundManager.volume=g.MUSICVOLUME
        self.musicManager = pyglet.media.Player()
        self.musicManager.volume=g.MUSICVOLUME
        self.musicManager.eos_action = pyglet.media.Player.EOS_LOOP
        self.loginMenu = loginMenu(g.screen)
        self.fightStartAnimation = fightstartanimation.FightStartAnimation()
        self.fightScreen = FightScreen()
        self.resManager = resourcemanager.ResourceManager()
        self.graphics = graphics.Graphics(g.screen,self.resManager.tileSheets,self.resManager.spriteSheets,self.resManager.mouseSheets)
        self.checkPressed = []
        self.fps = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
        g.screen.push_handlers(on_key_press=self.my_key_press,on_key_release=self.my_key_release,on_mouse_press=self.mouseClick,on_mouse_release=self.mouseRelease,on_mouse_motion=self.mouseMove)
        self.fpsTick = 0
        self.lastTick=0
        self.fpsDisplay = pyglet.window.FPSDisplay(g.screen)
        
        self.screenshotting=False
        pyglet.gl.glClearColor(0,0,0,255)
    def init(self):
        tick = LoopingCall(self.gameLoop)
        tick.start(1./g.FPS)
        reactor.run()
    
    def playSoundEffect(self,sound):
        if g.SOUND:
            self.resManager.soundEffects[sound].play(g.SOUNDVOLUME)
    def playSound(self,sound):
        if g.SOUND:
            self.fightScreen.sounds[sound].play(g.SOUNDVOLUME)
            #self.fightScreen.sounds[sound]._set_volume(0.05)
    def changeMusicSong(self,song,fadetime=1.0,loaded=False):
        if not loaded:
            self.musicManager.queue(pyglet.media.load(g.dataPath+'/sounds/'+song+'.mp3'))
        else:
            try:
                self.musicManager.queue(song)
            except Exception, e:
                print Exception, e
        if g.MUSIC:
            g.fadeTime=fadetime
            g.fadeTick=g.currTick
            g.fadingOut=True
            g.fadingIn=False
            if not self.musicManager.playing:
                g.fadingIn=True
                g.fadingOut=False
                self.musicManager.volume=0
                self.musicManager.play()
        else:
            while len(self.musicManager._groups)>1:
                self.musicManager.next_source()
    def initConnection(self):
        connectionProtocol = startConnection()
        g.tcpConn = TCPConnection(connectionProtocol)
    def disconnect(self):
        g.connector.disconnect()
    def mouseMove(self,x,y,dx,dy):
        g.cursorX = x
        g.cursorY = y
        if g.hoverPaint:
            found=False
            for c in npcList:
                if g.cursorX>=c.tmpPlayer.posx and g.cursorX<c.tmpPlayer.posx+TILESIZE and g.cursorY>=c.tmpPlayer.posy and g.cursorY<c.tmpPlayer.posy+TILESIZE:
                    g.hoverTarget=c.name
                    found=True
            for c in Players:
                if g.cursorX>=c.tmpPlayer.posx and g.cursorX<c.tmpPlayer.posx+TILESIZE and g.cursorY>=c.tmpPlayer.posy and g.cursorY<c.tmpPlayer.posy+TILESIZE:
                    g.hoverTarget=c.name
                    found=True
            if g.cursorX>=(g.SCREEN_WIDTH-TILESIZE)/2 and g.cursorX<(g.SCREEN_WIDTH+TILESIZE)/2 and g.cursorY>=(g.SCREEN_HEIGHT-TILESIZE)/2 and g.cursorY<(g.SCREEN_HEIGHT+TILESIZE)/2:
                g.hoverTarget=myPlayer.name
                found=True
            if not found:
                g.hoverTarget=None
    def mouseClick(self,x,y,button,modifiers):
        g.screen.set_mouse_cursor(g.cursorDown)
        if g.gameState == GAMESTATE_INGAME:
            if button == pyglet.window.mouse.LEFT:
                sendFaceTarget(g.cursorXTile,g.cursorYTile)
            if button == pyglet.window.mouse.RIGHT:
                sendMoveTarget(g.cursorXTile,g.cursorYTile)
            else:
                if g.selectWindowOpened == True:
                    self.graphics.selectWindow.delete(None)
                if g.selectedWindowOpened:
                    self.graphics.selectedWindow.delete(None)
                removeTarget=True
                found = []
                if myPlayer.x == g.cursorXTile and myPlayer.y == g.cursorYTile:
                    found.append(myPlayer)
                for c in npcList:
                    if c.x == g.cursorXTile and c.y == g.cursorYTile:
                        found.append(c)
                    elif c.tmpPlayer.moving:
                        if c.x+1==g.cursorXTile and c.y==g.cursorYTile and c.dir==DIR_LEFT and g.currTick-c.tmpPlayer.moveTick<=WALKSPEED/2:
                            found.append(c)
                        elif c.x-1==g.cursorXTile and c.y==g.cursorYTile and c.dir==DIR_RIGHT and g.currTick-c.tmpPlayer.moveTick<=WALKSPEED/2:
                            found.append(c)
                        elif c.x==g.cursorXTile and c.y-1==g.cursorYTile and c.dir==DIR_UP and g.currTick-c.tmpPlayer.moveTick<=WALKSPEED/2:
                            found.append(c)
                        elif c.x==g.cursorXTile and c.y+1==g.cursorYTile and c.dir==DIR_DOWN and g.currTick-c.tmpPlayer.moveTick<=WALKSPEED/2:
                            found.append(c)
                        
                for c in Players:
                    if c.x == g.cursorXTile and c.y == g.cursorYTile:
                        found.append(c)
                    
                    
                if g.cursorXTile == g.cursorSelectedTile[0] and g.cursorYTile == g.cursorSelectedTile[1]:
                    g.cursorRound+=1
                else:
                    g.cursorRound=0
                if len(found)<g.cursorRound+1:
                    g.cursorRound=-1
                elif len(found)>0:
                    if g.cursorTarget is not None and g.cursorTarget.name == found[g.cursorRound].name:
                        g.cursorTarget=None
                        g.cursorRound=-1
                        g.cursorSelectedTile =[-1,-1]
                    else:
                        g.cursorTarget = found[g.cursorRound]
                        self.graphics.initSelectWindow()
                        removeTarget=False
                if removeTarget:
                    g.cursorTarget=None
                if g.cursorTarget is None and g.cursorXTile == g.cursorSelectedTile[0] and g.cursorYTile == g.cursorSelectedTile[1]:
                    g.cursorSelectedTile =[-1,-1]
                elif g.cursorRound!=-1:
                    g.cursorSelectedTile =[g.cursorXTile,g.cursorYTile]
                
    def mouseRelease(self,x,y,button,modifiers):
        g.screen.set_mouse_cursor(g.cursorUp)
        g.cursorTile = 0
    def my_key_release(self,symbol,modifiers):
        if g.gameState == GAMESTATE_INGAME:
            if (self.graphics.chat.chatInput.focused or (self.graphics.reportWindow is not None and self.graphics.reportWindow.reportInput.focused) or (self.graphics.reportAnswerWindow is not None and self.graphics.reportAnswerWindow.reportInput.focused)) and g.chatFocus is not True:
                g.chatFocus = True
            elif self.graphics.chat.chatInput.focused == False and (self.graphics.reportWindow is None or (self.graphics.reportWindow is not None and self.graphics.reportWindow.reportInput.focused == False)) and (self.graphics.reportAnswerWindow is None or (self.graphics.reportAnswerWindow is not None and self.graphics.reportAnswerWindow.reportInput.focused == False)) and g.chatFocus == True:
                g.chatFocus = False
            if not g.chatFocus and not g.popupWindowOpened:
                toMove=False
                pressedKey = None
                for i in self.checkPressed:
                    if symbol == i[0]:
                        del self.checkPressed[self.checkPressed.index(i)]
                for i in self.checkPressed:
                    if pyglet.window.key.A == i[0] or pyglet.window.key.W == i[0] or pyglet.window.key.D == i[0] or pyglet.window.key.S == i[0]:
                        toMove = True
                        pressedKey = i[0]
                if not toMove and (symbol == pyglet.window.key.A or symbol == pyglet.window.key.S or  symbol == pyglet.window.key.W or  symbol == pyglet.window.key.D):
                    stopMove()
                if pressedKey is not None:
                    if pressedKey == pyglet.window.key.A:
                        sendMove(DIR_LEFT)
                    elif pressedKey == pyglet.window.key.W:
                        sendMove(DIR_UP)
                    elif pressedKey == pyglet.window.key.D:
                        sendMove(DIR_RIGHT)
                    elif pressedKey == pyglet.window.key.S:
                        sendMove(DIR_DOWN)
            
    def my_key_press(self,symbol,modifiers):
        if g.gameState == GAMESTATE_LOGIN:
            if symbol==pyglet.window.key.ENTER:
                self.loginMenu.tryLogin(None)
            elif symbol==pyglet.window.key.TAB:
                if modifiers==0:
                    if self.loginMenu.logininput.focused:
                        self.loginMenu.man1.set_focus(self.loginMenu.passwordinput)
                    elif self.loginMenu.passwordinput.focused:
                        self.loginMenu.man1.set_focus(self.loginMenu.button)
                elif modifiers==1:
                    if self.loginMenu.passwordinput.focused:
                        self.loginMenu.man1.set_focus(self.loginMenu.logininput)
                    elif self.loginMenu.button.focused:
                        self.loginMenu.man1.set_focus(self.loginMenu.passwordinput)
        elif symbol not in (i[0] for i in self.checkPressed) and (g.gameState == GAMESTATE_INGAME or g.gameState == GAMESTATE_FIGHTING):
            #if symbol==pyglet.window.key.T:
            #    self.graphics.initPartyWindow()
            if symbol==pyglet.window.key.ENTER:
                if self.graphics.chat.chatInput.focused:
                    self.graphics.chat.sendMessage(None)
                else:
                    self.graphics.chat.set_focus(self.graphics.chat.chatInput)
                    if g.chatting != None:
                        self.graphics.chat.chatInput.set_text(g.chatting)
                        #self.graphics.chat.chatInput.set_text("/w " + g.whisperingTo + " ")
                    self.checkPressed[:]=[]
                    stopMove()
            elif symbol==pyglet.window.key.ESCAPE:
                if g.talkingToNpc is not None:
                    sendStopTalkToNpc(npcList[g.talkingToNpc].name)
                    stopMove()
                elif g.escWindowOpened:
                    g.escWindowOpened=False
                    self.graphics.escWindow.delete(None)
                elif g.popupWindow is not None:
                    g.popupWindow.delete()
                elif g.npcTalkWindowOpened:
                    self.graphics.npcTalkWindow.delete(None)
                elif g.selectWindowOpened:
                    self.graphics.selectWindow.delete(None)
                elif g.selectedWindowOpened:
                    self.graphics.selectedWindow.delete(None)
                elif g.friendWindowOpened:
                    self.graphics.friendWindow.delete(None)
                elif g.ignoreWindowOpened:
                    self.graphics.ignoreWindow.delete(None)
                elif g.guildWindowOpened:
                    self.graphics.guildWindow.delete(None)
                elif g.reportAnswerWindowOpened:
                    g.gameEngine.graphics.reportAnswerWindow.delete(None)
                elif g.adminWindowOpened:
                    self.graphics.adminWindow.delete(None)
                elif g.meneWindowOpened:
                    g.gameEngine.graphics.meneWindow.delete(None)
                elif g.postWindowOpened:
                    g.gameEngine.graphics.postWindow.delete(None)
                elif g.selectMeneWindowOpened and g.gameEngine.fightScreen.meneSelector.closeButton:
                    g.gameEngine.fightScreen.meneSelector.delete()
                else:
                    if g.settingsWindowOpened:
                        g.settingsWindowOpened=False
                        self.graphics.settingsWindow.delete(None)
                    elif g.gameSettingsWindowOpened:
                        g.gameSettingsWindowOpened=False
                        self.graphics.gameSettingsWindow.delete(None)
                    elif g.reportWindowOpened:
                        self.graphics.reportWindow.delete(None)
                    elif g.keybindingsWindowOpened:
                        self.graphics.keybindingsWindow.delete(None)
                    
                    g.escWindowOpened=True
                    self.graphics.initEscWindow()
                return True
            if (self.graphics.chat.chatInput.focused or (self.graphics.reportWindow is not None and self.graphics.reportWindow.reportInput.focused) or (self.graphics.reportAnswerWindow is not None and self.graphics.reportAnswerWindow.reportInput.focused) or (g.gameState == GAMESTATE_FIGHTING and self.fightScreen.meneMan is not None and self.fightScreen.nameInput.focused)) and g.chatFocus is not True:
                g.chatFocus = True
            elif self.graphics.chat.chatInput.focused == False and (self.graphics.reportWindow is None or (self.graphics.reportWindow is not None and self.graphics.reportWindow.reportInput.focused == False)) and (self.graphics.reportAnswerWindow is None or (self.graphics.reportAnswerWindow is not None and self.graphics.reportAnswerWindow.reportInput.focused == False)) and (self.fightScreen.meneMan is None or (self.fightScreen.meneMan is not None and self.fightScreen.nameInput.focused==False)) and g.chatFocus == True:
                g.chatFocus = False
            if g.chatFocus == False and not g.popupWindowOpened:
                self.checkPressed.append([symbol,g.currTick])
                if symbol==pyglet.window.key.A:
                    sendMove(DIR_LEFT)
                elif symbol==pyglet.window.key.W:
                    sendMove(DIR_UP)
                elif symbol==pyglet.window.key.D:
                    sendMove(DIR_RIGHT)
                elif symbol==pyglet.window.key.S:
                    sendMove(DIR_DOWN)
                elif symbol==pyglet.window.key.O:
                    if g.friendWindowOpened:
                        self.graphics.closeAllWindows()
                    else:
                        self.graphics.initFriendWindow()
                elif symbol==pyglet.window.key.I:
                    if g.ignoreWindowOpened:
                        self.graphics.closeAllWindows()
                    else:
                        self.graphics.initIgnoreWindow()
                elif symbol==pyglet.window.key.P and myPlayer.access>0:
                    if g.adminWindowOpened:
                        self.graphics.closeAllWindows()
                    else:
                        self.graphics.initAdminWindow()
                elif symbol==pyglet.window.key.L:
                    if g.meneWindowOpened:
                        self.graphics.closeAllWindows()
                    else:
                        self.graphics.initMeneWindow()
                elif symbol==pyglet.window.key.G:
                    if g.guildWindowOpened:
                        self.graphics.closeAllWindows()
                    else:
                        self.graphics.initGuildWindow()
                elif symbol==pyglet.window.key.F12:
                    self.screenshotting=True
        if g.gameState==GAMESTATE_FIGHTING and not g.chatFocus:
            if symbol==pyglet.window.key._1:
                try:
                    self.fightScreen.abilityButtons.abilityCont.content[0].on_mouse_press(0,0, 1, 0)
                except Exception, e:    
                    print Exception, e
            elif symbol==pyglet.window.key._2:
                try:
                    self.fightScreen.abilityButtons.abilityCont.content[1].on_mouse_press(0,0, 1, 0)
                except Exception, e:    
                    print Exception, e
            elif symbol==pyglet.window.key._3:
                try:
                    self.fightScreen.abilityButtons.abilityCont.content[2].on_mouse_press(0,0, 1, 0)
                except Exception, e:    
                    print Exception, e
            elif symbol==pyglet.window.key._4:
                try:
                    self.fightScreen.abilityButtons.abilityCont.content[3].on_mouse_press(0,0, 1, 0)
                except Exception, e:    
                    print Exception, e
            
    def gameLoop(self):
        #tmpTime=time.time()
        g.screen.clear()
        g.screen.dispatch_events()
        #print g.gameState
        g.currTick = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
        tick= int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds())
        if tick==self.lastTick:
            self.fpsTick+=1
        elif tick>self.lastTick:
            self.lastTick = tick
            if g.gameState == GAMESTATE_INGAME or g.gameState==GAMESTATE_FIGHTING:
                sendLatencyTick()
            self.fpsTick=1
            #print Players
        #print 1000/(g.currTick-g.lastTick)
        #g.curFPS=1000/(test-self.fps)
        if g.screen.has_exit:
            reactor.stop()
        if g.gameState == GAMESTATE_LOGIN or g.gameState == GAMESTATE_AUTH:
            if self.loginMenu.changing:
                self.loginMenu.charSprite = loadPlayerSprites(myPlayer,self.graphics.spriteSheets,createChar=True)
                self.loginMenu.changing=False
            elif self.loginMenu.ready:
                sendCreateCharacter()
                self.loginMenu.ready=False
            elif self.loginMenu.naming and self.loginMenu.menename != "":
                meneNameConfirm(self.loginMenu.menename)
                self.loginMenu.menename=""
                self.loginMenu.nameInput.set_text("")
            self.loginMenu.update()
            #if self.loginMenu.loadedMap:
            #    changeGameState(GAMESTATE_INGAME)
        elif g.gameState == GAMESTATE_INGAME:
            self.graphics.update()
        elif g.gameState == GAMESTATE_LOADING_FIGHTING:
            self.graphics.update()
            if not self.fightStartAnimation.finished:
                self.fightStartAnimation.update()
            else:
                self.fightStartAnimation.finished=False
                changeGameState(GAMESTATE_FIGHTING)
        elif g.gameState == GAMESTATE_FIGHTING:
            self.fightScreen.update()
        #elif g.gameState == GAMESTATE_CREATECHAR:
        #    print "moi"
        elif g.gameState == GAMESTATE_EXIT:
            reactor.stop()
        #g.alertBatch.draw()
        if g.showFps:
            self.fpsDisplay.draw()
        g.screen.flip()
        if self.screenshotting:
            saveScreenshot()
            self.screenshotting=False
        if g.MUSIC and (g.fadingOut or g.fadingIn):
            if g.fadingOut:
                volume = g.MUSICVOLUME - ((g.currTick-g.fadeTick)/(1000*g.fadeTime))*g.MUSICVOLUME
            elif g.fadingIn:
                volume = ((g.currTick-g.fadeTick)/(1000*g.fadeTime))*g.MUSICVOLUME
            if volume<0:
                volume=0.0
            elif volume>g.MUSICVOLUME:
                volume=g.MUSICVOLUME
            if g.currTick > g.fadeTick+g.fadeTime*1000:
                if g.fadingOut:
                    g.fadingOut=False
                    g.fadingIn=True
                    g.fadeTick=g.currTick+g.fadeTime
                    while len(self.musicManager._groups)>1:
                        self.musicManager.next_source()
                elif g.fadingIn:
                    g.fadingIn=False
            self.musicManager.volume=volume
            #self.musicManager.volume=(g.currTick-g.fadeTick)/(g.fadeTime*)
        #print str((time.time()-tmpTime)*1000) + " ms to draw shit"
        g.lastTick=g.currTick
        
    