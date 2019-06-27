import math
import numpy as np

def observe(agent, sun, fuel, width, height):
	r = math.sqrt((sun.x - agent.x)**2 + (sun.y - agent.y)**2)
	wall_dist = min(agent.x, agent.y, width - agent.x, height - agent.y)
	return [round(agent.v_x,3), round(agent.v_y,3), round(r,2), int(wall_dist), agent.m, fuel]

def act(pattern, q_table):

	action_space = [None, "UP", "DOWN"]
	random_probability = [0.50, 0.25, 0.25]
	action = None

	if pattern == "Random":
		action = np.random.choice(action_space, 1, random_probability)

	return action, q_table
	


def init_Qtable():
	q_table = np.zeros([5,3])
	return q_table



def smooth_Qtable(q_table):
	''' 
	This function was created to make the statespace seem more continouous.
	
	Why?
	
	Because with a large statespace initialized at zeros, it will take a large amount of time to populate
	the Q table with observations, as each Q value will remain at zero until it has been visited, which is highly unlikely.
	
	The alternative is also not ideal: a small statespace. In this case, the Q table is quickly populated, but the response will be jumpy.

	The smooth function, at each episode, takes the Q table entries and "bleeds" each Q value into the 
	directly adjacent unvisited (zero) cells in the matrix.

	For example, if after the first episode, my Q table looks like this:

	state 	"Up" 	"Down" 	"Stay"
	1		0		0		0
	2		0		0		0
	3		89		12		0
	4		0		0		0
	5		0		0		0
	6		0		34		0
	7		0		0		0

	and "Smooths" the values into adjacent states

	state 	"Up" 	"Down" 	"Stay"
	1		0		0		0
	2		89		12		0
	3		89		12		0
	4		89		12		0
	5		0		34		0
	6		0		34		0
	7		0		34		0

	The smooth function allows the following:
	I can have a large statespace to help make each action more tailored to a narrowly defined state.
	I can populate the table more quickly, without actually visiting

	'''
	return q_table
