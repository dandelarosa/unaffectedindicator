#!/usr/bin/python

import pygame

from World import *

def main():

	pygame.init()
	screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
	pygame.display.set_caption('Shmup!')

	screen.fill((0, 0, 0))
	pygame.display.flip()
	
	clock = pygame.time.Clock()
	
	world = World()
	
	while True:
		clock.tick(30)

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				return
				
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return
		
		world.update()
					
		screen.fill((0,0,0))
		
		world.draw(screen)
		
		pygame.display.flip()

main()
