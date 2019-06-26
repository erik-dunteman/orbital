import math

def observe(agent, sun, fuel, width, height):
	r = math.sqrt((sun.x - agent.x)**2 + (sun.y - agent.y)**2)
	wall_dist = min(agent.x, agent.y, width - agent.x, height - agent.y)
	return [round(agent.v_x,3), round(agent.v_y,3), round(r,2), int(wall_dist), agent.m, fuel]