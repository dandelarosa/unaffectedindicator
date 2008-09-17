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
    def __init__(self, image, numFrames, initial, final, center = (0, 0)):
        image = loadImage(image)
        rect = image.get_rect()
        imageStrip = pygame.Surface((rect.width * numFrames, rect.height)).convert_alpha()
        imageStrip.fill((0,0,0,0))
        image = image.convert_alpha(imageStrip)
        
        for i in range(numFrames):
            scale = [(final[j] - initial[j]) * (float(i)/numFrames) + initial[j] for j in range(len(final))]
            offset = [center[j] * (1 - scale[j]) for j in range(len(center))]
            
            scale = (int(scale[0] * rect.width), int(scale[1] * rect.height))
            offset = (int(offset[0] * rect.width), int(offset[1] * rect.height))
            
            imageStrip.blit(pygame.transform.scale(image, scale), (rect.width * i + offset[0], offset[1]))
        
        super(ResizeAnimation, self).__init__(imageStrip, rect.width, 1, False)
        

class ColorFadeAnimation(Animation):
    def __init__(self, image, framesIn, framesOut, color):
        image = loadImage(image)
        rect = image.get_rect()
        imageStrip = pygame.Surface((rect.width * (framesIn + framesOut + 1), rect.height)).convert_alpha()
        imageStrip.fill((0,0,0,0))
        image = image.convert_alpha(imageStrip)
        
        for i in range(framesIn):
            fillcolor = [color[j] * (float(i) / framesIn) for j in range(len(color))]
            imageStrip.blit(image, (rect.width * i, 0), None, pygame.BLEND_RGBA_ADD)
            imageStrip.fill(fillcolor, (rect.width * i, 0, rect.width, rect.height), pygame.BLEND_RGBA_ADD)
        
        for i in range(framesOut + 1):
            fillcolor = [color[j] * (float(framesOut - i) / framesOut) for j in range(len(color))]
            imageStrip.blit(image, (rect.width * (i + framesIn), 0), None, pygame.BLEND_RGBA_ADD)
            imageStrip.fill(fillcolor, (rect.width * (i + framesIn), 0, rect.width, rect.height), pygame.BLEND_RGBA_ADD)
        
        super(ColorFadeAnimation, self).__init__(imageStrip, rect.width, 1, False)
        
