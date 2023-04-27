from pygame import *
import sys
from settings import *
from level import Level
from game_data import level_0


window = display.set_mode((win_w, win_h))
clock = time.Clock()
level = Level(level_0, window)

while True:
	for ev in event.get():
		if ev.type == QUIT: 
			quit()
			sys.exit()
	
	# window.blit(transform.scale(image.load('../graphics/background.jpg'), (win_w, win_h)), (0,0))
	window.fill('grey')
	level.run()

	display.update()
	clock.tick(60) 