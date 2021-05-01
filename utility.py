
# GLBB 1
def rumus_glbb(velocity, acc, dt):
	return velocity * dt + (acc * 0.5) * (dt * dt)

# GLBB 2
def rumus_glbb2(velocity, acc, dt):
	vel_end = velocity + (acc * dt)
	vel_avg = (velocity + vel_end)/2
	s = vel_avg * dt
	return vel_end, s


# Collision
def collision_test(x, y, w, h, mxy, my=None):
	if my == None:
		mx = mxy[0]
		my = mxy[1]
	else:
		mx = mxy
	return mx > x and mx < x + w and my > y and my < y + h


# Mencari Gradien/Slope
def gradien(xy1, xy2):
	try:
		m = (xy2[1] - xy1[1]) / (xy2[0] - xy1[0])
	except ZeroDivisionError:
		m = 0
	return m

# Mencari Persamaan garis
def persamaan(xy1, xy2, panjang):
	m = gradien(xy1, xy2)
	y = xy2[1] + m * (panjang - xy2[0])
	return panjang, y


