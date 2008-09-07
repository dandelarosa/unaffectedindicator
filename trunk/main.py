#!/usr/bin/python

import pygame

import World

def main():

	pygame.init()
	screen = pygame.display.set_mode((World.SCREEN_WIDTH, World.SCREEN_HEIGHT),pygame.FULLSCREEN)
	pygame.display.set_caption('Shmup!')

	screen.fill((0, 0, 0))
	pygame.display.flip()
	
	clock = pygame.time.Clock()
	
	world = World.World()
	world.spawnWorld()
	
	while True:
		clock.tick(30)

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				return
				
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return
		
		world.update()
					
		screen.fill((255,255,255))
		pygame.draw.rect(screen, (200, 200, 255), (World.PLAY_WIDTH, 0, World.HUD_WIDTH, World.SCREEN_HEIGHT))
		world.draw(screen)
		
		
		pygame.display.flip()

main()
