import pygame, random

import entity
from constants import *

class Bkg(entity.StaticEntity):
    def __init__(self):
        imageFilename = 'folderBig.png'
        position = (400, -360)
        super(Bkg, self).__init__(position, imageFilename)

        self.movey = 2

