PLAY_WIDTH = 824
HUD_WIDTH = 200
SCREEN_WIDTH = PLAY_WIDTH + HUD_WIDTH
SCREEN_HEIGHT = 768

MUSIC_LENGTH_MAIN = 5040        # Main.mp3 = 2:48 = 168 seconds = 5040 frames
MUSIC_LENGTH_MAIN_LOOP = 3240   # Mainloop.mp3 = 1:48 = 108 seconds = 3240 frames
MUSIC_LENGTH_BOSS = 2550        # Boss.mp3 = 1:25 = 85 seconds = 2550 frames

# play through Main.mp3 and Mainloop.mp3 once each, then boss shows up
#FRAMES_UNTIL_BOSS = MUSIC_LENGTH_MAIN + MUSIC_LENGTH_MAIN_LOOP

# or just play Main.mp3 once to keep things shorter
FRAMES_UNTIL_BOSS = MUSIC_LENGTH_MAIN

# or uncomment this to just test boss
#FRAMES_UNTIL_BOSS = 1

LIVES = 10
MAX_HEALTH = 15

PLAY_BG_COLOR = (255, 255, 255)
HUD_BG_COLOR = (230, 230, 230)

BACKGROUND_IMAGE_FILES = ('disc.png', 'folder.png', 'game icon.png', 'game icon 2.png', 'mp3.png', 'my computer.png', 'notepad.png', 'world icon.png')

