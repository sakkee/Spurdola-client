from pyglet_gui.gui import Label, Graphic
from pyglet_gui.containers import VerticalContainer, HorizontalContainer
from pyglet_gui.constants import HALIGN_LEFT, VALIGN_BOTTOM,HALIGN_RIGHT
from constants import *
import global_vars as g

def abilityHoverTemplate(args):
    cont=[]
    if 'name' in args:
        cont.append(Label(args['name'],bold=True,font_size=g.theme['font_size']+1))
    if 'type' in args:
        cont.append(Label(args['type']))
    if 'info' in args:
        cont.append(Label(args['info'].format(*args['args']),width=TILESIZE*4,multiline=True,color=g.loginFontColor))
    return VerticalContainer(cont,align=HALIGN_LEFT,padding=0)

def pingHoverTemplate(text):
    return Label("Ping: %.0f ms" % text)
    
def bagHoverTemplate(money,es):
    moneyTmp = money/100.0
    moneyCont = HorizontalContainer(content=[Label("%.2f" % moneyTmp),Graphic("euro")])
    esCont = HorizontalContainer(content=[Label("%s" % es),Graphic('es_icon')])
    return VerticalContainer(content=[esCont,moneyCont],align=HALIGN_RIGHT)
    
def itemHoverTemplate(args):
    cont=[]
    if 'name' in args:
        cont.append(Label(args['name'],bold=True,font_size=g.theme['font_size']+1))
    if 'type' in args:
        cont.append(Label(args['type']))
    if 'info' in args:
        cont.append(Label(args['info'].format(*args['args']),width=TILESIZE*4,multiline=True,color=g.loginFontColor))
    return VerticalContainer(cont,align=HALIGN_LEFT,padding=0)