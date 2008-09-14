#!/usr/bin/python

import pygame, time

import world
from constants import *

def main():

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), False) #pygame.FULLSCREEN)
    pygame.display.set_caption('Shmup!')

    screen.fill((0, 0, 0))
    pygame.display.flip()
    
    clock = pygame.time.Clock()
    
    gameOver = False
    
    gameWorld = world.World()
    gameWorld.spawnWorld()
    
    while True:
        clock.tick(30)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    gameWorld.leftMouseButtonDown()
                                        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_k:
                    gameWorld.destroy_all_enemies()
                elif event.key == pygame.K_SPACE and gameOver == True:
                    gameOver = False
                    gameWorld = world.World()
                    gameWorld.spawnWorld()
                    
        
        gameWorld.update()
                    
        screen.fill((255,255,255))
        pygame.draw.rect(screen, (200, 200, 255), (PLAY_WIDTH, 0, HUD_WIDTH, SCREEN_HEIGHT))
        gameWorld.draw(screen)
        
        if gameOver == True:
                    
            pygame.display.set_caption("Game Over")
            screen = pygame.display.get_surface()
            s1 = pygame.image.load('data/images/Gameover1.png')
            screen.blit(s1, (0,0))
            f = pygame.font.Font(None,32)
            txt = "Score: "+str(gameWorld.score)
            image = f.render(txt,1,(0,0,0))
            r = image.get_rect()
            r.center = (350,100)
            screen.blit(image,r)
            pygame.display.flip()
          
        
        if gameWorld.lives == 0:
            gameOver = True
        
        pygame.display.flip()

    
main()
