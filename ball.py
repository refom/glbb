
import pygame
import math

from vec import Vector2D
from utility import FontText, rumus_glbb2, collision_test

class Bola:
	def __init__(self, pos, koef=0, color=(255,255,255), size=50):

		self.color = color
		self.rect = pygame.Rect(pos, (size, size))
		self.size = size

		self.pos = Vector2D(pos)
		self.velocity = Vector2D(0, 0)
		self.acc = Vector2D(0, 0)
		self.rect.bottom = self.pos.y
		self.line_in = [
			Vector2D(0, -self.size/2),
			Vector2D(0, self.size/2),
		]
		self.line_out = [
			Vector2D(0, -self.size/2),
			Vector2D(0, self.size/2),
		]

		self.angle_degrees = 0
		self.limit_vel = Vector2D(3, 7)
		self.speed = Vector2D(2, 15)
		self.gravity = 9.8/20
		self.friction = -0.1
		self.koef = koef
		self.massa = math.pi * size/2 * size/2
		self.keliling = math.pi * size

		self.constant = False
		self.constant_spd = 2
		self.left, self.right = False, False
		self.scale_up, self.scale_down = False, False
		self.in_air, self.can_bounce = False, False
		self.points = []

		self.button_down = False
		self.selected = False
		self.last_mouse_pos = Vector2D(0,0)
		self.spring_force, self.drag_force = Vector2D(0,0), Vector2D(0,0)
		self.tali_str = 10
		self.drag_acc = self.tali_str * 2


	def draw(self, surface):
		pygame.draw.ellipse(surface, self.color, self.rect)
		point_a = (self.line_out[0].x + self.rect.centerx, self.line_out[0].y + self.rect.centery)
		point_b = (self.line_out[1].x + self.rect.centerx, self.line_out[1].y + self.rect.centery)
		pygame.draw.line(surface, (255,0,0), point_a, point_b, 5)
	
		for i in self.points:
			pygame.draw.circle(surface, (100,255,100), i.xy, 10)

		if len(self.points) % 2 == 0:
			for i, point in enumerate(self.points):
				if (i+1) % 2 == 0:
					continue
				p1 = self.points[i]
				p2 = self.points[i+1]
				length_x = p1.x - p2.x
				length_y = p1.y - p2.y
				mid = (p1.x - length_x//2, p1.y - length_y//2)

				pygame.draw.line(surface, (100,100,255), p1.xy, p2.xy)
				teks = FontText.font_normal.render(f"{abs(int(length_x))}", False, (255,255,255))
				surface.blit(teks, mid)
		
	def draw_string(self, surface):
		pygame.draw.line(surface, (100,255,100), self.rect.center, self.last_mouse_pos.xy, 2)


	def update(self, dt):
		self.scaling()
		self.movement_x(dt)
		self.movement_y(dt)


	def scaling(self):
		if self.scale_up:
			self.size += 1
		if self.scale_down:
			self.size -= 1

		self.rect.w = self.rect.h = self.size
		self.massa = math.pi * (self.size/2)**2
		self.keliling = math.pi * self.size

		self.line_in[0].y = -self.size/2
		self.line_in[1].y = self.size/2

	def movement_x(self, dt):
		x_forces = 0
		
		if self.left:
			x_forces -= self.speed.x
		if self.right:
			x_forces += self.speed.x
		
		if self.constant:
			x_forces = self.constant_spd

		all_forces = (self.massa * x_forces) + self.spring_force.x + self.drag_force.x
		acc_benda = all_forces / self.massa
		self.acc.x = acc_benda
		
		# pengurangan karena gesekan
		self.acc.x += self.velocity.x * self.friction

		vel_end, s = rumus_glbb2(self.velocity.x, self.acc.x, dt)
		self.pos.x += s
		# self.velocity.x = vel_end

		# line
		r = self.size/2
		teta = s / r
		degree = math.degrees(teta)
		v = r * teta / dt
		# w = v / r
		# v_end = math.degrees(w)

		self.velocity.x = v

		self.angle_degrees = self.angle_degrees % 360 + degree
		for i in range(len(self.line_in)):
			self.line_out[i] = self.line_in[i].rotate(self.angle_degrees)

		if self.pos.x < 0:
			self.pos.x = 0
			self.velocity.x *= -1
			if self.constant:
				self.constant_spd *= -1
		elif self.pos.x > 1000 - self.size:
			self.pos.x = 1000 - self.size
			self.velocity.x *= -1
			if self.constant:
				self.constant_spd *= -1

		self.rect.x = self.pos.x
		self.spring_force.x = 0
		self.drag_force.x = 0

		# if self.velocity.x > self.limit_vel.x:
		# 	self.velocity.x = self.limit_vel.x
		# elif self.velocity.x < -self.limit_vel.x:
		# 	self.velocity.x = -self.limit_vel.x
		if abs(self.velocity.x) < 0.01: self.velocity.x = 0


	def movement_y(self, dt):
		all_forces = (self.massa * self.gravity) + self.drag_force.y + self.spring_force.y
		acc_benda = all_forces / self.massa
		self.acc.y = acc_benda

		vel_end, s = rumus_glbb2(self.velocity.y, self.acc.y, dt)
		self.pos.y += s
		self.velocity.y = vel_end

		if self.pos.y > 600:
			if self.can_bounce:
				self.fix_bounce()
				self.velocity.y = -self.velocity.y * self.koef
				if abs(self.velocity.y) < 3.5: self.in_air = False
			else:
				self.velocity.y = 0
				self.in_air = False
			self.pos.y = 600
			self.acc.y += -self.acc.y

		self.rect.bottom = self.pos.y
		self.spring_force.y = 0
		self.drag_force.y = 0


	def fix_bounce(self):
		penetrate = 600 - self.pos.y
		if penetrate < 0:
			self.pos.y -= 2 * penetrate

	def jump(self):
		if not self.in_air:
			self.velocity.y -= self.speed.y
			self.in_air = True

	def put_point(self):
		x = self.line_out[0].x + self.rect.centerx
		y = self.line_out[0].y + self.rect.centery
		self.points.append(Vector2D(x, y))


	def grab(self):

		if not self.selected:
			if self.button_down and collision_test(self.rect.x, self.rect.y, self.rect.w, self.rect.h, self.last_mouse_pos.xy):
				self.selected = True
		else:
			if not self.button_down:
				self.selected = False
			else:
				# X
				dx = self.last_mouse_pos.x - self.rect.centerx
				self.spring_force.x += dx * self.tali_str
				self.drag_force.x += self.velocity.x * -1 * self.drag_acc

				# Y
				dy = self.last_mouse_pos.y - self.rect.centery
				self.spring_force.y += dy * self.tali_str
				self.drag_force.y += self.velocity.y * -1 * self.drag_acc


	def get_input(self, events):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					self.button_down = True

			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					self.button_down = False

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
				if event.key == pygame.K_f:
					self.put_point()
				if event.key == pygame.K_g:
					self.points.clear()
				if event.key == pygame.K_e:
					self.scale_up = True
				if event.key == pygame.K_q:
					self.scale_down = True

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a:
					self.left = False
				if event.key == pygame.K_d:
					self.right = False
				if event.key == pygame.K_e:
					self.scale_up = False
				if event.key == pygame.K_q:
					self.scale_down = False

		if self.button_down:
			self.last_mouse_pos.xy = mouse_pos = pygame.mouse.get_pos()
			self.last_mouse_pos.x = mouse_pos[0]
			self.last_mouse_pos.y = mouse_pos[1]


