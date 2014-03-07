#!/usr/bin/python

# This is a pygame demo to help me understanding
# the way of writing an interesting game.
# This demo is a practice of 
# http://www.raywenderlich.com/24252/beginning-game-programming-for-teens-with-python

# 1 - import related library
import pygame, sys, math, random
from pygame.locals import *

# 2 - Initialize the game
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

# Control the bunny
keys = [False, False, False, False] # W, A, S, D
bunny_position = [100, 100]

# Shoot control
accurate = [0, 0] # [shoot count, arrow count]
arrows = [] # [arrow angle, arrow position x, arrow position y]

# Badbuy control
badtimer = 100	# after badtimer, spawn a new badger
badtimer1 = 0	# control the how long the next badger spawn
badguys = [[640, 100]]	# position of badguys

healthvalue = 194	# Healthvalue of the entire game

# Init the sound
pygame.mixer.init()

# 3 - Load the pictures
bunny = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
badguyimg1 = pygame.image.load("resources/images/badguy.png")
badguyimg = badguyimg1
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

# 3.1 - Load audio
hit_sound = pygame.mixer.Sound("resources/audio/explode.wav")
enemy_sound = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot_sound = pygame.mixer.Sound("resources/audio/shoot.wav")
hit_sound.set_volume(0.05)
enemy_sound.set_volume(0.05)
shoot_sound.set_volume(0.05)
pygame.mixer.music.load("resources/audio/moonlight.wav")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# 4 - Main loop
running = True 	# Keep track of whether the game is over
exitcode = 0	# Keep track of whether the player win(1) or lose(0)
while running:
	# Decrement the badtimer
	badtimer -= 1
	# 5 - clear the screen before drawing it again
	screen.fill(0)

	# 6 - Draw the elements on the screen
	for x in xrange(width/grass.get_width() + 1):
		for y in xrange(height/grass.get_height() + 1):
			screen.blit(grass, [x * grass.get_width(), y * grass.get_height()])
	
	for y in xrange(4):
		screen.blit(castle, [0, 30+y*105])
	
	# 6.1 - Rotate the buny
	mouse_position = pygame.mouse.get_pos()
	angle = math.atan2(mouse_position[1]-(bunny_position[1]+bunny.get_height()/2), 
		mouse_position[0]-(bunny_position[0]+bunny.get_width()/2))
	bunny_rot = pygame.transform.rotate(bunny, -angle * 57.29)
	bunny_rot_position = [bunny_position[0]+bunny.get_width()/2-bunny_rot.get_rect().width/2, bunny_position[1]+bunny.get_height()/2-bunny_rot.get_rect().height/2]
	screen.blit(bunny_rot, bunny_rot_position)

	# 6.2 - Draw arrows
	index = 0
	for bullet in arrows:
		# Calculate the arrow speed
		velx = math.cos(bullet[0]) * 10
		vely = math.sin(bullet[0]) * 10
		bullet[1] += velx
		bullet[2] += vely
		if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
			arrows.pop(index)
			index -= 1
		index += 1
		for projectile in arrows:
			arrow1 = pygame.transform.rotate(arrow, -projectile[0]*57.29)
			screen.blit(arrow1, [projectile[1], projectile[2]])

	# 6.3 - Draw badgers
	# Spawn a badger
	if badtimer == 0:
		badguys.append([640, random.randint(50, 430)])
		badtimer = 100 - (badtimer1 * 2)
		if badtimer1 >= 25:
			badtimer1 = 25
		else:
			badtimer1 += 5

	# Delete a badger
	index = 0
	for badguy in badguys:
		if badguy[0] < -64:
			badguys.pop(index)
			index -= 1
		badguy[0] -= 5

		# 6.3.1 - Attack castle
		badger_rect = badguyimg.get_rect()
		badger_rect.top = badguy[1]
		badger_rect.left = badguy[0]
		if badger_rect.left < 64:
			hit_sound.play()
			healthvalue -= random.randint(5, 20)
			badguys.pop(index)
			index -= 1

		# 6.3.2 - Check for collisions between arrow and badger
		index1 = 0
		for bullet in arrows:
			bullet_rect = arrow.get_rect()
			bullet_rect.left = bullet[1]
			bullet_rect.top = bullet[2]
			if badger_rect.colliderect(bullet_rect):
				enemy_sound.play()
				accurate[0] += 1
				badguys.pop(index)
				index -= 1
				arrows.pop(index1)
				index1 -= 1
			index1 += 1

		# 6.3.3 - Next bad guy
		index += 1

	# Draw a badger
	for badguy in badguys:
		screen.blit(badguyimg, badguy)

	# 6.4 - Draw a clock
	font = pygame.font.Font(None, 24)
	survive_time = font.render(str((90000-pygame.time.get_ticks())/60000)+":"+str((90000-pygame.time.get_ticks())/1000%60).zfill(2),
		True, (0,0,0))
	survive_time_rec = survive_time.get_rect()
	survive_time_rec.topright = [635, 5]
	screen.blit(survive_time, survive_time_rec)

	# 6.5 - Draw health bar
	screen.blit(healthbar, [5, 5])
	for health_value in xrange(healthvalue):
		screen.blit(health, [health_value+8, 8])

	# 7 - Update the screen
	pygame.display.update()

	# 8 - Loop through events
	for event in pygame.event.get():
		# Check if he event is the X button
		if event.type == QUIT:
			pygame.quit()
			sys.exit(0)

		# Buny movement controls
		if event.type == KEYDOWN:
			if event.key == K_w:
				keys[0] = True
			elif event.key == K_a:
				keys[1] = True
			elif event.key == K_s:
				keys[2] = True
			elif event.key == K_d:
				keys[3] = True
		if event.type == KEYUP:
			if event.key == K_w:
				keys[0] = False
			elif event.key == K_a:
				keys[1] = False
			elif event.key == K_s:
				keys[2] = False
			elif event.key == K_d:
				keys[3] = False

		# Shoot control
		if event.type == MOUSEBUTTONDOWN:
			shoot_sound.play()
			mouse_position = pygame.mouse.get_pos()
			accurate[1] += 1
			arrows.append([math.atan2(mouse_position[1]-(bunny_rot_position[1]+bunny_rot.get_width()/2),
				mouse_position[0]-(bunny_rot_position[0]+bunny_rot.get_height()/2)), 
				bunny_rot_position[0] + bunny_rot.get_width()/2, bunny_rot_position[1] + bunny_rot.get_height()/2])


	# 9 - Move the buny
	if keys[0] == True:
		bunny_position[1] -= 5
	elif keys[2] == True:
		bunny_position[1] += 5

	if keys[1] == True:
		bunny_position[0] -= 5
	elif keys[3] == True:
		bunny_position[0] += 5

	# 10 - Win/Lose Check
	if pygame.time.get_ticks() >= 90000:
		running = False
		exitcode = 1
	if healthvalue <= 0:
		running = False
		exitcode = 0
	if accurate[1] != 0:
		score = accurate[0] * 1.0 / accurate[1] * 100
	else:
		score = 0

# 11 - Win/Lose display
if exitcode == 0:
	# Lose
	pygame.font.init()
	font = pygame.font.Font(None, 24)
	text = font.render("Accuracy :" + str(score) + "%", True, (255, 0, 0))
	text_rect = text.get_rect()
	text_rect.centerx = screen.get_rect().centerx
	text_rect.centery = screen.get_rect().centery + 24
	screen.blit(gameover, [0, 0])
	screen.blit(text, text_rect)
else:
	# Win
	pygame.font.init()
	font = pygame.font.Font(None, 24)
	text = font.render("Accuracy :" + str(score) + "%", True, (255, 0, 0))
	text_rect = text.get_rect()
	text_rect.centerx = screen.get_rect().centerx
	text_rect.centery = screen.get_rect().centery + 24
	screen.blit(youwin, [0, 0])
	screen.blit(text, text_rect)

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit(0)
	pygame.display.flip()