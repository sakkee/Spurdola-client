# -*- coding: utf-8 -*- 
import time
import os.path
#from database import *
from gamelogic import *
import global_vars as g
from objects import *
from constants import *
from packettypes import *
import random
from utils.utils import *
from client import *
import base64
import datetime
from templates import *
from gui.popupWindow import popUpWindow
from gui.popupConfirm import popUpConfirm
from unidecode import unidecode
from Crypto.PublicKey import RSA
from Crypto import Random

from pyglet.gl import *
class DataHandler():
    def __init__(self,protocol=2):
        self.protocol = protocol
    def handleLoginData(self,jsonData):
        packetType = jsonData["p"]
        print jsonData
        if packetType == LoginServerPackets.AskForLoginInformation:
            g.loginRSAKey = RSA.importKey(jsonData["k"])
            username = base64.b64encode(g.gameEngine.loginMenu.username.encode('utf-8'))
            pw = base64.b64encode(g.gameEngine.loginMenu.password.encode('utf-8'))
            
            un_encrypted = base64.b64encode(g.loginRSAKey.encrypt(username,128)[0])
            pw_encrypted = base64.b64encode(g.loginRSAKey.encrypt(pw,128)[0])
            #print un_encrypted
            packet = json.dumps({"p": LoginClientPackets.SendLoginInformation, "n":un_encrypted, "pw":pw_encrypted,'v':GAME_VERSION})
            g.tcpConn.sendData(packet)
        elif packetType == LoginServerPackets.VersionOutdated:
            self.handleVersionOutdated()
        elif packetType == LoginServerPackets.LoginWrong:
            popUpWindow("Username or password wrong!")
        elif packetType == LoginServerPackets.PasswordOK:
            g.gameIP = jsonData["ip"]
            g.gamePORT = jsonData["port"]
            g.loginToken = jsonData["k"]
            #g.gameState=GAMESTATE_AUTH
            changeGameState(GAMESTATE_AUTH)
            
            g.gameEngine.initConnection()
            g.connectedToLoginServer=False
        elif packetType == LoginServerPackets.Banned:
            self.handleBan(jsonData["d"],jsonData["r"])
        elif packetType == LoginServerPackets.GameServerDown:
            self.handleGameServerDown()
            
    def handleData(self,jsonData):
        #jsonData = decodeJSON(data)
        print jsonData
        packetType = jsonData["p"]
        if packetType == ServerPackets.RequestAuth:
            packet = json.dumps({"p": ClientPackets.Login, "k":g.loginToken})
            g.tcpConn.sendData(packet)
        #elif packetType == ServerPackets.LoginOK:
        #    if int(jsonData[0]["ok"]) == 0:
        #        g.gameEngine.disconnect()
        #        #popUpWindow("Username or password wrong!")
        elif packetType == ServerPackets.SendChar:
            self.handleSendChar(jsonData)
        #elif packetType == ServerPackets.SendRequestedMap:
            
        #    self.setupMap(jsonData)
        #elif packetType == ServerPackets.MapLine:
        #    self.addToMapData(jsonData)
        elif packetType == ServerPackets.PlayerMove:
            self.handlePlayerMove(jsonData["d"],jsonData["n"])
        elif packetType == ServerPackets.PlayerMoveStop:
            self.handlePlayerMoveStop(jsonData['n'],jsonData['x'],jsonData['y'],jsonData['d'])
        elif packetType == ServerPackets.PlayerMoveNext:
            self.handlePlayerMoveNext(jsonData['n'],jsonData['d'])
        elif packetType == ServerPackets.SendPlayerConnect:
            self.handlePlayerConnect(jsonData)
        elif packetType == ServerPackets.SendCharsFromMap:
            for i in xrange(len(jsonData["pl"])):
                self.handlePlayerConnect(jsonData["pl"][i])
        elif packetType == ServerPackets.SendPlayerDisconnect:
            i = findPlayerIndex(jsonData['n'])
            if i != None:
                if g.cursorTarget is not None and Players[i].name == g.cursorTarget.name:
                    closeSelectWindow(None)
                    g.cursorTarget=None
                #Players[i].tmpPlayer.nameTextShadow[:]=[]
                if Players[i].tmpPlayer.lastMsg is not None:
                    Players[i].tmpPlayer.lastMsg.delete()
                    Players[i].tmpPlayer.lastMsg=None
                del Players[i]
        elif packetType == ServerPackets.PlayerMoveReal:
            self.handlePlayerMoveReal(jsonData['n'],jsonData['x'],jsonData['y'],jsonData['d'])
        #elif packetType == ServerPackets.PathNotFound:
        #    g.redBlockX = jsonData[0]['x']
        #    g.redBlockY = jsonData[0]['y']
        #    g.redBlockTick = g.currTick
        #    g.redBlockDisabled = 0
        elif packetType == ServerPackets.PlayerMovePath:
            if jsonData["n"]==myPlayer.name:
                myPlayer.tmpPlayer.movePath[:]=[]
                myPlayer.tmpPlayer.movePath=jsonData['pa']
                g.redBlockX = jsonData['pa'][-1][0]
                g.redBlockY = jsonData['pa'][-1][1]
                g.redBlockTick = g.currTick
                g.redBlockDisabled = 1
            else:
                i = findPlayerIndex(jsonData['n'])
                if i != None:
                    Players[i].tmpPlayer.movePath[:]=[]
                    Players[i].tmpPlayer.movePath=jsonData['pa']
        elif packetType == ServerPackets.PlayerDirection:
            self.handlePlayerDirection(jsonData['d'],jsonData['n'])
        elif packetType == ServerPackets.PlayerChatMsg:
            if "a" in jsonData:
                self.handlePlayerChatMsg(jsonData['n'],jsonData['m'],jsonData['a'])
            else:
                self.handlePlayerChatMsg(jsonData['n'],jsonData['m'])
        elif packetType == ServerPackets.ErrorMsg:
            if "t" in jsonData:
                self.handleErrorMsg(jsonData['m'],jsonData["t"])
            else:
                self.handleErrorMsg(jsonData['m'])
        elif packetType == ServerPackets.PlayerWhisper:
            self.handlePlayerWhisper(jsonData["n"],jsonData["o"],jsonData["m"])
        elif packetType==ServerPackets.PlayerTeleportLeave:
            i = findPlayerIndex(jsonData['n'])
            if i != None:
                if g.cursorTarget is not None and Players[i].name == g.cursorTarget.name:
                    g.gameEngine.graphics.selectWindow.delete(None)
                    g.cursorTarget=None
                if Players[i].tmpPlayer.lastMsg is not None:
                    Players[i].tmpPlayer.lastMsg.delete()
                    Players[i].tmpPlayer.lastMsg=None
                del Players[i]
        elif packetType==ServerPackets.PlayerTeleportSelf:
            myPlayer.map = jsonData["m"]
            myPlayer.x = jsonData["x"]
            myPlayer.y = jsonData["y"]
            myPlayer.tmpPlayer.nextMoveDir = -1
            myPlayer.tmpPlayer.nextStep = False
            myPlayer.tmpPlayer.nextMoveDir = -1
            myPlayer.tmpPlayer.nextStep=False
            myPlayer.tmpPlayer.nextRealMove =None
            myPlayer.tmpPlayer.moving = False
            g.cursorSelectedTile = [-1,-1]
            myPlayer.tmpPlayer.movePath[:]=[]
            if g.cursorTarget is not None:
                g.gameEngine.graphics.selectWindow.delete(None)
                g.cursorTarget=None
            resetFace(myPlayer)
            Players[:] = []
            npcList[:]=[]
            g.talkingToNpc = None
            g.gameEngine.graphics.SetupMap()
            
        elif packetType == ServerPackets.PlayerTeleportJoin:
            self.handlePlayerConnect(jsonData)
        elif packetType == ServerPackets.SendFriends:
            self.addFriendsToList(jsonData["i"])
        elif packetType == ServerPackets.RemoveFriend:
            self.removeFriendFromList(jsonData["i"])
        elif packetType == ServerPackets.FriendLoggedIn:
            self.handleFriendLoggedIn(jsonData["n"],jsonData["m"])
        elif packetType == ServerPackets.FriendLoggedOut:
            self.handleFriendLoggedIn(jsonData["n"],jsonData["m"],loggedIn=False)
        elif packetType == ServerPackets.SendIgnores:
            self.handleIgnores(jsonData['i'])
        elif packetType == ServerPackets.RemoveIgnore:
            self.handleIgnoreRemove(jsonData['i'])
        elif packetType == ServerPackets.LatencyTick:
            g.latency=(time.time()-g.latencyTick)*1000 - jsonData["t"]
            #print str(int(g.latency))
            refresh=False
            g.lastLatencies[2]=g.lastLatencies[1]
            g.lastLatencies[1]=g.lastLatencies[0]
            if g.latency<50:
                g.lastLatencies[0]=PING_TYPE_GREEN
            elif g.latency<100:
                g.lastLatencies[0]=PING_TYPE_YELLOW
            else:
                g.lastLatencies[0]=PING_TYPE_RED
            lat = max(set(g.lastLatencies), key=g.lastLatencies.count)
            if lat == PING_TYPE_GREEN:
                if g.latencyType != PING_TYPE_GREEN:
                    g.latencyType = PING_TYPE_GREEN
                    refresh=True
            elif lat == PING_TYPE_YELLOW:
                if g.latencyType != PING_TYPE_YELLOW:
                    g.latencyType = PING_TYPE_YELLOW
                    refresh=True
            else:
                if g.latencyType != PING_TYPE_RED:
                    g.latencyType = PING_TYPE_RED
                    refresh=True
            if refresh is True:
                g.gameEngine.graphics.normalUI.refreshLatencybar()
            if g.hoveringType==HOVERING_PING:
                g.gameEngine.graphics.hoverWindow.updateContent(pingHoverTemplate(g.latency))
                #g.gameEngine.graphics.normalUI.delete()
                #g.gameEngine.graphics.initGUI()
        elif packetType == ServerPackets.SendNpcsFromMap:
            self.handleNPCs(jsonData["npcs"])
        elif packetType == ServerPackets.SendNpcMove:
            self.handleNPCMove(jsonData)
        elif packetType == ServerPackets.SendNpcDir:
            self.handleNPCDir(jsonData["n"],jsonData["d"])
        elif packetType == ServerPackets.Banned:
            self.handleBan(jsonData["d"],jsonData["r"])
            g.connector.disconnect()
        elif packetType == ServerPackets.CreateCharInit:
            self.handleCreateCharInit(jsonData["n"],jsonData["c"])
        elif packetType == ServerPackets.CreateMeneInit:
            self.handleCreateMeneInit(jsonData["s"])
        #elif packetType == ServerPackets.SendMeneNameSecondConfirm:
        #    self.handleMeneConfirm(jsonData[0]["n"])
        elif packetType == ServerPackets.SendMenes:
            self.handleSendMenes(jsonData["m"])
        elif packetType == ServerPackets.SendGetReport:
            self.handleSendGetReport(jsonData["t"],jsonData['n'],jsonData["id"])
        elif packetType == ServerPackets.SendMails:
            self.handleSendMails(jsonData['m'])
        elif packetType == ServerPackets.SendGuildmembers:
            self.handleSendGuildmembers(jsonData["gname"],jsonData["m"])
        elif packetType == ServerPackets.SendLeaveGuild:
            self.handleSendLeaveGuild(jsonData["n"])
        elif packetType == ServerPackets.SendJoinedGuild:
            self.handleSendJoinedGuild(jsonData["n"])
        elif packetType == ServerPackets.SendRefreshName:
            self.handleSendRefreshName(jsonData["n"],jsonData["g"])
        elif packetType == ServerPackets.SendGuildInvite:
            self.handleSendGuildInvite(jsonData["e"],jsonData["t"])
        elif packetType == ServerPackets.GuildMemberLogged:
            self.handleGuildMemberLogged(jsonData["n"],jsonData["in"])
        elif packetType == ServerPackets.GuildMemberPromoted:
            self.handleGuildMemberPromote(jsonData["n"],jsonData["a"],jsonData['s'],jsonData['r'])
        elif packetType == ServerPackets.GuildMemberKicked:
            self.handleGuildMemberKicked(jsonData["n"],jsonData["k"])
        elif packetType == ServerPackets.PlayerGuildMsg:
            self.handlePlayerGuildMsg(jsonData['n'],jsonData['m'])
        elif packetType == ServerPackets.SendFightTriggerToMap:
            self.handleFightTriggerToMap(jsonData['n'],jsonData["s"])
        elif packetType == ServerPackets.StartFight:
            self.handleStartFight(jsonData["turn"],jsonData["i"],jsonData["m"])
        elif packetType == ServerPackets.SendAttack:
            self.handleSendAttack(jsonData["t"],jsonData["hp"],jsonData["po"],jsonData["sp"],jsonData["rng"],jsonData["n"],jsonData["ty"],jsonData["ta"],jsonData["c"])
        #elif packetType == ServerPackets.VersionOutdated:
        #    self.handleVersionOutdated()
        elif packetType == ServerPackets.SendPartyInvite:
            self.handleSendPartyInvite(jsonData["e"],jsonData["t"])
        elif packetType == ServerPackets.PlayerPartyMsg:
            self.handlePlayerPartyMsg(jsonData['n'],jsonData['m'])
        elif packetType == ServerPackets.SendPlayerJoinsParty:
            self.handleSendPlayerJoinsParty(jsonData["n"],jsonData["s"],jsonData["sh"],jsonData["h"],jsonData["f"],jsonData["o"],jsonData["j"])
        elif packetType == ServerPackets.SendPlayerLeavesParty:
            self.handleSendPlayerLeavesParty(jsonData["n"],jsonData["o"],jsonData["k"])
        elif packetType == ServerPackets.XpReceived:
            self.handleXPreceived(jsonData["xp"],jsonData["l"],jsonData["m"],jsonData["hp"],jsonData["hpmax"],jsonData["s"],jsonData["d"],jsonData["po"])
        elif packetType == ServerPackets.EndMatch:
            self.handleMatchEnd(jsonData["result"])
        elif packetType == ServerPackets.HealMenes:
            self.handleHealMenes()
        elif packetType == ServerPackets.MeneDies:
            self.handleMeneDies(jsonData["m"])
        elif packetType == ServerPackets.SendItems:
            self.handleSendItems(jsonData["i"])
        elif packetType == ServerPackets.SendMoneyUpdate:
            self.handleSendMoneyUpdate(jsonData["m"],jsonData["es"])
        elif packetType == ServerPackets.ThrowES:
            self.handleThrowES(jsonData["s"],jsonData["a"])
        elif packetType == ServerPackets.ChangeFightMene:
            self.handleChangeFightMene(jsonData["player"],jsonData["mene"])
        elif packetType == ServerPackets.InitiateMeneSelect:
            self.handleInitiateMeneSelect()
        elif packetType == ServerPackets.MoneyReceived:
            self.handleMoneyReceived(jsonData["m"],jsonData["nm"])
        
    def handleMoneyReceived(self,money,newmoney):
        g.moneyAmount=newmoney
        if money>0:
            g.gameEngine.playSoundEffect("moneyreceived")
        if g.gameState==GAMESTATE_FIGHTING:
            
            g.gameEngine.fightScreen.statusText._set_text(WARNINGS["ENEMY_MENE_DIED"][0] % (g.enemyMene.name,money/100.0))
            
    def handleInitiateMeneSelect(self):
        g.gameEngine.fightScreen.meneDied=True
        openMeneSelector(closeBtn=False)
    def handleChangeFightMene(self,player,mene):
        if player==1:
            if g.selectMeneWindowOpened:
                g.gameEngine.fightScreen.meneSelector.delete()
            g.turn=PLAYER_TWO_TURN
            g.currMeneID=mene
            newMene=None
            for m in meneList:
                if m.ID==mene:
                    m.defaultMene=1
                    newMene=m
                else:
                    m.defaultMene=2
            g.gameEngine.fightScreen.myMene=newMene#
            g.gameEngine.fightScreen.startMeneSwitch()
            #g.gameEngine.fightScreen.mene1_img=g.gameEngine.resManager.meneSprites[newMene.spriteName]["behind"]
            #g.gameEngine.fightScreen.mene1Manager.updateInfo(newMene.name,newMene.level,newMene.hp,newMene.maxhp)
            #g.gameEngine.fightScreen.startXP=newMene.xp
            #g.gameEngine.fightScreen.startLevel=newMene.level
            #g.gameEngine.fightScreen.mene1Manager.setPos(g.gameEngine.fightScreen.posX1+(319-256)/2,g.gameEngine.fightScreen.meneposY1+256)
            #g.gameEngine.fightScreen.xpBar.setHP(newMene.xp,(newMene.level+1)**3)
    def handleThrowES(self,success,attempts):
        g.turn=PLAYER_TWO_TURN
        
        randomAngle = random.randint(0,360)
        g.gameEngine.fightScreen.esRotationAngle = randomAngle
        point = getPointOnCircle(g.gameEngine.fightScreen.mene2_img.width/2,-randomAngle-90,g.gameEngine.fightScreen.mene2_img.width/2+g.gameEngine.fightScreen.meneposX2,g.gameEngine.fightScreen.mene2_img.height/2+g.gameEngine.fightScreen.meneposY2-64)
        g.gameEngine.fightScreen.esEndX = point[0]
        g.gameEngine.fightScreen.esEndY = point[1]
        g.gameEngine.fightScreen.dropX = point[0]
        g.gameEngine.fightScreen.throwingES=True
        g.gameEngine.fightScreen.esAttempts=attempts
        g.gameEngine.fightScreen.currentEsAttempt=0
        g.gameEngine.fightScreen.throwingTick=g.currTick
        g.gameEngine.playSoundEffect("throw_ES")
    def handleSendMoneyUpdate(self,money,es):
        g.moneyAmount=money
        g.esAmount=es
        if g.npcTalkWindowOpened:
            g.gameEngine.playSoundEffect("sell_buy_item")
            g.gameEngine.graphics.npcTalkWindow.updateMoney(money,es)
    def handleSendItems(self,items):
        for item in items:
            Items[item] = items[item]
        #print Items
    def handleMeneDies(self,meneID):
        meneIndex=getMeneListIndex(meneID)
        g.gameEngine.fightScreen.statusText._set_text(WARNINGS["YOUR_MENE_DIED"][0] % meneList[meneIndex].name)
    def handleHealMenes(self):
        for mene in meneList:
            mene.hp=mene.maxhp
        if g.gameState != GAMESTATE_FIGHTING:
            self.handleErrorMsg("MENES_HEALED")
    def handleMatchEnd(self,result):
        g.gameEngine.fightScreen.endScreen(result)
        #changeGameState(GAMESTATE_INGAME)
    def handleXPreceived(self,xp,level,meneID,hp,hpmax,speed,defense,power):
        meneIndex=getMeneListIndex(meneID)
        oldXp=meneList[meneIndex].xp
        meneList[meneIndex].xp+=xp
        levelUp=False
        g.gameEngine.fightScreen.endXP=oldXp+xp
        if level>meneList[meneIndex].level:
        
            g.gameEngine.fightScreen.changedLevel=True
        meneList[meneIndex].level=level
        meneList[meneIndex].hp=hp
        meneList[meneIndex].hpmax=hpmax
        meneList[meneIndex].speed=speed
        meneList[meneIndex].power=power
        meneList[meneIndex].defense=defense
        #g.gameEngine.fightScreen.statusText._set_text(WARNINGS["ENEMY_MENE_DIED"][0] % g.enemyMene.name)
        #g.gameEngine.fightScreen.statusText._set_text("Victory! XP received: " + str(xp))
        #print xp, level, meneID
    def handleSendPlayerLeavesParty(self,name,newOwner,kicked=False):
        if name==myPlayer.name:
            g.mePartyleader=False
            g.partyMembers[:]=[]
            g.gameEngine.graphics.deletePartyWindow()
            if not kicked:
                self.handleErrorMsg("YOU_LEFT_PARTY")
            else:
                self.handleErrorMsg('YOU_WERE_KICKED_FROM_PARTY')
        else:
            if newOwner==myPlayer.name:
                g.mePartyleader=True
            theMember=None
            for member in g.partyMembers:
                if member.name==newOwner:
                    member.access=True
                else:
                    member.access=False
                if member.name==name:
                    theMember=member
            try:
                g.partyMembers.remove(theMember)
                g.gameEngine.graphics.initPartyWindow()
                if not kicked:
                    self.handleErrorMsg("HAS_LEFT_PARTY",[name])
                else:
                    self.handleErrorMsg("KICKED_FROM_PARTY",[name])
            except:
                pass
            
    def handleSendPlayerJoinsParty(self,name,shirt,shoes,hat,face,access,joined):
        partymember = PartyMember(name,shirt,shoes,face,hat,access)
        partymember.texture = loadPlayerSprites(partymember,g.gameEngine.graphics.spriteSheets,partyMember=True)[0].texture
        g.partyMembers.append(partymember)
        if name==myPlayer.name:
            if access:
                g.mePartyleader=True
            if joined:
                self.handleErrorMsg("YOU_JOINED_PARTY")
        elif joined:
            if access:
                g.mePartyleader=False
            self.handleErrorMsg("HAS_JOINED_PARTY",[name])
        g.gameEngine.graphics.initPartyWindow()
    def handleSendChar(self,jsonData):
    
        myPlayer.name=jsonData["n"]
        myPlayer.hat=jsonData["h"]
        myPlayer.face=jsonData["f"]
        myPlayer.shirt=jsonData["s"]
        myPlayer.shoes=jsonData["sh"]
        myPlayer.access=jsonData["a"]
        myPlayer.x=jsonData["x"]
        myPlayer.y=jsonData["y"]
        myPlayer.map=jsonData["m"]
        myPlayer.dir=jsonData["dir"]
        g.moneyAmount=jsonData["mo"]
        g.esAmount = jsonData["ES"]
        resetFace(myPlayer)
        friendList[:]=[]
        ignoreList[:]=[]
        npcList[:]=[]
        Players[:]=[]
        myPlayer.tmpPlayer.nameText = createNameText(myPlayer.name,g.guiNameColor,g.guildName)
        #if findMap(myPlayer.map, jsonData[1]["md5"]):
        changeGameState(GAMESTATE_INGAME)
    def handleVersionOutdated(self):
        g.gameEngine.loginMenu.button.disabled = True
        g.updateAvailable=True
        if g.popupWindow is not None:
            g.popupWindow.delete()
        popUpConfirm(WARNINGS['UPDATE_AVAILABLE'][0],on_ok=startUpdate)
    def handleSendAttack(self,turn,hp,power,animation,rng,name,type,target,attacker):
        #print "TAAAAAAAAAAAAAA"
        g.turn=turn
        if g.turn!=PLAYER_ONE_TURN and g.selectMeneWindowOpened:
            g.gameEngine.fightScreen.meneSelector.delete()
        if target==1:
            g.gameEngine.fightScreen.myMene.hp=hp
            g.gameEngine.fightScreen.mene1_targetHP=hp
        else:
            g.enemyMene.hp=hp
            g.gameEngine.fightScreen.mene2_targetHP=hp
        g.gameEngine.fightScreen.startAnimation(animation,target,power,rng,type)
        #sendFightReady()
            
    def handleStartFight(self,turn,defaultMeneID,enemyMene):
        g.turn=turn
        g.enemyMene=Menemon(name=enemyMene["n"],hp=enemyMene["hp"],maxhp=enemyMene["hp"],level=enemyMene["l"],spriteName=enemyMene["sp"])
        g.enemyMeneAnimations[:]=[]
        for animation in enemyMene["a"]:
            g.enemyMeneAnimations.append(animation)
        g.defaultMene=defaultMeneID
        changeGameState(GAMESTATE_LOADING_FIGHTING)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    def handleFightTriggerToMap(self,name,fighting):
        index=findPlayerIndex(name)
        if index is None:
            return
        if fighting:
            #TODO: DOWNLOAD IT IN GAME LAUNCH
            Players[index].tmpPlayer.battling = pyglet.image.load(g.dataPath + '/theme/battling.png')
        else:
            Players[index].tmpPlayer.battling = None
    def handlePlayerPartyMsg(self,name,message):
        if message[0]=='>':
            postColor=g.greentextColor
        else:
            postColor=g.partyColor
        constructText(message,postColor,name,g.partyColor)
    def handlePlayerGuildMsg(self,name,message):
        if message[0]=='>':
            postColor=g.greentextColor
        else:
            postColor=g.greenColor
        constructText(message,postColor,name,g.greenColor)
            
    def handleGuildMemberKicked(self,kickedName,kickerName):
        index=getMemberListIndex(kickedName)
        
        if kickedName==myPlayer.name:
            constructText(WARNINGS["YOU_HAVE_BEEN_KICKED_FROM_GUILD"][0] % (kickerName,g.guildName),WARNINGS["YOU_HAVE_BEEN_KICKED_FROM_GUILD"][1])
            guildList[:]=[]
            g.myGuildAccess=None
            g.guildName=None
        elif index is None:
            return
        else:
            constructText(WARNINGS["GUILD_MEMBER_KICKED"][0] % (kickedName,kickerName,g.guildName),WARNINGS["GUILD_MEMBER_KICKED"][1])
            del guildList[index]
        if g.guildWindowOpened:
            g.gameEngine.graphics.guildWindow.delete(None)
            g.gameEngine.graphics.initGuildWindow()
    def handleGuildMemberPromote(self,promotedName,access,promotedOrNot,promoterName):
        index=getMemberListIndex(promotedName)
        if index is None:
            return
        if access==GUILD_MEMBER:
            text='Member'
        elif access==GUILD_MODERATOR:
            text='Moderator'
        else:
            text='Admin'
        if promotedOrNot:
            constructText(WARNINGS["GUILD_MEMBER_PROMOTED"][0] % (promoterName,promotedName,text),WARNINGS["GUILD_MEMBER_PROMOTED"][1])
        else:
            constructText(WARNINGS["GUILD_MEMBER_DEMOTED"][0] % (promoterName,promotedName,text),WARNINGS["GUILD_MEMBER_DEMOTED"][1])
        guildList[index][1]=access
        if promotedName==myPlayer.name:
            g.myGuildAccess=access
        if g.guildWindowOpened:
            g.gameEngine.graphics.guildWindow.delete(None)
            g.gameEngine.graphics.initGuildWindow()
    def handleGuildMemberLogged(self,name,loggedIn):
        index=getMemberListIndex(name)
        if index is None:
            return
        if loggedIn:
            guildList[getMemberListIndex(name)][2]=1
            if not isIgnored(name) and not isFriend(name) and myPlayer.name!=name:
                constructText(WARNINGS["GUILD_MEMBER_LOGGED_IN"][0] % (name),WARNINGS["GUILD_MEMBER_LOGGED_IN"][1])
        else:
            guildList[getMemberListIndex(name)][2]=0
            if not isIgnored(name) and not isFriend(name) and myPlayer.name!=name:
                constructText(WARNINGS["GUILD_MEMBER_LOGGED_OUT"][0] % (name),WARNINGS["GUILD_MEMBER_LOGGED_OUT"][1])
        if g.guildWindowOpened:
            g.gameEngine.graphics.guildWindow.delete(None)
            g.gameEngine.graphics.initGuildWindow()
    def handleSendPartyInvite(self,errormsg,variables):
        a = ()
        for var in variables:
            a = a + (var,)
        if g.popupWindow is not None:
            g.popupWindow.delete()
        popUpConfirm(WARNINGS[errormsg][0] % a,on_cancel=cancelPartyInvite,on_ok=acceptPartyInvite)
    def handleSendGuildInvite(self,errormsg,variables):
        a = ()
        for var in variables:
            a = a + (var,)
        if g.popupWindow is not None:
            g.popupWindow.delete()
        popUpConfirm(WARNINGS[errormsg][0] % a,on_cancel=cancelGuildInvite,on_ok=acceptGuildInvite)
    def handleSendRefreshName(self,name,guild):
        if name==myPlayer.name:
            myPlayer.tmpPlayer.nameText = createNameText(myPlayer.name,g.guiNameColor,guild)
        else:
            if findPlayerIndex(name) is not None:
                Players[findPlayerIndex(name)].tmpPlayer.guild=guild
                if isInParty(name):
                    color = g.partyNameColor
                elif isFriend(name):
                    color=g.friendNameColor
                else:
                    color=g.guiNameColor
                Players[findPlayerIndex(name)].tmpPlayer.nameText = createNameText(Players[findPlayerIndex(name)].name,color,Players[findPlayerIndex(name)].tmpPlayer.guild)
    def handleSendJoinedGuild(self,name):
        if name!=myPlayer.name:
            guildList.append([name,0,1])
        if g.guildWindowOpened:
            g.gameEngine.graphics.guildWindow.delete(None)
            g.gameEngine.graphics.initGuildWindow()
        constructText(name + ' has joined the guild!',g.greenColor)
        
    def handleSendLeaveGuild(self,name):
        if name==myPlayer.name:
            constructText('You have left ' + g.guildName + '!',g.errorColor)
            g.guildName=None
            guildList[:]=[]
        else:
            constructText(name + ' has left the guild!',g.greenColor)
            for i in xrange(len(guildList)):
                if guildList[i][0]==name:
                    del guildList[i]
                    break
        if g.guildWindowOpened:
            g.gameEngine.graphics.guildWindow.delete(None)
            g.gameEngine.graphics.initGuildWindow()
            
    def handleSendGuildmembers(self,guildname,members):
        #print guildName
        g.guildName=guildname
        myPlayer.tmpPlayer.nameText = createNameText(myPlayer.name,g.guiNameColor,g.guildName)
        for member in members:
            if member[0]==myPlayer.name:
                g.myGuildAccess=member[1]
            guildList.append(member)
        #print guildName,guildList
    
    def handleSendMails(self,mails):
        g.mails[:]=[]
        g.mails=mails[::-1]
        try:
            if len(g.mails)>0:
                g.gameEngine.graphics.normalUI.addMail()
            else:
                g.gameEngine.graphics.normalUI.removeMail()
        except:
            pass
    def handleSendGetReport(self,text,name=0,rid=None):
        
        if name==0 and g.reportWindowOpened:
            g.gameEngine.graphics.reportWindow.reportInput.set_text(text)
            g.gameEngine.graphics.reportWindow.reportInput.on_gain_focus()
            g.gameEngine.graphics.reportWindow.reportInput.on_lose_focus()
        elif name!=0 and g.reportAnswerWindowOpened:
            g.gameEngine.graphics.reportAnswerWindow._reportid=rid
            if name==None and text=='':
                g.gameEngine.graphics.reportAnswerWindow.report.set_text('No reports')
            else:
                g.gameEngine.graphics.reportAnswerWindow.report.set_text(name + ': ' + text)
            #g.gameEngine.graphics.reportAnswerWindow.reportInput.on_gain_focus()
            #g.gameEngine.graphics.reportAnswerWindow.reportInput.on_lose_focus()
        
    def handleSendMenes(self,menelist):
        meneList[:]=[]
        for c in menelist:
            meneList.append(Menemon(ID=c["i"],name=c["n"],hp=c["hp"],xp=c["xp"],maxhp=c['hpmax'],level=c["l"],power=c["p"],defense=c["de"],speed=c["s"],spriteName=c["sp"],attack1=c["a1"],attack2=c["a2"],attack3=c["a3"],attack4=c["a4"],defaultMene=c["d"]))
        
    def handleMeneConfirm(self,menename):
        def removeDisable(event):
            g.gameEngine.loginMenu.saveBtn.disabled = False
        def onOk(event):
            packet = json.dumps([{"p": ClientPackets.SendMeneNameDouble}])
            g.tcpConn.sendData(packet)
        if g.popupWindow is not None:
            g.popupWindow.delete()
        popUpConfirm(menename + " will be your mene's name.",on_cancel=removeDisable,on_ok=onOk)
    def handleCreateMeneInit(self,spritename):
        g.spriteName=spritename
        changeGameState(GAMESTATE_NAMEMENE)
        
    def handleCreateCharInit(self,name, pairs):
        myPlayer.name=name
        g.clothingPairs=pairs
        changeGameState(GAMESTATE_CREATECHAR)
        
    def handleGameServerDown(self):
        g.banned = 'Game Server down ;__; Try out later'
    def handleBan(self,minutes,reason):
        banEndTime = (datetime.datetime.now()+datetime.timedelta(minutes=minutes)).strftime("%d.%m.%Y %H:%M:%S")
        g.banned = 'You are banned! ;_; End time: {}. Reason: {}'.format(banEndTime,unidecode(reason))
        
    def handleNPCDir(self,npcName,dir):
        npcIndex = findNpcIndex(npcName)
        if npcList[npcIndex].tmpPlayer.moving:
            npcList[npcIndex].tmpPlayer.nextDir = dir
        else:
            npcList[npcIndex].dir=dir
            resetSpriteFacing(npcList[npcIndex],dir)
    def handleNPCMove(self,data):
        i = findNpcIndex(data["n"])
        if i!=None:
            #TODO: Fix this
            
            npcList[i].x=data["x"]
            npcList[i].y=data["y"]
            npcList[i].dir=data["d"]
            changeSpriteFacing(npcList[i],npcList[i].dir)
            npcList[i].tmpPlayer.moveTick = g.currTick
            npcList[i].tmpPlayer.moving = True
            if i == g.talkingToNpc:
                checkNpcDistance(data["n"],True)
    def handleNPCs(self,npcs):
        for c in npcs:
            npc=NPCClass()
            npc.name=c["n"]
            npc.shirt=c["s"]
            npc.hat=c["h"]
            npc.face=c["f"]
            npc.shoes=c["sh"]
            npc.x=c["x"]
            npc.y=c["y"]
            npc.dir=c["d"]
            npc.text=c["te"]
            npc.actionType=c["type"]
            resetFace(npc)
            npc.tmpPlayer.sprite = loadPlayerSprites(npc,g.gameEngine.graphics.spriteSheets)
            npc.tmpPlayer.nameText = createNameText(c["n"],g.npcColor)
            #createNameTexts(npc,0,0,PLAYER_TYPE_NPC)
            npcList.append(npc)
    def handleIgnoreRemove(self,name):
        for i in xrange(len(ignoreList)):
            if ignoreList[i]==name:
                del ignoreList[i]
                break
        if g.ignoreWindowOpened:
            g.gameEngine.graphics.ignoreWindow.delete(None)
            g.gameEngine.graphics.initIgnoreWindow()
        if g.cursorTarget is not None and g.cursorTarget.name == name and g.ignoreWindowOpened and g.selectWindowOpened:
            g.gameEngine.graphics.selectWindow.delete(None)
            g.gameEngine.graphics.initSelectWindow()
    def handleIgnores(self,ignores):
        for c in ignores:
            ignoreList.append(c)
        if g.ignoreWindowOpened:
            g.gameEngine.graphics.ignoreWindow.delete(None)
            g.gameEngine.graphics.initIgnoreWindow()
        index=None
        if len(ignores)>0:
            index = findPlayerIndex(ignores[0])
        if index!=None:
            if g.cursorTarget is not None and ignores[0]==g.cursorTarget.name and g.ignoreWindowOpened and g.selectWindowOpened:
                g.gameEngine.graphics.selectWindow.delete(None)
                g.gameEngine.graphics.initSelectWindow()
    def handleFriendLoggedIn(self,friendName,errorMsg,loggedIn=True):
        for i in xrange(len(friendList)):
            if friendList[i][0]==friendName[0]:
                if loggedIn==True:
                    friendList[i][1]=1
                else:
                    friendList[i][1]=0
        if g.friendWindowOpened:
            g.gameEngine.graphics.friendWindow.delete(None)
            g.gameEngine.graphics.initFriendWindow()
        self.handleErrorMsg(errorMsg,friendName)
    def removeFriendFromList(self,name):
        for i in xrange(len(friendList)):
            if friendList[i][0]==name:
                del friendList[i]
                break
        if g.friendWindowOpened:
            g.gameEngine.graphics.friendWindow.delete(None)
            g.gameEngine.graphics.initFriendWindow()
        index = findPlayerIndex(name)
        if index!=None:
            #Players[index].tmpPlayer.nameText._set_color(g.guiNameColor)
            if g.cursorTarget is not None and g.cursorTarget.name == name and g.friendWindowOpened and g.selectWindowOpened:
                g.gameEngine.graphics.selectWindow.delete(None)
                g.gameEngine.graphics.initSelectWindow()
        
    def addFriendsToList(self,data):
        for c in data:
            friendList.append(c)
        if g.friendWindowOpened:
            g.gameEngine.graphics.friendWindow.delete(None)
            g.gameEngine.graphics.initFriendWindow()
        index=None
        if len(data)>0:
            index = findPlayerIndex(data[0][0])
        if index!=None:
            #Players[index].tmpPlayer.nameText._set_color(g.guiFriendColor)
            if g.cursorTarget is not None and g.cursorTarget.name == data[0][0] and g.friendWindowOpened and g.selectWindowOpened:
                g.gameEngine.graphics.selectWindow.delete(None)
                g.gameEngine.graphics.initSelectWindow()
    def handlePlayerWhisper(self,fromName,toName,message):
        
        whisperText=None
        whisperingName=None
        if toName==myPlayer.name:
            #g.chatLog+= '\n{background_color '+str(g.postBgColor)+'}{color '+str(g.whisperColor)+'}{bold True}From '+fromName+': {bold False}'+message+'\n' 
            constructText(message,g.whisperColor,fromName,g.whisperColor,whisperText='From ')
            #whisperText ='From '
            #whisperingName = toName
        if fromName==myPlayer.name:
            #g.chatLog+= '\n{background_color '+str(g.postBgColor)+'}{color '+str(g.whisperColor)+'}{bold True}To '+toName+': {bold False}'+message+'\n' 
            constructText(message,g.whisperColor,toName,g.whisperColor,whisperText='To ')
        #constructText(message,)
        #checkChatLogLength()
        #g.gameEngine.graphics.chat.textArea.update_text(g.chatLog)
        
    def handleErrorMsg(self,error,text=None):
        if text is None:
            constructText(WARNINGS[error][0],WARNINGS[error][1])
        else:
            a=()
            for t in text:
                a = a + (t,)
            constructText(WARNINGS[error][0] % a,WARNINGS[error][1])
        
    def handlePlayerChatMsg(self,name,message,a=0):
        if message[0]=='>':
            postColor=g.greentextColor
        else:
            postColor=g.postColor
        nameColor=g.nameColor
        modText=None
        if a>0:
            if a==ADMIN_MODERATOR:
                nameColor = g.modColor
                modText = '#Mod#'
            elif a==ADMIN_ADMIN:
                nameColor = g.adminColor
                modText = '#Admin#'
            else:
                nameColor = g.adminColor
                modText = '#Owner#'

        constructText(message,postColor,name,nameColor,modText)
        if name == myPlayer.name:
            handleChatBubble(myPlayer,message,a)
        else:
            i = findPlayerIndex(name)
            if i != None:
                handleChatBubble(Players[i],message,a)
    def setupMap(self,jsonData):
        Map.song = jsonData[0]["song"]
        Map.width = jsonData[0]["width"]
        Map.height =jsonData[0]["height"]
        Map.menes=jsonData[0]["menes"]
        g.tmpMapTiles=Map.width
        Map.tile = [[TileClass() for i in xrange(Map.height)] for i in xrange(Map.width)]
        changeGameState(GAMESTATE_LOADING)
    def addToMapData(self,jsonData):
        j=0
        while j<len(jsonData[1]):
            Map.tile[jsonData[1][j][0]['x']][jsonData[1][j][0]["y"]].l1 = jsonData[1][j][0]["l1"]
            Map.tile[jsonData[1][j][0]['x']][jsonData[1][j][0]["y"]].l2 = jsonData[1][j][0]["l2"]
            Map.tile[jsonData[1][j][0]['x']][jsonData[1][j][0]["y"]].l3 = jsonData[1][j][0]["l3"]
            Map.tile[jsonData[1][j][0]['x']][jsonData[1][j][0]["y"]].f = jsonData[1][j][0]["f"]
            Map.tile[jsonData[1][j][0]['x']][jsonData[1][j][0]["y"]].t = jsonData[1][j][0]["t"]
            Map.tile[jsonData[1][j][0]['x']][jsonData[1][j][0]["y"]].d1 = jsonData[1][j][0]["d1"]
            Map.tile[jsonData[1][j][0]['x']][jsonData[1][j][0]["y"]].d2 = jsonData[1][j][0]["d2"]
            Map.tile[jsonData[1][j][0]['x']][jsonData[1][j][0]["y"]].d3 = jsonData[1][j][0]["d3"]
            j+=1
            
        
        g.tmpMapTiles-=1
        if g.tmpMapTiles==0:
            tmpMap = Map.__dict__
            tiles=[]
            for x in xrange(len(tmpMap["tile"])):
                tilesX=[]
                for y in xrange(len(tmpMap["tile"][x])):
                    
                    tilesX.append(tmpMap["tile"][x][y].__dict__)
                tiles.append(tilesX)
            tmpMap["tile"]=tiles
            with open(g.dataPath+'/maps/'+myPlayer.map+'.map','w') as fp:
                json.dump(tmpMap, fp)
            #g.gameEngine.graphics.SetupMap()
            g.tmpMapTiles=1
            changeGameState(GAMESTATE_INGAME)
    def handlePlayerDirection(self,direction,name):
        if name == myPlayer.name:
            resetSpriteFacing(myPlayer,direction)
            
        else:
            i = findPlayerIndex(name)
            if i != None:
                resetSpriteFacing(Players[i],direction)
    def handlePlayerMove(self,direction,name):
        if name == myPlayer.name:
            handleMove(myPlayer,direction)
        else:
            i = findPlayerIndex(name)
            if i != None:
                handleMove(Players[i],direction)
            
    def handlePlayerMoveStop(self,name,x,y,direction):
        if name == myPlayer.name:
            handleStop(myPlayer,x,y,direction)
        else:
            i = findPlayerIndex(name)
            if i != None:
                handleStop(Players[i],x,y,direction)
            
            
    def handlePlayerMoveNext(self,name,direction):
        if name == myPlayer.name:
            myPlayer.tmpPlayer.nextMoveDir = direction
            myPlayer.tmpPlayer.movePath[:]=[]
        else:
            i = findPlayerIndex(name)
            if i != None:
                Players[i].tmpPlayer.nextMoveDir=direction
                Players[i].tmpPlayer.movePath[:]=[]
    def handlePlayerMoveReal(self,name,x,y,direction):
        pos = checkPositionChange(direction)
        if name == myPlayer.name and (myPlayer.x != x or myPlayer.y != y):
            if myPlayer.x+pos[0] == x and myPlayer.y+pos[1] == y:
                myPlayer.tmpPlayer.moving = True
                myPlayer.tmpPlayer.nextRealMove = direction
            elif myPlayer.x != x or myPlayer.y != y:
                handleMove(myPlayer,direction,x=x,y=y)
        else:
            index = findPlayerIndex(name)
            if index != None and (Players[index].x != x or Players[index].y != y):
                if Players[index].x+pos[0] == x and Players[index].y+pos[0] == y:
                    Players[index].tmpPlayer.moving = True
                    Players[index].tmpPlayer.nextRealMove = direction
                elif Players[index].x != x or Players[index].y != y:
                    handleMove(Players[index],direction,x=x,y=y)
    def handlePlayerConnect(self,data):
        player = PlayerClass()
        player.name = data['n']
        player.hat = data['h']
        player.face = data['f']
        player.shoes = data['sh']
        player.shirt = data['s']
        player.access = data['a']
        player.x = data['x']
        player.y = data['y']
        player.dir = data['d']
        player.tmpPlayer.guild = data["g"]
        if 'fi' in data and data['fi']:
            self.handleFightTriggerToMap(player.name, True)
        resetFace(player)
        player.tmpPlayer.sprite = loadPlayerSprites(player,g.gameEngine.graphics.spriteSheets)
        
        
        #createNameTexts(player,0,0)
        Players.append(player)
        self.handleSendRefreshName(player.name,player.tmpPlayer.guild)