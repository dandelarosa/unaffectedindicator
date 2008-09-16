#!/usr/bin/python

import pygame, time

import world
from constants import *

def main():
    """Does the main loop, 30fps, handles input and output of the game world"""

    pygame.mixer.pre_init(44100)  # sample at 44100 khz instead of default 22050
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), False) 
    #initialize the screen
    pygame.display.set_caption('Shmup!')

    playArea = pygame.Rect(0,0,PLAY_WIDTH,SCREEN_HEIGHT)
    screen.fill((200,200,200))
    screen.fill((255, 255, 255),playArea)
    pygame.display.flip()
    
    
    clock = pygame.time.Clock()
    
    gameWorld = world.World()
    gameWorld.spawnWorld()
    #create the world
    
    while True:
        clock.tick(30)
        #30 fps
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            elif event.type == pygame.KEYDOWN and gameWorld.gameOver == True:
                #reset the game if the game is over
                gameWorld.gameOver = False
                gameWorld = world.World()
                gameWorld.spawnWorld()
                
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
                    pygame.display.set_caption('Shmup!')
                elif event.key == pygame.K_r:
                    #use CTRL_ALT_DEL function, resets the damage
                    if gameWorld.player.hasCtrl and gameWorld.player.hasAlt and gameWorld.player.hasDel:
                        gameWorld.damage = 0
                        gameWorld.player.hasCtrl = False
                        gameWorld.player.hasAlt = False
                        gameWorld.player.hasDel = False
        
        if not gameWorld.gameOver:
            gameWorld.update()
            
        screen.fill(HUD_BG_COLOR)
        screen.fill(PLAY_BG_COLOR, playArea)
        
        gameWorld.draw(screen)
        
        if gameWorld.gameOver:
            #the game is over at this point, blit the game over screen and give option for replay
            pygame.display.set_caption("Game Over")
            screen = pygame.display.get_surface()
            s1 = pygame.image.load('data/images/alternateBlueScreen.jpg')
            screen.blit(s1, (0,0))
        
        pygame.display.flip()

    
main()
