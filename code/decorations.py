from settings import vertical_tile_num, tile_size, win_w
from pygame import *
from tiles import AnimatedTile, StaticTile
from support import import_folder
from random import choice, randint

class Sky:
	def __init__(self, horizon):
		self.top = image.load('../graphics/decorations/sky/top.png').convert()
		self.middle = image.load('../graphics/decorations/sky/middle.png').convert()
		self.bottom = image.load('../graphics/decorations/sky/bottom.png').convert()
		self.horizon = horizon

		self.top = transform.scale(self.top, (win_w, tile_size))
		self.middle = transform.scale(self.middle, (win_w, tile_size))
		self.bottom = transform.scale(self.bottom, (win_w, tile_size))


	def draw(self,surface):
		for row in range(vertical_tile_num):
			y = row* tile_size
			if row < self.horizon:
				surface.blit(self.top, (0,y))
			elif row == self.horizon:
				surface.blit(self.middle, (0,y))
			else:
				surface.blit(self.bottom, (0,y))



class Water:
	def __init__(self, top, level_width):
		start = -win_w
		tile_w = 192
		tile_x_amount = int((level_width + win_w*2) / tile_w)
		self.water_sprites = sprite.Group()

		for tile in range(tile_x_amount):
			x = tile * tile_w + start
			y = top
			tile_sprite = AnimatedTile(192, x,y, "../graphics/decorations/water")
			tile_sprite.speed = 0.1
			self.water_sprites.add(tile_sprite)
	def draw(self,surface, shift):
		self.water_sprites.update(shift)
		self.water_sprites.draw(surface)

class Clouds:
	def __init__(self, horizon, level_width, cloud_num):
		cloud_surf_list = import_folder('../graphics/decorations/clouds')
		min_x  = - win_w
		max_x = level_width + win_w
		min_y = 0 
		max_y = horizon
		self.cloud_sprites = sprite.Group()

		for cloud in range(cloud_num):
			cloud = transform.scale(choice(cloud_surf_list), (150,80))
			x = randint(min_x, max_x)
			y = randint(min_y, max_y)
			tile_sprite =  StaticTile(0, x, y, cloud)
			self.cloud_sprites.add(tile_sprite)
	def draw(self, surface, shift):
		self.cloud_sprites.update(shift)
		self.cloud_sprites.draw(surface)