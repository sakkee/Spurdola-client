import pyglet
import global_vars as g
from constants import *
import datetime
from gamelogic import *
from gui.hpbar import HpBar
from pyglet_gui.manager import Manager
from gui.meneStats import MeneStats
from pyglet_gui.text_input import TextInput
from pyglet_gui.buttons import HighlightedButton
from gui.abilityButtons import AbilityButtons
from pyglet_gui.containers import VerticalContainer, HorizontalContainer
from pyglet_gui.gui import Label, Frame, Graphic

import os
from pyglet.gl import *

class FightScreen():
    def __init__(self):
        #self.screen = screen     
        self.ring = pyglet.resource.image(g.dataPath + '/gui/fightring.png')
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        self.startTick = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
        self.mene1_img=None
        self.mene2_img=None
        self.meneNamingPopped=False
        self.mene2_img_esCatch=None
        self.myMene=None
        self.meneSelector = None
        self.posX1=g.SCREEN_WIDTH*0.05
        self.posY1=g.SCREEN_HEIGHT*0.05
        self.posX2=g.SCREEN_WIDTH*0.95-319
        self.posY2=g.SCREEN_HEIGHT*0.40
        self.animationX1=-319
        self.startX1=-319
        self.throwingPhase=0
        self.esAttempts=0
        self.currentEsAttempt=0
        self.throwingPhaseTimes = [1000,1000,500,1000,250,250,1000,1000]
        self.animationX2=g.SCREEN_WIDTH
        self.startX2=g.SCREEN_WIDTH
        self.animationSheets={}
        self.sounds={}
        self.meneposX1=g.SCREEN_WIDTH*0.05+(319-256)/2
        self.meneposX2=g.SCREEN_WIDTH*0.95-319+(319-256)/2
        self.meneposY1=g.SCREEN_HEIGHT*0.05+68
        self.meneposY2=g.SCREEN_HEIGHT*0.40+68
        self.mene1Manager=None
        self.mene2Manager=None
        self.xpBar=HpBar(type="xp",height=50,width=300)
        self.startXP=0
        self.endXP=0
        self.startLevel=1
        self.xpBarMan=None
        esIc = pyglet.resource.image(g.dataPath+'/gui/es3.png')
        esIc.anchor_x=9
        esIc.anchor_y=25
        self.esIcon = pyglet.sprite.Sprite(esIc,x=0,y=0)
        self.catchAnimation = pyglet.sprite.Sprite(pyglet.resource.image(g.dataPath+'/gui/esexplosion.png'))
        
        self.esStartX = 200
        self.esStartY = 200
        self.dropY=0
        self.dropX=0
        self.esEndX = 800
        self.esEndY = 600
        self.esRotationAngle=0
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        self.statusText=pyglet.text.Label("",font_size=28,bold=True,color=(255,255,255,255),anchor_x='center',anchor_y='center')
        self.mene1_targetHP=None
        self.mene2_targetHP=None
        self.mene1_currHP=None
        self.mene2_currHP=None
        self.missed=False
        self.throwingES=False
        self.catchingES=False
        self.meneDied=False
        self.changingMene=0
        self.throwingTick=0
        self.statusTextChangedToLevel=False
        self.fightMusic = pyglet.media.load(g.dataPath+'/sounds/'+FIGHTMUSIC+'.mp3',streaming=False)
        self.winMusic = pyglet.media.load(g.dataPath+'/sounds/'+FIGHTWIN +'.mp3',streaming=False)
        self.lossMusic = pyglet.media.load(g.dataPath+'/sounds/'+FIGHTLOSS +'.mp3',streaming=False)
        self.captureMusic = pyglet.media.load(g.dataPath+'/sounds/menecapture.mp3',streaming=False)
        self.currentAnimation=None
        self.currentAnimationSprite=0
        self.attackAnimationTick=0
        self.attackText=pyglet.text.Label("xx",font_size=28,bold=True,color=(255,0,0,255),width=256,anchor_x='center',anchor_y='center')
        self.attackAnimationX=0
        self.attackAnimationY=0
        self.attackAnimationStartY=0
        self.animationEndTick=0
        self.animationStartTick=0
        self.endTick=0
        self.finished=False
        self.changedLevel=False
        self.fightOver=False
        self.meneMan=None
        self.levelTick=0
        self.xpTick=0
        self.startingAnimationLength=2000.0
        self.endingLength=6000.0
        backgroundImg = pyglet.image.load(g.dataPath+'/gui/fight_background.png')
        self.backgroundImg = backgroundImg.get_texture()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        
        self.abilityButtons = None
        self.scaleBackground()
        #self.animationRunning=True
        self.loadAnimations()
        self.loadSounds()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    def scaleBackground(self):
        self.backgroundImg.width=g.SCREEN_WIDTH
        self.backgroundImg.height=g.SCREEN_HEIGHT
        #self.backgroundImg.scale = min(self.backgroundImg.height,g.SCREEN_HEIGHT)/max(self.backgroundImg.height,g.SCREEN_HEIGHT),min(g.SCREEN_WIDTH, self.backgroundImg.width)/max(g.SCREEN_WIDTH, self.backgroundImg.width)
        #self.backgroundImg.width=g.SCREEN_WIDTH
        #self.backgroundImg.height=g.SCREEN_HEIGHT
        #self.backgroundImg.texture.width=g.SCREEN_WIDTH
        #self.backgroundImg.texture.height=g.SCREEN_HEIGHT
    def loadSounds(self):
        for file in os.listdir(g.dataPath+"/abilities/sounds/"):
            if file.endswith(".mp3"):
                try:
                    self.sounds[file[:-4]]=pyglet.media.load(g.dataPath+'/abilities/sounds/'+file, streaming=False)
                except Exception, e:
                    pass
    def loadAnimations(self):
        for file in os.listdir(g.dataPath+"/abilities/animations/"):
            if file.endswith(".png"):
                try:
                    img=pyglet.resource.image(g.dataPath+'/abilities/animations/'+file)
                    grid = pyglet.image.ImageGrid(img,img.height//256,img.width//256)
                    self.animationSheets[file[:-4]]={'grid':grid,'length':img.width//256}
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                except Exception, e:
                    pass
    def startScreen(self):
        #pyglet.gl.glClearColor(1, 1, 1, 1)
        #self.animationRunning=True
        self.myMene=getDefaultMene()
        g.currMeneID=self.myMene.ID
        self.meneNamingPopped=False
        self.currentAnimation=None
        self.currentAnimationSprite=0
        self.attackAnimationX=0
        self.attackAnimationY=0
        self.posX1=g.SCREEN_WIDTH*0.05
        self.posY1=g.SCREEN_HEIGHT*0.05
        self.posX2=g.SCREEN_WIDTH*0.95-319
        self.posY2=g.SCREEN_HEIGHT*0.40
        self.animationX1=-319
        self.startX1=-319
        self.levelTick=0
        self.xpTick=0
        self.throwingPhase=0
        self.statusTextChangedToLevel=False
        self.changingMene=0
        self.meneposX1=g.SCREEN_WIDTH*0.05+(319-256)/2
        self.meneposX2=g.SCREEN_WIDTH*0.95-319+(319-256)/2
        self.meneposY1=g.SCREEN_HEIGHT*0.05+68
        self.meneposY2=g.SCREEN_HEIGHT*0.40+68
        self.esStartX = self.meneposX1+128-self.esIcon.width/2
        self.esStartY = self.meneposY1
        self.esEndX = self.meneposX2+128-self.esIcon.width/2
        self.esEndY = self.meneposY2
        self.mene1_targetHP=None
        self.mene2_targetHP=None
        self.finished=False
        self.changedLevel=False
        self.meneMan=None
        self.meneDied=False
        self.mene1_currHP=self.myMene.hp
        self.mene2_currHP=g.enemyMene.hp
        self.mene1Manager=MeneStats(self.myMene.name,self.myMene.level,self.myMene.hp,self.myMene.maxhp)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        self.mene2Manager=MeneStats(g.enemyMene.name,g.enemyMene.level,g.enemyMene.hp,g.enemyMene.maxhp)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        self.statusText._set_text(WARNINGS["WILD_APPEARED"][0] % g.enemyMene.name)
        
        self.startXP=self.myMene.xp
        self.startLevel=self.myMene.level
        #constructText(WARNINGS["WILD_APPEARED"][0] % g.enemyMene.name,WARNINGS["WILD_APPEARED"][1])
        
        #self.mene1_img=pyglet.resource.image(g.dataPath + '/menes/'+self.myMene.spriteName+'_behind.png')
        self.mene1_img=g.gameEngine.resManager.meneSprites[self.myMene.spriteName]["behind"]
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        #self.mene2_img=pyglet.sprite.Sprite(pyglet.resource.image(g.dataPath + '/menes/'+g.enemyMene.spriteName+'_front.png'))
        self.mene2_img=pyglet.sprite.Sprite(g.gameEngine.resManager.meneSprites[g.enemyMene.spriteName]["front"])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        self.mene2_img_esCatch = g.gameEngine.resManager.meneSprites[g.enemyMene.spriteName]['fronttest']
        self.abilityButtons = AbilityButtons(self.myMene.attack1,self.myMene.attack2,self.myMene.attack3,self.myMene.attack4)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        #if g.turn==PLAYER_TWO_TURN:
        #    self.abilityButtons.changeDisableds(True)
        #else:
        #    self.abilityButtons.changeDisableds(False)
        self.startTick = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
        self.updatePositions()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        
    def initNameMene(self):
        def sendMeneName(event):
            
            meneNameConfirmFight(self.nameInput.get_text())
        label = Label("Name Your Mene",color=g.postColor,font_size=18,bold=True)
        picture = Graphic(texture=g.gameEngine.resManager.meneSprites[g.enemyMene.spriteName]['front'])
        self.nameInput = TextInput(text="",padding=2,length=12,max_length=12,width=200,font_size=16)
        self.saveBtn = HighlightedButton(label="Save",on_release=sendMeneName,width=100,height=40,font_size=16)
        frame = Frame(VerticalContainer(content=[label,picture,HorizontalContainer([self.nameInput,self.saveBtn])]),path='frame_npc_talk')
        self.meneMan = Manager(frame,
            window=g.screen,
            batch=g.guiBatch,
            theme=g.theme,
            offset=(0,0),
            is_movable=True)
    #def removeNamingManager(self):
    #    self.meneMan.delete()
    def updatePositions(self):
        self.posX1=g.SCREEN_WIDTH*0.05
        self.posY1=g.SCREEN_HEIGHT*0.05
        self.posX2=g.SCREEN_WIDTH*0.95-319
        self.posY2=g.SCREEN_HEIGHT*0.40
        self.statusText._set_x(g.SCREEN_WIDTH/2)
        self.statusText._set_y(g.SCREEN_HEIGHT/2)
        self.meneposX1=g.SCREEN_WIDTH*0.05+(319-256)/2
        self.meneposX2=g.SCREEN_WIDTH*0.95-319+(319-256)/2
        self.meneposY1=g.SCREEN_HEIGHT*0.05+68
        self.meneposY2=g.SCREEN_HEIGHT*0.40+68
        if g.gameState==GAMESTATE_FIGHTING:
            self.mene2_img.set_position(self.meneposX2,self.meneposY2)
            self.mene2_img_esCatch.set_position(self.meneposX2,self.meneposY2)
        self.animationX1=-319
        self.startX1=-319
        self.dropY=self.meneposY2-64
        self.animationX2=g.SCREEN_WIDTH
        self.startX2=g.SCREEN_WIDTH
        if self.mene1Manager is not None:
            self.mene1Manager.setPos(self.posX1+(319-256)/2,self.meneposY1+256)
            self.mene2Manager.setPos(self.posX2+(319-256)/2,self.meneposY2+256)
        #print 
        if self.abilityButtons is not None:
            self.abilityButtons.setPos((self.posX1+319+(g.SCREEN_WIDTH-self.posX1-319-self.abilityButtons.width)/2),self.posY1)
        
    def startMeneSwitch(self):
        self.changingMene=1
        self.finished=False
        self.animationStartTick=g.currTick
        self.animationEndTick=g.currTick+self.startingAnimationLength
        
    def startAnimation(self, animationsprite, target, power,hitType=1,abilityType=ABILITY_TYPE_ATTACK):
        if abilityType==ABILITY_TYPE_ATTACK:
            attackText='-'+str(power)
            self.attackText.set_style("color",(255,0,0,255))
        else:
            attackText='+'+str(power)
            self.attackText.set_style("color",(0,255,0,255))
            
        if hitType==ATTACK_RNG_MISS:
            self.attackText.set_style("font_size",28)
            self.attackText._set_text("MISS")
        elif hitType==ATTACK_RNG_CRIT:
            self.attackText.set_style("font_size",42)
            self.attackText._set_text(attackText)
        else:
            self.attackText.set_style("font_size",28)
            self.attackText._set_text(attackText)
        #print "TARGEET", target
        if target==1:
            self.attackAnimationX=self.meneposX1
            self.attackAnimationY=self.meneposY1
            self.attackText.x=self.meneposX1+128
            self.attackText.y=self.meneposY1+128
            self.attackAnimationStartY=self.meneposY1+128
        else:
            self.attackAnimationX=self.meneposX2
            self.attackAnimationY=self.meneposY2
            self.attackText.x=self.meneposX2+128
            self.attackText.y=self.meneposY2+128
            self.attackAnimationStartY=self.meneposY2+128
        if hitType==ATTACK_RNG_MISS:
            if g.SOUND:
                g.gameEngine.playSound("miss1")
            self.missed=True
        else:
            if g.SOUND:
                g.gameEngine.playSound(animationsprite)
            self.missed=False
        self.currentAnimation=animationsprite
        self.currentAnimationSprite=0
        self.attackAnimationTick=g.currTick
        self.animationStartTick=g.currTick
        self.animationEndTick=g.currTick+100*self.animationSheets[self.currentAnimation]['length']
        
    def updateMeneSwitchAnimation(self):
        if self.changingMene==1:
            self.animationX1=self.posX1-(self.posX1-self.startX1)*((g.currTick-self.animationStartTick)/self.startingAnimationLength)
        else:
            self.animationX1=self.startX1+(self.posX1-self.startX1)*((g.currTick-self.animationStartTick)/self.startingAnimationLength)
    def updateAnimation(self):
        self.animationX1=self.startX1+(self.posX1-self.startX1)*((g.currTick-self.startTick)/self.startingAnimationLength)
        self.animationX2=self.startX2+(self.posX2-self.startX2)*((g.currTick-self.startTick)/self.startingAnimationLength)
        self.statusText._set_y(int(g.SCREEN_HEIGHT/2+(g.SCREEN_HEIGHT/8)*((g.currTick-self.startTick)/self.startingAnimationLength)))
        if self.animationX1>=self.posX1:
            self.finished=True
            self.mene2_img.set_position(self.meneposX2,self.meneposY2)
            self.mene2_img_esCatch.set_position(self.meneposX2,self.meneposY2)
            self.statusText._set_text("")
            self.statusText._set_y(int(g.SCREEN_HEIGHT/2))
            
            sendFightReady()
    def endScreen(self,result=1):
        #self.xpBarMan = Manager(self.xpBar,window=g.screen,batch=g.guiBatch,is_movable=False,offset=(0,-g.SCREEN_HEIGHT/10),theme=g.theme)
        self.result=result
        #self.xpTick=g.currTick+self.endingLength/2
        if result==MATCH_PLAYER_WON:
            g.gameEngine.changeMusicSong(self.winMusic,fadetime=0.1,loaded=True)
            self.xpBarMan = Manager(self.xpBar,window=g.screen,batch=g.guiBatch,is_movable=False,offset=(0,-g.SCREEN_HEIGHT/10),theme=g.theme)
            self.xpTick=g.currTick+self.endingLength/2
            self.endTick=g.currTick+self.endingLength
            self.fightOver=True
        elif result==MATCH_NPC_WON:
            g.gameEngine.changeMusicSong(self.lossMusic,fadetime=0.1,loaded=True)
            self.endTick=g.currTick+self.endingLength
            self.fightOver=True
        elif result==MATCH_PLAYER_LEFT:
            self.fightOver=True
    def update(self):
        self.backgroundImg.blit(0,0)
        
        if self.finished:
            self.ring.blit(self.posX1,self.posY1)
            self.ring.blit(self.posX2,self.posY2)
            self.mene1_img.blit(self.meneposX1,self.meneposY1)
            self.mene2_img.draw()
            #self.mene2_img.blit(self.meneposX2,self.meneposY2)
        else:
            if self.changingMene:
                if g.currTick>self.animationEndTick:
                    self.changingMene+=1
                    if self.changingMene==3:
                        self.finished=True
                        sendFightReady()
                    elif self.changingMene==2:
                        self.mene1_img=g.gameEngine.resManager.meneSprites[self.myMene.spriteName]["behind"]
                        self.mene1Manager.updateInfo(self.myMene.name,self.myMene.level,self.myMene.hp,self.myMene.maxhp)
                        self.startXP=self.myMene.xp
                        self.startLevel=self.myMene.level
                        self.mene1_targetHP=self.myMene.hp
                        self.mene1_currHP=self.myMene.hp
                        self.mene1Manager.setPos(self.posX1+(319-256)/2,self.meneposY1+256)
                        self.abilityButtons.updateAbilityButtons(self.myMene.attack1,self.myMene.attack2,self.myMene.attack3,self.myMene.attack4)
                        if self.abilityButtons is not None:
                            self.abilityButtons.setPos((self.posX1+319+(g.SCREEN_WIDTH-self.posX1-319-self.abilityButtons.width)/2),self.posY1)
                        self.animationStartTick=g.currTick
                        self.animationEndTick=g.currTick+self.startingAnimationLength
                self.updateMeneSwitchAnimation()
                self.ring.blit(self.animationX1,self.posY1)
                self.ring.blit(self.posX2,self.posY2)
                self.mene1_img.blit(self.animationX1+(319-256)/2,self.meneposY1)
                self.mene2_img.draw()
            else:
                self.mene2_img.set_position(self.animationX2+(319-256)/2,self.meneposY2)
                self.updateAnimation()
                self.ring.blit(self.animationX1,self.posY1)
                self.ring.blit(self.animationX2,self.posY2)
                self.mene1_img.blit(self.animationX1+(319-256)/2,self.meneposY1)
                self.mene2_img.draw()
        #if self.changingMene:
        #    if self.changingMene==1:
        #        if g.currTick>self.animationEndTick:
        #            self.changingMene==2
        #        else:
        #            xPos = 500*(1.0*g.currTick-self.animationStartTick)/(self.animationEndTick-self.animationStartTick)
        #            self.mene1_img.blit(self.meneposX1-xPos,self.meneposY1)
                    
                
        if self.currentAnimation is not None:
            #print (g.currTick-self.animationStartTick), float(self.animationEndTick-self.animationStartTick), 125*((g.currTick-self.animationStartTick)/float(self.animationEndTick-self.animationStartTick))
            self.attackText._set_y(int(self.attackAnimationStartY+100*((g.currTick-self.animationStartTick)/float(self.animationEndTick-self.animationStartTick))))
            #print self.attackText.y
            
            if self.mene1_targetHP is not None:
                if g.currTick>=self.animationEndTick:
                    self.mene1_currHP=self.mene1_targetHP
                    self.mene1_targetHP=None
                else:
                    self.mene1Manager.hpBar.setHP(self.mene1_targetHP + (self.mene1_currHP-self.mene1_targetHP)*((self.animationEndTick-g.currTick)/(self.animationEndTick-float(self.animationStartTick))))
            elif self.mene2_targetHP is not None:
                if g.currTick>=self.animationEndTick:
                    self.mene2_currHP=self.mene2_targetHP
                    self.mene2_targetHP=None
                else:
                    self.mene2Manager.hpBar.setHP(self.mene2_targetHP + (self.mene2_currHP-self.mene2_targetHP)*((self.animationEndTick-g.currTick)/(self.animationEndTick-float(self.animationStartTick))))
            if g.currTick>self.attackAnimationTick+100:
                self.attackAnimationTick=g.currTick
                self.currentAnimationSprite+=1
                if self.currentAnimationSprite>self.animationSheets[self.currentAnimation]['length']-1:
                    self.currentAnimation=None
                    self.currentAnimationSprite=0
                    sendFightReady()
                else:
                    if not self.missed:
                        self.animationSheets[self.currentAnimation]['grid'][self.currentAnimationSprite].blit(self.attackAnimationX,self.attackAnimationY)
            else:
                if not self.missed:
                    self.animationSheets[self.currentAnimation]['grid'][self.currentAnimationSprite].blit(self.attackAnimationX,self.attackAnimationY)
            self.attackText.draw()
        if self.throwingES:
            x = self.esStartX + ((g.currTick-self.throwingTick)/1000.0)*(self.esEndX-self.esStartX)
            y = self.esStartY + ((g.currTick-self.throwingTick)/1000.0)*(self.esEndY-self.esStartY)
            self.esIcon.set_position(x,y)
            self.esIcon.opacity=255
            self.esIcon.rotation = (self.esRotationAngle+360)*((g.currTick-self.throwingTick)/1000.0)
            #self.mene2_img.scale=1-(g.currTick-self.throwingTick)/1500.0
            self.esIcon.draw()
            if g.currTick-1000 > self.throwingTick:
                self.catchingES=True
                self.throwingES=False
                self.throwingPhase=0
                g.gameEngine.playSoundEffect("open_ES")
                self.throwingTick = g.currTick
        elif self.catchingES:
            if g.currTick-self.throwingPhaseTimes[self.throwingPhase] > self.throwingTick:
                if self.throwingPhase==5:
                    self.throwingPhase=3
                    self.currentEsAttempt+=1
                else:
                    self.throwingPhase+=1
                if self.throwingPhase==4 and self.currentEsAttempt!=self.esAttempts:
                    g.gameEngine.playSoundEffect("jump_ES")
                self.throwingTick = g.currTick
            if self.throwingPhase==0:
                self.catchAnimation.opacity=255
                self.catchAnimation.scale = ((g.currTick-self.throwingTick)/1000.0)
                self.catchAnimation.set_position(self.esIcon.x-self.catchAnimation.width/2,self.esIcon.y-self.catchAnimation.height/2)
                self.mene2_img_esCatch.opacity = ((g.currTick-self.throwingTick)/1000.0)*255
                self.mene2_img.opacity = (1-((g.currTick-self.throwingTick)/1000.0))*255
            elif self.throwingPhase==1:
                self.esIcon.rotation=90
                self.mene2_img.opacity = 0
                self.catchAnimation.opacity = (1-((g.currTick-self.throwingTick)/1000.0))*255
                self.mene2_img_esCatch.opacity = (1-((g.currTick-self.throwingTick)/1000.0))*255
            elif self.throwingPhase==2:
                self.catchAnimation.opacity=0
                y = self.dropY + ((1-(g.currTick-self.throwingTick)/500.0))*(self.esEndY-self.dropY)
                self.esIcon.set_position(self.esIcon.x,y)
            elif self.throwingPhase==4:
                if self.currentEsAttempt==self.esAttempts and self.currentEsAttempt!=4:
                    self.throwingPhase=6
                    g.gameEngine.playSoundEffect("open_ES")
                elif self.currentEsAttempt==self.esAttempts and self.currentEsAttempt==4 and self.result==MATCH_MENE_CAUGHT:
                    g.gameEngine.changeMusicSong(self.captureMusic,fadetime=0.1,loaded=True)
                    self.catchingES=False
                    self.statusText._set_text(WARNINGS["MENE_CAPTURED"][0] % g.enemyMene.name)
                    self.fightOver=True
                    self.endTick=g.currTick+self.endingLength
                else:
                    y = self.dropY + ((g.currTick-self.throwingTick)/250.0)*32
                    self.esIcon.set_position(self.esIcon.x,y)
            elif self.throwingPhase==5:
                y = self.dropY + (1-(g.currTick-self.throwingTick)/250.0)*32
                self.esIcon.set_position(self.esIcon.x,y)
            elif self.throwingPhase==6:
                self.mene2_img_esCatch.opacity = ((g.currTick-self.throwingTick)/1000.0)*255
                self.catchAnimation.set_position(self.dropX-self.catchAnimation.width/2,self.dropY-self.catchAnimation.height/2)
                self.catchAnimation.opacity = ((g.currTick-self.throwingTick)/1000.0)*255
            elif self.throwingPhase==7:
                self.esIcon.opacity=0
                self.mene2_img_esCatch.opacity = (1-((g.currTick-self.throwingTick)/1000.0))*255
                self.mene2_img.opacity = ((g.currTick-self.throwingTick)/1000.0)*255
                self.catchAnimation.opacity = (1-((g.currTick-self.throwingTick)/1000.0))*255
            elif self.throwingPhase==8:
                self.catchingES=False
            self.mene2_img_esCatch.draw()
            self.esIcon.draw()
            self.catchAnimation.draw()
        if self.meneDied:
            if g.currTick < self.endTick:
                self.statusText._set_y(int(g.SCREEN_HEIGHT/2+(1-(self.endTick-g.currTick)/self.endingLength)*g.SCREEN_HEIGHT/8))
            else:
                self.statusText._set_text("")
                self.meneDied=False
        if self.fightOver:
            if self.result == MATCH_MENE_CAUGHT:
                if g.currTick<self.endTick:
                    self.statusText._set_y(int(g.SCREEN_HEIGHT/2+(1-(self.endTick-g.currTick)/self.endingLength)*g.SCREEN_HEIGHT/8))
                elif not self.meneNamingPopped:
                    self.statusText._set_text("")
                    self.initNameMene()
                    self.meneNamingPopped=True
                
                self.esIcon.draw()
            elif self.result == MATCH_PLAYER_LEFT:
                self.fightOver=False
                g.gameEngine.changeMusicSong(Map.song,fadetime=0.1)
                changeGameState(GAMESTATE_INGAME)
            elif g.currTick>self.endTick:
                if g.currTick<self.levelTick:
                    if not self.statusTextChangedToLevel:
                        self.levelTick=g.currTick+self.endingLength
                        
                        self.statusText._set_text(WARNINGS["NEW_LEVEL"][0]%(self.myMene.name,str(self.startLevel)))
                        self.statusTextChangedToLevel=True
                    self.statusText._set_y(int(g.SCREEN_HEIGHT/2+(1-(self.levelTick-g.currTick)/self.endingLength)*g.SCREEN_HEIGHT/8))
                else:
                    self.fightOver=False
                    g.gameEngine.changeMusicSong(Map.song,fadetime=0.1)
                    changeGameState(GAMESTATE_INGAME)
            else:
                #print (self.startXP-self.startLevel**3), (self.endXP-self.startXP), (1-(self.endTick-g.currTick)/self.endingLength)
                #print (self.startXP-self.startLevel**3)+(self.endXP-self.startXP)*(1-(self.endTick-g.currTick)/float(self.endingLength))
                if self.changedLevel and self.endXP>=(self.startLevel+1)**3 and self.xpBar.get_progress()>=1:
                    self.changedLevel=False
                    self.startLevel+=1
                    self.levelTick=g.currTick+self.endingLength
                    g.gameEngine.playSoundEffect("levelup")
                    self.mene1Manager.updateLevel(self.startLevel)
                if g.currTick<self.xpTick and self.xpBar:
                    #print (self.startXP-self.startLevel**3)+(self.endXP-self.startXP)*(1-(self.xpTick-g.currTick)/(self.endingLength/2)), self.endXP-self.startLevel**3
                    self.xpBar.setHP((self.startXP-self.startLevel**3)+(self.endXP-self.startXP)*(1-(self.xpTick-g.currTick)/(self.endingLength/2)),((self.startLevel+1)**3-self.startLevel**3))
                self.statusText._set_y(int(g.SCREEN_HEIGHT/2+(1-(self.endTick-g.currTick)/self.endingLength)*g.SCREEN_HEIGHT/8))
        g.guiBatch.draw()
        self.statusText.draw()
        g.selectWindowBatch.draw()                                                                                                            