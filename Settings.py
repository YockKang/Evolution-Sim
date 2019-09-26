############
# Settings #
############

import pygame, pygame.font, secrets, math, os, time, matplotlib
pygame.init()
os.environ['SDL_VIDEODRIVER']='dummy'
screen_w = 1200
screen_h = 700
fieldborder=[[400,screen_w],[0,screen_h]]
size = (screen_w, screen_h)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("path testing")
text = pygame.font.SysFont('calibri',8)

events = pygame.event.get()
######################
## Importing Images ##
######################
asset_folder = os.path.join(os.path.dirname(__file__), 'assets')
blob_img = pygame.image.load(os.path.join(asset_folder, 'Blob.png')).convert_alpha()
blobdie_img = pygame.image.load(os.path.join(asset_folder, 'Blob-die.png')).convert_alpha()
food_img = pygame.image.load(os.path.join(asset_folder, 'Carrot.png')).convert_alpha()
home_img = pygame.image.load(os.path.join(asset_folder, 'Home.png')).convert_alpha()
TURQUOISE = (0,255,254)
organii_default_blue = (48, 166, 211)
