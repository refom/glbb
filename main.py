import pygame, sys
from pygame.locals import *

from ball import Bola
from utility import FontText

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
		bola.update(dt)

		window.surface.fill((0, 0, 0))
		bola.draw(window.surface)
		pygame.draw.line(window.surface, (255,255,255), (0, 450), (window.size[0], 450))

		teks = FontText.font_normal.render(f"velocity_x = {bola.velocity.x}", False, (255,255,255))
		window.surface.blit(teks, (20, 20))
		teks = FontText.font_normal.render(f"velocity_y = {bola.velocity.y}", False, (255,255,255))
		window.surface.blit(teks, (20, 40))
		teks = FontText.font_normal.render(f"koefisien = {bola.koef}", False, (255,255,255))
		window.surface.blit(teks, (20, 60))
		teks = FontText.font_normal.render(f"acc_y = {bola.acc.y}", False, (255,255,255))
		window.surface.blit(teks, (20, 80))
		teks = FontText.font_normal.render(f"angle_degrees = {bola.angle_degrees}", False, (255,255,255))
		window.surface.blit(teks, (20, 100))
		teks = FontText.font_normal.render(f"keliling = {bola.keliling}", False, (255,255,255))
		window.surface.blit(teks, (20, 120))
		teks = FontText.font_normal.render(f"massa = {bola.massa}", False, (255,255,255))
		window.surface.blit(teks, (20, 140))

		pygame.display.flip()


if __name__ == "__main__":
	main()

