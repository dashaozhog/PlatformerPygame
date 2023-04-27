from pygame  import * 
from support import import_folder

class Player(sprite.Sprite):
	def __init__(self, pos, surface, jump_particles):
		super().__init__()
		self.char_assets()

		self.frame_index = 0
		self.animation_speed = 0.15
		self.image = self.animations['idle'][self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)


		self.dust_run_assets()
		self.dust_frame_index = 0
		self.dust_animation_speed = 0.15
		self.display_surface = surface
		self.create_jump_particles =jump_particles

		self.direction = math.Vector2(0,0)
		self.speed = 8
		self.gravity = 0.8
		self.jump_speed = -16

		self.status = 'idle'
		self.facing_right = True

		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False

	def char_assets(self):
		path = '../graphics/character/'
		self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[]}
		for animation in self.animations:
			full_path = path + animation
			self.animations[animation] = import_folder(full_path)


	def dust_run_assets(self):
		self.dust_run_particles = import_folder('../graphics/character/dust_run')
				
	def animate(self):
		 animation = self.animations[self.status]
		 self.frame_index += self.animation_speed
		 if self.frame_index >= len(animation):
		 	self.frame_index = 0

		 image = animation[int(self.frame_index)]
		 image = transform.scale(image, (50,50))
		 if self.facing_right:
		 	self.image = image
		 else:
		 	self.image = transform.flip(image, True, False)


		 if self.on_ground and self.on_right:
		 	self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
		 elif self.on_ground and self.on_left:
		 	self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
		 elif self.on_ground:
		 	self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

		 if self.on_ceiling and self.on_right:
		 	self.rect = self.image.get_rect(topright = self.rect.topright)
		 elif self.on_ceiling and self.on_left:
		 	self.rect = self.image.get_rect(topleft = self.rect.topleft)
		 elif self.on_ceiling:
		 	self.rect = self.image.get_rect(midtop = self.rect.midtop)  

	def dust_run_animation(self):
		if self.status == 'run' and self.on_ground:
			self.dust_frame_index += self.dust_animation_speed
			if self.dust_frame_index>=len(self.dust_run_particles):
				self.dust_frame_index = 0
			dust_particle = transform.scale(self.dust_run_particles[int(self.dust_frame_index)], (64,64))
			pos = self.rect.bottomleft - math.Vector2(0,60)
			if self.facing_right:
				self.display_surface.blit(dust_particle, pos)
			elif not self.facing_right:
				self.display_surface.blit(transform.flip(dust_particle, True, False), pos)
	def get_input(self):
		keys = key.get_pressed()
		if keys[K_RIGHT]:
			self.direction.x = 1
			self.facing_right = True
		elif keys[K_LEFT]:
			self.direction.x = -1
			self.facing_right = False
			
		else:
			self.direction.x = 0
		if keys[K_SPACE] and self.on_ground:
			self.jump()
			self.create_jump_particles(self.rect.center - math.Vector2(0, -15))

	def get_status(self):
		if self.direction.y < 0:
			self.status = 'jump'
		elif self.direction.y > 0.8:
			self.status = 'fall'
		else:
			if self.direction == (0,0):
				self.status = 'idle'
			elif self.direction.x != 0:
				self.status = 'run'

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y
	def jump(self):
		self.direction.y = self.jump_speed
	def update(self):
		self.get_input()
		self.get_status()
		self.animate()
		self.dust_run_animation()
