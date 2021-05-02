
import pygame

class FontText:
	pygame.font.init()
	title = None
	normal = None
	empty = None

	@classmethod
	def update(cls):
		cls.font_22 = pygame.font.Font(cls.empty, 22)
		cls.font_small = pygame.font.Font(cls.normal, 18)
		cls.font_normal = pygame.font.Font(cls.normal, 24)
		cls.font_semi_normal = pygame.font.Font(cls.normal, 21)
		cls.font_title = pygame.font.Font(cls.title, 100)
		cls.font_h1 = pygame.font.Font(cls.normal, 80)
		cls.font_h2 = pygame.font.Font(cls.normal, 60)
		cls.font_h3 = pygame.font.Font(cls.normal, 36)

	@staticmethod
	def render(surface, font, pos, text, color, aa=False):
		teks = font.render(str(text), aa, color)
		surface.blit(teks, teks.get_rect(center=pos))

