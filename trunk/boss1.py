#!/usr/bin/env python

import pygame

from entity import Entity

# These are my boss classes

class Chainlink(Entity):
	"""A link on the chain"""
	def __init__(self, position = (0, 0), image = None):
		Entity.__init__(self, position, image)

class Tentacle():
	"""Overall handler for the boss's tentacle"""
	def __init__(self, init_pos, num_links, link_size=32):
		# Set origin of object
		self.x = init_pos[0]
		self.y = init_pos[1]
		self.motion_timer = pygame.time.get_ticks()
		# Add links to list
		self.links = []
		self.link_motion = []
		self.num_links = num_links
		for i in range(self.num_links):
			new_link = Chainlink((self.x, self.y + i * link_size), pygame.image.load("sample.png").convert_alpha())
			self.links.append(new_link)
			self.link_motion.append((0,0))
		self.init_motion_vector = (0,0)
		self.link_to_update = 0
		self.velocity_timer = pygame.time.get_ticks()
	def init_motion(self, motion_vector):
		"""'Pulls' end of tentacle in a direction"""
		self.init_motion_vector = motion_vector
	def update(self):
		"""updates state of the Tentacle"""
		currenttime = pygame.time.get_ticks()
		# update motion of each link
		if currenttime - self.motion_timer > 30:
			motion_vector_to_copy = self.link_motion[self.num_links-1]
			for i in range(self.num_links):
				self.links[i].rect.move_ip(self.link_motion[i])
			self.motion_timer = currenttime
		
		if currenttime - self.velocity_timer > 60:
			# set root_of_tentacle to 0 to hold it in place; -1 to release
			root_of_tentacle = -1
			if self.link_to_update == root_of_tentacle:
				self.link_to_update = self.num_links - 1
			if self.num_links > 1:
				if self.link_to_update == self.num_links - 1:
					self.link_motion[self.link_to_update] = self.init_motion_vector
				else:
					self.link_motion[self.link_to_update] = self.link_motion[self.link_to_update+1]
			else:
				self.link_motion[self.link_to_update] = init_motion_vector
			self.link_to_update -= 1
			self.motion_timer = currenttime


class Boss(Entity):
	"""Overall handler for the final boss"""
	def __init__(self):
		super(Boss,self).__init__()
