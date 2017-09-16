import os
import pyglet
from pyglet_gui.theme import Theme
from pyglet_gui.manager import ViewerManagerGroup


# path for data files
dataPath = 'data'
connectedToLoginServer=True
loginRSAKey=None
#loginmenu
dx = 0
# connection
gameEngine = None
soundEngine = None

tcpConn = None
connector = None
isConnected = False
gameIP='login.sakkee.org'
gamePORT=2729
loginToken=None

clothingPairs=None

#fps and ticks
FPS = 1000
currTick = 0
lastTick=0
showFps=False

# gameloop
inGame = False
isLogging = True
gameState = 0
connectionStatus = ""

updateAvailable=False
banned=None
guildName=None
chatFocus = False
myGuildAccess=0

esAmount=0
moneyAmount=0


cursorUp =  pyglet.window.ImageMouseCursor(pyglet.image.load(dataPath+'/gui/cursorUp.png'), 1, 18)
cursorDown = pyglet.window.ImageMouseCursor(pyglet.image.load(dataPath+'/gui/cursorDown.png'), 1, 26)
gameIcon = pyglet.image.load(dataPath+'/icons/gameicon.png')
# input
inpDIR_UP = False
inpDIR_DOWN = False
inpDIR_LEFT = False
inpDIR_RIGHT = False

tmpMapTiles=1

# freeze controls when getting map
gettingMap = False

# mouse position (and tile position)
cursorX = 0
cursorY = 0
cursorXTile = 0
cursorYTile = 0
cursorTile = 0
cursorSelectedTile = [-1,-1]
cursorTarget = None
cursorRound=-1
offSetX = 0
offSetY = 0
redBlockX=0
redBlockY=0
redBlockTick = 0
redBlockDisabled = 1
selectPaint=False
hoverTarget=None
hoverPaint=True
talkingToNpc=None
movePath=None
currMeneID=None
hoveringType=None

# --------------------
MAX_HAT=2
MAX_FACE=3
MAX_SHIRT=3
MAX_SHOES=2
###SETTINGS###
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FULLSCREEN=False
VSYNC=False
SCREENSELECTED=0
WINDOW_POSY_RELATIVE=0.12
MUSIC=True
MUSICVOLUME=0.1
SOUNDVOLUME=0.15
SOUND=True
# sdl
screen = None
alertBatch = pyglet.graphics.Batch()
chatBubbleBatch = pyglet.graphics.Batch()
guiBatch = pyglet.graphics.Batch()
nameBatch = pyglet.graphics.Batch()
selectWindowBatch=pyglet.graphics.Batch()
#background=pyglet.graphics.OrderedGroup(0)
#foreground=pyglet.graphics.OrderedGroup(10)
# surfaces
gameSurfaceXOffset = 0
gameSurfaceYOffset = 0

escWindowOpened = False
settingsWindowOpened = False
friendWindowOpened = False
ignoreWindowOpened = False
selectWindowOpened = False
npcTalkWindowOpened = False
gameSettingsWindowOpened=False
adminWindowOpened=False
meneWindowOpened=False
reportWindowOpened = False
reportAnswerWindowOpened = False
postWindowOpened = False
guildWindowOpened=False
selectedWindowOpened=False
partyWindowOpened=False
popupWindowOpened=False
selectMeneWindowOpened = False
keybindingsWindowOpened=False
popupWindow=None

latencyTick=0
latency=0
lastLatencies=[0,0,0]
latencyType = 0

#AUDIO#
fadeTick=0
fadeTime=3.0
fadingOut=False
fadingIn=False

enemyMene=None
defaultMene=None
turn=1
enemyMeneAnimations=[]
partyMembers=[]
mePartyleader=False
tmpName=''
#tmp#
spriteName="uusimene.png"
# fonts
''' change these to customize the in-game fonts '''
#defaultFont = pygame.font.Font(dataPath + '/fonts/Lato-Regular.ttf', 24)
pyglet.font.add_file(dataPath+'/fonts/Lato-Regular.ttf')
loginFont = pyglet.font.load('Lato-Regular')
pyglet.font.add_file(dataPath+'/fonts/segoeui.ttf')
defaultFont = pyglet.font.load('Segoe UI')
pyglet.font.add_file(dataPath+'/fonts/password.ttf')
defaultPWFont = pyglet.font.load('password')

#these should be taken somewhere else...
loginFontColor = [250,200,50,255]
nameColor = (15, 93, 12,255)
nameColorLighter=(15, 150, 12,255)
guiNameColor=(30,230,30,255)
whiteColor = (255,255,255,255)
postColor = (128,0,0,255)
errorColor = (150,0,0,255)
postBgColor = (243,230,222,255)
helpColor = (34,97,153,255)
greenColor = (0,150,0,255)
partyColor = (110,110,245,255)
whisperColor = (150,0,150,225)
npcColor = (230,230,30,255)
npcColorLighter = (140,140,15,255)
friendColor = (30,30,230,255)
friendColorLighter=(15,15,150,255)
guiFriendColor=(100,200,255,255)
greentextColor=(120,153,34,255)
adminColor =(128,0,128,255)
adminColorLighter=(190,0,190,255)
modColor=(255,0,0,255)
blackColor=(0,0,0,255)
partyNameColor = (200,230,230,255)
friendNameColor = (200,250,200,255)



theme = Theme({
    "font": defaultFont.name,
    "font_size": 16,
    "font_size_small": 10,
    "gui_color": [255, 255, 255, 255],
    "disabled_color": [160, 160, 160, 255],
    "text_color": [220,220,220, 255],
    "focus_color": [255, 255, 255, 64],
    "highlight_color": [255, 255,255, 255],
    "button": {
       "down": {
           "highlight": {
                "image": {
                   "source": "button_down.png",
                   "frame": [6,6,6,6],
                   "padding": [5,5,3,3]
               },
               "gui_color": [255,255,255,255],
                "text_color": loginFontColor
           },
           "image": {
               "source": "button_press.png",
               "frame": [6,6,6,6],
               "padding": [5,5,3,3]
           },
           "gui_color": [255,255,255,255],
           "text_color": loginFontColor
       },
       "up": {
           "highlight": {
                "image": {
                   "source": "button_down.png",
                   "frame": [6,6,6,6],
                   "padding": [5,5,3,3]
               },
               "gui_color": [255,255,255,255],
               "text_color": loginFontColor
           },
           "image": {
               "source": "button_up.png",
               "frame": [6,6,6,6],
               "padding": [5,5,3,3]
           },
           "gui_color": [255,255,255,255],
           "text_color": loginFontColor
       },
       "font_size": 13
    },
    "frame": {
        "image": {
            "source": "dialog_alternative_2.png",
            "frame": [13,13,10,10], #12,10,9,8
            "padding": [15, 15, 12, 10]
        },
        "gui_color":[255,255,255,255],
        
        },
    "frame_npc_talk_shop": {
        "image": {
            "source": "dialog_npc_talk_shop.png",#dialogtest2
            "frame": [13,13,10,10], #12,10,9,8
            "padding": [15, 15, 12, 10]
        },
        "gui_color":[255,255,255,255],
        
        },
    "frame_npc_talk": {
        "image": {
            "source": "dialog_npc_talk.png",#dialogtest2
            "frame": [13,13,10,10], #12,10,9,8
            "padding": [15, 15, 12, 10]
        },
        "gui_color":[255,255,255,255],
        
        },
    "frame_alternative": {
        "image": {
            "source": "dialog_alternative_1.png",
            "frame": [7,7,7,7], #12,10,9,8
            "padding": [8,8, 5, 5]
        },
        "gui_color":[255,255,255,255],
        
        },
    "input": {
       "image": {
           "source": "input_alternative.png",
           "frame": [5,5,5,5],
           "padding": [3, 3, 2, 3]
       },
       "focus_color": [0,0,0,0],
       "focus": {
           "image": {
               "source": "input_alternative.png"
           }
       },
       "gui_color": [255,255,255,255],
    },
    "dropdown": {
       "pulldown": {
           "image": {
            "source": "dialog_alternative_1.png",
            "frame": [7,7,7,7],
            "padding": [8, 8, 5, 5]
        },
        "gui_color":[255,255,255,220],
        "font_size": 12
       },
       "image": {
           "source": "button_up.png",
           "frame": [6,6,6,6],
           "padding": [6, 6, 6, 6]
       },
       "highlight": {
            "image": {
               "source": "button_down.png",
               "frame": [6,6,6,6],
               "padding": [0,0,0,0]
           },
           "gui_color": [255,255,255,255],
            "text_color": loginFontColor
       },
       "text_color": loginFontColor,
       "font_size": 12
   },
   "vscrollbar": {
       "knob": {
           "image": {
               "source": "vscrollbar.png",
               "region": [0, 16, 16, 16],
               "frame": [0, 6, 16, 4],
               "padding": [0, 0, 0, 0]
           },
           "offset": [0, 0]
       },
       "bar": {
           "image": {
               "source": "vscrollbar.png",
               "region": [0, 64, 16, 16]
           },
           "padding": [0, 0, 0, 0]
       }
   },
   "checkbox": {
        "checked": {
            "image": {
               "source": "checkbox_checked.png",
               "frame": [4, 4, 4, 4]
           }
       },
       "unchecked": {
            "image": {
               "source": "checkbox.png",
               "frame": [4,4,4,4]
           }
       }
   },
   'chatwhisper': {
       "down": {
           "highlight": {
                "image": {
                   "source": "chatwhisperhighlighted.png"
               }
           },
           "image": {
               "source": "chatwhisperhighlighted.png"
           }
       },
       "up": {
           "highlight": {
                "image": {
                   "source": "chatwhisperhighlighted.png"
               }
           },
           "image": {
               "source": "chatwhisper.png"
           }
       },
       "gui_color": [255,255,255,255]
    },
    'delete_alt': {
        'down': {
            "highlight": {
                "image": {
                    "source": "deletehighlighted.png"
                }
            },
            "image": {
               "source": "deletehighlighted.png"
           }
        },
        'up': {
            "highlight": {
                "image": {
                    "source": "deletehighlighted.png"
                }
            },
            "image": {
               "source": "delete.png"
           }
        }
    },
   'delete': {
        'down': {
            "highlight": {
                "image": {
                    "source": "closebuttondown.png"
                }
            },
            "image": {
               "source": "closebuttonpress.png"
           }
        },
        'up': {
            "highlight": {
                "image": {
                    "source": "closebuttondown.png"
                }
            },
            "image": {
               "source": "closebuttonup.png"
           }
        },
        "gui_color": [255,255,255,255],
        "text_color": loginFontColor
    },
    "btn_friendwindow": {
       "down": {
           "highlight": {
                "image": {
                   "source": "friendshighlighted.png"
               }
           },
           "image": {
               "source": "friendshighlighted.png"
           }
       },
       "up": {
           "highlight": {
                "image": {
                   "source": "friendshighlighted.png"
               }
           },
           "image": {
               "source": "friends.png"
           }
       }
    },
    "mail": {
       "down": {
           "highlight": {
                "image": {
                   "source": "mailhighlighted.png"
               }
           },
           "image": {
               "source": "mailhighlighted.png"
           }
       },
       "up": {
           "highlight": {
                "image": {
                   "source": "mailhighlighted.png"
               }
           },
           "image": {
               "source": "mail.png"
           }
       }
    },
    "mailopen": {
       "down": {
           "highlight": {
                "image": {
                   "source": "mailopenhighlighted1.png"
               }
           },
           "image": {
               "source": "mailopenhighlighted1.png"
           }
       },
       "up": {
           "highlight": {
                "image": {
                   "source": "mailopenhighlighted1.png"
               }
           },
           "image": {
               "source": "mailopen1.png"
           }
       }
    },
    "guild": {
       "down": {
           "highlight": {
                "image": {
                   "source": "guildhighlighted.png"
               }
           },
           "image": {
               "source": "guildhighlighted.png"
           }
       },
       "up": {
           "highlight": {
                "image": {
                   "source": "guildhighlighted.png"
               }
           },
           "image": {
               "source": "guild.png"
           }
       }
    },
    "close": {
       "down": {
           "highlight": {
                "image": {
                   "source": "closebuttondown.png"
               }
           },
           "image": {
               "source": "closebuttonpress.png"
           }
       },
       "up": {
           "highlight": {
                "image": {
                   "source": "closebuttondown.png"
               }
           },
           "image": {
               "source": "closebuttonpress.png"
           }
       },
       "gui_color": [255,255,255,255]
    },
    "es": {
       "down": {
           "highlight": {
                "image": {
                   "source": "goldeneshighlighted.png"
               }
           },
           "image": {
               "source": "goldeneshighlighted.png"
           }
       },
       "up": {
           "highlight": {
                "image": {
                   "source": "goldeneshighlighted.png"
               }
           },
           "image": {
               "source": "goldenes.png"
           }
       },
       "gui_color": [255,255,255,255]
    },
    "menes": {
       "down": {
           "highlight": {
                "image": {
                   "source": "menes.png"
               }
           },
           "image": {
               "source": "menes.png"
           }
       },
       "up": {
           "highlight": {
                "image": {
                   "source": "menes.png"
               }
           },
           "image": {
               "source": "meneshighlighted.png"
           }
       },
       "gui_color": [255,255,255,255]
    },
    "btn_ignorewindow": {
       "down": {
           "highlight": {
                "image": {
                   "source": "ignoreshighlighted.png"
               }
           },
           "image": {
               "source": "ignoreshighlighted.png"
           }
       },
       "up": {
           "highlight": {
                "image": {
                   "source": "ignoreshighlighted.png"
               }
           },
           "image": {
               "source": "ignores.png"
           }
       },
       "gui_color": [255,255,255,255]
    },
    "bag": {
       "image": {
            "source": "bag.png"
       }
    },
    "baghighlighted": {
       "image": {
            "source": "baghighlighted.png"
       }
    },
    "es_icon": {
       "image": {
            "source": "es.png"
       }
    },
    "euro": {
       "image": {
            "source": "euro.png"
       }
    },
    "ping_green": {
       "image": {
           "source": "ping_green.png"
       }
    },
    "ping_red": {
       "image": {
           "source": "ping_red.png"
       }
    },
    "ping_yellow": {
       "image": {
           "source": "ping_yellow.png"
       }
    },
    "document": {
       "image": {
           "source": "chatboxbg.png"
       },
       "gui_color": [255,255,255,255]
    },
    "settings": {
       "down": {
           "highlight": {
                "image": {
                   "source": "settingshighlighted.png"
               }
           },
           "image": {
               "source": "settingshighlighted.png"
           }
       },
       "up": {
           "highlight": {
                "image": {
                   "source": "settingshighlighted.png"
               }
           },
           "image": {
               "source": "settings.png"
           }
       },
       "gui_color": [255,255,255,255]
    },
    'empty': {
           "down": {
               "image": {
                   "source": 'emptypixel.png'
               }
           },
           "up": {
               "image": {
                   "source": 'emptypixel.png'
               }
           },
       "gui_color": [255,255,255,255]
    },
    'partyleader': {
       "image": {
           "source": 'partyleader.png'
       }
    },
    'partymember': {
       "image": {
           "source": 'meneoutline.png'
       }
    },
    'menewindowbutton': {
           "down": {
               "image": {
                   "source": 'meneoutline_selected.png',
                   "frame": [11,11,11,11]
               }
           },
           "up": {
               "image": {
                   "source": 'meneoutline.png',
                   "frame": [11,11,11,11]
               }
           }
    },
    'abilityoutline': {
       "image": {
           "source": 'ability_outline.png',
           "frame": [9,9,9,9]
       }
    },
    'abilityoutline_disabled': {
       "image": {
           "source": 'ability_outline_disabled.png',
           "frame": [9,9,9,9]
       }
    },
    'abilityoutline_highlighted': {
       "image": {
           "source": 'ability_outline_highlighted.png',
           "frame": [9,9,9,9]
       }
    },
    'baroutline': {
        'image': {
            'source':'bar_outline.png',
            "frame": [4, 4, 4, 4]
        }
    },
    'leavematch': {
        'image': {
            'source':'leavematch.png'
        }
    },
    'mymenes': {
        'image': {
            'source':'mymenes.png'
        }
    },
    'empty': {
        "down": {
           "highlight": {
                "image": {
                   'source':'emptyhighlighted.png',
                    "frame": [4, 4, 4, 4]
               }
           },
           "image": {
               'source':'emptyhighlighted.png',
                "frame": [4, 4, 4, 4]
           }
       },
       "up": {
           "highlight": {
                "image": {
                   'source':'emptyhighlighted.png',
                "frame": [4, 4, 4, 4]
               }
           },
           "image": {
               'source':'empty.png',
                "frame": [4, 4, 4, 4]
           }
       }
    },
    'baroutline_btn': {
        "down": {
           "highlight": {
                "image": {
                   'source':'emptyhighlighted1.png',
                    "frame": [4, 4, 4, 4]
               }
           },
           "image": {
               'source':'emptyhighlighted1.png',
                "frame": [4, 4, 4, 4]
           }
       },
       "up": {
           "highlight": {
                "image": {
                   'source':'emptyhighlighted1.png',
                "frame": [4, 4, 4, 4]
               }
           },
           "image": {
               'source':'empty1.png',
                "frame": [1,1,1,1]
           }
       },
       "text_color":loginFontColor
    },
    'hpbar': {
        'image': {
            'source':'hpbar.png'
        }
    },
    'xpbar': {
        'image': {
            'source':'xpbar.png'
        }
    },
    "slider": {
       "knob": {
           "image": {
               "source": "slider_knob.png"
           },
           "offset": [-4, -10]
       },
       "padding": [8, 8, 8, 8],
       "step": {
           "image": {
               "source": "slider-step.png"
           },
           "offset": [-2, -8]
       },
       "bar": {
           "image": {
               "source": "slider_bg.png",
               "frame": [4,4,4,4],
               "padding": [8, 8, 8, 8]
           }
       }
    }
    
}, resources_path=dataPath+'/theme/')
##f0e0d6 bg-color
##800000 post-color
chatLog=[]
chatLogLength=1
chatDeleteCheck=False #stupid hack
mails=[]
chatReloaded=False
chatting=None
chatTheme = Theme({
    "font": defaultFont.name,
    "font_size": 13,
    "gui_color": [255, 255, 255, 255],
    "text_color": [128,0,0, 255],
    "input": {
       "image": {
           "source": "input.normal.png",
           "frame": [4, 4, 4, 4],
           "padding": [3,3,0,0]
       },
       "focus_color": [0,0,0,0],
       "focus": {
           "image": {
               "source": "input.png",
               "padding": [3,3,0,0]
           }
       },
       "text_color": [0,0,0, 255],
       "gui_color": [255,255,255,255]
    },
    "vscrollbar": {
       "knob": {
           "image": {
               "source": "vscrollbar.png",
               "region": [0, 16, 16, 16],
               "frame": [0, 6, 16, 4],
               "padding": [0, 0, 0, 0]
           },
           "offset": [0, 0]
       },
       "bar": {
           "image": {
               "source": "vscrollbar.png",
               "region": [0, 64, 16, 16]
           },
           "padding": [0, 0, 0, 0]
       }
   },
    "document": {
       "image": {
           "source": "chatboxbg.png",
           "frame": [0, 0, 0, 0],
           "padding": [0, 0, 0, 0]
       },
       "gui_color": [255,255,255,255]
    },
    "button": {
       "down": {
           "highlight": {
                "image": {
                   "source": "button_down.png",
                   "frame": [6, 6, 6,6],
                   "padding": [0, 0, 0, 0]
               },
               "gui_color": [255,255,255,255],
                "text_color": loginFontColor
           },
           "image": {
               "source": "button_down.png",
               "frame": [6, 6, 6,6],
               "padding":[0, 0, 0, 0]
           },
           "gui_color": [255,255,255,255],
           "text_color": loginFontColor
       },
       "up": {
           "highlight": {
                "image": {
                   "source": "button_down.png",
                   "frame": [6, 6,6,6],
                   "padding":[0, 0, 0, 0]
               },
               "gui_color": [255,255,255,255],
               "text_color": loginFontColor
           },
           "image": {
               "source": "button_up.png",
               "frame": [6, 6, 6,6],
               "padding": [0, 0, 0, 0]
           },
           "gui_color": [255,255,255,255],
           "text_color": loginFontColor
       }
    },
    "highlight_color": [255,255,255,255],
   "frame": {
       "image": {
           "source": "chatbubble.png",
           "frame": [8,8,8,8],
           "padding": [8, 8, 0, 0]
       }
   },
   
  }
  ,resources_path=dataPath+'/theme/'
)