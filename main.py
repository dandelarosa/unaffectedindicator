#!/usr/bin/python

import pygame

import world

def main():

	pygame.init()
	screen = pygame.display.set_mode((world.SCREEN_WIDTH, world.SCREEN_HEIGHT), False) #pygame.FULLSCREEN)
	pygame.display.set_caption('Shmup!')

	screen.fill((0, 0, 0))
	pygame.display.flip()
	
	clock = pygame.time.Clock()
	
	gameWorld = world.World()
	gameWorld.spawnWorld()
	
	while True:
		clock.tick(30)

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				return
				
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return
		
		gameWorld.update()
					
		screen.fill((255,255,255))
		pygame.draw.rect(screen, (200, 200, 255), (world.PLAY_WIDTH, 0, world.HUD_WIDTH, world.SCREEN_HEIGHT))
		gameWorld.draw(screen)
		
		
		pygame.display.flip()

main()
