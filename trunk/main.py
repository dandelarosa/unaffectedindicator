#!/usr/bin/python

import pygame, time

import world
from constants import *

def main():
    """Does the main loop, 30fps, handles input and output of the game world"""

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), False) 
    #initialize the screen
    pygame.display.set_caption('Shmup!')

    screen.fill((0, 0, 0))
    pygame.display.flip()
    
    clock = pygame.time.Clock()
    
    gameOver = False
    
    gameWorld = world.World()
    gameWorld.spawnWorld()
    #create the world
    
    while True:
        clock.tick(30)
        #30 fps
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #shooting
                    gameWorld.leftMouseButtonDown()
                    
                if event.button == 3:
                    gameWorld.rightMouseButtonDown()
                                        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #quit
                    return
                elif event.key == pygame.K_k:
                    #destroy all enemies if possible
                    gameWorld.destroy_all_enemies()
                elif event.key == pygame.K_SPACE and gameOver == True:
                    #reset the game if the game is over
                    gameOver = False
                    gameWorld = world.World()
                    gameWorld.spawnWorld()
                elif event.key == pygame.K_r:
                    #use CTRL_ALT_DEL function, resets the damage
                    if gameWorld.player.hasCtrl and gameWorld.player.hasAlt and gameWorld.player.hasDel:
                        gameWorld.damage = 0
                        gameWorld.player.hasCtrl = False
                        gameWorld.player.hasAlt = False
                        gameWorld.player.hasDel = False
        
        gameWorld.update()
                    
        screen.fill((255,255,255))
        pygame.draw.rect(screen, (200, 200, 255), (PLAY_WIDTH, 0, HUD_WIDTH, SCREEN_HEIGHT))
        gameWorld.draw(screen)
        
        if gameOver == True:
            #the game is over at this point, blit the game over screen and give option for replay
            pygame.display.set_caption("Game Over")
            screen = pygame.display.get_surface()
            s1 = pygame.image.load('data/images/Gameover1.png')
            screen.blit(s1, (0,0))
            f = pygame.font.Font(None,32)
            txt = "Score: "+str(gameWorld.score)
            image = f.render(txt,1,(255,255,255))
            r = image.get_rect()
            r.center = (350,100)
            screen.blit(image,r)
            pygame.display.flip()
          
        
        if gameWorld.lives == 0:
            gameOver = True
        
        pygame.display.flip()

    
main()
