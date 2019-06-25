import random
from classes import Agent, Sun, Astroid

def setup_map(width, height):
	# Initial Agent Positioning & Motion
	x = x_start = 10
	y = y_start = height
	v_x = v_x_start = 1
	v_y = v_y_start = -4

	# Initial Agent Mass
	m = random.randint(2, 5) / 10

	# Initial Sun Positioning
	x_sun = random.randint(int(width/5),int(4*width/5))
	y_sun = random.randint(int(height/5),int(4*height/5))

	agent = Agent(m, x, y, v_x, v_y)
	sun = Sun(10, x_sun, y_sun)

	return(agent,sun)

def random_astroid(width, height):
	#Create an astroid
	x = x_start = 500
	y = y_start = height
	v_x = v_x_start = random.randint(-8,8)
	v_y = v_y_start = random.randint(-10,0)
	m = random.randint(2, 8) / 10
	astroid = Astroid(m, x, y, v_x, v_y)
	return astroid

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