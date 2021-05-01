import pygame
from pygame.math import Vector2


class Bola:
	def __init__(self, pos, koef=0, color=(255,255,255), width=50, height=50):
		# self.img = pygame.image.load("data/bola.png")
		# self.rect = self.img.get_rect()

		self.color = color
		self.rect = pygame.Rect(pos, (width, height))

		self.pos = Vector2(pos)
		self.velocity = Vector2(0, 0)
		self.acc = Vector2(0, 0)
		self.rect.bottom = self.pos.y

		self.limit_vel = Vector2(3, 7)
		self.speed = Vector2(2, 15)
		self.gravity = 9.8/20
		self.friction = -0.12
		self.koef = koef
		self.massa = width * height
		self.jump_high = 0

		self.constant = False
		self.constant_spd = 3
		self.left, self.right = False, False
		self.in_air, self.can_bounce = False, False

	def draw(self, surface):
		pygame.draw.rect(surface, self.color, self.rect)


	def update(self, dt):

		self.movement_x(dt)
		self.movement_y(dt)


	def movement_x(self, dt):
		self.acc.x = 0
		if self.left:
			self.acc.x -= self.speed.x
		if self.right:
			self.acc.x += self.speed.x
		
		if self.constant:
			self.acc.x = self.constant_spd

		# pengurangan karena gesekan
		self.acc.x += self.velocity.x * self.friction

		# rumus GLBB
		vel_end = self.velocity.x + (self.acc.x * dt)
		# kecepatan rata-rata = posisi akhir - posisi awal = jarak
		vel_avg = (self.velocity.x + vel_end)/2
		self.pos.x += vel_avg * dt

		# bisa juga make ini
		# s = self.velocity.x * dt + (self.acc.x * 0.5) * (dt * dt)
		# self.pos.x += s
		self.velocity.x = vel_end

		if self.pos.x < 0:
			self.pos.x = 0
			self.velocity.x *= -1
			if self.constant:
				self.constant_spd *= -1
		elif self.pos.x > 1000 - self.rect.w:
			self.pos.x = 1000 - self.rect.w
			self.velocity.x *= -1
			if self.constant:
				self.constant_spd *= -1

		self.rect.x = self.pos.x

		if self.velocity.x > self.limit_vel.x:
			self.velocity.x = self.limit_vel.x
		elif self.velocity.x < -self.limit_vel.x:
			self.velocity.x = -self.limit_vel.x
		elif abs(self.velocity.x) < 0.01: self.velocity.x = 0


	def movement_y(self, dt):
		all_forces = self.massa * self.gravity
		acc_benda = all_forces / self.massa
		self.acc.y = acc_benda

		vel_end = self.velocity.y + (self.acc.y * dt)
		vel_avg = (self.velocity.y + vel_end)/2
		self.pos.y += vel_avg * dt
		self.velocity.y = vel_end

		# self.velocity.y += self.acc.y * dt
		# self.pos.y += self.velocity.y * dt + (self.acc.y * 0.5) * (dt * dt)

		if self.velocity.y < self.jump_high:
			self.jump_high = self.velocity.y

		# Batas atas
		if self.pos.y < self.rect.h:
			self.pos.y = self.rect.h

		if self.pos.y > 450:
			if self.can_bounce:
				self.fix_bounce()
				self.velocity.y = -self.velocity.y * self.koef
				if abs(self.velocity.y) < 3.5: self.in_air = False
				# if abs(self.velocity.y) < 3.5: self.can_bounce = False
				
				# if abs(self.velocity.y) < 0.3:
				# 	self.velocity.y = 0
				# 	self.can_bounce = False
				# else:
				# 	self.velocity.y = -1 * self.velocity.y * self.koef
				# self.velocity.y = -self.velocity.y * self.koef
				# if self.velocity.y == 0: self.can_bounce = False
			else:
				self.velocity.y = 0
				self.in_air = False
			self.pos.y = 450
		self.rect.bottom = self.pos.y


	def fix_bounce(self):
		penetrate = 450 - self.pos.y
		if penetrate < 0:
			self.pos.y -= 2 * penetrate
		# forces = -1 * abs(self.jump_high) * self.koef
		# self.velocity.y = forces
		# self.velocity.y = -1 * self.velocity.y * self.koef

		# if abs(self.velocity.y) < 0.1: self.can_bounce = False

		# if not self.jump_high:
		# 	self.velocity.y = 0
		# 	self.can_bounce = False

		# self.jump_high = 0



	def jump(self):
		if not self.in_air:
			self.velocity.y -= self.speed.y
			self.in_air = True


	def get_input(self, events):
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					self.left = True
				if event.key == pygame.K_d:
					self.right = True
				if event.key == pygame.K_w:
					self.jump()
				if event.key == pygame.K_s:
					self.can_bounce = not self.can_bounce
				if event.key == pygame.K_c:
					self.constant = not self.constant

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a:
					self.left = False
				if event.key == pygame.K_d:
					self.right = False
				# if event.key == pygame.K_w:
				# 	pass
				# if event.key == K_s:
				# 	self.down = False
		

# class Bola:
# 	def __init__(self, pos):
# 		self.img_ori = pygame.image.load("data/bola.png")

# 		self.size = [80, 80]
# 		self.pos = Vector2(pos)
# 		self.angle = 0

# 		self.img = pygame.transform.scale(self.img_ori, self.size)
# 		self.current_img = self.img
# 		self.rect = self.img.get_rect(center=pos)

# 		self.v = 200

# 		self.left = False
# 		self.right = False
# 		self.up = False
# 		self.down = False


# 	def move(self, dt):
# 		change = self.v * dt

# 		if self.up:
# 			self.size[0] = self.size[0] + 1
# 			self.size[1] = self.size[1] + 1
# 		if self.down:
# 			self.size[0] = self.size[0] - 1
# 			self.size[1] = self.size[1] - 1

# 		self.img = pygame.transform.scale(self.img_ori, self.size)

# 		if self.left:
# 			self.pos.x -= change
# 			self.angle += (self.v / (self.size[0]//2)) * change
# 		if self.right:
# 			self.pos.x += change
# 			self.angle -= (self.v / (self.size[0]//2)) * change

# 		# clip angle
# 		if self.angle < -360:
# 			self.angle = 360
# 		elif self.angle > 360:
# 			self.angle = -360

# 		self.current_img = pygame.transform.rotate(self.img, self.angle)

# 	def draw(self, surface):
# 		mid = self.current_img.get_rect(center=self.pos.xy)
# 		surface.blit(self.current_img, mid)
