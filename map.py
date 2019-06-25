import random
from classes import Agent, Sun

def setup_map(width, height):
	# Initial Agent Positioning & Motion
	x = x_start = 10
	y = y_start = height
	v_x = v_x_start = 1
	v_y = v_y_start = -4

	# Initial Agent Mass
	m = random.randint(2, 8) / 10

	# Initial Sun Positioning
	x_sun = random.randint(int(width/5),int(4*width/5))
	y_sun = random.randint(int(height/5),int(4*height/5))

	agent = Agent(m, x, y, v_x, v_y)
	sun = Sun(10, x_sun, y_sun)

	return(agent,sun)

def check_quadrant(x,y,x_sun,y_sun):
	# Where top right is zero, and 
	# it counts clockwise from there
	if x > x_sun and y < y_sun:
		quad = 1
	if x < x_sun and y < y_sun:
		quad = 2
	if x < x_sun and y > y_sun:
		quad = 3
	if x > x_sun and y > y_sun:
		quad = 4

	return quad