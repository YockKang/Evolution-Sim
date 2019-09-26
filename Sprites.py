###########
# Sprites #
###########

import pygame, pygame.font, secrets, math, os, time, random
from statistics import mean 
from Settings import *
from Graphing import *

######################
## Classes: Organii ##
######################
class Organii(pygame.sprite.Sprite):

    def __init__(self, x, y, movemode, spd, img):
        self.x = x
        self.y = y
        self.movemode = movemode
        self.tgtfound = False
        self.dx = 0
        self.dy = 0
        self.eat = 0
        self.food = None
        self.repro=2
        self.spd = spd
        if spd <= 0:
            self.spd = 1
        self.lifelength = daylength * (400/self.spd)
        self.livetime = 0
        self.endday = False
        self.athome = False
        self.colourscale = self.spd/800
        if self.colourscale > 1:
            self.colourscale = 1
        self.rgb = colour_convert(self.colourscale)
        img.lock()
        self.img = colourreplace(img, self.rgb)
        img.unlock()
        self.rect = self.img.get_rect(center = (x,y))
        self.mask = pygame.mask.from_surface(self.img)
        
    def findtgt(self):
        closestfood = None
        closestfooddist = 10**100
        for food in foods:
            tgtx = food.x
            tgty = food.y
            posx = self.x
            posy = self.y
            xdiff = tgtx - posx
            ydiff = tgty - posy
            dist = math.sqrt(math.fabs(xdiff)**2 + math.fabs(ydiff)**2)
            if dist < closestfooddist:
                closestfood = food
                closestfooddist = dist
        if self.food != closestfood:
            try:
                self.food = closestfood
                self.tgt = (closestfood.x, closestfood.y)

            except:
                self.movemode= 'returning'
                self.endday = True

    def postotgt(self):
        try:
            tgtx = self.tgt[0]
            tgty = self.tgt[1]
            posx = self.x
            posy = self.y
            xdiff = tgtx - posx
            ydiff = tgty - posy
            dist = math.sqrt(math.fabs(xdiff)**2 + math.fabs(ydiff)**2)
            scale = self.spd/dist
            self.dx = xdiff * scale
            self.dy = ydiff * scale
        except:
            self.dx = 0
            self.dy = 0

    def movehome(self):
        homex= home.rect.centerx
        homey= home.rect.centery+10
        posx= self.x
        posy= self.y
        xdiff = homex - posx
        ydiff = homey - posy
        dist = math.sqrt(math.fabs(xdiff)**2 + math.fabs(ydiff)**2)
        scale = self.spd/dist
        self.dx = xdiff * scale
        self.dy = ydiff * scale
        if self.x <= homex+5 and self.x >= homex-5:
            self.dx = 0
        if self.y <= homey+5 and self.y >= homey-5:
            self.dy = 0
        if self.x <= homex+5 and self.x >= homex-5 and self.y <= homey+5 and self.y >= homey-5:
            self.athome = True


    def update(self, timepass):

        if self.eat>= self.repro or len(foods)== 0 or self.endday == True:
            if self.eat == 0:
                self.dx = 0
                self.dy = 0
                self.img = blobdie_img
                self.movemode = 'dead'
            else:
                self.movemode = 'returning'
        else:
            self.movemode = 'orienting'

        if self.movemode == 'returning':
            self.movehome()
        if self.movemode == 'orienting':
            self.findtgt()
            self.postotgt()

        self.livetime += timepass
        self.x = self.x + self.dx * timepass
        self.y = self.y + self.dy * timepass
        self.rect.center = (self.x, self.y)
        
        if self.movemode != 'dead':
            for food in foods:
                if pygame.sprite.collide_mask(self, food) != None:
                    foods.remove(food)
                    self.eat += 1
                    self.movemode = None
        
        if self.livetime > self.lifelength:
            self.endday = True
 


    def draw(self, screen):
        screen.blit(self.img, self.rect)

        
####################
## Classes: Foods ##
####################
class Food(pygame.sprite.Sprite):

    def __init__(self, x, y, img, home):
        self.x = x
        self.y = y
        self.img = img
        self.rect = self.img.get_rect(center = (x,y))
        self.mask = pygame.mask.from_surface(self.img)
        self.death=0 #attribute to determine whether the sprite needs to be removed
        if pygame.sprite.collide_mask(self, home):
            newfood()
            self.death=10


    def draw(self, screen):
        if self.death==10:
            foods.remove(self)

        screen.blit(self.img, self.rect)

###############################
## Classes: Game Environment ##
###############################
class Home():
    def __init__(self, screen):
        self.x = (fieldborder[0][0] + fieldborder[0][1])/2
        self.y = (fieldborder[1][0] + fieldborder[1][1])/2
        self.img = home_img
        self.rect = self.img.get_rect(center= (self.x,self.y))
        self.mask = pygame.mask.from_surface(self.img)


    def draw(self, screen):
        screen.blit(self.img, self.rect)


def pause():
    paused = True
    while paused == True:
        pass


class Game():
    def __init__(self,ono, dl):
        self.time=0
        self.organii_no=ono
        self.day=0
        self.daylength= dl
        self.dayprogress=0


    def update(self, timee=0):
        check = 0
        for item in organii:
            if item.athome == True or item.movemode =='dead' :
                check += 1
        if check == len(organii):
            self.day += 1
            newday(self)


def newday(game):
    deadorganii = []
    for i in organii:
        if i.eat<=0:
            index = organii.index(i)
            deadorganii.append(index)
    for i in range(len(deadorganii)):
        organii.remove(organii[deadorganii[i]-i])
        
    for i in organii:
        if i.eat>=i.repro:
            new = Organii(home.x + secrets.choice(plusminus)*secrets.randbelow(16), home.y + secrets.choice(plusminus)*secrets.randbelow(16), 'orienting', i.spd+secrets.randbelow(spddeviation+1)*secrets.choice(plusminus), blob_img)
            organii.append(new)

        i.eat=0
        i.livetime = 0
        i.athome = False
        i.movemode = 'orienting'
        i.endday = False
    count = 0
    newfoods = []
    for i in range(foodsno):
        newfood()
    organiicount.append(len(organii))
    dayno.append(game.day)
    organiino_graph.update(organiicount,dayno)

    listall = []
    for thing in organii:
        listall.append(thing.spd)
    totalavg = 0
    if listall != []:
        totalavg = mean(listall)
        
    highest.append(max(listall))
    lowest.append(min(listall))
    avg.append(totalavg)
    organiiavgspd_graph.update(avg,dayno)
    organiiavgspd_graph.update(highest,dayno, 'green')
    organiiavgspd_graph.update(lowest,dayno, 'red')

    foodsnum.append(len(foods))
    foods_graph.update(foodsnum, dayno)
    
    if len(dayno) > 1:
        dayno.remove(dayno[0])
        organiicount.remove(organiicount[0])
        avg.remove(avg[0])
        foodsnum.remove(foodsnum[0])
        highest.remove(highest[0])
        lowest.remove(lowest[0])
    
def newfood():
    random.seed(secrets.token_bytes())
    randx = random.randint(fieldborder[0][0], fieldborder[0][1])
    randy = random.randint(fieldborder[1][0], fieldborder[1][1])
    foods.append(Food(randx, randy, food_img, home))

def colour_convert(scale):
    if scale<=0.75:
        rescale = scale *(1/0.75)
        hue = 300 - (rescale  * (300))
        sat = 1
        light = 0.25 + 0.25*rescale
    else:
        rescale = scale *(4) - 3
        hue = -math.log((scale-0.75), 2)+328
        sat = 1 - rescale
        light = 0.5 + 0.5*rescale
        
    c = (1 - math.fabs(2*light - 1))*sat
    x = c*(1 - math.fabs((hue/60)%2 - 1))
    rgb = [0,0,0]
    rgb_l = [0,0,0]
    if hue < 60:
        rgb_l[0] = c
        rgb_l[1] = x
    elif hue < 120:
        rgb_l[0] = x
        rgb_l[1] = c
    elif hue < 180:
        rgb_l[1] = c
        rgb_l[2] = x
    elif hue < 240:
        rgb_l[1] = x
        rgb_l[2] = c
    elif hue < 300:
        rgb_l[0] = x
        rgb_l[2] = c
    else:
        rgb_l[0] = c
        rgb_l[2] = x
    m = light - c/2
    for i in range(len(rgb_l)):
        rgb[i] = (rgb_l[i]+m)*255
    rgb_out = (rgb[0],rgb[1],rgb[2])
    return rgb_out

def colourreplace(img, rgb):
    array = pygame.PixelArray(img)
    array.replace(organii_default_blue,rgb)
    outimg = array.make_surface()
    array.replace(rgb, organii_default_blue)
    del array
    return outimg

clock = pygame.time.Clock()
home= Home(screen)


######################
## Global Variables ##
######################

plusminus = [-1, 1]
organii = []
foods = []
organii_number= 15
foodsno=40
daylength=2
done = False
startspd = 200
spddeviation = 20
organiicount = [organii_number]
dayno = [0]
foodsnum = [foodsno]
avg = [startspd]
highest = [startspd]
lowest = [startspd]

for i in range(organii_number):
    randx = fieldborder[0][0] + 10 + secrets.randbelow(fieldborder[0][1]-fieldborder[0][0])
    randy = fieldborder[1][0] + 10 + secrets.randbelow(fieldborder[1][1]-fieldborder[1][0])
    organii.append(Organii(randx, randy, 'finding', startspd, blob_img))

while len(foods) < foodsno:
    newfood()

game= Game(organii_number, daylength)
organiino_graph = Graph(datax = [0], datay = [organii_number], name='organii no')
organiiavgspd_graph = Graph(datax = [0], datay = [startspd], name = 'organii avg spd')
foods_graph = Graph(datax = [0], datay = [foodsno], name = 'no. of foods')
