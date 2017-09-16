import global_vars as g
import os.path
from utils import configobj #import configobj.ConfigObj

def readCfg():
    Config = None
    
    
    if not os.path.isfile('game.cfg'):
        Config = configobj.ConfigObj()
        Config.filename='game.cfg'
        #configobj.ConfigObj = open("game.cfg",'w')
        #Config.add_section("Cfg")
        Config["Resolution"]=str(g.SCREEN_WIDTH)+':'+str(g.SCREEN_HEIGHT)
        Config["Vsync"]=g.VSYNC
        Config["Fullscreen"]=g.FULLSCREEN
        Config["Screenselected"]=g.SCREENSELECTED
        Config["Selectpaint"]=g.selectPaint
        Config["Hoverpaint"]=g.hoverPaint
        Config["MUSIC"]=g.MUSIC
        Config["MUSICVOLUME"]=g.MUSICVOLUME
        Config["SOUND"]=g.SOUND
        Config["SOUNDVOLUME"]=g.SOUNDVOLUME
        #Config.set('Cfg','Resolution',str(g.SCREEN_WIDTH)+':'+str(g.SCREEN_HEIGHT))
        #Config.set('Cfg','Vsync',g.VSYNC)
        #Config.set('Cfg','Fullscreen',g.FULLSCREEN)
        #Config.set('Cfg','Screenselected',g.SCREENSELECTED)
        #Config.set('Cfg','Selectpaint',g.selectPaint)
        #Config.set('Cfg','Hoverpaint',g.hoverPaint)
        #Config.set('Cfg','MUSIC',g.MUSIC)
        #Config.set('Cfg','MUSICVOLUME',g.MUSICVOLUME)
        #Config.set('Cfg','SOUND',g.SOUND)
        #Config.write(cfgfile)
        Config.write()
    Config=configobj.ConfigObj('game.cfg')
    #Config.read("game.cfg")
    try:
        g.SCREEN_WIDTH=int(Config["Resolution"].split(":")[0])
        g.SCREEN_HEIGHT=int(Config["Resolution"].split(":")[1])
        
        #g.SCREEN_WIDTH=int(Config.get('Cfg','Resolution').split(":")[0])
        #g.SCREEN_HEIGHT=int(Config.get('Cfg','Resolution').split(":")[1])
    except:
        #cfgfile = open('game.cfg','w')
        #try:
        Config["Resolution"]=str(g.SCREEN_WIDTH)+':'+str(g.SCREEN_HEIGHT)
        #    #Config.set('Cfg','Resolution',str(g.SCREEN_WIDTH)+':'+str(g.SCREEN_HEIGHT))
        #except:
        #    #Config.add_section("Cfg")
        #    #Config.set('Cfg','Resolution',str(g.SCREEN_WIDTH)+':'+str(g.SCREEN_HEIGHT))
        Config.write()
        #cfgfile.close()
    try:
        g.VSYNC = Config["Vsync"]=='True'
        #g.VSYNC=Config.getboolean('Cfg','Vsync')
    except:
        Config["Vsync"]=g.VSYNC
        Config.write()
        #cfgfile = open('game.cfg','w')
        #Config.set('Cfg','Vsync',g.VSYNC)
        #Config.write(cfgfile)
        #cfgfile.close()
    try:
        g.FULLSCREEN = Config["Fullscreen"]=='True'
        #g.FULLSCREEN = boolean(Config["Fullscreen"])
        #g.FULLSCREEN=Config.getboolean('Cfg','Fullscreen')
    except Exception, e:
        Config["Fullscreen"]=g.FULLSCREEN
        Config.write()
        #cfgfile = open('game.cfg','w')
        #Config.set('Cfg','Fullscreen',g.FULLSCREEN)
        #Config.write(cfgfile)
        #cfgfile.close()
    try:
        g.SCREENSELECTED=int(Config["Screenselected"])
        #tmp=Config.get('Cfg','Screenselected')
        #moi = int(tmp)
        #g.SCREENSELECTED=tmp
    except:
        Config["Screenselected"]=g.SCREENSELECTED
        Config.write()
        #cfgfile = open('game.cfg','w')
        #Config.set('Cfg','Screenselected',0)
        #Config.write(cfgfile)
        #cfgfile.close()
    try:
        g.selectPaint=Config["Selectpaint"]=='True'
        #g.mouseoverPaint=Config.getboolean('Cfg','selectpaint')
    except:
        Config["Selectpaint"]=g.selectPaint
        Config.write()
        #cfgfile = open('game.cfg','w')
        #Config.set('Cfg','Selectpaint',g.selectPaint)
        #Config.write(cfgfile)
        #cfgfile.close()
    try:
        g.hoverPaint = Config["hoverpaint"]=='True'
        #g.hoverPaint=Config.getboolean('Cfg','hoverpaint')
    except:
        Config["hoverpaint"]=g.hoverPaint
        Config.write()
        #cfgfile = open('game.cfg','w')
        #Config.set('Cfg','Hoverpaint',g.hoverPaint)
        #Config.write(cfgfile)
        #cfgfile.close()
    try:
        g.MUSIC=Config["MUSIC"]=='True'
        #g.MUSIC=Config.getboolean('Cfg','MUSIC')
    except:
        Config["MUSIC"]=g.MUSIC
        Config.write()
        #cfgfile = open('game.cfg','w')
        #Config.set('Cfg','MUSIC',g.MUSIC)
        #Config.write(cfgfile)
        #cfgfile.close()
    try:
        g.MUSICVOLUME = float(Config["MUSICVOLUME"])
    except Exception, e:
        Config["MUSICVOLUME"]=g.MUSICVOLUME
        Config.write()
    try:
        g.SOUNDVOLUME = float(Config["SOUNDVOLUME"])
    except Exception, e:
        Config["SOUNDVOLUME"]=g.SOUNDVOLUME
        Config.write()
    try:
        g.SOUND=Config["SOUND"]=='True'
        #g.SOUND=Config.getboolean('Cfg','SOUND')
    except:
        Config["SOUND"]=g.SOUND
        Config.write()
        #cfgfile = open('game.cfg','w')
        #Config.set('Cfg','SOUND',g.SOUND)
        #Config.write(cfgfile)
        #cfgfile.close()
def saveCfg(key,value):
    Config = configobj.ConfigObj('game.cfg')
    Config[key]=value
    Config.write()
    #Config = ConfigParser.ConfigParser()
    #Config.read("game.cfg")
    #cfgfile = open('game.cfg','w')
    #Config.set('Cfg',key,value)
    #Config.write(cfgfile)
    #cfgfile.close()