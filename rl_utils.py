import math
import numpy as np
import random

def observe(agent, sun, fuel, width, height):
	r = math.sqrt((sun.x - agent.x)**2 + (sun.y - agent.y)**2)
	wall_dist = min(agent.x, agent.y, width - agent.x, height - agent.y)
	return [round(agent.v_x,3), round(agent.v_y,3), round(r,2), int(wall_dist), agent.m, fuel]


def get_state(observation, statespace):
	axis_v_x = 0
	axis_v_y = 0
	axis_r = 0
	axis_wall_dist = 0
	axis_m = 0
	axis_fuel = 0
    
	if statespace == "Tiny":
		def vel_state(v):
			if v < 0:
				neg = True
			else:
				neg = False
            
			v = abs(v)
			if v < 20:
				axis = int((v - (v % 5)) / 5)
			if v >= 20 and v < 100:
				v -= int(20)
				axis = int((v - (v % 40)) / 40) + 4
			if v >= 100:
				axis = 5
            
			if neg:
				axis = 6-1-axis
			else:
				axis = 6+axis
            
			return axis
        
		axis_v_x = vel_state(observation[0])
		axis_v_y = vel_state(observation[1])
        
        
		if observation[2] >= 2500:
			axis_r = 4
		else:
			axis_r = int((observation[2] - (observation[2] % 500)) / 500)
        
		if observation[3] >= 500:
			axis_wall_dist = 4
		else:
			axis_wall_dist = int((observation[3] - (observation[3] % 100)) / 100)
        
		if observation[4] >= 0.5:
			axis_m = 3
		else:
			val = round(observation[4] - 0.2,1)
			# print(val % 0.1)
			axis_m = int((val - (val % 0.1)) / 0.1)
        
		if observation[5] >= 200:
			axis_fuel = 1
		else:
			axis_fuel = int((observation[5] - (observation[5] % 100)) / 100)
        
	state = [axis_v_x, axis_v_y, axis_r, axis_wall_dist, axis_m, axis_fuel]

	return state



def get_action(q_table, state, epsilon):
	
	action_vals = q_table[state[0], state[1], state[2], state[3], state[4], state[5]]

	# Find highest reward action
	action = action_vals.argmax()

	# Add some degree of randomness based on Epsilon
	rand = random.randint(0,100)
	if rand <= epsilon*100:
		print("Random")
		action = random.randint(0,2)

	print("State: " + str(state) + "    Action_Vals: " + str(action_vals) + "    Action: " + str(action))

	return action


def update_Qtable(q_table, action, reward, pre_action_state, post_action_state,
			alpha, gamma):

	action_vals_future = q_table[post_action_state[0], 
	post_action_state[1], post_action_state[2], 
	post_action_state[3], post_action_state[4], 
	post_action_state[5]]

	Q_s1_a1 = int(max(action_vals_future))

	Q_s0_a0 = reward + gamma*(Q_s1_a1)
	q_table[pre_action_state[0], 
	pre_action_state[1], pre_action_state[2], 
	pre_action_state[3], pre_action_state[4], 
	pre_action_state[5], action]

	return q_table
	

def init_Qtable(statespace):
	'''Considering state space with the following bounds:
			v_x , v_y (precision):	-20,20
			v_x , v_y (large):		-100,100
			r:						0, 2165
			wall_dist:				0, 500
			m:						0.2, 0.5
			fuel:					0, 200
	'''
	
	if statespace == "Large" or statespace == "LargeSmoothed":
		'''Considering state space with the following discrete step sizes, bound inclusive:
				v_x , v_y (precision):	0.1 40 discrete states
				v_x , v_y (large):		5 	32 discrete states
					Total					432^2 discrete states
				r:				5			434 discrete states
				wall_dist:		5			101 discrete states
				m:				0.1			4 discrete states
				fuel:			10			21 discrete states

				Total statespace size:		432^2*434*101*4*21 = 690 billion

			Actionspace: 3
		'''
		q_table = np.zeros([433,433,434,101,4,21,3])


	if statespace == "Small":
		'''Considering state space with the following discrete step sizes, bound inclusive:
				v_x , v_y (precision):	1 	40 discrete states 
				v_x , v_y (large):		20 	8 discrete states 
					Total					48^2 discrete states
				r:				100			23 discrete states (note that the final state is a smaller range of 2100 - 2165)
				wall_dist:		50			11 discrete states
				m:				0.1			4 discrete states
				fuel:			40			6 discrete states

				Total statespace size:		48^2*23*11*4*6= 14 million

			Actionspace: 3
		'''
		q_table = np.zeros([48,48,23,11,4,6,3])


	if statespace == "Tiny":
		'''Considering state space with the following discrete step sizes, bound inclusive:
				v_x , v_y (precision):	5 	8 discrete states
				v_x , v_y (large):		40 	4 discrete states
					Total					12^2 discrete states
				r:				500			5 discrete states (note that the final state is a smaller range of 2000 - 2165)
				wall_dist:		100			4 discrete states
				m:				0.1			4 discrete states
				fuel:			100			2 discrete states

				Total statespace size:		12^2*5*6*4*2= 41,472

			Actionspace: 3
		'''
		q_table = np.zeros([13,13,6,6,4,2,3])
	return q_table


def save_Qtable(q_table):
	np.save("q_tiny.npy", q_table)

def load_Qtable():
	print("Loading Q-Table")
	return np.load("q_tiny.npy")

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
