
import pygame
from pygame import Vector2


class InputBox:
	pygame.font.init()
	all_input_box = []
	last_mouse_pos = (0,0)

	def __init__(self, xy, wh, value, func_type=int,
				font=None, text_size=18, text_color=(255,255,255), active_color=(102, 255, 102), hover_color=(0,191,255)):
		self.pos = Vector2(xy)
		self.rect = pygame.Rect(xy, wh)

		self.value = value
		self.text = str(value)

		self.text_color = text_color
		self.active_color = active_color
		self.hover_color = hover_color

		self.active = False

		self.func_type = func_type

		self.font = pygame.font.Font(font, text_size)
		
		self.all_input_box.append(self)

	def render(self, surface):
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y

		if self.active:
			text = self.font.render(str(self.text), True, self.active_color)
		else:
			color = self.text_color
			self.text = str(self.value)
			if self.check_collisions(InputBox.last_mouse_pos):
				color = self.hover_color
			text = self.font.render(str(self.text), True, color)
		surface.blit(text, self.rect)

	@classmethod
	def handle_event(cls, events):
		for event in events:
			for i_box in cls.all_input_box:
				if event.type == pygame.MOUSEBUTTONDOWN:
					if i_box.check_collisions(event.pos):
						i_box.active = not i_box.active
					else:
						i_box.active = False

				if event.type == pygame.KEYDOWN and i_box.active:
					if event.key == pygame.K_RETURN:
						try:
							i_box.value = i_box.func_type(i_box.text)
						except:
							i_box.value = 0
						i_box.active = False
					elif event.key == pygame.K_BACKSPACE:
						i_box.text = i_box.text[:-1]
					else:
						i_box.text += event.unicode

		cls.last_mouse_pos = pygame.mouse.get_pos()

	def check_collisions(self, mouse_pos):
		return self.rect.collidepoint(mouse_pos)

	@classmethod
	def check_all_col(cls, mouse_pos):
		for box in cls.all_input_box:
			if box.check_collisions(mouse_pos): return True

	@classmethod
	def clear_all(cls):
		cls.all_input_box.clear()

