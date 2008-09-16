PLAY_WIDTH = 824
HUD_WIDTH = 200
SCREEN_WIDTH = PLAY_WIDTH + HUD_WIDTH
SCREEN_HEIGHT = 768

MUSIC_LENGTH_MAIN = 5040
MUSIC_LENGTH_MAIN_LOOP = 3240
MUSIC_LENGTH_BOSS = 2550

#play through Main.mp3 and Mainloop.mp3 once each, then boss shows up
#length = 2:48 + 1:48 = 276 seconds = 8280 frames
FRAMES_UNTIL_BOSS = 8280

#or just play Main.mp3 once to keep things shorter
#length = 2:48 = 168 seconds = 5040 frames
#FRAMES_UNTIL_BOSS = 5040

#uncomment this to just test boss
#FRAMES_UNTIL_BOSS = 1

#length of Boss.mp3, switch to Bossloop.mp3 after
#1:25 = 85 seconds = 2550
FRAMES_BOSS_MUSIC = 2550

LIVES = 3
MAX_HEALTH = 15

PLAY_BG_COLOR = (255, 255, 255)
HUD_BG_COLOR = (230, 230, 230)

BACKGROUND_IMAGE_FILES = ('disc.png', 'folder.png', 'game icon.png', 'game icon 2.png', 'mp3.png', 'my computer.png', 'notepad.png', 'world icon.png')

