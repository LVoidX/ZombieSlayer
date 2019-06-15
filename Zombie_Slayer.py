# Imports
import time
from ZS_classes import *
import ZS_globalvars
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# Beeld
FPS = 30

# Kleuren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(ZS_globalvars.SCREENSIZE, pygame.FULLSCREEN)
pygame.display.set_caption("Unnamed")
clock = pygame.time.Clock()

# Load all game graphics
background = pygame.image.load(os.path.join(img_dir, 'background.png')).convert_alpha()
background_rect = background.get_rect()
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Player()
ZS_globalvars.PLAYER = player
all_sprites.add(player)

# variables
now = pygame.time.get_ticks()
last_mob_spawn = now
mob_spawn_delay = 1000
player_lives = 3
coins = 0
font_name = pygame.font.match_font("arial")
mobs_per_wave = 0
wave = 1
max_mob_spawn_per_wave = 5
l = 0
show_wave_text = False
show_main_menu = True
required_coins_1 = 10
required_coins_2 = 5
required_coins_3 = 10
required_coins_4 = 25
reload_level = 1


# define functions
def newmob():
	global last_mob_spawn
	global mobs_per_wave
	global max_mob_spawn_per_wave
	global l
	m1 = Mob_1()
	m2 = Mob_2()
	m3 = Mob_3()
	if wave < 5:
		all_sprites.add(m1)
		mobs.add(m1)
	elif wave >= 5:
		if wave == 5:
			if l == 4:
				all_sprites.add(m2)
				mobs.add(m2)
				l = 0
			elif l != 4:
				all_sprites.add(m1)
				mobs.add(m1)
				l += 1
		elif wave == 6:
			if l == 4 or l == 3:
				all_sprites.add(m2)
				mobs.add(m2)
				l = 0
			elif l != 4 or l != 3:
				all_sprites.add(m1)
				mobs.add(m1)
				l += 1
		elif wave == 7:
			if l == 4 or l == 3 or l == 2:
				all_sprites.add(m2)
				mobs.add(m2)
				l = 0
			elif l != 4 or l != 3 or l != 2:
				all_sprites.add(m1)
				mobs.add(m1)
				l += 1
		elif wave == 8:
			if l == 4 or l == 1 or l == 3 or l == 2:
				all_sprites.add(m2)
				mobs.add(m2)
				l = 0
			elif l != 4 or l != 3 or l != 2 or l != 1:
				all_sprites.add(m1)
				mobs.add(m1)
				l += 1
		elif wave == 9:
			if l == 4 or l == 0 or l == 1 or l == 3 or l == 2:
				all_sprites.add(m2)
				mobs.add(m2)
				l = 0
			elif l != 4 or l != 3 or l != 2 or l != 1 or l != 0:
				all_sprites.add(m1)
				mobs.add(m1)
				l += 1
		elif wave == 10:
			if l == 1:
				all_sprites.add(m3)
				mobs.add(m3)
				l = 0
			elif l != 1:
				all_sprites.add(m2)
				mobs.add(m2)
				l += 1
		elif wave == 11:
			if l == 1 or l == 2:
				all_sprites.add(m3)
				mobs.add(m3)
				l = 0
			elif l != 1 or l != 2:
				all_sprites.add(m2)
				mobs.add(m2)
				l += 1
		elif wave == 12:
			if l == 1 or l == 2 or l == 3:
				all_sprites.add(m3)
				mobs.add(m3)
				l = 0
			elif l != 1 or l != 2 or l != 3:
				all_sprites.add(m2)
				mobs.add(m2)
				l += 1
		elif wave == 13:
			if l == 1 or l == 2 or l == 3 or l == 4:
				all_sprites.add(m3)
				mobs.add(m3)
				l = 0
			elif l != 1 or l != 2 or l != 3 or l != 4:
				all_sprites.add(m2)
				mobs.add(m2)
				l += 1
		elif wave == 14:
			if l == 1 or l == 2 or l == 3 or l == 4 or l == 0:
				all_sprites.add(m3)
				mobs.add(m3)
				l = 0
			elif l != 1 or l != 2 or l != 3 or l != 4 or l != 0:
				all_sprites.add(m2)
				mobs.add(m2)
				l += 1
		elif wave == 15:
			all_sprites.add(m3)
			mobs.add(m3)
			l = 0

	last_mob_spawn += 1
	mobs_per_wave += 1

def draw_coins(surf):
	global coins
	font = pygame.font.Font(font_name, 15)
	text = "COINS: " + str(coins)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.topleft = (5, 5)
	surf.blit(text_surface, text_rect)

def draw_lives(surf):
	global player_lives
	font = pygame.font.Font(font_name, 15)
	text = "LIVES: " + str(player_lives)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.topright = (ZS_globalvars.SCREENSIZE[0] - 5, 5)
	surf.blit(text_surface, text_rect)

def draw_wave(surf):
	global wave
	font = pygame.font.Font(font_name, 15)
	text = "WAVE: " + str(wave)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.center = (ZS_globalvars.SCREENSIZE[0] / 2, 15)
	surf.blit(text_surface, text_rect)

def draw_wave_text(surf):
	font = pygame.font.Font(font_name, 25)
	text = "WAVE CLEARED!!! Press Enter to continue"
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.center = (ZS_globalvars.SCREENSIZE[0] / 2, ZS_globalvars.SCREENSIZE[1] / 2)
	surf.blit(text_surface, text_rect)

def draw_shop_reload(surf):
	font = pygame.font.Font(font_name, 15)
	text = "RELOAD LVL: " + str(reload_level) + ". LVL UP COSTS: " + str(required_coins_1) + " COINS. PRESS 1 TO LEVEL UP."
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.center = (ZS_globalvars.SCREENSIZE[0] / 2, ZS_globalvars.SCREENSIZE[1] / 2 - 10)
	surf.blit(text_surface, text_rect)

def draw_shop_bullet_speed(surf):
	font = pygame.font.Font(font_name, 15)
	text = "BULLET SPEED: " + str(ZS_globalvars.bullet_speed) + ". SPEED UP COSTS: " + str(required_coins_2) + " COINS. PRESS 2 TO LEVEL UP."
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.center = (ZS_globalvars.SCREENSIZE[0] / 2, ZS_globalvars.SCREENSIZE[1] / 2 + 10)
	surf.blit(text_surface, text_rect)

def draw_shop_movement_speed(surf):
	font = pygame.font.Font(font_name, 15)
	text = "MOVEMENT SPEED: " + str(ZS_globalvars.movement_speed) + ". SPEED UP COSTS: " + str(required_coins_3) + " COINS. PRESS 3 TO LEVEL UP."
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.center = (ZS_globalvars.SCREENSIZE[0] / 2, ZS_globalvars.SCREENSIZE[1] / 2 + 30)
	surf.blit(text_surface, text_rect)

def draw_shop_lives(surf):
	font = pygame.font.Font(font_name, 15)
	text = "LIVES: " + str(player_lives) + ". +1 LIVE COSTS: " + str(required_coins_4) + " COINS. PRESS 4 TO LEVEL UP."
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.center = (ZS_globalvars.SCREENSIZE[0] / 2, ZS_globalvars.SCREENSIZE[1] / 2 + 50)
	surf.blit(text_surface, text_rect)

def draw_main_menu(surf):
	font = pygame.font.Font(font_name, 50)
	text = '! ZOMBIE SLAYER !'
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.center = (ZS_globalvars.SCREENSIZE[0] / 2, ZS_globalvars.SCREENSIZE[1] / 2 - 50)
	surf.blit(text_surface, text_rect)




# Game Loop
running = True
while running:
	# Process input (events)
	for event in pygame.event.get():
		# check for closing window
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False
			elif event.key == pygame.K_RETURN:
				# wave up when defeated all mobs
				if mobs_per_wave == max_mob_spawn_per_wave and len(mobs) == 0:
					wave += 1
					if player_lives < 3:
						player_lives = 3
					else:
						player_lives += 1
					show_wave_text = False
					max_mob_spawn_per_wave += 5
					mobs_per_wave = 0
					if wave <= 5:
						mob_spawn_delay -= 10
						if not ZS_globalvars.Mob_1_speed == 8:
							ZS_globalvars.Mob_1_speed += 1
					elif wave > 5:
						if not ZS_globalvars.Mob_2_speed == 8:
							ZS_globalvars.Mob_2_speed += 1
						if not ZS_globalvars.Mob_3_speed == 8 and wave > 10:
							ZS_globalvars.Mob_3_speed += 1
			elif event.key == pygame.K_1:
				if show_main_menu:
					if coins >= required_coins_1:
						ZS_globalvars.player_shoot_delay -= 50
						coins -= required_coins_1
						required_coins_1 += 10
						reload_level += 1
			elif event.key == pygame.K_2:
				if show_main_menu:
					if coins >= required_coins_2:
						ZS_globalvars.bullet_speed += 2
						coins -= required_coins_2
						required_coins_2 += 5
			elif event.key == pygame.K_3:
				if show_main_menu:
					if coins >= required_coins_3:
						ZS_globalvars.movement_speed += 1
						coins -= required_coins_3
						required_coins_3 += 10
			elif event.key == pygame.K_4:
				if show_main_menu:
					if coins >= required_coins_4:
						player_lives += 1
						coins -= required_coins_4
						required_coins_4 += 25
			elif event.key == pygame.K_TAB:
				if show_main_menu == True:
					show_main_menu = False
					player_lives = 3
					wave = 1
					

	# check keypresses
	keystate = pygame.key.get_pressed()
	mousestate = pygame.mouse.get_pressed()
	if keystate[pygame.K_SPACE] or mousestate[0]:
		player.shoot(bullets, all_sprites)

	# Update
	if not show_main_menu:
		all_sprites.update()
	# Check if a Mob hits Player
	hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
	for hit in hits:
		player_lives -= 1
		coins += 1
		if player_lives == 0:
			show_main_menu = True
	# check to see if a bullet hit a mob
	hits = pygame.sprite.groupcollide(mobs, bullets, False, True, pygame.sprite.collide_circle)
	for hit in hits:
		coins += 1
		hit.hit()

	# generate mobs
	if show_main_menu == False:
		now = pygame.time.get_ticks()
		if now - last_mob_spawn > mob_spawn_delay:
			if mobs_per_wave < max_mob_spawn_per_wave:
				newmob()
				last_mob_spawn = now
			else:
				if len(mobs) == 0:
					show_wave_text = True

	# Draw / render
	screen.fill(BLACK)
	screen.blit(background, background_rect)
	draw_coins(screen)
	draw_lives(screen)
	draw_wave(screen)
	if show_wave_text:
		draw_wave_text(screen)
	if show_main_menu:
		draw_main_menu(screen)
		draw_shop_reload(screen)
		draw_shop_bullet_speed(screen)
		draw_shop_movement_speed(screen)
		draw_shop_lives(screen)
	if not show_main_menu:
		all_sprites.draw(screen)
	# *after* drawing everything, flip the display
	pygame.display.flip()
	clock.tick(FPS)
pygame.quit()

