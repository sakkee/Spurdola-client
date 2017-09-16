import os
import global_vars as g
from constants import *
from pyglet.gl import *
from PIL import Image

class SpriteSheetReader:
    def __init__(self, imageName, tileSize):
        self.spritesheet = Image.open(imageName)
        self.tileSize = tileSize
        
    def getTile(self, tileX, tileY,width=None):
        posX = self.tileSize * tileX
        posY = self.tileSize * tileY
        
        if width is not None:
            box = (posX, posY, posX + width*self.tileSize, posY + self.tileSize)
        else:
            box = (posX, posY, posX + self.tileSize, posY + self.tileSize)
        return self.spritesheet.crop(box)
        
        
class ResourceManager():
    def __init__(self):
        self.tileSheets = []
        self.spriteSheets = []
        self.mouseSheets = None
        self.abilities = {}
        self.soundEffects={}
        self.meneSprites = {}
        self.items = {}
        self.loadItems()
        self.loadMeneSprites()
        self.loadSoundEffects()
        self.loadBg()
        self.loadCharSprites()
        self.loadMouseTiles()
        self.loadAbilities()
        
    def loadMeneSprites(self):
        for file in os.listdir(g.dataPath+'/menes'):
            if file.endswith(".png"):
                tmpname = file[:-4].split('_')
                if len(tmpname)==2:
                    if tmpname[0] not in self.meneSprites:
                        self.meneSprites[tmpname[0]] = {}
                    if tmpname[1]=='front':
                        img = Image.open(g.dataPath+'/menes/'+file)
                        image_data = img.load()
                        for y in xrange(img.size[1]):
                            for x in xrange(img.size[0]):
                                if image_data[x, y][3] != 0:
                                    image_data[x, y] = (255, 255, 0, 255)
                        img = img.transpose(Image.FLIP_TOP_BOTTOM)
                        raw_data = img.tobytes()
                        img = pyglet.image.ImageData(256,256,'RGBA',raw_data)
                        self.meneSprites[tmpname[0]][tmpname[1]+'test']=pyglet.sprite.Sprite(img)
                        #self.meneSprites[tmpname[0]][tmpname[1]+'test'] 
                    self.meneSprites[tmpname[0]][tmpname[1]]=pyglet.resource.image(g.dataPath+'/menes/'+file)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                
    def loadItems(self):
        for file in os.listdir(g.dataPath+'/items'):
            if file.endswith(".png"):
                self.items[file[:-4]]=pyglet.resource.image(g.dataPath+'/items/'+file)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    def loadSoundEffects(self):
        for file in os.listdir(g.dataPath+'/sound_effects'):
            if file.endswith(".mp3"):
                self.soundEffects[file[:-4]]=pyglet.media.load(g.dataPath+'/sound_effects/'+file,streaming=False)
    def loadAbilities(self):
        for file in os.listdir(g.dataPath+'/abilities'):
            if file.endswith(".png"):
                self.abilities[file[:-4]]=pyglet.resource.image(g.dataPath+'/abilities/'+file)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    def loadMouseTiles(self):
        mouse = None
        try:
            mouse = pyglet.resource.image(g.dataPath+'/gui/mouseSelection.png')
            self.mouseSheets = pyglet.image.ImageGrid(mouse,1,4)
        except Exception, e:
            pass
    def loadBg(self):
        groundSheets=[]
        for x in range(5):
            try:
                tileset = SpriteSheetReader(g.dataPath+'/tilesets/ground/'+str(x)+'.png',TILESHEET_WIDTH)
                groundSheets.append(tileset)
            except Exception, e:
                break
        self.tileSheets.append(groundSheets)
        
        wallSheets = []
        for x in range(5):
            try:
                tileset = SpriteSheetReader(g.dataPath+'/tilesets/wall/'+str(x)+'.png',TILESHEET_WIDTH)
                wallSheets.append(tileset)
            except:
                break
        self.tileSheets.append(wallSheets)
        
        treesSheets = []
        for x in range(5):
            try:
                tileset = SpriteSheetReader(g.dataPath+'/tilesets/trees/'+str(x)+'.png',TILESHEET_WIDTH)
                treesSheets.append(tileset)
            except:
                break
        self.tileSheets.append(treesSheets)
        
        propsSheets = []
        for x in range(5):
            try:
                tileset = SpriteSheetReader(g.dataPath+'/tilesets/props/'+str(x)+'.png',TILESHEET_WIDTH)
                propsSheets.append(tileset)
            except:
                break
        self.tileSheets.append(propsSheets)
        
        buildingSheets = []
        for x in range(5):
            try:
                tileset = SpriteSheetReader(g.dataPath+'/tilesets/building/'+str(x)+'.png',TILESHEET_WIDTH)
                buildingSheets.append(tileset)
            except:
                break
        self.tileSheets.append(buildingSheets)
        
        otherSheets = []
        for x in range(5):
            try:
                tileset = SpriteSheetReader(g.dataPath+'/tilesets/other/'+str(x)+'.png',TILESHEET_WIDTH)
                otherSheets.append(tileset)
            except:
                break
        self.tileSheets.append(otherSheets)
        
    def loadCharSprites(self):
        tileset = SpriteSheetReader(g.dataPath+'/sprites/char.png',TILESHEET_WIDTH)
        self.spriteSheets.append(tileset)
        tileset = SpriteSheetReader(g.dataPath+'/sprites/face.png',TILESHEET_WIDTH)
        g.MAX_FACE= tileset.spritesheet.size[1]//TILESHEET_WIDTH
        self.spriteSheets.append(tileset)
        tileset = SpriteSheetReader(g.dataPath+'/sprites/hat.png',TILESHEET_WIDTH)
        g.MAX_HAT= tileset.spritesheet.size[1]//TILESHEET_WIDTH
        self.spriteSheets.append(tileset)
        tileset = SpriteSheetReader(g.dataPath+'/sprites/shirt.png',TILESHEET_WIDTH)
        g.MAX_SHIRT= tileset.spritesheet.size[1]//TILESHEET_WIDTH
        self.spriteSheets.append(tileset)
        tileset = SpriteSheetReader(g.dataPath+'/sprites/shoes.png',TILESHEET_WIDTH)
        g.MAX_SHOES= tileset.spritesheet.size[1]//TILESHEET_WIDTH
        self.spriteSheets.append(tileset)
       