import pygame

def loadImage (image):
    if (isinstance(image, str)):
        return pygame.image.load('data/images/' + image).convert_alpha()
    else:
        assert(isinstance(image, pygame.Surface))
        return image.convert_alpha()
    

class Animation (object):

    def __init__(self, image = None, frameWidth = 0, frameRate = 1, loops = -1):
        super(Animation, self).__init__()
        
        self.loadAnimation(image, frameWidth)
        
        self.frame = 0
        self.animFrame = 0
        self.frameRate = frameRate
        self.loopTotal = loops
        self.loopCount = 0
        self.done = False
        
    def update(self):
        self.animRect = self.animRects[self.animFrame]
        self.frame += 1
        if self.frame % self.frameRate == 0:
            self.animFrame += 1
            if self.animFrame == self.frames():
                if self.loopCount < self.loopTotal or self.loopTotal == -1:
                    self.animFrame = 0
                    self.loopCount += 1
                else:
                    self.animFrame = self.frames() - 1
                    self.done = True
    
    def frames(self):
        return len(self.animRects)
    
    def reset(self):
        self.frame = 0
        self.animFrame = 0
        self.loopCount = 0
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
    def __init__(self, image, framesIn, framesOut, initial, final, center = (0, 0), loops = 0):
    
        image = loadImage(image)
        rect = image.get_rect()
        imageStrip = pygame.Surface((rect.width * (framesIn + framesOut), rect.height)).convert_alpha()
        imageStrip.fill((0,0,0,0))
        image = image.convert_alpha(imageStrip)
        
        for i in range(framesIn):
            scale = [(final[j] - initial[j]) * (float(i) / framesIn) + initial[j] for j in range(len(final))]
            offset = [center[j] * (1 - scale[j]) for j in range(len(center))]
            
            scale = (int(scale[0] * rect.width), int(scale[1] * rect.height))
            offset = (int(offset[0] * rect.width), int(offset[1] * rect.height))
            
            imageStrip.blit(pygame.transform.scale(image, scale), (rect.width * i + offset[0], offset[1]))
            
        for i in range(framesOut):
            scale = [(final[j] - initial[j]) * (float(framesOut - i) / framesOut) + initial[j] for j in range(len(final))]
            offset = [center[j] * (1 - scale[j]) for j in range(len(center))]
            
            scale = (int(scale[0] * rect.width), int(scale[1] * rect.height))
            offset = (int(offset[0] * rect.width), int(offset[1] * rect.height))
            
            imageStrip.blit(pygame.transform.scale(image, scale), (rect.width * i + offset[0], offset[1]))
        
        super(ResizeAnimation, self).__init__(imageStrip, rect.width, 1, loops)
        

# This class requires pygame 1.8.1 or higher for the BLEND_RGBA_ADD flags
class ColorFadeAnimation(Animation):
    def __init__(self, image, framesIn, framesOut, color, loops = 0):
        image = loadImage(image)
        rect = image.get_rect()
        imageStrip = pygame.Surface((rect.width * (framesIn + framesOut), rect.height)).convert_alpha()
        imageStrip.fill((0,0,0,0))
        image = image.convert_alpha(imageStrip)
        
        for i in range(framesIn):
            fillcolor = [color[j] * (float(i) / framesIn) for j in range(len(color))]
            imageStrip.blit(image, (rect.width * i, 0))
            imageStrip.fill(fillcolor, (rect.width * i, 0, rect.width, rect.height), pygame.BLEND_RGBA_ADD)
        
        for i in range(framesOut):
            fillcolor = [color[j] * (float(framesOut - i) / framesOut) for j in range(len(color))]
            imageStrip.blit(image, (rect.width * (i + framesIn), 0))
            imageStrip.fill(fillcolor, (rect.width * (i + framesIn), 0, rect.width, rect.height), pygame.BLEND_RGBA_ADD)
        
        super(ColorFadeAnimation, self).__init__(imageStrip, rect.width, 1, loops)
        
class TriColorAnimation(Animation):
    def __init__(self, image, c1, c2, c3, color1, color2, color3, loops=0):
        image = loadImage(image)
        rect = image.get_rect()
        imageStrip = pygame.Surface((rect.width * (c1 + c2 + c3), rect.height)).convert_alpha()
        imageStrip.fill((0,0,0,0))
        image = image.convert_alpha(imageStrip)
        
        for i in range(c1):
            imageStrip.blit(image, (rect.width * i, 0))
            imageStrip.fill(color1, (rect.width * i, 0, rect.width, rect.height), pygame.BLEND_RGBA_ADD)
        
        for i in range(c2):
            imageStrip.blit(image, (rect.width * (i+c1), 0))
            imageStrip.fill(color2, (rect.width * (i+c1), 0, rect.width, rect.height), pygame.BLEND_RGBA_ADD)
        
        for i in range(c3):
            fillcolor = [color3[j] * (float(c3 - i) / c3) for j in range(len(color3))]
            imageStrip.blit(image, (rect.width * (i + c1+c2), 0))
            imageStrip.fill(fillcolor, (rect.width * (i + c1+c2), 0, rect.width, rect.height), pygame.BLEND_RGBA_ADD)
        
        super(TriColorAnimation, self).__init__(imageStrip, rect.width, 1, loops)

