#!/usr/bin/python

import pygame

from boss1 import * 
from constants import *

def main():

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), False) #pygame.FULLSCREEN)
    pygame.display.set_caption('Shmup!')

    screen.fill((0, 0, 0))
    pygame.display.flip()

    masterclock = pygame.time.Clock()

    # Create chain (pending implementation)
    # Tentacle is created with origin at (100,100) with 10 chain links attached
    tentacles = [ Tentacle((250,300),10), Tentacle((350,300),10)]
    to_pull = (0,0)

    # Main game loop
    gameover = False
    while gameover == False:
        masterclock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_SPACE:
                    for tentacle in tentacles:
                        tentacle.destroy_link()
                elif event.key == pygame.K_a:
                    tentacles[0].destroy_link()
                elif event.key == pygame.K_s:
                    tentacles[1].destroy_link()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                to_pull = ( event.pos[0]-tentacle.x, event.pos[1]-tentacle.y )
                for tentacle in tentacles:
                    tentacle.init_extend(to_pull)

        #update stuff
        for tentacle in tentacles:
            tentacle.update()

        #draw stuff
        screen.fill((0, 0, 0))

        # this function call displays the tentacle
        for tentacle in tentacles:
            for link in tentacle.links:
                screen.blit(link.image,link.rect)

        # display everything on screen
        pygame.display.flip() 

main()