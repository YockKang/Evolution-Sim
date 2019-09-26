########
# GAME #
########
import pygame, pygame.font, secrets, math, os, time, matplotlib
from os import path
from Settings import *
from Sprites import *
from Graphing import *
import matplotlib.pyplot as plt
pygame.init()
os.environ['SDL_VIDEODRIVER']='dummy'

while not done:
    #change number here for number of food

    sec_elapsed = clock.tick()/1000
    game.update(sec_elapsed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill((49,99,0))
    keys = pygame.key.get_pressed()

    home.draw(screen)

    for item in foods:
        item.draw(screen)

    for item in organii:
        item.update(sec_elapsed)
        item.draw(screen)

    showgraph(organiino_graph,(0,100))
    
    showgraph(organiiavgspd_graph,(0,300))

    showgraph(foods_graph,(0,500))
    
    pygame.display.flip()
    
    
pygame.quit()
