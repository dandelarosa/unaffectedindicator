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
	tentacle = Tentacle((100,100),10)

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
				elif event.key == pygame.K_UP:
					tentacle.init_motion((0,-10))
				elif event.key == pygame.K_DOWN:
					tentacle.init_motion((0,10))
				elif event.key == pygame.K_LEFT:
					tentacle.init_motion((-10,0))
				elif event.key == pygame.K_RIGHT:
					tentacle.init_motion((10,0))

		#update stuff
		tentacle.update()
		
		#draw stuff
		screen.fill((0, 0, 0))
		
		# this function call displays the tentacle
		for link in tentacle.links:
			screen.blit(link.image,link.rect)
		
		# display everything on screen
		pygame.display.flip() 

main()