import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, win_w, win_h
from tiles import Tile, StaticTile, Crate, Coin, Tree
from enemy import Enemy
from decorations import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect

class Level:
	def __init__(self, level_data, surface):

		self.display_surface = surface
		self.worldshift = 0
		self.current_x = None

		player_layout = import_csv_layout(level_data['player'])
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.player_setup(player_layout)

		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False

		terrain_layout = import_csv_layout(level_data['terrain'])
		self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain') ##

		grass1_layout = import_csv_layout(level_data['grass1'])
		self.grass1_sprites = self.create_tile_group(grass1_layout, 'grass1')

		plants_layout = import_csv_layout(level_data['plants'])
		self.plants_sprites = self.create_tile_group(plants_layout, 'plants')

		crates_layout = import_csv_layout(level_data['crates'])
		self.crates_sprites = self.create_tile_group(crates_layout, 'crates')  ##

		coins_layout = import_csv_layout(level_data['coins'])
		self.coins_sprites = self.create_tile_group(coins_layout, 'coins')

		collided_trees_layout = import_csv_layout(level_data['collided_trees'])
		self.trees_sprites = self.create_tile_group(collided_trees_layout, 'collided_trees') ##

		enemy_layout = import_csv_layout(level_data['enemies'])
		self.enemies_sprites = self.create_tile_group(enemy_layout, 'enemies')

		constr_layout = import_csv_layout(level_data['constraints'])
		self.constr_sprites = self.create_tile_group(constr_layout, 'constraints')

		self.sky = Sky(6)
		level_width = len(terrain_layout[0]*tile_size)
		self.water = Water(win_h - 40, level_width)
		self.clouds = Clouds(400, level_width, 20)
	def create_tile_group(self, layout, type):
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index, val in enumerate(row):
				if val != "-1":
					x = col_index*tile_size
					y = row_index * tile_size
					if type == 'terrain':
						terrain_tile_list = import_cut_graphics('../graphics/terrain/tileset.png')
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)
					if type == 'grass1':
						grass_tile_list = import_cut_graphics("../graphics/terrain/Mossy - Decorations&Hazards.png")
						tile_surface = grass_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)
					if type == 'plants':
						plants_tile_list = import_cut_graphics('../graphics/terrain/Mossy - Hanging Plants.png')
						tile_surface = plants_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)
					if type == 'crates': 
						sprite = Crate(tile_size,x,y)
					if type == 'coins':
						if val == '1': sprite = Coin(tile_size,x,y,'../graphics/coins/gold')
						if val == '0': sprite = Coin(tile_size,x,y,'../graphics/coins/silver')
					if type == 'collided_trees':
						sprite = Tree(tile_size,x,y,'../graphics/decorations/trees', 10)
					if type == 'enemies':
						sprite = Enemy(tile_size, x,y)
					if type == 'constraints':
						sprite = Tile(tile_size,x,y)


					sprite_group.add(sprite)

		return sprite_group
	def scroll_X(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < win_w/4 and direction_x<0:
			self.worldshift = 8
			player.speed = 0
		elif player_x >win_w - (win_w/4) and direction_x>0:
			self.worldshift = -8
			player.speed = 0
		else:
			self.worldshift = 0
			player.speed = 8

	def player_setup(self, layout):
		for row_index, row in enumerate(layout):
			for col_index, val in enumerate(row):
				x = col_index*tile_size
				y = row_index * tile_size
				if val == "0":
					sprite = Player((x,y), self.display_surface, self.create_jump_particles)
					self.player.add(sprite)
				if val == "1":
					sprite = StaticTile(tile_size,x,y, pygame.image.load('../graphics/character/fall/1.png').convert_alpha())
					self.goal.add(sprite)

	def enemy_reverse(self):
		for enemy in self.enemies_sprites.sprites():
			if pygame.sprite.spritecollide(enemy, self.constr_sprites, False):
				enemy.reverse()
	def create_jump_particles(self, pos):
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(10,5)
		else:
			pos+= pygame.math.Vector2(10,-5)
		jump_dust_sprite = ParticleEffect(pos, 'jump')
		self.dust_sprite.add(jump_dust_sprite)

	def hor_collide(self):
		player = self.player.sprite
		collid_sprites = self.terrain_sprites.sprites()+self.crates_sprites.sprites() + self.trees_sprites.sprites()
		player.rect.x +=player.direction.x * player.speed

		for sprite in collid_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0:
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True 
					self.current_x = player.rect.right
		if player.on_left and (player.rect.left < self.current_x or player.direction.x>=0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x<=0):
			player.on_right = False
	def ver_collide(self):
		player = self.player.sprite
		player.apply_gravity()
		collid_sprites = self.terrain_sprites.sprites()+self.crates_sprites.sprites() + self.trees_sprites.sprites()
		for sprite in collid_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0:
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True
		if player.on_ground and player.direction.y < 0 or player.direction.y >1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0:
			player.on_ceiling= False				

	def get_player_onground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else: 
			self.player_on_ground = False

	def create_landing_dust(self):
		if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
			if self.player.sprite.facing_right:
				offset = pygame.math.Vector2(10,15)
			else:
				offset = pygame.math.Vector2(-5,15)
			fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
			self.dust_sprite.add(fall_dust_particle)

	def run(self):
		self.sky.draw(self.display_surface)

		# self.display_surface.blit(pygame.transform.scale(pygame.image.load('../graphics/background.jpg'), (win_w, win_h)), (0,0))

		self.clouds.draw(self.display_surface, self.worldshift)

		self.terrain_sprites.update(self.worldshift)
		self.terrain_sprites.draw(self.display_surface)
		
		self.grass1_sprites.update(self.worldshift)
		self.grass1_sprites.draw(self.display_surface)

		self.plants_sprites.update(self.worldshift)
		self.plants_sprites.draw(self.display_surface)

		self.crates_sprites.update(self.worldshift)
		self.crates_sprites.draw(self.display_surface)

		self.enemies_sprites.update(self.worldshift)
		self.constr_sprites.update(self.worldshift)
		self.enemy_reverse()
		self.enemies_sprites.draw(self.display_surface)

		self.coins_sprites.update(self.worldshift)
		self.coins_sprites.draw(self.display_surface)
		
		self.trees_sprites.update(self.worldshift)
		self.trees_sprites.draw(self.display_surface)

		self.dust_sprite.update(self.worldshift)
		self.dust_sprite.draw(self.display_surface)

		self.player.update()
		self.hor_collide()
		self.get_player_onground()
		self.ver_collide()
		self.create_landing_dust()
		self.scroll_X()
		self.player.draw(self.display_surface)
		self.goal.update(self.worldshift)
		self.goal.draw(self.display_surface)

		self.water.draw(self.display_surface, self.worldshift)
		


		

		