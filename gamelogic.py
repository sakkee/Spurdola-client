import time
import pyglet
import sys
import datetime
import json
import global_vars as g
import os
import re
import hashlib
import math
from utils import pathfinder
from constants import *
from objects import *
from PIL import Image, ImageFilter, ImageFont, ImageDraw
from pyglet.gl import *
from network.client import *
from network.packettypes import *
from gui.chatbubble import ChatBubble
from gui.popupWindow import popUpWindow
from gui.popupInput import popUpInput
from gui.popupConfirm import popUpConfirm
from gui.selectMene import MeneSelector
from templates import *


def getSmallestResolution():
    minRes=(1024,768)
    screenWidth=999999
    screenHeight=999999
    modes = pyglet.window.get_platform().get_default_display().get_default_screen().get_modes()
    for mode in modes:
        if mode.width >= minRes[0] and mode.width < screenWidth and mode.height>=minRes[1] and mode.height < screenHeight:
            screenWidth=mode.width
            screenHeight=mode.height
    g.SCREEN_WIDTH=screenWidth
    g.SCREEN_HEIGHT=screenHeight
    #print screenWidth, screenHeight
def startUpdate(arg):
    changeGameState(GAMESTATE_EXIT)
    os.startfile('Updater.exe')
def sendFightReady():
    packet = json.dumps({"p": ClientPackets.SendFightReady})
    g.tcpConn.sendData(packet)
    #if g.turn==0:
    #    g.gameEngine.fightScreen.abilityButtons.changeDisableds(True)
    #else:
    #    g.gameEngine.fightScreen.abilityButtons.changeDisableds(False)
def sendAttack(uid):
    packet = json.dumps({"p": ClientPackets.SendAttack,'id':uid})
    g.tcpConn.sendData(packet)
def relocateChat(gamestate):
    if gamestate==GAMESTATE_INGAME:
        g.gameEngine.graphics.chat.setPos(g.SCREEN_WIDTH*0.05,g.SCREEN_HEIGHT*0.1)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    elif gamestate==GAMESTATE_FIGHTING:
        g.gameEngine.graphics.chat.setPos(g.SCREEN_WIDTH*0.05,g.SCREEN_HEIGHT*0.64)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
def relocateNormalGui(gamestate):
    if gamestate==GAMESTATE_INGAME:
        g.gameEngine.graphics.normalUI.setPos(g.gameEngine.graphics.normalUI.get_position()[0],g.SCREEN_HEIGHT*0.025)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    elif gamestate==GAMESTATE_FIGHTING:
        g.gameEngine.graphics.normalUI.setPos(g.gameEngine.graphics.normalUI.get_position()[0],g.SCREEN_HEIGHT*0.975-50)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        
def iHasMene(spriteName=None):
    for mene in meneList:
        if mene.spriteName==spriteName:
            return True
    return False
    
def sendLeaveMatch(argument):
    packet = json.dumps({"p": ClientPackets.SendLeaveMatch})
    g.tcpConn.sendData(packet)
    
def openMeneSelector(argument=None,closeBtn=True):
    if g.selectMeneWindowOpened == False and g.turn == PLAYER_ONE_TURN:
        g.gameEngine.fightScreen.meneSelector = MeneSelector(closeBtn)
    elif g.selectMeneWindowOpened:
        g.gameEngine.fightScreen.meneSelector.delete()
def leaveMatchStartConfirm(argument):
    if g.popupWindow is None and g.turn==PLAYER_ONE_TURN:
        popUpConfirm(WARNINGS["LEAVE_MATCH"][0],on_ok=sendLeaveMatch)
def makeDefaultMene(ID,openMeneWindow=True):
    isAliveAndFound=False
    for mene in meneList:
        if mene.ID == ID and mene.hp>0:
            isAliveAndFound=True
            mene.defaultMene=1
        elif mene.defaultMene==1:
            mene.defaultMene=2
    if isAliveAndFound:
        for mene in meneList:
            if mene.ID == ID:
                mene.defaultMene=1
            elif mene.defaultMene==1:
                mene.defaultMene=2
        packet = json.dumps({"p": ClientPackets.ChangeDefaultMene,'id':ID})
        g.tcpConn.sendData(packet)
        g.gameEngine.graphics.initMeneWindow()
def sendSelectMene(meneID):
    packet = json.dumps({"p": ClientPackets.ChangeDefaultMene,'id':meneID})
    g.tcpConn.sendData(packet)
def getDefaultMene():
    for mene in meneList:
        if mene.defaultMene==1:
            return mene
    return None
def getMeneName(ID):
    for mene in meneList:
        if mene.ID==ID:
            return mene.name
    return None
def getDefaultMeneID():
    for mene in meneList:
        if mene.defaultMene==1:
            return mene.ID
def getDefaultMeneName():
    for mene in meneList:
        if mene.defaultMene==1:
            return mene.name
def getMemberListIndex(name):
    for i in range(len(guildList)):
        if guildList[i][0]==name:
            return i
    return None
def cancelPartyInvite(event):
    packet = json.dumps({"p": ClientPackets.RespondPartyInvite,'r':False})
    g.tcpConn.sendData(packet)
def acceptPartyInvite(event):
    packet = json.dumps({"p": ClientPackets.RespondPartyInvite,'r':True})
    g.tcpConn.sendData(packet)
def cancelGuildInvite(event):
    packet = json.dumps({"p": ClientPackets.RespondGuildInvite,'r':False})
    g.tcpConn.sendData(packet)
def acceptGuildInvite(event):
    packet = json.dumps({"p": ClientPackets.RespondGuildInvite,'r':True})
    g.tcpConn.sendData(packet)
#def openSettingsGuild(event):
#    print "poo"
def invitePlayerGuildPopup(event):
    popUpInput("Enter name of player to invite:",on_ok=invitePlayer)
    
def invitePlayer(text):
    sendChatMsg('/guildinvite ' + text)
def addIgnorePopup(event):
    popUpInput("Enter name of player to ignore:",on_ok=addIgnore)
def addFriendPopup(event):
    popUpInput("Enter name of friend to add:",on_ok=addFriend)
    #closeSelectWindow(None)
def isFriendOnline(text):
    for friend in friendList:
        if friend[0]==text and friend[1]==1:
            return True
    return False
def talkNPC(text):
    checkNpcDistance(text)
    closeSelectWindow(None)
def whisper(text):
    g.gameEngine.graphics.chat.set_focus(g.gameEngine.graphics.chat.chatInput)
    g.gameEngine.graphics.chat.chatInput.set_text("/w " + text + " ")
    closeSelectWindow(None)
def closeSelectWindow(event):
    g.gameEngine.graphics.selectedWindow.delete(None)
def kickPlayer(text):
    sendChatMsg('/guildkick ' + text)
    closeSelectWindow(None)
def promotePlayer(text):
    sendChatMsg('/guildpromote ' + text)
    closeSelectWindow(None)
def demotePlayer(text):
    sendChatMsg('/guilddemote ' + text)
    closeSelectWindow(None)
def addFriend(text):
    sendChatMsg('/friend ' + text)
    if g.selectedWindowOpened:
        closeSelectWindow(None)
def leaveParty(text):
    sendChatMsg('/leaveparty')
    closeSelectWindow(None)
def kickFromParty(text):
    sendChatMsg('/kick ' + text)
    closeSelectWindow(None)
def inviteToParty(text):
    sendChatMsg('/invite ' + text)
    closeSelectWindow(None)
def removeFriend(text):
    sendChatMsg('/unfriend ' + text)
    closeSelectWindow(None)
def removeIgnore(text):
    sendChatMsg('/unignore ' + text)
    closeSelectWindow(None)
def addIgnore(text):
    sendChatMsg('/ignore ' + text)
    closeSelectWindow(None)
def special_match(strg, search=re.compile(r'[^a-zA-Z0-9 -]').search):
    if bool(search(strg)):
        if strg==u'\xe4' or strg==u'\xc4' or strg==u'\xf6' or strg==u'\xd6' or strg==u"'":
            return True
        return False
    return True
def sendLeaveGuild():
    packet = json.dumps({"p": ClientPackets.LeaveGuild})
    g.tcpConn.sendData(packet)
def createGuild(event):
    packet = json.dumps({"p": ClientPackets.CreateGuild,'guildname':g.tmpName})
    g.tcpConn.sendData(packet)
def deleteMail(mid):
    packet = json.dumps({"p": ClientPackets.DeleteMail,'id':mid})
    g.tcpConn.sendData(packet)
def solveReport(rid,text="",remove=False):
    if rid is not None and rid!=None:
        packet = json.dumps({"p": ClientPackets.SolveReport,'id':rid,'text':text,'r':remove})
        g.tcpConn.sendData(packet)
        
def useES(arg):
    if g.esAmount<1:
        return
    packet = json.dumps({"p": ClientPackets.ThrowES})
    g.tcpConn.sendData(packet)
def getReport(admin=False):
    packet = json.dumps({"p": ClientPackets.GetReport,'a':admin})
    g.tcpConn.sendData(packet)
def sendReport(text):
    packet = json.dumps({"p": ClientPackets.SendReport,"r":text})
    g.tcpConn.sendData(packet)
def getAbilityTypeName(type):
    if type==ABILITYTYPE_ATTACK:
        return "Attack"
    elif type==ABILITYTYPE_HEAL:
        return "Heal"
def onHover(stuff=None,argument=False,x=None,y=None,hoveringType=None):
    if argument:
        g.hoveringType=hoveringType
        g.gameEngine.graphics.initHoverWindow(stuff,x,y)
        #if hoveringType==HOVERING_PING:
        #    g.gameEngine.graphics.hoverWindow.updateContent(pingHoverTemplate(g.latency))
        #elif hoveringType==HOVERING_ABILITY:
        #    g.gameEngine.graphics.hoverWindow.updateContent(abilityHoverTemplate())

        if hoveringType == HOVERING_ITEM:
            y = y-g.gameEngine.graphics.hoverWindow.height/2
            g.gameEngine.graphics.hoverWindow.setPos(x,y-g.gameEngine.graphics.hoverWindow.height/2)
        else:
            if g.gameState==GAMESTATE_FIGHTING and hoveringType != HOVERING_ABILITY:
                y=y-g.gameEngine.graphics.hoverWindow.height
            x = x-g.gameEngine.graphics.hoverWindow.width/2
        if x<0:
            x=0
        if y<0:
            y=g.SCREEN_HEIGHT
        if x+g.gameEngine.graphics.hoverWindow.width>g.SCREEN_WIDTH:
            x = g.SCREEN_WIDTH - g.gameEngine.graphics.hoverWindow.width
        if y+g.gameEngine.graphics.hoverWindow.height>g.SCREEN_HEIGHT:
            y=g.SCREEN_HEIGHT-g.gameEngine.graphics.hoverWindow.height
        g.gameEngine.graphics.hoverWindow.setPos(x,y)
    elif x is None and y is None:
        g.hoveringType=None
        g.gameEngine.graphics.hoverWindow.delete(None)
    else:
        g.gameEngine.graphics.hoverWindow.setPos(x-g.gameEngine.graphics.hoverWindow.width/2,y)
        
def meneNameConfirmFight(menename1):
    menename = ''.join(char for char in menename1 if special_match(char))
    if len(menename)>12 or len(menename)<1:
        popUpWindow(WARNINGS["INVALID_MENE_NAME"][0] % (menename))
        return
    popUpConfirm(WARNINGS["YOUR_MENE_NAME"][0] % (menename),on_ok=sendMeneNameConfirm,argument=menename)
def meneNameConfirm(menename1):
    menename = ''.join(char for char in menename1 if special_match(char))
    g.gameEngine.loginMenu.saveBtn.disabled = False
    for c in meneList:
        if menename==c.name:
            popUpWindow("You already have a mene named " + menename + "!")
            return
    if len(menename)>12 or len(menename)<1:
        popUpWindow(WARNINGS["INVALID_MENE_NAME"][0] % (menename))
        return
    popUpConfirm(WARNINGS["YOUR_MENE_NAME"][0] % (menename),on_ok=sendMeneNameConfirm,argument=menename)

def sendMeneNameConfirm(menename):
    packet = json.dumps({"p": ClientPackets.SendMeneNameConfirm,"n":menename})
    g.tcpConn.sendData(packet)
    if g.gameState == GAMESTATE_FIGHTING:
        g.gameEngine.fightScreen.fightOver=False
        g.gameEngine.changeMusicSong(Map.song,fadetime=0.1)
        changeGameState(GAMESTATE_INGAME)
def constructText(text,fontClr,name=None,nameColor=None,adminText=None,whisperText=''):
    t1=time.time()*1000
    msg=''
    msg1=None
    msg2=None
    if name is not None:
        if adminText is not None:
            msg='{color '+str(nameColor)+'}{bold True}'+name
            msg1='{bold False} ' + adminText
            msg2=': '
        else:
            msg='{color '+str(nameColor)+'}{bold True}'+whisperText+name+': '
            
    message = '\n\n'+msg
    duplicates = set('{}')
    newmsg = "".join(char*2 if char in duplicates else char for char in text)
    secondMessage='{bold False}{color '+str(fontClr)+'}'+newmsg
    formatted = pyglet.text.decode_attributed(message)
    g.gameEngine.graphics.chat.addText(pyglet.text.decode_attributed(message))
    if msg1 is not None:
        g.gameEngine.graphics.chat.addText(pyglet.text.decode_attributed(msg1))
    if msg2 is not None:
        g.gameEngine.graphics.chat.addText(pyglet.text.decode_attributed(msg2))
    
    g.gameEngine.graphics.chat.addText(pyglet.text.decode_attributed(secondMessage))
    
    #if len(g.gameEngine.graphics.chat.textArea.get_text())>200:
    #        g.gameEngine.graphics.chat.textArea._document.delete_text(0,5)
    #print len(g.gameEngine.graphics.chat.textArea.get_text())
    g.chatLog.append(len(g.gameEngine.graphics.chat.textArea._document.text)-g.chatLogLength)
    #print g.gameEngine.graphics.chat.textArea._document.text
    #print g.chatLog
    g.chatLogLength+=g.chatLog[-1]
    checkChatLogLength()
    g.gameEngine.graphics.chat.textArea.compute_size()
    g.gameEngine.graphics.chat.textArea.layout()
def checkChatLogLength():
    if g.chatLogLength>MAXCHATLOGLENGTH:
        if not g.chatDeleteCheck:
            g.chatLog[0]+=1
            g.chatDeleteCheck=True
        g.gameEngine.graphics.chat.textArea._document.delete_text(0,g.chatLog[0])
        g.chatLogLength-=g.chatLog[0]
        del g.chatLog[0]
def sendCreateCharacter():
    packet = json.dumps({"p": ClientPackets.SendCreateChar,"sh":myPlayer.shirt,'s':myPlayer.shoes,'f':myPlayer.face,'h':myPlayer.hat})
    g.tcpConn.sendData(packet)
def infoText(text):
    constructText(text,g.helpColor)
def isIgnored(name):
    for c in ignoreList:
        if c==name:
            return True
    return False
    
def getMeneListIndex(ID):
    for i in xrange(len(meneList)):
        if meneList[i].ID==ID:
            return i
    return None
def isFriend(name):
    print friendList,name
    for c in friendList:
        if c[0] == name:
            return True
    return False
def distance(x1,y1,x2,y2):
    return abs(x2-x1)+abs(y2-y1)
def sendStopTalkToNpc(name):
    packet = json.dumps({"p": ClientPackets.StopTalkWithNPC,"n":name})
    g.tcpConn.sendData(packet)
    
    if g.npcTalkWindowOpened:
        g.gameEngine.graphics.npcTalkWindow.delete(None)
    else:
        g.talkingToNpc=None
        
def buyItem(item):
    packet = json.dumps({"p": ClientPackets.SendBuyItem, 'i':item})
    g.tcpConn.sendData(packet)
def sendHealMenes():
    packet = json.dumps({"p": ClientPackets.SendHealMenes})
    g.tcpConn.sendData(packet)
def sendTalkToNpc(name):
    packet = json.dumps({"p": ClientPackets.TalkWithNPC,"n":name})
    g.tcpConn.sendData(packet)
def checkNpcDistance(name,reCheck=False):
    
    i=findNpcIndex(name)
    if i!=-1:
        dist= distance(myPlayer.x,myPlayer.y,npcList[i].x,npcList[i].y)
        if dist<=MAX_NPC_TALK_DISTANCE:
            openNpcTalk(name)
        else:
            if not reCheck:
                sendTalkToNpc(name)
            sendMoveTarget(npcList[i].x,npcList[i].y,npc=True,dir=npcList[i].dir)
        g.talkingToNpc=findNpcIndex(name)
def openNpcTalk(name):
    i=findNpcIndex(name)
    if i!=-1:
        g.gameEngine.graphics.initNpcTalkWindow(npcList[i].name,npcList[i].text,npcList[i].actionType)
        #print npcList[i].text
def sendLatencyTick():
    g.latencyTick = time.time()
    packet = json.dumps({"p": ClientPackets.LatencyTick})
    g.tcpConn.sendData(packet)
def updateUi():
    g.chatReloaded=True
    if int(g.SCREENSELECTED)<len(pyglet.window.get_platform().get_default_display().get_screens()) and int(g.SCREENSELECTED)>=0:
        defaultMonitor = pyglet.window.get_platform().get_default_display().get_screens()[int(g.SCREENSELECTED)]
    else:
        defaultMonitor = pyglet.window.get_platform().get_default_display().get_default_screen()
    g.screen.set_fullscreen(fullscreen=g.FULLSCREEN,width=g.SCREEN_WIDTH,height=g.SCREEN_HEIGHT,screen=defaultMonitor)
    g.screen.set_vsync(g.VSYNC)
    g.gameEngine.graphics.normalUI.delete()
    g.gameEngine.graphics.chat.delete()
    del g.gameEngine.graphics.chat
    
    g.gameEngine.graphics.initGraphics()
    if g.npcTalkWindowOpened:
        g.gameEngine.graphics.npcTalkWindow.delete(None)
    if g.friendWindowOpened:
        g.gameEngine.graphics.friendWindow.delete(None)
    if g.ignoreWindowOpened:
        g.gameEngine.graphics.ignoreWindow.delete(None)
    if g.meneWindowOpened:
        g.gameEngine.graphics.meneWindow.delete(None)
    if g.gameSettingsWindowOpened:
        g.gameEngine.graphics.gameSettingsWindow.delete(None)
    if g.reportWindowOpened:
        g.gameEngine.graphics.reportWindow.delete(None)
    if g.reportAnswerWindowOpened:
        g.gameEngine.graphics.reportAnswerWindow.delete(None)
    if g.guildWindowOpened:
        g.gameEngine.graphics.guildWindow.delete(None)
    if g.postWindowOpened:
        g.gameEngine.graphics.postWindow.delete(None)
    relocateChat(g.gameState)
    relocateNormalGui(g.gameState)
    g.gameEngine.fightScreen.updatePositions()

def handleChatBubble(player,message,a=0):
    player.tmpPlayer.lastMsgTick = g.currTick
    if player.tmpPlayer.lastMsg is not None:
        player.tmpPlayer.lastMsg.delete()
        player.tmpPlayer.lastMsg=None
    player.tmpPlayer.lastMsg = ChatBubble(player.name,message,a)
    if player.name == myPlayer.name:
        posx=int((g.SCREEN_WIDTH-player.tmpPlayer.lastMsg._content[0].width)/2)
        posy=int((g.SCREEN_HEIGHT+TILESIZE)/2+TILESIZE/16)
    else:
        posx = int((player.x-myPlayer.x)*TILESIZE+(g.SCREEN_WIDTH-TILESIZE)/2+player.tmpPlayer.xOffset+myPlayer.tmpPlayer.xOffset-player.tmpPlayer.lastMsg._content[0].width/2+TILESIZE/2)
        posy = int((-player.y+myPlayer.y)*TILESIZE+(g.SCREEN_HEIGHT-TILESIZE)/2+player.tmpPlayer.yOffset+myPlayer.tmpPlayer.yOffset+TILESIZE/16*17)
    player.tmpPlayer.lastMsg.setPos(posx,posy)
    if len(message)<MAX_CHAT_INPUT/3:
        player.tmpPlayer.chatBubbleTime = CHAT_SHORTMSG_TIME
    elif len(message)<MAX_CHAT_INPUT/3*2:
        player.tmpPlayer.chatBubbleTime = CHAT_NORMALMSG_TIME
    else:
        player.tmpPlayer.chatBubbleTime = CHAT_LONGMSG_TIME
def saveScreenshot():
    string= str(long(time.time()*1000)) +'.png'
    pyglet.image.get_buffer_manager().get_color_buffer().save('screenshots/'+string)
def findMap(mapName, md5):
    if os.path.exists(g.dataPath + '/maps/'+mapName+'.map'):
        BLOCKSIZE = 65536
        hasher = hashlib.md5()
        with open(g.dataPath + '/maps/'+mapName+'.map', 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        if md5 == hasher.hexdigest():
            return True
    return False
def sendChatMsg(text):
    if len(text)>3 and text[:4]=='/fps':
        if g.showFps:
            g.showFps=False
        else:
            g.showFps=True
    elif len(text)>8 and text[:9]=='/reloadui':
        updateUi()
    elif len(text)==6 and text[:6]=='/admin':
        if myPlayer.access!=0:
            g.gameEngine.graphics.initAdminWindow()
        else:
            constructText('You are not an admin ;_;',g.errorColor)
            #g.chatLog+= '\n{background_color '+str(g.postBgColor)+'}{color '+str(g.errorColor)+'}You are not an admin :(\n' 
            #checkChatLogLength()
            #g.gameEngine.graphics.chat.textArea.update_text(g.chatLog)
    else:
        if len(text)>3 and text[:3]=='/w ':
            g.chatting = '/w '
        elif len(text)>3 and text[:3]=='/g ':
            g.chatting='/g '
        elif len(text)>3 and text[:3]=='/p ':
            g.chatting='/p '
        else:
            g.chatting=''
            #g.whisperingTo = None
        packet = json.dumps({"p": ClientPackets.SendMessage, "m":text})
        g.tcpConn.sendData(packet)
def changeGameState(gamestate):
    #print g.gameState, GAMESTATE_LOGIN, g.gameEngine.loginMenu.charSprite, g.gameEngine.loginMenu.naming
    if g.gameState == GAMESTATE_LOGIN:
        #g.gameState=GAMESTATE_LOADING
        if g.gameEngine.loginMenu.charSprite is None:
            if g.gameEngine.loginMenu.naming:
                g.gameEngine.loginMenu.removeMenenaming()
            else:
                g.gameEngine.loginMenu.removeManagers()
        else:
            g.gameEngine.loginMenu.removeCharCreating()
        if gamestate == GAMESTATE_INGAME:
            g.gameEngine.graphics.SetupMap()
            g.gameEngine.graphics.initGraphics()
    elif g.gameState == GAMESTATE_AUTH:
        if gamestate == GAMESTATE_INGAME:
            g.gameEngine.graphics.SetupMap()
            g.gameEngine.graphics.initGraphics()
    elif g.gameState == GAMESTATE_INGAME or g.gameState==GAMESTATE_LOADING_FIGHTING:
        if gamestate==GAMESTATE_LOGIN:
            g.gameEngine.graphics.normalUI.delete()
            g.gameEngine.graphics.chat.delete()
            g.gameEngine.graphics.clearGraphics()
            if g.escWindowOpened:
                g.gameEngine.graphics.escWindow.delete(None)
                g.escWindowOpened=False
            if g.settingsWindowOpened:
                g.gameEngine.graphics.settingsWindow.delete(None)
                g.settingsWindowOpened=False
            if g.friendWindowOpened:
                g.gameEngine.graphics.friendWindow.delete(None)
            if g.ignoreWindowOpened:
                g.gameEngine.graphics.ignoreWindow.delete(None)
            if g.selectWindowOpened:
                g.gameEngine.graphics.selectWindow.delete(None)
            if g.hoveringType is not None:
                g.gameEngine.graphics.hoverWindow.delete(None)
            if g.npcTalkWindowOpened:
                g.gameEngine.graphics.npcTalkWindow.delete(None)
            if g.gameSettingsWindowOpened:
                g.gameEngine.graphics.gameSettingsWindow.delete(None)
            if g.adminWindowOpened:
                g.gameEngine.graphics.adminWindow.delete(None)
            if g.meneWindowOpened:
                g.gameEngine.graphics.meneWindow.delete(None)
            if g.reportWindowOpened:
                g.gameEngine.graphics.reportWindow.delete(None)
            if g.reportAnswerWindowOpened:
                g.gameEngine.graphics.reportAnswerWindow.delete(None)
            if g.guildWindowOpened:
                g.gameEngine.graphics.guildWindow.delete(None)
            if g.postWindowOpened:
                g.gameEngine.graphics.postWindow.delete(None)
            g.gameEngine.graphics.deletePartyWindow()
            g.partyMembers[:]=[]
            meneList[:]=[]
            guildList[:]=[]
            g.guildName=None
            g.chatLog[:]=[]
            g.gameEngine.loginMenu.initManagers()
    elif g.gameState==GAMESTATE_FIGHTING and gamestate!=GAMESTATE_FIGHTING:
        g.gameEngine.fightScreen.abilityButtons.delete()
        g.gameEngine.fightScreen.mene1Manager.delete()
        g.gameEngine.fightScreen.mene2Manager.delete()
        if g.gameEngine.fightScreen.meneMan is not None:
            g.gameEngine.fightScreen.meneMan.delete()
        if g.gameEngine.fightScreen.xpBarMan is not None:
            g.gameEngine.fightScreen.xpBarMan.delete()
        if g.selectMeneWindowOpened:
            g.gameEngine.fightScreen.meneSelector.delete()
        if gamestate==GAMESTATE_LOGIN:
            g.gameEngine.graphics.chat.delete()
            g.gameEngine.graphics.clearGraphics()
            g.gameEngine.graphics.normalUI.delete()
            g.gameEngine.graphics.closeAllWindows()
            if g.escWindowOpened:
                g.gameEngine.graphics.escWindow.delete(None)
                g.escWindowOpened=False
            if g.settingsWindowOpened:
                g.gameEngine.graphics.settingsWindow.delete(None)
                g.settingsWindowOpened=False
            if g.selectWindowOpened:
                g.gameEngine.graphics.selectWindow.delete(None)
            if g.gameSettingsWindowOpened:
                g.gameEngine.graphics.gameSettingsWindow.delete(None)
            g.gameEngine.graphics.deletePartyWindow()
            g.partyMembers[:]=[]
            meneList[:]=[]
            guildList[:]=[]
            g.guildName=None
            g.chatLog[:]=[]
            g.gameEngine.loginMenu.initManagers()
        
    if gamestate == GAMESTATE_CREATECHAR:
        g.gameEngine.loginMenu.initCreateChar()
        gamestate = GAMESTATE_LOGIN
    elif gamestate == GAMESTATE_NAMEMENE:
        g.gameEngine.loginMenu.initNameMene()
        gamestate = GAMESTATE_LOGIN
    elif gamestate == GAMESTATE_LOADING_FIGHTING:
        g.gameEngine.checkPressed[:]=[]
        g.gameEngine.fightStartAnimation.icon.set_position((g.SCREEN_WIDTH-163)/2,(g.SCREEN_HEIGHT-165)/2)
        g.gameEngine.changeMusicSong(g.gameEngine.fightScreen.fightMusic,fadetime=0.1,loaded=True)
        g.gameEngine.fightStartAnimation.initStartTick()
    elif gamestate == GAMESTATE_FIGHTING:
        g.gameEngine.graphics.closeHoverWindow()
        g.gameEngine.fightScreen.startScreen()
        relocateChat(gamestate)
        relocateNormalGui(gamestate)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)  
    elif gamestate==GAMESTATE_INGAME:
        relocateChat(gamestate)
        relocateNormalGui(gamestate)
    g.gameState = gamestate
def sendMove(direction):
    if g.talkingToNpc is not None:
        sendStopTalkToNpc(npcList[g.talkingToNpc].name)
    pos = checkPositionChange(dir)
    if direction == myPlayer.dir and Map.tile[myPlayer.x+pos[0]][myPlayer.y+pos[1]]==TILE_TYPE_BLOCKED:
        return
    packet = json.dumps({"p": ClientPackets.SendMove, "d":direction})
    g.tcpConn.sendData(packet)

def stopMove():
    packet = json.dumps({"p": ClientPackets.StopMove})
    g.tcpConn.sendData(packet)
def initMap():
    with open(g.dataPath+'/maps/'+myPlayer.map+'.map', 'r') as fp:
        tmpMap=json.load(fp)
    Map.width = tmpMap["width"]
    Map.height = tmpMap["height"]
    Map.song = tmpMap["song"]
    Map.menes = tmpMap["menes"]
    Map.tile = [[TileClass() for i in xrange(tmpMap["height"])] for i in xrange(tmpMap["width"])]
    tmpTiles = []
    for x in xrange(tmpMap["width"]):
        tmpTilesW=[]
        for y in xrange(tmpMap["height"]):
            tmpTile = TileClass()
            tmpTile.l1 = tmpMap['tile'][x][y]["l1"]
            tmpTile.l2 = tmpMap['tile'][x][y]["l2"]
            tmpTile.l3 = tmpMap['tile'][x][y]["l3"]
            tmpTile.f = tmpMap['tile'][x][y]["f"]
            tmpTile.t = tmpMap['tile'][x][y]["t"]
            tmpTile.d1 = tmpMap['tile'][x][y]["d1"]
            tmpTile.d2= tmpMap['tile'][x][y]["d2"]
            tmpTile.d3 = tmpMap['tile'][x][y]["d3"]
            tmpTilesW.append(tmpTile)
        tmpTiles.append(tmpTilesW)
    Map.tile = tmpTiles
    Map.walls=None
    walls = set()
    for i in range(-1,Map.width):
        for j in(-1,Map.height):
            walls.add((i,j))
    for j in range(-1, Map.height):
        for i in (-1, Map.width):
            walls.add((i,j))
    for i in range(Map.width):
        for j in range(Map.height):
            if Map.tile[i][j].t == TILE_TYPE_BLOCKED:
                walls.add((i,j))
    Map.walls=walls
def resetFace(player):
    if player.dir == DIR_DOWN:
        player.tmpPlayer.spriteFacing = 0
    elif player.dir == DIR_UP:
        player.tmpPlayer.spriteFacing = 5
    elif player.dir == DIR_RIGHT:
        player.tmpPlayer.spriteFacing = 3
    elif player.dir == DIR_LEFT:
        player.tmpPlayer.spriteFacing = 8
def findNpcIndex(name):
    for i in xrange(len(npcList)):
        if npcList[i].name==name:
            return i
    return None
def findPlayerIndex(name):
    for i in xrange(len(Players)):
        if Players[i].name==name:
            return i
    return None
def getPointOnCircle(radius,degrees,originX,originY):
    radian = degrees * math.pi / 180.0
    x = radius * math.cos(radian) + originX
    y = radius * math.sin(radian) + originY
    return (x,y)
def handleStop(player,x,y,direction):
    pos = checkPositionChange(direction)
    if x == player.x and y == player.y:
        player.tmpPlayer.nextMoveDir = -1
        if not player.tmpPlayer.moving:
            player.dir = direction
            resetFace(player)
        player.tmpPlayer.nextDir=direction
        return

    elif pos[0] == 0 and pos[1] == 0:
        player.x=x
        player.y=y
        player.dir = direction
        player.tmpPlayer.moving=False
        resetFace(player)
    elif player.x+pos[0]==x and player.y+pos[1] == y:
        player.tmpPlayer.nextRealMove = direction
        player.tmpPlayer.nextDir=direction
    elif player.x-pos[0]==x and player.y-pos[1] == y:
        print player.x,x,player.y,y,pos,direction
        player.x=x
        player.y=y
        player.dir = direction
        player.tmpPlayer.moving=False
        resetFace(player)
    elif player.x != x or player.y != y:
        handleMove(player,direction,x=x,y=y)
        player.tmpPlayer.nextDir=direction
        player.tmpPlayer.nextRealMove = -1
    player.tmpPlayer.nextMoveDir = -1
    player.tmpPlayer.nextDir=direction
    player.tmpPlayer.movePath[:]=[]
def resetSpriteFacing(player,direction):
    if direction == DIR_DOWN:
        player.tmpPlayer.spriteFacing = 0
    elif direction == DIR_UP:
        player.tmpPlayer.spriteFacing = 5
    elif direction == DIR_LEFT:
        player.tmpPlayer.spriteFacing = 8
    elif direction == DIR_RIGHT:
        player.tmpPlayer.spriteFacing = 3
    player.dir = direction
def changeSpriteFacing(player,direction):
    if direction == DIR_DOWN:
        player.tmpPlayer.spriteFacing = 2
    elif direction == DIR_UP:
        player.tmpPlayer.spriteFacing = 7
    elif direction == DIR_LEFT:
        player.tmpPlayer.spriteFacing = 9
    elif direction == DIR_RIGHT:
        player.tmpPlayer.spriteFacing = 4
def handleMove(player,direction,x=None,y=None):
    if x is None and y is None:
        pos = checkPositionChange(direction)
        player.y+=pos[1]
        player.x+=pos[0]
    else:
        player.x=x
        player.y=y
    changeSpriteFacing(player,direction)
    player.tmpPlayer.nextMoveDir = direction
    player.dir = direction
    player.tmpPlayer.moveTick = g.currTick
    player.tmpPlayer.moving = True
    player.tmpPlayer.nextStep = False


def createNameText(text,color,guildName=None):
    t1=time.time()*1000
    font = ImageFont.truetype(g.dataPath+'/fonts/segoeuib.ttf',13+(TILE_SCALE-1)*3)
    
    img=Image.new("RGBA",(500,200),(0,0,0,0))
    draw=ImageDraw.Draw(img)
    draw.text((0,0),text,(0,0,0),font=font)
    draw.text((0,2),text,(0,0,0),font=font)
    draw.text((2,0),text,(0,0,0),font=font)
    draw.text((2,2),text,(0,0,0),font=font)
    draw.text((1,1),text,(color[0],color[1],color[2]),font=font)
    draw=ImageDraw.Draw(img)
    
    im2 = img.getbbox()
    cropped=img.crop(im2)
    cropped = cropped.transpose(Image.FLIP_TOP_BOTTOM)
    if guildName is not None:
        guildName = '<'+guildName+'>'
        font2 = ImageFont.truetype(g.dataPath+'/fonts/segoeuib.ttf',11+(TILE_SCALE-1)*3)
        img2 = Image.new("RGBA",(500,200),(0,0,0,0))
        draw2=ImageDraw.Draw(img2)
        draw2.text((0,0),guildName,(0,0,0),font=font2)
        draw2.text((0,2),guildName,(0,0,0),font=font2)
        draw2.text((2,0),guildName,(0,0,0),font=font2)
        draw2.text((2,2),guildName,(0,0,0),font=font2)
        draw2.text((1,1),guildName,(color[0],color[1],color[2]),font=font2)
        draw2=ImageDraw.Draw(img2)
        im3 = img2.getbbox()
        cropped2=img2.crop(im3)
        cropped2 = cropped2.transpose(Image.FLIP_TOP_BOTTOM)
        img_w, img_h = cropped.size
        img_w2, img_h2 = cropped2.size
        img3 = Image.new("RGBA",(max(img_w,img_w2),img_h+img_h2),(0,0,0,0))
        bg_w, bg_h = img3.size
        offset = ((bg_w - img_w) / 2, img_h2)
        img3.paste(cropped,offset)
        offset2 = ((bg_w - img_w2) / 2, 0)
        img3.paste(cropped2,offset2)
        im1 = pyglet.image.ImageData(bg_w,bg_h,'RGBA',img3.tobytes())
    else:
        im1 = pyglet.image.ImageData(cropped.size[0],cropped.size[1],'RGBA',cropped.tobytes())
    im1.anchor_x = im1.width//2
    im1.anchor_y = im1.height//2
    return im1
def loadPlayerSprites(player,spritesheets,createChar=False,partyMember=False):
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    if createChar:
        scale=4
    else:
        scale=TILE_SCALE
    img = Image.new("RGBA", (TILESHEET_WIDTH*10, TILESHEET_WIDTH), (0,0,0,0))
    
    img.paste(spritesheets[0].getTile(0,0,width=10),(0,0),spritesheets[0].getTile(0,0,width=10).convert('RGBA'))
    img.paste(spritesheets[4].getTile(0,player.shoes,width=10),(0,0),spritesheets[4].getTile(0,player.shoes,width=10).convert('RGBA'))
    img.paste(spritesheets[3].getTile(0,player.shirt,width=10),(0,0),spritesheets[3].getTile(0,player.shirt,width=10).convert('RGBA'))
    img.paste(spritesheets[1].getTile(0,player.face,width=10),(0,0),spritesheets[1].getTile(0,player.face,width=10).convert('RGBA'))
    img.paste(spritesheets[2].getTile(0,player.hat,width=10),(0,0),spritesheets[2].getTile(0,player.hat,width=10).convert('RGBA'))
    img = img.resize((TILESHEET_WIDTH*10*scale,TILESHEET_WIDTH*scale),Image.NEAREST)
    
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    if not createChar and not partyMember:
        outlineImg= Image.new("RGBA", (TILESHEET_WIDTH*10*scale, TILESHEET_WIDTH*scale), (0,0,0,0))
        test1 = img.filter(ImageFilter.FIND_EDGES)
        datas = test1.getdata()
        newData=[]
        for item in datas:
            if item[3]!=0:
                newData.append((0,255,0,255))
            else:
                newData.append((0,0,0,0))
        outlineImg.putdata(newData)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        
        r=outlineImg.tobytes()
        outlineImg = pyglet.image.ImageData(TILESHEET_WIDTH*10*scale,TILESHEET_WIDTH*scale,'RGBA',r)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        player.tmpPlayer.highlightSprite=pyglet.image.ImageGrid(outlineImg,1,10)
    raw_data = img.tobytes()
    img = pyglet.image.ImageData(TILESHEET_WIDTH*10*scale,TILESHEET_WIDTH*scale,'RGBA',raw_data)
    return pyglet.image.ImageGrid(img,1,10)

def getDirection(x1,y1,x2,y2):
    if x2>x1:
        return DIR_RIGHT
    elif x2<x1:
        return DIR_LEFT
    elif y2>y1:
        return DIR_DOWN
    else:
        return DIR_UP
def checkPositionChange(direction):
    changeX = 0
    changeY = 0
    if direction == DIR_DOWN:
        changeY = 1
    elif direction == DIR_UP:
        changeY = -1
    elif direction == DIR_LEFT:
        changeX = -1
    elif direction == DIR_RIGHT:
        changeX = 1
    return [changeX,changeY]
def sendMoveTarget(x,y,npc=False, dir=None):
    if g.talkingToNpc is not None and not npc:
        sendStopTalkToNpc(npcList[g.talkingToNpc].name)
    if x>=0 and y>=0 and x<Map.width and y<Map.height:
        if Map.tile[x][y].t == TILE_TYPE_BLOCKED:
            g.redBlockX = x
            g.redBlockY = y
            g.redBlockTick = g.currTick
            g.redBlockDisabled = 0
            return
        pather = pathfinder.Star((myPlayer.x,myPlayer.y),(x,y),"rook",Map.walls)
        needToRemove=False
        while not pather.solution:
            pather.evaluate()
        if pather.solution == "NO SOLUTION":
            needToRemove=True
            red=True
            if npc and dir is not None:
                posChange = checkPositionChange(dir)
                pather = pathfinder.Star((myPlayer.x,myPlayer.y),(x+posChange[0]*2,y+posChange[1]*2),"rook",Map.walls)
                while not pather.solution:
                    pather.evaluate()
                if pather.solution != "NO SOLUTION":
                    red=False
            if red:
                g.redBlockX = x
                g.redBlockY = y
                g.redBlockTick = g.currTick
                g.redBlockDisabled = 0
                return
        foundPath = list(reversed(pather.solution))
        g.movePath = foundPath
        if npc is True and not needToRemove:
            del g.movePath[-1]
        
        packet = json.dumps({"p": ClientPackets.PlayerMovePath, "pa":foundPath})
        g.tcpConn.sendData(packet)
def isInParty(name):
    for partymember in g.partyMembers:
        if partymember.name==name:
            return True
    return False
def sendFaceTarget(x,y):
    if x>=0 and x<Map.width and y>=0 and y<Map.height:
        packet = json.dumps({"p": ClientPackets.SendFaceTarget, "x":x,"y":y})
        g.tcpConn.sendData(packet)
def removeFromPlayerPath(player,x,y):
    for i in xrange(len(player.tmpPlayer.movePath)):
        if player.tmpPlayer.movePath[i]==[x,y]:
            del player.tmpPlayer.movePath[:i+1]
            break
def checkOffset(player):
    if player.tmpPlayer.moving:
        offset = TILESIZE - TILESIZE * (g.currTick-player.tmpPlayer.moveTick)/WALKSPEED
        if offset <= 0:
            offset = TILESIZE
            removeFromPlayerPath(player,player.x,player.y)
            player.tmpPlayer.nextStep = False
            dir = player.tmpPlayer.nextMoveDir
            if player.tmpPlayer.movePath!=[]:
                dir=getDirection(player.x,player.y,player.tmpPlayer.movePath[0][0],player.tmpPlayer.movePath[0][1])
            if player.tmpPlayer.nextRealMove != None:
                dir = player.tmpPlayer.nextRealMove
                player.tmpPlayer.nextRealMove = None
            pos = checkPositionChange(dir)
            if pos[0]+player.x<0 or pos[0]+player.x >= Map.width or pos[1]+player.y<0 or pos[1]+player.y>=Map.height or Map.tile[pos[0]+player.x][pos[1]+player.y].t == TILE_TYPE_BLOCKED:
                dir = -1
            if dir == -1:
                player.tmpPlayer.moving = False
                offset=0
                player.tmpPlayer.nextStep = True
                player.tmpPlayer.movePath[:]=[]
            if player.tmpPlayer.nextDir is not None:
                player.dir=player.tmpPlayer.nextDir
                player.tmpPlayer.nextDir=None
                player.tmpPlayer.movePath[:]=[]
            if dir != -1:
                changeSpriteFacing(player,dir)
                player.dir = dir
                player.tmpPlayer.moveTick = g.currTick
                player.x+=pos[0]
                player.y+=pos[1]
                #removeFromPlayerPath(player,player.x,player.y)
        elif offset <=TILESIZE/2 and player.tmpPlayer.nextStep is not True:
            player.tmpPlayer.spriteFacing-=1
            player.tmpPlayer.nextStep = True
        if player.dir == DIR_DOWN:
            return [0,-offset]
        elif player.dir == DIR_LEFT:
            return [-offset,0]
        elif player.dir == DIR_UP:
            return [0,offset]
        else:
            return [offset,0]
    else:
        if player.tmpPlayer.nextStep:
            resetFace(player)
            player.tmpPlayer.nextStep = False
        return [0,0]