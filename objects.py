from constants import *

class TmpPlayer():
    def __init__(self):
        self.sprite = None
        self.highlightSprite=None
        self.moveTick = None
        self.xOffset = 0
        self.yOffset = 0
        self.moving = False
        self.spriteFacing=0
        self.nextMoveDir = -1
        self.nextStep=False
        self.nextRealMove =None
        self.nextDir=None
        self.lastMsgTick = 0
        self.lastMsg = None
        self.chatBubbleTime = CHAT_NORMALMSG_TIME
        self.nameText = None
        self.movePath=[]
        self.guild=None
        self.posx=0
        self.posy=0
        self.battling=None
class PlayerClass():
    def __init__(self):
        # General
        self.name = ""
        
        self.hat = 1
        self.face=0
        self.shoes=0
        self.shirt = 0
        self.playerType=0
        self.access = 0

        self.map = "Start"  
        self.x = 0 
        self.y = 0  
        self.dir = 0

        self.tmpPlayer = TmpPlayer()

class NPCClass():
    def __init__(self):
        self.name = ""
        self.hat = 1
        self.face=0
        self.shoes=0
        self.shirt = 0
        self.sprite=0
        self.dir = 1
        self.x=0
        self.y=0
        self.playerType=1
        self.walkingType=0
        self.radius=0
        self.text=""
        self.tmpPlayer = TmpPlayer()
        self.maps=[]#[name,x,y,direction]
class TileClass():
    def __init__(self):
        self.l1 = None
        self.l2 = None
        self.l3 = None
        self.f = None
        self.t = 0
        self.d1 = None
        self.d2 = 0
        self.d3 = 0



class MapClass():
    def __init__(self):
        self.width = 15
        self.height = 11
        self.tile = []
        self.menes=[]
        self.song=""
        self.walls=[]
        self.death = ["",0,0]

class Menemon():
    def __init__(self,name="",hp=1,maxhp=1,xp=0,level=1,power=1,defense=1,speed=1,spriteName="",attack1=None,attack2=None,attack3=None,attack4=None,defaultMene=2,ID=None):
        self.ID=ID
        self.name=name
        self.hp = hp
        self.maxhp=maxhp
        self.xp=xp
        self.level=level
        self.power = power
        self.defense=defense
        self.speed = speed
        if attack1 is not None:
            self.attack1=Ability(attack1['id'],attack1['name'],attack1['infotext'],attack1['length'],attack1['targetType'],attack1['missChance'],attack1['critChance'],attack1['targetFactor'],attack1['abilityType'],attack1['power'],attack1['spriteName'],attack1["animation"])
        else:
            self.attack1=None
        if attack2 is not None:
            self.attack2=Ability(attack2['id'],attack2['name'],attack2['infotext'],attack2['length'],attack2['targetType'],attack2['missChance'],attack2['critChance'],attack2['targetFactor'],attack2['abilityType'],attack2['power'],attack2['spriteName'],attack2["animation"])
        else:
            self.attack2=None
        if attack3 is not None:
            self.attack3=Ability(attack3['id'],attack3['name'],attack3['infotext'],attack3['length'],attack3['targetType'],attack3['missChance'],attack3['critChance'],attack3['targetFactor'],attack3['abilityType'],attack3['power'],attack3['spriteName'],attack3["animation"])
        else:
            self.attack3=None
        if attack4 is not None:
            self.attack4=Ability(attack4['id'],attack4['name'],attack4['infotext'],attack4['length'],attack4['targetType'],attack4['missChance'],attack4['critChance'],attack4['targetFactor'],attack4['abilityType'],attack4['power'],attack4['spriteName'],attack4["animation"])
        else:
            self.attack4=None
        
        self.spriteName=spriteName
        self.defaultMene=defaultMene
class Ability():
    def __init__(self,id=None,name="",infotext="",length=1,targetType=1,missChance=0,critChance=10,targetFactor=0,abilityType=0,power=1,spriteName="",animation=""):
        self.id=id
        self.name=name
        self.infotext=infotext
        self.length=length
        self.targetType=targetType
        self.missChance=missChance
        self.critChance=critChance
        self.targetFactor=targetFactor
        self.abilityType=abilityType
        self.power=power
        self.spriteName=spriteName
        self.animation=animation

class PartyMember():
    def __init__(self,name,shirt,shoes,face,hat,access):
        self.name=name
        self.shirt=shirt
        self.shoes=shoes
        self.face=face
        self.hat=hat
        self.access=access
        self.texture=None
# Data initializations
Map = MapClass()

Players = []
myPlayer=PlayerClass()
friendList = []
ignoreList = []
npcList=[]
meneList=[]
guildList=[]
Items={}