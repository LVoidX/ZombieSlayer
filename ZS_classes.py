import pygame, random
import ZS_globalvars
import os
from pygame.locals import *
import math

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')


class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.original_image = pygame.image.load(os.path.join(img_folder, 'Player.png')).convert_alpha()
		self.image = pygame.image.load(os.path.join(img_folder, 'Player.png')).convert_alpha()
		self.rect = self.image.get_rect(center=(250,250))
		self.movespeed = ZS_globalvars.movement_speed
		self.speedx = 0
		self.speedy = 0
		self.last_shot = pygame.time.get_ticks()
		ZS_globalvars.player_shoot_delay = 500
		self.degrees = 0
		self.radius = 20


	def shoot(self, bullets, all_sprites):
		now = pygame.time.get_ticks()
		if now - self.last_shot > ZS_globalvars.player_shoot_delay:
			bullet = Bullet(self.rect.centerx, self.rect.centery, self.degrees)
			self.last_shot = now
			bullets.add(bullet)
			all_sprites.add(bullet)


	def update(self):
		# x movement
		self.speedx = 0
		self.speedy = 0
		keystate = pygame.key.get_pressed()
		if keystate[K_LEFT] or keystate[K_a]:
			self.speedx -= self.movespeed
		if keystate[K_RIGHT] or keystate[K_d]:
			self.speedx += self.movespeed
		self.rect.x += self.speedx
		if self.rect.left > ZS_globalvars.SCREENSIZE[0]:
			self.rect.right = 0
		elif self.rect.right < 0:
			self.rect.left = ZS_globalvars.SCREENSIZE[0]
		self.speedx = 0
		# y movement
		if keystate[K_DOWN] or keystate[K_s]:
			self.speedy += self.movespeed
		if keystate[K_UP] or keystate[K_w]:
			self.speedy -= self.movespeed
		self.rect.y += self.speedy
		if self.rect.top > ZS_globalvars.SCREENSIZE[1]:
			self.rect.bottom = 0
		elif self.rect.bottom < 0:
			self.rect.top = ZS_globalvars.SCREENSIZE[1]
		self.speedy = 0
		
		# point at mouse
		playerpos = self.rect.center
		mousepos = pygame.mouse.get_pos()
		dx = mousepos[0] - playerpos[0]
		dy = playerpos[1] - mousepos[1]
		self.degrees = (180/math.pi) * math.atan2(dy, dx)
		self.image = pygame.transform.rotate(self.original_image, self.degrees)
		self.rect = self.image.get_rect(center = playerpos)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, degrees):
		pygame.sprite.Sprite.__init__(self)
		image = pygame.image.load(os.path.join(img_folder, 'Bullet.png'))
		self.image = pygame.transform.rotate(image, degrees).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		speed = ZS_globalvars.bullet_speed
		# shoot the right direction
		self.speedy = -speed * math.sin(math.radians(degrees))
		self.speedx = speed * math.cos(math.radians(degrees))

	def update(self):
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		# kill if it moves off screen
		if self.rect.bottom < 0:
			self.kill()
		elif self.rect.right < 0:
			self.kill()
		elif self.rect.top > ZS_globalvars.SCREENSIZE[1]:
			self.kill()
		elif self.rect.left > ZS_globalvars.SCREENSIZE[0]:
			self.kill()

class Mob_1(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.original_image = pygame.image.load(os.path.join(img_folder, 'zombie_1.png'))
		self.image = self.original_image
		self.rect = self.image.get_rect()
		self.radius = 23
		# choose random spawn location
		spawn_position = random.randrange(1, 5)
		if spawn_position == 1:
			self.rect.bottom = random.randrange(-50, 1)
			self.rect.centerx = random.randrange(-50, ZS_globalvars.SCREENSIZE[0] + 50)
		elif spawn_position == 2:
			self.rect.left = random.randrange(ZS_globalvars.SCREENSIZE[0], ZS_globalvars.SCREENSIZE[0] + 50)
			self.rect.centery = random.randrange(-50, ZS_globalvars.SCREENSIZE[1] + 50)
		elif spawn_position == 3:
			self.rect.top = random.randrange(ZS_globalvars.SCREENSIZE[1], ZS_globalvars.SCREENSIZE[1] + 50)
			self.rect.centerx = random.randrange(-50, ZS_globalvars.SCREENSIZE[0] + 50)
		elif spawn_position == 4:
			self.rect.right = random.randrange(-50, 1)
			self.rect.centery = random.randrange(-50, ZS_globalvars.SCREENSIZE[1] + 50)
		self.speed = ZS_globalvars.Mob_1_speed
		# look at player
		playercenter = ZS_globalvars.PLAYER.rect.center
		mobcenter = self.rect.center
		dx = playercenter[0] - mobcenter[0]
		dy = mobcenter[1] - playercenter[1]
		self.degrees = (180/math.pi) * math.atan2(dy, dx)
		self.image = pygame.transform.rotate(self.original_image, self.degrees).convert_alpha()
		self.rect = self.image.get_rect(center = mobcenter)
		# move to player
		self.speedy = -self.speed * math.sin(math.radians(self.degrees))
		self.speedx = self.speed * math.cos(math.radians(self.degrees))

	def update(self):
		# look at player
		playercenter = ZS_globalvars.PLAYER.rect.center
		mobcenter = self.rect.center
		dx = playercenter[0] - mobcenter[0]
		dy = mobcenter[1] - playercenter[1]
		self.degrees = (180/math.pi) * math.atan2(dy, dx)
		self.image = pygame.transform.rotate(self.original_image, self.degrees).convert_alpha()
		self.rect = self.image.get_rect(center = mobcenter)
		# move to player
		self.speedy = -self.speed * math.sin(math.radians(self.degrees))
		self.speedx = self.speed * math.cos(math.radians(self.degrees))
		self.rect.x += self.speedx
		self.rect.y += self.speedy
	
	def hit(self):
		self.kill()

class Mob_2(Mob_1):
	def __init__(self):
		Mob_1.__init__(self)
		self.original_image = pygame.image.load(os.path.join(img_folder, 'zombie_2.png'))
		self.speed = ZS_globalvars.Mob_2_speed
		self.lives = 1

	def hit(self):
		if self.lives == 1:
			self.original_image = pygame.image.load(os.path.join(img_folder, 'zombie_1.png'))
			self.speed = ZS_globalvars.Mob_1_speed
			self.lives -= 1
		else:
			self.kill()

class Mob_3(Mob_1):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.original_image = pygame.image.load(os.path.join(img_folder, 'zombie_3.png'))
		self.speed = ZS_globalvars.Mob_3_speed
		self.lives = 2


	def update(self):
		self.image = self.original_image

	def hit(self):
		if self.lives == 2:
			self.original_image = pygame.image.load(os.path.join(img_folder, 'zombie_2.png'))
			self.speed = ZS_globalvars.Mob_2_speed
			self.lives -= 1
		elif self.lives == 1:
			self.original_image = pygame.image.load(os.path.join(img_folder, 'zombie_1.png'))
			self.speed = ZS_globalvars.Mob_3_speed
		else:
			self.kill()
