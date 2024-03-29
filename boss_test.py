#!/usr/bin/python

import pygame

from boss1 import * 
from constants import *

def main():

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), False) #pygame.FULLSCREEN)
    pygame.display.set_caption('Shmup!')

    screen.fill((255, 255, 255))
    pygame.display.flip()

    masterclock = pygame.time.Clock()

    # Create chain (pending implementation)
    # Tentacle is created with origin at (100,100) with 10 chain links attached
    boss = Boss((25,-200))
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
                    for tentacle in boss.tentacles:
                        tentacle.destroy_link()
                elif event.key == pygame.K_a:
                    boss.tentacles[0].destroy_link()
                elif event.key == pygame.K_s:
                    boss.tentacles[1].destroy_link()
                elif event.key == pygame.K_1:
                    boss.skip_to_main_phase()
                elif event.key == pygame.K_2:
                    boss.go_to_death_phase()
#            elif event.type == pygame.MOUSEBUTTONDOWN:
#                to_pull = ( event.pos[0]-200, event.pos[1]-150 )
#                for tentacle in boss.tentacles:
#                    tentacle.init_extend(to_pull)

        #update stuff
        boss.update()
        for tentacle in boss.tentacles:
            tentacle.update()

        #draw stuff
        screen.fill((255, 255, 255))

        # this function call displays the tentacle
        if boss.death_frame < 6:
            screen.blit(boss.image,boss.rect)
        for tentacle in boss.tentacles:
            for link in tentacle.links:
                screen.blit(link.image,link.rect)

        # display everything on screen
        pygame.display.flip() 

main()