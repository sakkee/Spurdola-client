import global_vars as g
from gamelogic import *
from pyglet_gui.text_input import TextInput
from pyglet_gui.manager import Manager
from pyglet_gui.gui import Frame, Spacer, Label
from pyglet_gui.scrollable import Scrollable
from pyglet_gui.containers import VerticalContainer, HorizontalContainer
from pyglet_gui.buttons import HighlightedButton, Button
from pyglet_gui.constants import HALIGN_LEFT, ANCHOR_LEFT
class ReportWindow(Manager):
    def __init__(self):
        g.reportWindowOpened = True
        getReport()
        label1=Label("Send Ticket",bold=True,color=g.loginFontColor)
        closeBtn =HighlightedButton("",on_release=self.delete,width=19,height=19,path='delete')
        horzCont = HorizontalContainer(content=[label1,None,closeBtn])
        #self.infoLabel = Label("No reports founds")
        self.reportInput = TextInput(text="",padding=5,length=16,max_length=400,width=g.SCREEN_WIDTH/3,height=g.SCREEN_HEIGHT/3,multiline=True)
       
        clearBtn = HighlightedButton("Clear",on_release=self.clear,width=120,height=30)
        deleteBtn = HighlightedButton("Delete",on_release=self.remove,width=120,height=30)
        sendBtn = HighlightedButton("Send",on_release=self.send,width=120,height=30)
        buttons = HorizontalContainer(content=[clearBtn,deleteBtn,sendBtn])
        frame = Frame(VerticalContainer(content=[horzCont,self.reportInput,buttons]))
        
        Manager.__init__(self,
            frame,
            window=g.screen,
            batch=g.guiBatch,
            is_movable=False,
            theme=g.theme)
        frame.expand(g.SCREEN_WIDTH/2,height=g.SCREEN_HEIGHT/4*3)    
    def send(self,event):
        sendReport(self.reportInput.get_text())
        #print self.reportInput.get_text()
        infoText('A ticket has been sent.')
        self.delete(None)
        
    def remove(self,event):
        if self.reportInput.get_text()!="":
            sendReport("")
            infoText('Your ticket has been deleted.')
            #self.clear(None)
        self.delete(None)
    def clear(self,event):
    
        self.reportInput.set_text("")
    def delete(self,event):
        g.chatFocus=False
        self.reportInput.focused = False
        super(Manager,self).delete()
        g.reportWindowOpened = False