import math
from classes import Agent, Sun

def accelerate(body, sun):
	r = math.sqrt((body.x-sun.x)**2 + (body.y-sun.y)**2)
	F = 10000 / (r**2)
	F_x = F * (sun.x-body.x) / r
	F_y = F * (sun.y-body.y) / r
	a_x = F_x / body.m
	a_y = F_y / body.m
	body.v_x += a_x
	body.v_y += a_y
	return body


def bounce (dir, agent, sun):
	r = math.sqrt((agent.x-sun.x)**2 + (agent.y-sun.y)**2)
	v_out_x = 1 * (sun.x-agent.x) / r
	v_out_y = 1 * (sun.y-agent.y) / r
	if dir == "DOWN":
		agent.v_x += v_out_x
		agent.v_y += v_out_y
	else:
		agent.v_x -= v_out_x
		agent.v_y -= v_out_y
	return(agent)