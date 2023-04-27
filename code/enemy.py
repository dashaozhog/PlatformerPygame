import pygame
from random import randint
from tiles import AnimatedTile

class Enemy(AnimatedTile):
	def __init__(self, size,x,y):
		super().__init__(size,x,y,'../graphics/enemies/run')
		self.rect.y += size - self.image.get_size()[1]
		self.move_speed = randint(3,5)
	def move(self):
		self.rect.x += self.move_speed
	def reverse_image(self):
		if self.move_speed < 0:
			self.image = pygame.transform.flip(self.image, True,False)
	def reverse(self):
		self.move_speed*= -1
	def update(self,shift):
		self.rect.x += shift
		self.animate()
		self.move()
		self.reverse_image()
