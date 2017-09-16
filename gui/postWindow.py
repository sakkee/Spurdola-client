import global_vars as g
from gamelogic import *
from objects import *
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Frame, Spacer, Label
from pyglet_gui.theme import Theme
from pyglet_gui.scrollable import Scrollable
from pyglet_gui.containers import VerticalContainer, HorizontalContainer
from pyglet_gui.buttons import HighlightedButton
from pyglet_gui.document import Document
from pyglet_gui.constants import HALIGN_LEFT, HALIGN_CENTER,ANCHOR_LEFT, VALIGN_TOP, HALIGN_RIGHT
class PostWindow(Manager):
    def __init__(self):
        g.postWindowOpened = True
        label1=Label("Notifications",bold=True,color=g.loginFontColor)
        closeBtn =HighlightedButton("",on_release=self.delete,width=19,height=19,path='delete')
        self.postCont= []
        #self.menes = [{"name":"Hitler","hp":100,"level":1,"power":50,"defense":40,"speed":60,"sprite":'americanbear'},{"name":"Stalin","hp":100,"level":1,"power":50,"defense":40,"speed":60,"sprite":'lorslara'},{"name":"Ebin","hp":100,"level":1,"power":50,"defense":40,"speed":60,"sprite":'squadlider'},{"name":"Mao","hp":100,"level":1,"power":50,"defense":40,"speed":60,"sprite":'mongolbear'},{"name":"Uusi mene","hp":100,"level":1,"power":50,"defense":40,"speed":60,"sprite":'mongol'},{"name":"Hintti","hp":50,"level":15,"power":60,"defense":50,"speed":70,'sprite':'uusimene'}]
        #self.selectedMene=self.menes[0]["name"]
        for c in g.mails:
            label=Label(c["s"],bold=True,color=g.guiNameColor,font_size=g.theme["font_size"]+2)
            label1=Label(c["t"][:16]+'...',color=g.whiteColor)
            deleteBtn = HighlightedButton("",on_release=self.deletemail,width=14,height=14,path='delete_alt',argument=c["id"])
            openBtn = HighlightedButton("",on_release=self.openmail,width=20,height=21,path='mailopen',argument=c["id"])
            self.postCont.append(VerticalContainer(content=[HorizontalContainer(content=[openBtn,label,deleteBtn]),label1],align=HALIGN_LEFT))
        self.vertCont=VerticalContainer(self.postCont,align=VALIGN_TOP)
        self.report = Document("",is_fixed_size=True,height=g.SCREEN_HEIGHT/2,width=g.SCREEN_WIDTH/5)
        self.scrollable = Scrollable(content=self.vertCont,height=g.SCREEN_HEIGHT/2,width=g.SCREEN_WIDTH/5)
        total = HorizontalContainer(content=[self.scrollable,self.report,closeBtn],align=VALIGN_TOP)
        Manager.__init__(self,
            Frame(total),
            window=g.screen,
            batch=g.guiBatch,
            is_movable=False,
            anchor=ANCHOR_LEFT,
            offset=(40,int(g.SCREEN_HEIGHT*g.WINDOW_POSY_RELATIVE)),
            theme=g.theme)
        if len(self.postCont)>0:
            self.openmail(self.postCont[0]._content[0]._content[0].arg)
        #self.changeInfos(self.selectedMene)
        #print str(int(time.time()*1000-t1)),"TIMEEE"
 
    def delete(self,event):
        super(Manager,self).delete()
        g.postWindowOpened = False
        
    def deletemail(self,event):
        deleteMail(event)
        for c in self.postCont:
            if c._content[0]._content[0].arg == event:
                self.vertCont.remove(c)
                self.postCont.remove(c)
                for d in g.mails:
                    if d["id"]==event:
                        g.mails.remove(d)
        if len(self.postCont)>0:
            self.openmail(self.postCont[0]._content[0]._content[0].arg)
            self.scrollable.reset_size()
        else:
            self.delete(None)
            g.gameEngine.graphics.normalUI.removeMail()
    def openmail(self,event):
        text=''
        for c in g.mails:
            if c["id"]==event:
                text=c["t"]+'\n\nt. '+c["s"]
        self.report.set_text(text)