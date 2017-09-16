import global_vars as g
from gamelogic import *
from pyglet_gui.text_input import TextInput
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Frame, Spacer, Label
from pyglet_gui.containers import VerticalContainer, HorizontalContainer
from pyglet_gui.buttons import HighlightedButton, Button
from pyglet_gui.document import Document
from pyglet_gui.constants import HALIGN_LEFT, ANCHOR_LEFT
class ReportAnswerWindow(Manager):
    def __init__(self):
        g.reportAnswerWindowOpened = True
        self._reportid=-1
        getReport(True)
        label1=Label("Answer to Ticket",bold=True,color=g.loginFontColor)
        closeBtn =HighlightedButton("",on_release=self.delete,width=19,height=19,path='delete')
        horzCont = HorizontalContainer(content=[label1,None,closeBtn])
        #self.infoLabel = Label("No reports founds")
        self.report = Document("",is_fixed_size=True,width=g.SCREEN_WIDTH/3,height=g.SCREEN_HEIGHT/4)
        self.reportInput = TextInput(text="",padding=0,length=16,max_length=500,width=g.SCREEN_WIDTH/3,height=g.SCREEN_HEIGHT/4,multiline=True)
        deleteBtn = HighlightedButton("Delete",on_release=self.remove,width=120,height=30)
        sendBtn = HighlightedButton("Send",on_release=self.send,width=120,height=30)
        buttons = HorizontalContainer(content=[deleteBtn,Spacer(0,0),sendBtn])
        frame = Frame(VerticalContainer(content=[horzCont,self.report,self.reportInput,buttons]))
        
        Manager.__init__(self,
            frame,
            window=g.screen,
            batch=g.guiBatch,
            is_movable=False,
            theme=g.theme)
        frame.expand(g.SCREEN_WIDTH/2,height=g.SCREEN_HEIGHT/4*3)    
    def send(self,event):
        if self._reportid!=None and self._reportid!=-1:
            solveReport(self._reportid,self.reportInput.get_text())
            infoText("Ticket has been marked as solved.")
            self.clear(None)
            getReport(True)
        #print self.reportInput.get_text()
        #sendReport(self.reportInput.get_text())
        #print self.reportInput.get_text()
        #self.delete(None)
        
    def remove(self,event):
        solveReport(self._reportid,"",True)
        infoText("Ticket has been marked as solved.")
        self.clear(None)
        getReport(True)
        
    def clear(self,event):
        self._reportid=-1
        self.report.set_text("")
        self.reportInput.set_text("")
    def delete(self,event):
        g.chatFocus=False
        self.reportInput.focused = False
        super(Manager,self).delete()
        g.reportAnswerWindowOpened = False