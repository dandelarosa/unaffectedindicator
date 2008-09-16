#!/usr/bin/env python

from __future__ import division
import random

import pygame

from entity import Entity

# These are my boss classes

class Chainlink(Entity):
    """A link on the chain"""
    def __init__(self, position = (0, 0), image = "Tentacle.png"):
        Entity.__init__(self, position, image, 32, 0)
        self.typeofenemy = "link"
        self.health = 3
        # Set default position of the link
        self.default_pos = position
        # Set destination to the default position
        self.destination = position
        # Set initial velocity to zero
        self.velocity = (0,0)
        # Set initial control parameters
        self.error = (0,0)
        self.previous_error = (0,0)
        self.sum_error = (0,0)
        
    def init_motion(self, position = (0,0)):
        # Initiate motion to given distance from the default position
        self.destination = ( self.default_pos[0] + position[0] , self.default_pos[1] + position[1] )
        # Calculate initial error
        current_pos = self.rect.topleft
        self.error = ( self.destination[0]-current_pos[0] , self.destination[1]-current_pos[1] )
        self.previous_error = self.error
        
    def update(self, PID = ( 0.1, 0.001, 0.05) ):
        """PID Control for motion"""
        proportional_gain = PID[0]
        integral_gain = PID[1]
        derivative_gain = PID[2]
        # Get current position
        current_pos = self.rect.topleft
        # Calculate current error
        self.error = ( self.destination[0]-current_pos[0] , self.destination[1]-current_pos[1] )
        self.sum_error = ( self.sum_error[0]+self.error[0] , self.sum_error[1]+self.error[1] )
        d_error = (self.error[0]-self.previous_error[0], self.error[1]-self.previous_error[1])
        # Move unit to rectify error
        motion_vector_x = proportional_gain * self.error[0] - derivative_gain * d_error[0] + integral_gain * self.sum_error[0]
        motion_vector_y = proportional_gain * self.error[1] - derivative_gain * d_error[1] + integral_gain * self.sum_error[1]
        motion_vector = ( motion_vector_x, motion_vector_y )
        self.rect.move_ip(motion_vector)
        self.previous_error = self.error

class Tentacle():
    """Overall handler for the boss's tentacle"""
    def __init__(self, init_pos, num_links):
        # Set origin of object
        self.x = init_pos[0]
        self.y = init_pos[1]
        self.motion_timer = pygame.time.get_ticks()
        # Add links to list
        self.links = []
        self.num_links = num_links
        for i in range(self.num_links):
            # all links start at the origin of the tentacle
            new_link = Chainlink((self.x, self.y))
            self.links.append(new_link)
            
    def init_extend(self, destination = (0,0)):
        """Specify distance (vector) to extend tentacle"""
        factor = self.num_links -1
        # Initiate motion for end of tentacle
        if self.num_links > 1:
            self.links[self.num_links-1].init_motion(destination)
        # Initiate motion for other links
        # Root link always stays in place so we don't initiate motion for it
        for i in range(1,self.num_links-1):
            this_destination = ( i * destination[0]/factor , i * destination[1]/factor)
            self.links[i].init_motion(this_destination)
            
    def destroy_link(self, link_id = -1):
        if self.num_links > 1:
            del self.links[link_id]
            self.num_links = self.num_links - 1
            
    def update(self):
        """updates state of the Tentacle"""
        currenttime = pygame.time.get_ticks()
        # update motion of each link
        if currenttime - self.motion_timer > 30:
            for link in self.links:
                link.update()
            self.motion_timer = currenttime


class Boss(Entity):
    """Overall handler for the final boss"""
    def __init__(self, position = (0, 0), image = "bossstrip.png"):
        Entity.__init__(self, position, image, 400, 0)
        # Define phase constants
        self.phase = 0
        self.timer = pygame.time.get_ticks()
        self.tentacles = []
        self.death_frame = 0
        self.typeofenemy = "boss"
        self.health = 100
        # Create Tentacles
        self.create_tentacles()

    def create_tentacles(self):
        # Get current boss coordinates
        x = self.rect.topleft[0]
        y = self.rect.topleft[1]
        # Create the tentacles
        for i in range(5):
            self.tentacles.append( Tentacle(( i * 72 + 40 + x, 150 + y ), 10) )
            
    def destroy_tentacles(self):
        # Does this remove the tentacle objects from memory?
        self.tentacles = []
        
    def go_to_main_phase(self):
        # Show attack face
        self.animRect = self.animRects[1]
        self.death_frame = 0
        # Create Tentacles
        self.create_tentacles()
        # Switch to next phase
        self.phase = 1
        
    def skip_to_main_phase(self):
        self.rect.topleft = ( self.rect.topleft[0], 0)
        self.go_to_main_phase()
        
    def go_to_death_phase(self):
        self.destroy_tentacles()
        self.phase = 2
        
    def update(self):
        # Check what phase the boss is in
        currenttime = pygame.time.get_ticks()
        if self.phase == 0: # Entry Phase
            if currenttime - self.timer > 30:
                self.rect.move_ip((0,1))
                for tentacle in self.tentacles:
                    tentacle.x = tentacle.x + 1
                    for link in tentacle.links:
                        link.default_pos = (link.default_pos[0],link.default_pos[1]+1)
                if self.rect.topleft[1] == 0:
                    self.go_to_main_phase()
                self.timer = currenttime
        elif self.phase == 1:   # Main Phase
            currenttime = pygame.time.get_ticks()
            if currenttime - self.timer > 600:
                for tentacle in self.tentacles:
                    tentacle.init_extend(( random.randint(-300,300),random.randint(-100,550) ))
                self.timer = currenttime
        elif self.phase == 2:   # Death Phase
            if currenttime - self.timer > 240:
                if self.death_frame < 5:
                    self.animRect = self.animRects[2+self.death_frame]
                    self.death_frame = self.death_frame + 1
                else:
                    self.phase = 3
                self.timer = currenttime
