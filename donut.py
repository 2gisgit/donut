import numpy as np

screen_size = 40
theta_spacing = 0.07
phi_spacing = 0.03
light = np.fromiter(".,-~:;=!*#$@", dtype="<U1")

A = 1
B = 1
R1 = 1
R2 = 2
K2 = 5
K1 = screen_size*K2*3/(8*(R1 + R2))

for _ in range(screen_size*screen_size):
	cos_A = np.cos(A)
	sin_A = np.sin(A)
	cos_B = np.cos(B)
	sin_B = np.sin(B)

	torus = np.full((screen_size, screen_size), " ")
	z_buffer = np.zeros((screen_size, screen_size))
	phi = np.arange(0, 2*np.pi, phi_spacing)
	theta = np.arange(0, 2*np.pi, theta_spacing)
	cos_p = np.cos(phi)
	sin_p = np.sin(phi)
	cos_t = np.cos(theta)
	sin_t = np.sin(theta)
	circle_x = R2 + R1*cos_t
	circle_y = R1*sin_t

	x = (np.outer(cos_B*cos_p + sin_A*sin_B*sin_p, circle_x) - circle_y*cos_A*sin_B).T
	y = (np.outer(sin_B*cos_p - sin_A*cos_B*sin_p, circle_x) + circle_y*cos_A*cos_B).T
	z = ((K2 + cos_A*np.outer(sin_p, circle_x)) + circle_y*sin_A).T
	recz = np.reciprocal(z)
	xp = (screen_size/2 + K1*recz*x).astype(int)
	yp = (screen_size/2 - K1*recz*y).astype(int)
	L1 = (((np.outer(cos_p, cos_t)*sin_B) - cos_A*np.outer(sin_p, cos_t)) - sin_A*sin_t)
	L2 = cos_B*(cos_A*sin_t - np.outer(sin_p, cos_t*sin_A))
	L = np.around(((L1 + L2)*8)).astype(int).T
	mask_L = (L >= 0)
	chars = light[L]

	for i in range(90):
		mask = mask_L[i] & (recz[i] > z_buffer[xp[i], yp[i]])
		z_buffer[xp[i], yp[i]] = np.where(mask, recz[i], z_buffer[xp[i], yp[i]])
		torus[xp[i], yp[i]] = np.where(mask, chars[i], torus[xp[i], yp[i]])

	A += theta_spacing
	B += phi_spacing
	print("\x1b[H")
	print(*[" ".join(arr) for arr in torus], sep="\n")
