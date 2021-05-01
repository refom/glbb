import pygame, sys, os
from pygame.locals import *

from ball import Bola
from font_teks import FontText
from warna import COLORS

# Window
class Window:
	def __init__(self, screen_size):
		self.size = screen_size

		pygame.display.set_caption("GLBB")
		self.surface = pygame.display.set_mode(screen_size)

		self.clock = pygame.time.Clock()
		self.run = True
		self.fps = 120


def main():
	pygame.init()

	window = Window((1000, 640))
	bola = Bola((400, 450), 0.9)

	# Font
	FontText.title = os.path.join(os.getcwd(), "data", "font", "title.otf")
	FontText.normal = os.path.join(os.getcwd(), "data", "font", "normal.ttf")
	FontText.update()

	while window.run:
		events = pygame.event.get()
		dt = window.clock.tick(120) * 0.001 * window.fps / 1.5

		for event in events:
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()

		bola.get_input(events)
		bola.grab()
		bola.update(dt)

		window.surface.fill(COLORS.black)
		bola.render(window.surface)
		if bola.selected:
			bola.render_string(window.surface)

		# Tanah
		pygame.draw.line(window.surface, COLORS.white, (0, 600), (window.size[0], 600))

		teks = FontText.font_small.render(f"FPS = {int(window.clock.get_fps())}", False, COLORS.white)
		window.surface.blit(teks, (window.size[0] - 100, 20))
		teks = FontText.font_small.render(f"Bola stats:", False, COLORS.white)
		window.surface.blit(teks, (20, 20))
		teks = FontText.font_small.render(f"radius (r) = {bola.size/2}", False, COLORS.white)
		window.surface.blit(teks, (20, 40))
		teks = FontText.font_small.render(f"angle_degrees = {bola.angle_degrees:.4f}", False, COLORS.white)
		window.surface.blit(teks, (20, 60))
		teks = FontText.font_small.render(f"koefisien = {bola.koef}", False, COLORS.white)
		window.surface.blit(teks, (20, 80))
		teks = FontText.font_small.render(f"keliling = {int(bola.keliling)}", False, COLORS.white)
		window.surface.blit(teks, (20, 100))
		teks = FontText.font_small.render(f"massa = {int(bola.massa)}", False, COLORS.white)
		window.surface.blit(teks, (20, 120))
		teks = FontText.font_small.render(f"friction = {bola.friction:.3f}", False, COLORS.white)
		window.surface.blit(teks, (20, 140))
		teks = FontText.font_small.render(f"elastis = {bola.can_bounce}", False, COLORS.white)
		window.surface.blit(teks, (20, 160))
		teks = FontText.font_small.render(f"konstan = {bola.constant}", False, COLORS.white)
		window.surface.blit(teks, (20, 180))

		pygame.display.flip()


if __name__ == "__main__":
	main()

