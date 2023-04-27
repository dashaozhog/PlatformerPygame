from pygame import *
from support import import_folder

class Tile(sprite.Sprite):
	def __init__(self, size,x , y):
		super().__init__()
		self.image = Surface((size,size))
		self.rect = self.image.get_rect(topleft = (x,y))

	def update(self, x_shift):
		self.rect.x += x_shift


class StaticTile(Tile):
	def __init__(self, size, x, y, surface):
		super().__init__(size, x,y)
		self.image = surface.convert_alpha()		

class Crate(StaticTile):
	def __init__(self,size,x,y):
		super().__init__(size, x, y+20, image.load("../graphics/decorations/bochka.png").convert_alpha())


class AnimatedTile(Tile):
	def __init__(self, size,x,y,path):
		super().__init__(size,x,y)
		self.frames = import_folder(path)
		self.frame_index = 0
		self.speed = 0.15
		self.image = self.frames[self.frame_index]

	def animate(self):
		self.frame_index +=self.speed
		if int(self.frame_index) >= 5:
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]
	def update(self,shift):
		self.animate()
		self.rect.x += shift

class Coin(AnimatedTile):
	def __init__(self,size,x,y,path):
		super().__init__(size,x,y,path)
		center_x = int(size/2)+x
		center_y = int(size/2)+y
		
		self.rect = self.image.get_rect(center = (center_x, center_y))


class Tree(AnimatedTile):
	def __init__(self, size,x,y,path, offset):
		super().__init__(size,x,y,path)
		offset_y = y-offset
		self.rect.topleft = (x, offset_y)
		self.speed = 0.10
