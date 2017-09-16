import global_vars as g
from gamelogic import *
from objects import *
import time
from gui.hpbar import HpBar
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Frame, Spacer, Label, Graphic
from pyglet_gui.theme import Theme
from pyglet_gui.scrollable import Scrollable
from pyglet_gui.containers import VerticalContainer, HorizontalContainer
from pyglet_gui.buttons import HighlightedButton, Button
from pyglet_gui.hoverbutton import HoverGraphic
from pyglet_gui.constants import HALIGN_LEFT, HALIGN_CENTER,ANCHOR_LEFT, VALIGN_TOP, HALIGN_RIGHT
class MeneWindow(Manager):
    def __init__(self):
        t1=time.time()*1000
        g.meneWindowOpened = True
        label1=Label("My Menes",bold=True,color=g.loginFontColor)
        closeBtn =HighlightedButton("",on_release=self.delete,width=19,height=19,path='delete')
        self.meneCont= []
        self.menes=[]
        self.established=False
        for c in meneList:
            self.menes.append({"name":c.name,
                               "hp":c.hp,
                               "maxhp":c.maxhp,
                               "xp":c.xp,
                               "level":c.level,
                               "power":c.power,
                               "id":c.ID,
                               "defense":c.defense,
                               "speed":c.speed,
                               "attack1":c.attack1,
                               "attack2":c.attack2,
                               "attack3":c.attack3,
                               "attack4":c.attack4,
                               "sprite":c.spriteName,
                               "defaultmene":c.defaultMene})
        #self.menes = [{"name":"Hitler","hp":100,"level":1,"power":50,"defense":40,"speed":60,"sprite":'americanbear'},{"name":"Stalin","hp":100,"level":1,"power":50,"defense":40,"speed":60,"sprite":'lorslara'},{"name":"Ebin","hp":100,"level":1,"power":50,"defense":40,"speed":60,"sprite":'squadlider'},{"name":"Mao","hp":100,"level":1,"power":50,"defense":40,"speed":60,"sprite":'mongolbear'},{"name":"Uusi mene","hp":100,"level":1,"power":50,"defense":40,"speed":60,"sprite":'mongol'},{"name":"Hintti","hp":50,"level":15,"power":60,"defense":50,"speed":70,'sprite':'uusimene'}]
        self.selectedMene=getDefaultMeneID()
        
        for i in range(6):
            if i < len(self.menes):
                if self.menes[i]["id"]==self.selectedMene:
                    menebutton = Button("",on_press=self.updateWindow,width=64,height=64, argument=self.menes[i]["id"],texture=g.gameEngine.resManager.meneSprites[self.menes[i]["sprite"]]["portrait"],is_pressed=True,outline='menewindowbutton')
                else:
                    menebutton = Button("",on_press=self.updateWindow,width=64,height=64, argument=self.menes[i]["id"],texture=g.gameEngine.resManager.meneSprites[self.menes[i]["sprite"]]["portrait"],is_pressed=False,outline='menewindowbutton')
                nameLabel = Label(self.menes[i]["name"],bold=True,color=g.npcColor)
                levelLabel = Label("Lvl " + str(self.menes[i]["level"]),color=g.whiteColor,font_size=g.theme["font_size_small"])
                defaultMeneLabel=None
                if self.menes[i]["defaultmene"]==1:
                    defaultMeneLabel= Label('Default Mene',color=g.whiteColor,font_size=g.theme["font_size_small"])
                    #self.meneCont.append(HorizontalContainer(content=[menebutton,VerticalContainer(content=[nameLabel,levelLabel,defaultMeneLabel],align=HALIGN_LEFT)],align=HALIGN_CENTER))
                #else:
                self.meneCont.append(HorizontalContainer(content=[menebutton,VerticalContainer(content=[nameLabel,levelLabel,defaultMeneLabel],align=HALIGN_LEFT)],align=HALIGN_CENTER))
            else:
                
                menebutton = Button("",width=64,height=64,is_pressed=False,path='menewindowbutton',disabled=True)
                self.meneCont.append(menebutton)
       
        self.menelisting = VerticalContainer(content=[label1,VerticalContainer(content=self.meneCont,align=HALIGN_LEFT)])
        
        properties=Label("Mene Properties",bold=True,color=g.loginFontColor)
        #horzCont = HorizontalContainer(content=[properties,closeBtn])
        nameinfoLabel = Label("Name:",color=g.whiteColor)
        self.selectedNAME = Label("Uusi mene",bold=True,color=g.npcColor)
        
        levelinfoLabel = Label("Level:",color=g.whiteColor)
        self.selectedLevel = Label("0",bold=True,color=g.npcColor)
        
        hpinfoLabel = Label("HP:",color=g.whiteColor)
        self.selectedHp = Label("0",bold=True,color=g.npcColor)
        
        xpinfoLabel = Label("XP:",color=g.whiteColor)
        #self.selectedXp = Label("0",bold=True,color=g.npcColor)
        
        attackinfoLabel = Label("Power:",color=g.whiteColor)
        self.selectedAttack = Label("0",bold=True,color=g.npcColor)
        
        self.hpBar = HpBar()
        
        self.defaultButton = HighlightedButton("Set Default Mene :D",argument=None,on_release=makeDefaultMene)
        
        self.xpBar = HpBar(type="xp",height=20,width=100)
        
        defenseinfoLabel = Label("Defense:",color=g.whiteColor)
        self.selectedDefense = Label("0",bold=True,color=g.npcColor)
        
        speedinfoLabel = Label("Speed:",color=g.whiteColor)
        self.selectedSpeed = Label("0",bold=True,color=g.npcColor)
        
        #selectTheme = Theme({'uusimene': {
        #                "image": {
        #                    "source": 'uusimene_front.png'
        #                },
        #                "gui_color": [255,255,255,255]
        #            }
        #        },resources_path=g.dataPath+'/menes/'
        #    )
            
        self.picture = Graphic(texture=g.gameEngine.resManager.meneSprites['uusimene']['front'])
        abilities = ['burger', 'burger']
        #abilityTheme = self.constructAbilityTheme(abilities)
        abilityButtons=[]
        for i in xrange(4):
            #if i<len(abilities):
            #    self.abilityButtons.append(HoverGraphic(width=50,height=50,path=abilities[i],alternative=abilityTheme,outline='abilityoutline',hover=onHover,hoveringType=HOVERING_ABILITY,arguments={'name':'Burger Attack','type':'Attack','info':'Throws a burger at the enemy. Deals X damage.'}))
            #else:
            abilityButtons.append(Graphic(width=50,height=50,path='abilityoutline'))

        
        infoCont1 = VerticalContainer([nameinfoLabel,levelinfoLabel,xpinfoLabel],align=HALIGN_LEFT)
        infoCont2 = VerticalContainer([attackinfoLabel,defenseinfoLabel,speedinfoLabel],align=HALIGN_LEFT)
        statsCont1 = VerticalContainer([self.selectedNAME,self.selectedLevel,self.xpBar],align=HALIGN_LEFT)
        statsCont2 = VerticalContainer([self.selectedAttack,self.selectedDefense,self.selectedSpeed],align=HALIGN_LEFT)
        
        infoAndStatsCont = HorizontalContainer([infoCont1,statsCont1,infoCont2,statsCont2])
        
        self.abilityCont = HorizontalContainer(abilityButtons,padding=10)
        rightFrame = VerticalContainer(content=[properties,self.picture,self.hpBar,infoAndStatsCont,self.abilityCont,self.defaultButton])
        total = HorizontalContainer(content=[self.menelisting,Spacer(30,0),rightFrame,closeBtn],align=VALIGN_TOP)
        Manager.__init__(self,
            Frame(total),
            window=g.screen,
            batch=g.guiBatch,
            is_movable=False,
            anchor=ANCHOR_LEFT,
            offset=(40,int(g.SCREEN_HEIGHT*g.WINDOW_POSY_RELATIVE)),
            theme=g.theme)
        self.changeInfos(self.selectedMene)
    
    def updateWindow(self,argument):
        for c in self.meneCont:
            try:
                if c.content[0].arg!=argument and c.content[0]._is_pressed:
                    c.content[0].changeStateWithoutFnc()
            except:
                break
        for c in self.meneCont:
            try:
                if c.content[0].arg==argument and not c.content[0]._is_pressed:
                    c.content[0].changeStateWithoutFnc()
            except:
                break
        
        self.changeInfos(argument)
    def constructAbilityButtons(self,a1,a2,a3,a4):
        if a1 is not None:
            self.abilityCont.add(HoverGraphic(width=50,height=50,outline='abilityoutline',hover=onHover,texture=g.gameEngine.resManager.abilities[a1.spriteName],hoveringType=HOVERING_ABILITY,arguments={'name':a1.name,'type':getAbilityTypeName(a1.abilityType),'info':a1.infotext,"args":(a1.power, a1.length)}))
        else:
            self.abilityCont.add(Graphic(width=50,height=50,path='abilityoutline'))
        if a2 is not None:
            self.abilityCont.add(HoverGraphic(width=50,height=50,outline='abilityoutline',texture=g.gameEngine.resManager.abilities[a2.spriteName],hover=onHover,hoveringType=HOVERING_ABILITY,arguments={'name':a2.name,'type':getAbilityTypeName(a2.abilityType),'info':a2.infotext,"args":(a2.power, a2.length)}))
        else:
            self.abilityCont.add(Graphic(width=50,height=50,path='abilityoutline'))
        if a3 is not None:
            self.abilityCont.add(HoverGraphic(width=50,height=50,outline='abilityoutline',texture=g.gameEngine.resManager.abilities[a3.spriteName],hover=onHover,hoveringType=HOVERING_ABILITY,arguments={'name':a3.name,'type':getAbilityTypeName(a3.abilityType),'info':a3.infotext,"args":(a3.power, a3.length)}))
        else:
            self.abilityCont.add(Graphic(width=50,height=50,path='abilityoutline'))
        if a4 is not None:
            self.abilityCont.add(HoverGraphic(width=50,height=50,outline='abilityoutline',texture=g.gameEngine.resManager.abilities[a4.spriteName],hover=onHover,hoveringType=HOVERING_ABILITY,arguments={'name':a4.name,'type':getAbilityTypeName(a4.abilityType),'info':a4.infotext,"args":(a4.power, a4.length)}))
        else:
            self.abilityCont.add(Graphic(width=50,height=50,path='abilityoutline'))
        
    def changeInfos(self,ID):
        selectedMene = None
        for c in self.menes:
            if c["id"]==ID:
                
                selectedMene=c
        #print selectedMene, self.selectedMene
        if selectedMene != None and (ID!=self.selectedMene or (ID==self.selectedMene and not self.established)):
            self.selectedMene=ID
            for i in reversed(range(len(self.abilityCont.content))):
                self.abilityCont.remove(self.abilityCont.content[0])
            #self.abilityCont.unload_content()
            #for c in self.abilityCont.content:
            #    self.abilityCont.remove()
            #for abilityButton in self.abilityButtons:
            #    abilityButton.unload()
            #print self.abilityCont.__dict__
            #for abilityButton in self.abilityButtons:
            #    print abilityButton.__dict__
            #    self.abilityCont.remove(abilityButton)
            self.constructAbilityButtons(selectedMene["attack1"],selectedMene["attack2"],selectedMene["attack3"],selectedMene["attack4"])
            #self.abilityCont.load_content()
            #self.abilityCont.remove(self.abilityButtons[0])
            #self.abilityCont.add(Graphic(width=50,height=50,path='abilityoutline'),0)
            self.selectedNAME.set_text(selectedMene["name"])
            self.selectedLevel.set_text(str(selectedMene["level"]))
            #self.selectedHp.set_text(str(selectedMene["hp"])+' / '+str(selectedMene["maxhp"]))
            self.hpBar.setHP(selectedMene["hp"],selectedMene["maxhp"])
            self.xpBar.setHP(selectedMene["xp"]-selectedMene["level"]**3,(selectedMene["level"]+1)**3-selectedMene["level"]**3)
            #self.selectedXp.set_text(str(selectedMene["xp"]))
            self.selectedAttack.set_text(str(selectedMene["power"]))
            self.selectedDefense.set_text(str(selectedMene["defense"]))
            self.selectedSpeed.set_text(str(selectedMene["speed"]))
            if selectedMene["defaultmene"]==1:
                self.defaultButton._label._set_text("Dis is default mene")
            else:
                self.defaultButton._label._set_text("Set Default Mene :D")
            self.defaultButton.layout()
            self.defaultButton.arg=ID
            
            #selectTheme = Theme({selectedMene["sprite"]: {
            #            "image": {
            #                "source": selectedMene["sprite"]+'_front.png'
            #            },
            #            "gui_color": [255,255,255,255]
            #        }
            #    },resources_path=g.dataPath+'/menes/'
            #)
            #self.picture._path=selectedMene["sprite"]
            #self.picture._alt=selectTheme
            self.picture.textureTmp = g.gameEngine.resManager.meneSprites[selectedMene["sprite"]]['front']
            #self.picture.unload_graphics(False)
            self.picture.reload()
            self.picture.layout()
            self.established=True
    def delete(self,event):
        super(Manager,self).delete()
        g.meneWindowOpened = False
        if g.hoveringType==HOVERING_ABILITY:
            g.gameEngine.graphics.hoverWindow.delete(None)
        
    #def on_mouse_motion(self,x,y,dx,dy):
    #    print self._hover