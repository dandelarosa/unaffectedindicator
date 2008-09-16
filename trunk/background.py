import entity
import random
from constants import *

class Bkg(entity.Entity):
    def __init__(self):
        images = ('disc.png', 'folder.png', 'game icon.png', 'game icon 2.png', 'monkey exe.png', 'mp3.png', 'my computer.png', 'notepad.png', 'world icon.png')
        self.image = random.choice(images)
        self.position = (random.randint(10,PLAY_WIDTH-32), -32)
        super(Bkg, self).__init__(self.position, self.image)
        self.movey = 2

