import pygame
from pygame import Vector2

class Button:
	pygame.font.init()
	all_buttons = []
	last_mouse_pos = (0,0)

	def __init__(self, xy, wh, color=(255,255,255), hover_color=(150,150,150), left=False):
		self.pos = Vector2(xy)
		self.width = wh[0]
		self.height = wh[1]
		self.rect = pygame.Rect(xy, wh)

		if not left:
			self.line = [
				(0,0),
				(wh[0], wh[1]/2),
				(0, wh[1]),
				(0,0),
			]
		else:
			self.line = [
				(wh[0],0),
				(0, wh[1]/2),
				(wh[0], wh[1]),
				(wh[0],0),
			]

		self.clicked = False

		self.color = color
		self.hover_color = hover_color

		self.all_buttons.append(self)

	def render(self, surface):

		line1 = (self.line[0][0] + self.pos.x, self.line[0][1] + self.pos.y)
		line2 = (self.line[1][0] + self.pos.x, self.line[1][1] + self.pos.y)
		line3 = (self.line[2][0] + self.pos.x, self.line[2][1] + self.pos.y)
		line4 = (self.line[3][0] + self.pos.x, self.line[3][1] + self.pos.y)

		all_line = [line1, line2, line3, line4]
		if self.check_collisions(self.last_mouse_pos):
			self.rect = pygame.draw.polygon(surface, self.hover_color, all_line)
		else:
			self.rect = pygame.draw.polygon(surface, self.color, all_line)


	@classmethod
	def handle_event(cls, events):
		for event in events:
			for btn in cls.all_buttons:
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1 and btn.check_collisions(event.pos):
						btn.clicked = True
				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						btn.clicked = False

		cls.last_mouse_pos = pygame.mouse.get_pos()

	def get_click(self):
		return self.clicked

	def check_collisions(self, mouse_pos):
		return self.rect.collidepoint(mouse_pos)

	@classmethod
	def check_all_col(cls, mouse_pos):
		for btn in cls.all_buttons:
			if btn.check_collisions(mouse_pos): return True

	@classmethod
	def clear_all(cls):
		cls.all_buttons.clear()


