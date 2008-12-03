#!/usr/bin/python

# Requires pygame 1.8.1 or higher for RGBA blending flags in animation.py

import pygame, time

import world
from constants import *

def main():
    """Does the main loop, 30fps, handles input and output of the game world"""

    pygame.mixer.pre_init(44100)  # sample at 44100 khz instead of default 22050
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    #initialize the screen
    pygame.display.set_caption('Shmup!')

    playArea = pygame.Rect(0, 0, PLAY_WIDTH, SCREEN_HEIGHT)
    screen.fill((200,200,200))
    screen.fill((255, 255, 255),playArea)
    pygame.display.flip()

    itrChosen = 0
    itrChosenDiff = 1
    
    clock = pygame.time.Clock()
    
    gameWorld = world.World()
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
                        gameWorld.startScreen = True
                    
                    elif gameWorld.winScreen:
                        pass

                    elif gameWorld.helpScreen:
                        if event.key == pygame.K_RETURN:
                            gameWorld.startScreen = True
                            gameWorld.helpScreen = False

                    elif gameWorld.difficultyScreen:
                        if event.key == pygame.K_UP:
                            itrChosenDiff -= 1
                            if itrChosenDiff < 0:
                                itrChosenDiff = 3
                        if event.key == pygame.K_DOWN:
                            itrChosenDiff += 1
                            if itrChosenDiff > 3:
                                itrChosenDiff = 0
                        if event.key == pygame.K_RETURN:
                            gameWorld.startScreen = True
                            gameWorld.difficultyScreen = False

                    elif gameWorld.startScreen:
                        if event.key == pygame.K_UP:
                            itrChosen -= 1
                            if itrChosen < 0:
                                itrChosen = 4
                        elif event.key == pygame.K_DOWN:
                            itrChosen += 1
                            if itrChosen > 4:
                                itrChosen = 0
                        elif event.key == pygame.K_RETURN:
                            if itrChosen == 0:
                                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                            if itrChosen == 1:
                                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                            if itrChosen == 2:
                                gameWorld.startScreen = False
                                gameWorld.helpScreen = True
                            if itrChosen == 3:
                                gameWorld.startScreen = False
                                gameWorld.difficultyScreen = True
                            if itrChosen == 4:
                                gameWorld.spawnWorld()
                                gameWorld.startScreen = False
                        
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
                        pass
                        
                    elif gameWorld.winScreen:
                        pos = pygame.mouse.get_pos()
                        if 807 < pos[0] and pos[0] < 943 and 654 < pos[1] and pos[1] < 694:
                            #reset the game if the game is over
                            gameWorld.winScreen = False
                            gameWorld = world.World()
                            gameWorld.startScreen = True
                            
                    elif not gameWorld.gameOver and not gameWorld.winScreen and not gameWorld.startScreen and not gameWorld.helpScreen and not gameWorld.difficultyScreen:
                        #shooting
                        gameWorld.leftMouseButtonDown()
                    
                elif event.button == 3 and not gameWorld.gameOver and not gameWorld.winScreen and not gameWorld.startScreen and not gameWorld.helpScreen and not gameWorld.difficultyScreen:
                    gameWorld.rightMouseButtonDown()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if not gameWorld.gameOver and not gameWorld.winScreen and not gameWorld.startScreen and not gameWorld.helpScreen and not gameWorld.difficultyScreen:
                        #releasing
                        gameWorld.leftMouseButtonUp()
        
        if not gameWorld.gameOver and not gameWorld.winScreen and not gameWorld.startScreen and not gameWorld.helpScreen and not gameWorld.difficultyScreen:
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

        elif gameWorld.startScreen:
            #when game first starts up, and after gameover and win screens    
            pygame.display.set_caption("Booting...")
            screen = pygame.display.get_surface()
            s1 = pygame.image.load('data/images/bootupscreen.png')
            screen.blit(s1, (0,0))
            
            chosen = pygame.Surface((500, 30))
            chosen.fill((230, 230, 230), chosen.get_rect())
            chosenstate = [ 220, 270, 330, 380, 465 ]
            r = chosen.get_rect()
            r.topleft = (100, chosenstate[itrChosen])
            screen.blit(chosen, r)
            
            f = pygame.font.Font('data/fonts/courbd.ttf', 24)
            color  = (230, 230, 230)
            if itrChosen is 0:
                color = (0, 0, 0)
            a = f.render("Enable Full Screen Display Mode", 1, color)
            r = a.get_rect()
            r.topleft = (100, chosenstate[0])
            screen.blit(a, r)

            color  = (230, 230, 230)
            if itrChosen is 1:
                color = (0, 0, 0)
            a = f.render("Enable Windowed Display Mode", 1, color)
            r = a.get_rect()
            r.topleft = (100, chosenstate[1])
            screen.blit(a, r)

            color  = (230, 230, 230)
            if itrChosen is 2:
                color = (0, 0, 0)
            a = f.render("View Help Manual", 1, color)
            r = a.get_rect()
            r.topleft = (100, chosenstate[2])
            screen.blit(a, r)

            color  = (230, 230, 230)
            if itrChosen is 3:
                color = (0, 0, 0)
            a = f.render("Configure Debug Options", 1, color)
            r = a.get_rect()
            r.topleft = (100, chosenstate[3])
            screen.blit(a, r)

            color  = (230, 230, 230)
            if itrChosen is 4:
                color = (0, 0, 0)
            a = f.render("Begin Debugging", 1, color)
            r = a.get_rect()
            r.topleft = (100, chosenstate[4])
            screen.blit(a, r)

        elif gameWorld.helpScreen:
            # can be chosen from the start screen
            screen = pygame.display.get_surface()
            pygame.display.set_caption("Controls")
            s = pygame.image.load('data/images/helpscreen.png')
            screen.blit(s, (0,0))

        elif gameWorld.difficultyScreen:
            # can be chosen from the start screen
            pygame.display.set_caption("Set Difficulty")
            screen = pygame.display.get_surface()
            s = pygame.image.load('data/images/difficultyscreen.png')
            screen.blit(s, (0,0))
            
            chosen = pygame.Surface((700, 30))
            chosen.fill((230, 230, 230), chosen.get_rect())
            chosenstate = [ 200, 300, 400, 500 ]
            r = chosen.get_rect()
            r.topleft = (100, chosenstate[itrChosenDiff])
            screen.blit(chosen, r)
            
            f = pygame.font.Font('data/fonts/courbd.ttf', 24)
            color  = (230, 230, 230)
            if itrChosenDiff is 0:
                color = (0, 0, 0)
            a = f.render("Easy", 1, color)
            gameWorld.difficulty = .7
            r = a.get_rect()
            r.topleft = (100, chosenstate[0])
            screen.blit(a, r)

            color  = (230, 230, 230)
            if itrChosenDiff is 1:
                color = (0, 0, 0)
            a = f.render("Normal", 1, color)
            gameWorld.difficulty = 1
            r = a.get_rect()
            r.topleft = (100, chosenstate[1])
            screen.blit(a, r)

            color  = (230, 230, 230)
            if itrChosenDiff is 2:
                color = (0, 0, 0)
            a = f.render("Hard", 1, color)
            gameWorld.difficulty = 1.3
            r = a.get_rect()
            r.topleft = (100, chosenstate[2])
            screen.blit(a, r)

            color  = (230, 230, 230)
            if itrChosenDiff is 3:
                color = (0, 0, 0)
            a = f.render("You don't want to. You REALLY don't want to.", 1, color)
            gameWorld.difficulty = 10
            r = a.get_rect()
            r.topleft = (100, chosenstate[3])
            screen.blit(a, r)
            


        elif gameWorld.winScreen:
            #you won! here's the win screen
            pygame.mouse.set_visible(True)
            screen = pygame.display.get_surface()
            pygame.display.set_caption("Congratulations!")
            s2 = pygame.image.load('data/images/winscreen.png')
            screen.blit(s2, (0,0))
            f = pygame.font.Font(None, 32)
            f2 = pygame.font.Font(None, 24)
            a = f.render(str(gameWorld.numEnemiesDestroyed + gameWorld.numEnemiesAppeared), 1, (0,0,0))
            r = a.get_rect()
            r.center = (900, 324)
            screen.blit(a, r)
            
            a = f.render(str((gameWorld.numEnemiesAppeared)), 1, (0,0,0))
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

            a = f.render("Score: "+str(gameWorld.score), 1, (0,0,0))
            r = a.get_rect()
            r.center = (186, 670)
            screen.blit(a, r)
            
        
        pygame.display.flip()
    
main()
