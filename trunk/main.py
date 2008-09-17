#!/usr/bin/python

import pygame, time

import world
from constants import *

def main():
    """Does the main loop, 30fps, handles input and output of the game world"""

    pygame.mixer.pre_init(44100)  # sample at 44100 khz instead of default 22050
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    #initialize the screen
    pygame.display.set_caption('Shmup!')

    playArea = pygame.Rect(0, 0, PLAY_WIDTH, SCREEN_HEIGHT)
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

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #quit
                    return
                    
                else:
                    if gameWorld.gameOver:
                        #reset the game if the game is over
                        gameWorld.gameOver = False
                        gameWorld = world.World()
                        gameWorld.spawnWorld()
                    
                    elif gameWorld.winScreen:
                        pass
                        
                    else:
                        if event.key == pygame.K_SPACE:
                            #destroy all enemies if possible
                            gameWorld.destroy_all_enemies()
                            
                        elif event.key == pygame.K_LALT or pygame.K_RALT or pygame.K_LCTRL or pygame.K_RCTRL or pygame.K_DELETE:
                            #use CTRL_ALT_DEL function, resets the damage
                            if gameWorld.player.hasCtrl and gameWorld.player.hasAlt and gameWorld.player.hasDel:
                                gameWorld.player.health = MAX_HEALTH
                                gameWorld.player.hasCtrl = False
                                gameWorld.player.hasAlt = False
                                gameWorld.player.hasDel = False
                                sound = pygame.mixer.Sound("data/sounds/CtrlAltDel.wav")
                                sound.play()
                                
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if gameWorld.gameOver == True:
                        #reset the game if the game is over
                        gameWorld.gameOver = False
                        gameWorld = world.World()
                        gameWorld.spawnWorld()
                        
                    elif gameWorld.winScreen:
                        pos = pygame.mouse.get_pos()
                        if 807 < pos[0] and pos[0] < 943 and 654 < pos[1] and pos[1] < 694:
                            #reset the game if the game is over
                            gameWorld.winScreen = False
                            gameWorld = world.World()
                            gameWorld.spawnWorld()
                            
                    elif not gameWorld.gameOver and not gameWorld.winScreen:
                        #shooting
                        gameWorld.leftMouseButtonDown()
                    
                elif event.button == 3 and not gameWorld.gameOver and not gameWorld.winScreen:
                    gameWorld.rightMouseButtonDown()
        
        if not gameWorld.gameOver and not gameWorld.winScreen:
            gameWorld.update()
            
            screen.fill(HUD_BG_COLOR)
            screen.fill(PLAY_BG_COLOR, playArea)
            
            gameWorld.draw(screen)
        
        elif gameWorld.gameOver:
            #the game is over at this point, blit the game over screen and give option for replay
            pygame.display.set_caption("Game Over")
            screen = pygame.display.get_surface()
            s1 = pygame.image.load('data/images/alternateBlueScreen.jpg')
            screen.blit(s1, (0,0))

        elif gameWorld.winScreen:
            #you won! here's the win screen
            pygame.mouse.set_visible(True)
            screen = pygame.display.get_surface()
            s2 = pygame.image.load('data/images/winscreen.jpg')
            screen.blit(s2, (0,0))
            f = pygame.font.Font(None, 32)
            f2 = pygame.font.Font(None, 24)
            a = f.render(str(gameWorld.numEnemiesAppeared), 1, (0,0,0))
            r = a.get_rect()
            r.center = (900, 324)
            screen.blit(a, r)
            
            a = f.render(str((gameWorld.numEnemiesAppeared - gameWorld.numEnemiesDestroyed)), 1, (0,0,0))
            r = a.get_rect()
            r.center = (900, 375)
            screen.blit(a, r)
            
            a = f.render(str(gameWorld.numEnemiesDestroyed), 1, (0,0,0))
            r = a.get_rect()
            r.center = (900, 425)
            screen.blit(a, r)
            
            a = f2.render(str(gameWorld.numViruses), 1, (0,0,0))
            r = a.get_rect()
            r.center = (900, 475)
            screen.blit(a, r)
            
            a = f2.render(str(gameWorld.numWorms), 1, (0,0,0))
            r = a.get_rect()
            r.center = (900, 505)
            screen.blit(a, r)
            
            a = f2.render(str(gameWorld.numPopUps), 1, (0,0,0))
            r = a.get_rect()
            r.center = (900, 535)
            screen.blit(a, r)
            
            a = f2.render(("1"), 1, (0,0,0))
            r = a.get_rect()
            r.center = (900, 565)
            screen.blit(a, r)
            
            a = f.render(("0"), 1, (0,0,0))
            r = a.get_rect()
            r.center = (900, 614)
            screen.blit(a, r)
            
            
            
        
        pygame.display.flip()
    
main()
