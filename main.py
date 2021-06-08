import pygame, sys, os
from pygame.locals import *

from ball import Bola
from font_teks import FontText
from warna import COLORS
from utility import collision_test
from input_box import InputBox
from button import Button

# Window
class Window:
	def __init__(self, screen_size):
		self.size = screen_size

		pygame.display.set_caption("GLBB")
		self.surface = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

		self.clock = pygame.time.Clock()
		self.run = True
		self.fps = 120
		self.background = pygame.image.load("desert.png")

	def update(self):
		self.size = self.surface.get_size()
		bg = pygame.transform.scale(self.background, self.size)
		self.surface.blit(bg, (0,0))

	

def render_teks(surface, arr, x, y, get_x=False, get_y=False):
	x_temp = 0
	for t in arr:
		t_obj = FontText.font_small.render(t, False, COLORS.black)
		surface.blit(t_obj, (x, y))
		y += 20
		
		r = t_obj.get_rect()
		if r.right > x_temp:
			x_temp = r.right

	if get_x:
		return x_temp
	if get_y:
		return y


def main():
	pygame.init()

	window = Window((1000, 640))
	bola = Bola((400, 450), 0.5, COLORS.deepskyblue)

	# Font
	FontText.title = os.path.join(os.getcwd(), "data", "font", "Kenney Blocks.ttf")
	FontText.normal = os.path.join(os.getcwd(), "data", "font", "Kenney Mini Square.ttf")
	FontText.update()

	si_teks = FontText.font_semi_normal.render(f"Show info >", False, COLORS.black)
	si_rect = si_teks.get_rect(x=20, y=20)
	show_info = False

	stat_teks = FontText.font_semi_normal.render(f"< Bola stats :", False, COLORS.black)
	stat_rect = stat_teks.get_rect(x=20, y=20)

	custom_vel = InputBox((0, 0), (100, 30), 0, text_color=COLORS.black)
	custom_vel.font = FontText.font_small

	btn_right = Button((0,0), (50,50), COLORS.black)
	btn_left = Button((0,0), (50,50), COLORS.black, left=True)

	while window.run:
		events = pygame.event.get()
		dt = window.clock.tick(120) * 0.001 * window.fps / 1.5
		window.update()

		for event in events:
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if not show_info:
					if event.button == 1 and collision_test(si_rect.x, si_rect.y, si_rect.w, si_rect.h, event.pos):
						show_info = True
				else:
					if event.button == 1 and collision_test(stat_rect.x, stat_rect.y, stat_rect.w, stat_rect.h, event.pos):
						show_info = False

		# Input handle
		custom_vel.pos.x = window.size[0] - 120
		custom_vel.pos.y = (window.size[1]/2) - 100

		btn_right.pos.x = window.size[0] - 60
		btn_right.pos.y = (window.size[1]/2) - 60

		btn_left.pos.x = window.size[0] - 120
		btn_left.pos.y = (window.size[1]/2) - 60

		InputBox.handle_event(events)
		Button.handle_event(events)

		if btn_right.get_click():
			bola.velocity.x = custom_vel.value
		elif btn_left.get_click():
			bola.velocity.x = -custom_vel.value


		# Bola handle
		bola.get_input(events)
		bola.grab()
		bola.update(dt, window)

		# Bola
		bola.render(window.surface)
		if bola.selected:
			bola.render_string(window.surface)

		# Custom Velocity
		custom_vel.render(window.surface)
		btn_right.render(window.surface)
		btn_left.render(window.surface)

		# # Tanah
		# pygame.draw.line(window.surface, COLORS.black, (0, 600), (window.size[0], 600))

		teks = FontText.font_small.render(f"fps = {int(window.clock.get_fps())}", False, COLORS.black)
		window.surface.blit(teks, (window.size[0] - 100, 20))
		teks = FontText.font_small.render(f"Elastis = {bola.can_bounce}", False, COLORS.black)
		window.surface.blit(teks, (20, 610))
		teks = FontText.font_small.render(f"Konstan = {bola.constant}", False, COLORS.black)
		window.surface.blit(teks, (220, 610))
		teks = FontText.font_small.render(f"Dalam box = {bola.in_box}", False, COLORS.black)
		window.surface.blit(teks, (420, 610))
		teks = FontText.font_small.render("Custom", False, COLORS.black)
		window.surface.blit(teks, (custom_vel.pos.x, custom_vel.pos.y - 50))
		teks = FontText.font_small.render("Velocity X", False, COLORS.black)
		window.surface.blit(teks, (custom_vel.pos.x, custom_vel.pos.y - 30))

		# info
		if not show_info:
			window.surface.blit(si_teks, si_rect)
		else:
			window.surface.blit(stat_teks, stat_rect)

			teks = [
				f"radius (r)",
				f"angle degrees",
				f"keliling",
				f"massa",
				f"friction",
				f"vel x",
				f"vel y",
				f"koefisien",
			]
			value = [
				f"= {bola.size/2}",
				f"= {bola.angle_degrees:.2f}",
				f"= {int(bola.keliling)}",
				f"= {int(bola.massa)}",
				f"= {bola.friction:.3f}",
				f"= {bola.velocity.x:.3f}",
				f"= {bola.velocity.y:.3f}",
				f"= {bola.koef:.2f}",
			]

			# Teks
			y = 50
			x = render_teks(window.surface, teks, 20, y, get_x=True)
			x += 40

			# Value
			y = render_teks(window.surface, value, x, y, get_y=True)

			# Keys
			y += 20
			teks = FontText.font_small.render("- Keys :", False, COLORS.black)
			window.surface.blit(teks, (20, y))
			y += 20

			teks = [
				"A/D",
				"W",
				"E/Q",
				"S/C",
				"2/1",
				"F/G",
				"B",
			]
			value = [
				"= bergerak kiri/kanan",
				"= lompat",
				"= Besar/Kecilin bola",
				"= Elastis/Konstan",
				"= naik/turunin friction",
				"= pasang/hapus titik",
				"= dalam/luar box",
			]

			# Teks
			x = render_teks(window.surface, teks, 20, y, True)
			x += 40

			# Value
			render_teks(window.surface, value, x, y)

			
		pygame.display.flip()


if __name__ == "__main__":
	main()

