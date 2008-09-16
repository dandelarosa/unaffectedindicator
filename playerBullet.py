import pygame

import entity

class PlayerBullet(entity.StaticEntity):
    def __init__(self, pos):
        super(PlayerBullet, self).__init__(pos, "bullet.png")
        self.movey = -8

    def update(self):
        super(PlayerBullet, self).update()
