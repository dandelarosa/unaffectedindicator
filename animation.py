import pygame

def loadImage (image):
    if (isinstance(image, str)):
        return pygame.image.load('data/images/' + image).convert_alpha()
    else:
        assert(isinstance(image, pygame.Surface))
        return image.convert_alpha()
    

class Animation (object):

    def __init__(self, image = None, frameWidth = 0, frameRate = 1, loops = True):
        super(Animation, self).__init__()
        
        self.loadAnimation(image, frameWidth)
        
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
    
    def loadAnimation(self, image = None, frameWidth = 0):
        if image is None:
            self.image = pygame.Surface((32, 32))
            color = (100, 100, 100)
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.animRects = [self.rect]
            
        else:
            self.image = loadImage(image)
            rectStrip = self.image.get_rect()
            
            if frameWidth == 0:
                frameWidth = rectStrip.width
            
            self.animRects = []
            for i in range(rectStrip.width / frameWidth):
                self.animRects.append(pygame.Rect(i * frameWidth, 0, frameWidth, rectStrip.height))
            
            self.animRect = self.animRects[0]
            self.rect = pygame.Rect(0, 0, self.animRect.width, self.animRect.height)
            
class ResizeAnimation(Animation):
    def __init__(self, image, numFrames, initial, final):
        image = loadImage(image)
        rect = image.get_rect()
        imageStrip = pygame.Surface((rect.width * numFrames, rect.height)).convert_alpha()
        imageStrip.fill((0,0,0,0))
        image = image.convert_alpha(imageStrip)
        
        for i in range(numFrames):
            scale = ((final[0] - initial[0]) * (float(i)/numFrames) + initial[0], (final[1] - initial[1]) * (float(i)/numFrames) + initial[1])
            scale = (int(scale[0] * rect.width), int(scale[1] * rect.height))
            imageStrip.blit(pygame.transform.scale(image, scale), (rect.width * i, 0))
        
        super(ResizeAnimation, self).__init__(imageStrip, rect.width, 1, False)
        
        
        
