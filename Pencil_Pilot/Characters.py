'''
This file contains the class of every character
'''

import pygame
from pygame.locals import *

# Window size
screen_wid, screen_hei = 480, 800

class Hero(pygame.sprite.Sprite):
	def __init__(self, plane_img, hero_rec, hero_pos):
		pygame.sprite.Sprite.__init__(self)
		
		self.img = []				# hero's images
		for rect in hero_rec:
			self.img.append(plane_img.subsurface(rect).convert_alpha())
		self.img_ix = 0				# Current image index

		self.rect = hero_rec[0]		# rectangle of the hero
		self.rect.topleft = hero_pos# postition of the hero
		self.radius = self.rect.width / 5	# Set the radius of the Hero for collide test
		
		self.vel = 10				# Velocity of the hero

		self.bullets = pygame.sprite.Group()	# Bullets
		self.is_hit = False						# Whether the hero is hit or not

	def shoot(self, bullet_img):
		bullet = Bullet(bullet_img, self.rect.midtop)
		self.bullets.add(bullet)

	def move_up(self):
		if self.rect.top >= -self.rect.height / 2:
			self.rect.top -= self.vel
	
	def move_down(self):
		if self.rect.top <= screen_hei - self.rect.height / 2:
			self.rect.top += self.vel

	def move_left(self):
		if self.rect.left >= -self.rect.width / 2:
			self.rect.left -= self.vel

	def move_right(self):
		if self.rect.right <= screen_wid + self.rect.width / 2:
			self.rect.left +=self.vel

# Bullet of the hero
class Bullet(pygame.sprite.Sprite):
	def __init__(self, bullet_img, bullet_midbottom):
		pygame.sprite.Sprite.__init__(self)
		self.image = bullet_img
		self.rect = self.image.get_rect()
		self.rect.midbottom = bullet_midbottom
		self.vel = 12 	# Velocity of the bullet

	def move(self):
		self.rect.top -= self.vel

class Enemy(pygame.sprite.Sprite):
	def __init__(self, enemy_img, enemy_down_imgs, enemy_pos, enemy_vel):
		pygame.sprite.Sprite.__init__(self)
		self.image = enemy_img
		self.rect = self.image.get_rect()
		self.rect.topleft = enemy_pos
		self.vel = enemy_vel

		self.down_imgs = enemy_down_imgs
		self.down_index = 0

	def move(self):
		self.rect.top += self.vel