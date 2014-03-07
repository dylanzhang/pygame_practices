'''
This is a desktop shoot game imitating WeChat's Pencil Pilot using pygame

@author Dylan
@email amzhang.ustc AT gmail.com
@date March 5th, 2014
@version 1.0
'''

# 1 - Import related libraries
import sys, random, pygame
from pygame.locals import *
from Characters import *
from utils import *


# 2 - Initialize the game
pygame.init()
# Set window size, screen_wid, screen_hei is defined in Characters model
screen = pygame.display.set_mode([screen_wid, screen_hei])
pygame.display.set_caption("Pencil Pilot")

def main_loop():
	# 3 - Load related resources
	# Simple pictures
	gameover_img = pygame.image.load("resource/gameover.png")

	# Simple sounds
	bullet_sound = pygame.mixer.Sound("resource/sound/bullet.wav")
	enemy1_down_sound = pygame.mixer.Sound("resource/sound/enemy1_down.wav")
	gameover_sound = pygame.mixer.Sound("resource/sound/game_over.wav")
	outporp_sound = pygame.mixer.Sound("resource/sound/out_porp.wav")
	bullet_sound.set_volume(0.3)
	enemy1_down_sound.set_volume(0.3)
	gameover_sound.set_volume(0.3)
	outporp_sound.set_volume(0.3)
	pygame.mixer.music.load("resource/sound/game_music.wav")
	pygame.mixer.music.play(-1, 0.0)
	pygame.mixer.music.set_volume(0.25)

	# 3.1 - Loading pictures and Background
	bg_img = pygame.image.load("resource/shoot_background.png")
	# bg_dict = {img_name : pygame.Rect}
	bg_dict = {}
	data_parser('shoot_background.pack', bg_dict)
	background = bg_img.subsurface(bg_dict['background'])

	# 3.2 - Planes and bullets
	plane_img = pygame.image.load("resource/shoot.png")
	plane_dict = {}
	data_parser('shoot.pack', plane_dict)

	# 3.2.1 - Hero planes
	hero_rec = []
	# Basic heros
	hero_rec.append(pygame.Rect(plane_dict['hero1']))
	hero_rec.append(pygame.Rect(plane_dict['hero2']))
	# Hero blowup
	hero_rec.append(pygame.Rect(plane_dict['hero_blowup_n1']))
	hero_rec.append(pygame.Rect(plane_dict['hero_blowup_n2']))
	hero_rec.append(pygame.Rect(plane_dict['hero_blowup_n3']))
	hero_rec.append(pygame.Rect(plane_dict['hero_blowup_n4']))

	# 3.2.2 - Bullets
	bullet1_img = plane_img.subsurface(plane_dict['bullet1'])
	bullet2_img = plane_img.subsurface(plane_dict['bullet2'])

	# 3.2.3 - Enemies
	enemy1_img = plane_img.subsurface(plane_dict['enemy1'])
	enemy1_down_imgs = []
	enemy1_down_imgs.append(plane_img.subsurface(plane_dict['enemy1_down1']))
	enemy1_down_imgs.append(plane_img.subsurface(plane_dict['enemy1_down2']))
	enemy1_down_imgs.append(plane_img.subsurface(plane_dict['enemy1_down3']))
	enemy1_down_imgs.append(plane_img.subsurface(plane_dict['enemy1_down3']))


	# 4 - Main loop

	# Hero initial position
	hero_pos = [140, 600]
	# Create an initial hero object
	hero = Hero(plane_img, hero_rec, hero_pos)
	# Keys to control the hero
	keys = [False, False, False, False]	# W, A, S, D

	enemy1_timer1 = 20 					# How long occurs an enemy
	enemy1_timer2 = 0					# Control the speed of the enemy occurs
	enemies = pygame.sprite.Group()		# enemies in a group
	enemies_down = pygame.sprite.Group()

	control_freq = 0	# Control the bullets and enemies ...
	running = True		# Control the main loop
	shoot_timer = 10 	# Control the bullets
	enemy_cnt = 0		# Make sure that enemy speedup for every ten enemies
	enemy_vel = 2 		# Enemy initial velocity
	score = 0			# Game score
	hero_down_index = 0
	clock = pygame.time.Clock()

	while running:
		clock.tick(60)
		control_freq += 1
		shoot_timer -= 1
		enemy1_timer1 -= 1
		

		# 5 - Clear the screen before drawing
		screen.fill(0)


		# 6 - Draw pictures on the screen
		screen.blit(background, [0, 0])

		# 6.1 - Draw the hero on the screen
		if not hero.is_hit:
			screen.blit(hero.img[hero.img_ix], hero.rect)
			hero.img_ix = control_freq % 2
		else:
			hero.img_ix = 2 + hero_down_index / 8
			screen.blit(hero.img[hero.img_ix], hero.rect)
			hero_down_index += 1
			if hero_down_index > 24:
				gameover_sound.play()
				running = False

		# 6.2 - Draw bullets
		if not hero.is_hit and shoot_timer <= 0:
			hero.shoot(bullet1_img)
			bullet_sound.play()
			shoot_timer = 10
			
		for bullet in hero.bullets:
			bullet.move()
			if bullet.rect.bottom < 0:
				hero.bullets.remove(bullet)

		hero.bullets.draw(screen)

		# 6.3 - Draw enemies
		if enemy1_timer1 <= 0:
			enemy_cnt += 1
			# Speedup once every 10 planes
			if enemy_cnt == 5 and enemy_vel < 7:
				enemy_vel += 1
				enemy_cnt = 0

			enemies.add(Enemy(enemy1_img, enemy1_down_imgs, [random.randint(0, screen_wid-enemy1_img.get_width()), 0], enemy_vel))
			enemy1_timer1 = 100 - enemy1_timer2
		else:
			if enemy1_timer2 <= 40:
				enemy1_timer2 += 1
			else:
				enemy1_timer2 = 40

		for enemy1 in enemies:
			enemy1.move()

			# Test whether enemies collide with the hero
			if pygame.sprite.collide_circle(enemy1, hero):
				enemies_down.add(enemy1)
				enemies.remove(enemy1)
				hero.is_hit = True

			# Test whether enemies collide with bullet
			for bullet1 in hero.bullets:
				if pygame.sprite.collide_rect(enemy1, bullet1):
					enemies_down.add(enemy1)
					enemies.remove(enemy1)
					hero.bullets.remove(bullet1)
					
			if enemy1.rect.top >= screen_hei:
				enemies.remove(enemy1)

		enemies.draw(screen)

		# Enemy collide animation
		for enemy_down in enemies_down:
			if enemy_down.down_index == 0:
				enemy1_down_sound.play()
			elif enemy_down.down_index >= 8:
				enemies_down.remove(enemy_down)
				score += 1000
				continue
			screen.blit(enemy_down.down_imgs[enemy_down.down_index / 2], enemy_down.rect)
			enemy_down.down_index += 1


		# 6.4 - Draw score
		score_font = pygame.font.Font(None, 36)
		score_text = score_font.render(str(score), True, (128, 128, 128))
		score_rect = score_text.get_rect()
		score_rect.topleft = [10, 10]
		screen.blit(score_text, score_rect)
		
		# 7 - Update the screen
		pygame.display.update()


		# 8 - Loop through events
		for event in pygame.event.get():
			# Handle the 'X' with exit
			if event.type == QUIT:
				pygame.quit()
				sys.exit(0)

			# Move hero
			if event.type == KEYDOWN:
				if event.key == K_w or event.key == K_UP:
					keys[0] = True
				elif event.key == K_a or event.key == K_LEFT:
					keys[1] = True
				elif event.key == K_s or event.key == K_DOWN:
					keys[2] = True
				elif event.key == K_d or event.key == K_RIGHT:
					keys[3] = True

			if event.type == KEYUP:
				if event.key == K_w or event.key == K_UP:
					keys[0] = False
				elif event.key == K_a or event.key == K_LEFT:
					keys[1] = False
				elif event.key == K_s or event.key == K_DOWN:
					keys[2] = False
				elif event.key == K_d or event.key == K_RIGHT:
					keys[3] = False

			# Shoot
			# if event.type == MOUSEBUTTONDOWN:
			# 	hero.shoot(bullet1_img)
			# 	bullet_sound.play()


		# 9 - Hanle the keys
		if keys[0] == True:
			hero.move_up()
		if keys[1] == True:
			hero.move_left()
		if keys[2] == True:
			hero.move_down()
		if keys[3] == True:
			hero.move_right()


	# 10 - Game over
	while True:
		screen.fill(0)
		screen.blit(background, [0, 0])
		screen.blit(gameover_img, [0, 0])

		# Draw "play again"
		bigfont = pygame.font.Font(None, 40)
		text = bigfont.render('Play again?', True, (128, 128, 128))
		textx_size = text.get_width()
		texty_size = text.get_height()
		textx = screen_wid / 2 - textx_size / 2
		texty = screen_hei / 2 - texty_size / 2
		pygame.draw.rect(screen, (255, 255, 255), ((textx - 5, texty + 10), (textx_size + 10, texty_size + 10)))
		screen.blit(text, (screen_wid / 2 - text.get_width() / 2, screen_hei / 2 - text.get_height() / 2 + 15))
		
		# Draw score
		score_font = pygame.font.Font(None, 50)
		score_text = score_font.render('Score : ' + str(score), True, (128, 128, 128))
		score_rect = score_text.get_rect()
		score_rect.topleft = [screen_wid * 1 / 3 - 15, screen_hei * 3 / 5]
		screen.blit(score_text, score_rect)
		
		pygame.display.update()

		# events on game over page
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit(0)
			if event.type == MOUSEBUTTONDOWN:
				x, y = event.pos
				if x >= textx -15 and x <= textx + textx_size + 15:
					if y >= texty - 15 and y <= texty + texty_size + 30:
						main_loop()

main_loop()

pygame.display.quit()
pygame.quit()