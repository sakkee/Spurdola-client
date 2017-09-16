import global_vars as g
from gamelogic import *
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Spacer, Graphic
from pyglet_gui.containers import HorizontalContainer
from pyglet_gui.theme import Theme
from pyglet_gui.hoverbutton import HoverGraphic, HoverButton, AbilityButton
from pyglet_gui.constants import ANCHOR_BOTTOM, VALIGN_BOTTOM

class AbilityButtons(Manager):
    def __init__(self,ability1=None,ability2=None,ability3=None,ability4=None):
        
        self.a1=ability1
        self.a2=ability2
        self.a3=ability3
        self.a4=ability4
        #self.abilityCont=[]
        abilityButtons=[]
        for i in xrange(4):
            abilityButtons.append(Graphic(width=100,height=100,path='abilityoutline'))
        self.abilityCont = HorizontalContainer(content=abilityButtons,align=VALIGN_BOTTOM)
        
        Manager.__init__(self,
            self.abilityCont,
            window=g.screen,
            batch=g.guiBatch,
            is_movable=False,
            anchor=ANCHOR_BOTTOM,
            offset=(0,0),
            theme=g.theme)
        self.constructAbilityButtons()
    def setPos(self,x,y):
        self.set_position(x,y)
    def delete(self):
        super(Manager,self).delete()
    def changeDisableds(self,disabled=True):
        try:
            for ability in self.abilityCont.content:
                ability.changeDisable(disabled)
        except:
            return
        
    def updateAbilityButtons(self,ability1=None,ability2=None,ability3=None,ability4=None):
        self.a1=ability1
        self.a2=ability2
        self.a3=ability3
        self.a4=ability4
        #for i in reversed(range(len(self.abilityCont.content))):
        #    self.abilityCont.remove(self.abilityCont.content[0])
        self.constructAbilityButtons()
        self.abilityCont.layout()
    def constructAbilityButtons(self):
        for i in reversed(range(len(self.abilityCont.content))):
            self.abilityCont.remove(self.abilityCont.content[0])
        if self.a1 is not None:
            self.abilityCont.add(AbilityButton(width=100,height=100,argument=self.a1.id,on_press=sendAttack,texture=g.gameEngine.resManager.abilities[self.a1.spriteName],outline='abilityoutline',hover=onHover,hoveringType=HOVERING_ABILITY,arguments={'name':self.a1.name,'type':getAbilityTypeName(self.a1.abilityType),'info':self.a1.infotext,"args":(self.a1.power, self.a1.length)}))
        else:
            self.abilityCont.add(Graphic(width=100,height=100,path='abilityoutline'))
        if self.a2 is not None:
            self.abilityCont.add(AbilityButton(width=100,height=100,argument=self.a2.id,on_press=sendAttack,texture=g.gameEngine.resManager.abilities[self.a2.spriteName],outline='abilityoutline',hover=onHover,hoveringType=HOVERING_ABILITY,arguments={'name':self.a2.name,'type':getAbilityTypeName(self.a2.abilityType),'info':self.a2.infotext,"args":(self.a2.power, self.a2.length)}))
        else:
            self.abilityCont.add(Graphic(width=100,height=100,path='abilityoutline'))
        if self.a3 is not None:
            self.abilityCont.add(AbilityButton(width=100,height=100,argument=self.a3.id,on_press=sendAttack,texture=g.gameEngine.resManager.abilities[self.a3.spriteName],outline='abilityoutline',hover=onHover,hoveringType=HOVERING_ABILITY,arguments={'name':self.a3.name,'type':getAbilityTypeName(self.a3.abilityType),'info':self.a3.infotext,"args":(self.a3.power, self.a3.length)}))
        else:
            self.abilityCont.add(Graphic(width=100,height=100,path='abilityoutline'))
        if self.a4 is not None:
            self.abilityCont.add(AbilityButton(width=100,height=100,argument=self.a4.id,on_press=sendAttack,texture=g.gameEngine.resManager.abilities[self.a4.spriteName],outline='abilityoutline',hover=onHover,hoveringType=HOVERING_ABILITY,arguments={'name':self.a4.name,'type':getAbilityTypeName(self.a4.abilityType),'info':self.a4.infotext,"args":(self.a4.power, self.a4.length)}))
        else:
            self.abilityCont.add(Graphic(width=100,height=100,path='abilityoutline'))
        if g.esAmount>0 and not iHasMene(spriteName=g.enemyMene.spriteName):
            disabled=False
        else:
            disabled=True
        self.abilityCont.add(AbilityButton(width=50,height=50,argument=Items["es"]["id"],disabled=disabled,on_press=useES,texture=g.gameEngine.resManager.items[Items["es"]["sprite"]],outline='abilityoutline',hover=onHover,hoveringType=HOVERING_ABILITY,arguments={'name':Items["es"]["name"],'info':Items["es"]["info"],"args":()}))
        self.abilityCont.add(AbilityButton(width=50,height=50,on_press=openMeneSelector,path='mymenes',outline='abilityoutline',hover=onHover,hoveringType=HOVERING_ABILITY,arguments={'name':"Change Mene",'info':"Don't have balls do play till death?? :D","args":()}))
        self.abilityCont.add(AbilityButton(width=50,height=50,on_press=leaveMatchStartConfirm,path='leavematch',outline='abilityoutline',hover=onHover,hoveringType=HOVERING_ABILITY,arguments={'name':"Leave Match",'info':"Run away :DD pussy :D","args":()}))
        