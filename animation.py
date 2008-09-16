import pygame

class Animation (object):

    def __init__(self, imageFile = None, frameWidth = 0, frameRate = 1, loops = True):
        super(Animation, self).__init__()
        
        self.loadAnimation(imageFile, frameWidth)
        
        self.frame = 0
        self.animFrame = 0
        self.frameRate = frameRate
        self.loops = loops
        self.done = False
        
    def update(self):
        self.animRect = self.animRects[self.animFrame]
        self.frame += 1
        if self.frame % self.frameRate == 0:
            self.animFrame += 1
            if self.animFrame == self.frames():
                if self.loops:
                    self.animFrame = 0
                else:
                    self.animFrame = self.frames() - 1
                    self.done = True
    
    def frames(self):
        return len(self.animRects)
    
    def reset(self):
        self.frame = 0
        self.animFrame = 0
        self.animRect = self.animRects[0]
        self.done = False
    
    def loadAnimation(self, imageFilename = None, frameWidth = 0):
        if imageFilename is None:
            self.image = pygame.Surface((32, 32))
            color = (100, 100, 100)
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.animRects = [self.rect]
            
        else:
            self.image = pygame.image.load('data/images/' + imageFilename).convert_alpha()
            rectStrip = self.image.get_rect()
            
            if frameWidth == 0:
                frameWidth = rectStrip.width
            
            self.animRects = []
            for i in range(rectStrip.width / frameWidth):
                self.animRects.append(pygame.Rect(i * frameWidth, 0, frameWidth, rectStrip.height))
            
            self.animRect = self.animRects[0]
            self.rect = pygame.Rect(0, 0, self.animRect.width, self.animRect.height)
            

