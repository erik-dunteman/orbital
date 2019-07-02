import os
import platform

import pygame
from pygame.locals import *
import math

from physics import accelerate, bounce
from map import setup_map, check_quadrant, random_astroid
from rl_utils import observe, get_action, get_state, load_Qtable, init_Qtable, update_Qtable, save_Qtable
from db_utils import write
from classes import Agent, Sun, Astroid


def run(controller, statespace, alpha, gamma, epsilon, 
	frame_reward, lap_reward, wall_reward):
#__________________________________
#__________________________________
# Game Global Variables

	# Window Dimensions
	width = 1920
	height = 1000

	# Colors
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	GREEN = (0, 255, 0)
	RED = (255, 0, 0)

	# Operating Variables
	score = 0
	agent_score = 0
	fuel = 200
	quad = 3
	done = False # This holds the game in a loop
	fail = False # This navigates to the fail screen


	# Log Variables for Reinforcement Learning
	observation = [None, None, None, None, None, None]
	pre_action_state = None
	reward = 0
	episode = 1

	# Global Variables for Reinforcement Learning
	if controller == "Agent":
		try:
			q_table = load_Qtable()
		except:
			q_table = init_Qtable(statespace)

#__________________________________
#__________________________________
# Fire-up

	# Set up display
	bashCommand = 'export DISPLAY=:0'
	os.system(bashCommand)
	os.environ['SDL_VIDEODRIVER']='x11'

	# Initialize Pygame system
	pygame.init()
	pygame.display.init()
	pygame.display.list_modes()
	pygame.font.init()
	myfont = pygame.font.SysFont('Comic Sans MS', 30)
	win = pygame.display.set_mode((width,height))
	clock = pygame.time.Clock()

	# Set up Map
	agent, sun = setup_map(width, height)
	# astroids = [random_astroid(width,height)]



#__________________________________
#__________________________________
# Game Logic

	while not done:
		
		# Set default variables
		thrust = "None"

	#__________________________________
	#__________________________________
	# Observe pre_action_state
		if controller == "Agent" and pre_action_state == None:
			observation = observe(agent, sun, fuel, width, height)
			pre_action_state = get_state(observation, statespace)

	#__________________________________
	#__________________________________
	# Get Action	
		
		# Give User [X] override ability to kill game
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
					save_Qtable(q_table)
					pygame.quit()

		action = None

		if controller == "Self": #The User is in control
			# Check User Input
			pressed = pygame.key.get_pressed()
			# Respond to Up (Thrust Away From Sun)
			if pressed[pygame.K_UP]:
				# print("UP")
				action = "UP"
			# Respond to Down (Thrust Toward Sun)
			if pressed[pygame.K_DOWN]:
				# print("DOWN")
				action = "DOWN"
		
		else: #The Agent is in control
			action = get_action(q_table, pre_action_state, epsilon)

	#__________________________________
	#__________________________________
	# Perform Action

		if action == 1:
			agent = bounce("UP", agent, sun)
			thrust = "UP"
			fuel -= 1
		if action == 2:
			agent = bounce("DOWN", agent, sun)
			thrust = "DOWN"
			fuel -= 1

		# Move the circle
		agent = accelerate(agent, sun)
		agent.x += agent.v_x
		agent.y += agent.v_y


	#__________________________________
	#__________________________________
	# Observe post_action_state and reward

		# Set reward for frame
		reward = frame_reward

		# Update reward if orbit
		# Increment score per orbit (threashold directly below sun)
		new_quad = check_quadrant(agent.x, agent.y, sun.x, sun.y)
		if new_quad == 3 and quad == 4:
			# Then it has passed a lap below the sun
			score += 1
			# Reward it!
			reward = lap_reward
			# if score % 1 == 0:
			# 	astroids.append(random_astroid(width,height))
		quad = new_quad

		# Update reward if out-of-bounds
		if agent.x < 0 or agent.x > width or agent.y < 0 or agent.y > height or fuel <= 0:
			reward = wall_reward
			# observation = observe(agent, sun, fuel, width, height)
			# write(episode, observation, reward)
			fail = True

		# Add reward to cumulative score (for display purposes)
		agent_score += reward

		# Observe post_action_state
		if controller == "Agent":
			observation = observe(agent, sun, fuel, width, height)
			post_action_state = get_state(observation, statespace)


	#__________________________________
	#__________________________________
	# Update Q Table
		q_table = update_Qtable(q_table, action, reward, pre_action_state, post_action_state,
			alpha, gamma)

	#__________________________________
	#__________________________________
	# Update state
		pre_action_state = post_action_state




#__________________________________
#__________________________________
# Observation and Reward Logging
		

		# print('{:<15s}{:<15s}{:<20s}{:<15s}{:<15s}{:<15s}'.format("V_x: " + str(observation[0]), 
		# 	"V_y: " + str(observation[1]), 
		# 	"Radius: " + str(observation[2]), 
		# 	"To Wall: " + str(observation[3]), 
		# 	"Mass: " + str(observation[4]), 
		# 	"Fuel: " + str(observation[5])))

		# write(episode, observation, reward)

#__________________________________
#__________________________________
# Update Environment

		# Move any astroids:
		# for astroid in astroids:
		# 	astroid = accelerate(astroid, sun)
		# 	astroid.x += astroid.v_x
		# 	astroid.y += astroid.v_y

#__________________________________
#__________________________________
# Draw
		
		# The Game Window
		win.fill(BLACK)
		scoretext = myfont.render("Score: " + str(score), False, WHITE)
		win.blit(scoretext, (5,50))
		scoretext = myfont.render("Agent Score: " + str(agent_score), False, WHITE)
		win.blit(scoretext, (5,30))
		episodetext = myfont.render("Episode: " + str(episode), False, WHITE)
		win.blit(episodetext, (5,10))
		fueltext = myfont.render("Fuel: " + str(fuel), False, WHITE)
		win.blit(fueltext, (5,100))
		pygame.draw.rect(win, GREEN,(10, 150, 30, fuel))
		pygame.draw.rect(win, RED, (0,0,width,height), 5)


		# The Features
		pygame.draw.circle(win, WHITE, 
			[int(agent.x), int(agent.y)], int(20*agent.m), 0)
		v_composite = math.sqrt(agent.v_x**2 + agent.v_y**2)
		pygame.draw.line(win, GREEN, [int(agent.x), int(agent.y)], 
			[int(agent.x + (25*agent.v_x)/v_composite), int(agent.y + (25*agent.v_y)/v_composite)], int(20*agent.m))
		pygame.draw.circle(win, RED, [sun.x,sun.y], 50, 0)
		# for astroid in astroids:
		# 	pygame.draw.circle(win, RED, 
		# 	[int(astroid.x), int(astroid.y)], int(20*astroid.m), 0)
		
		if thrust == "UP":
			# Draw a thrust flame toward sun
			r = math.sqrt((agent.x-sun.x)**2 + (agent.y-sun.y)**2)
			pygame.draw.line(win, RED, [int(agent.x), int(agent.y)], 
			[int(agent.x + (sun.x - agent.x)*50/r), int(agent.y + (sun.y - agent.y)*50/r)], int(10*agent.m))
		
		if thrust == "DOWN":
			# Draw a thrust flame away from sun
			r = math.sqrt((agent.x-sun.x)**2 + (agent.y-sun.y)**2)
			pygame.draw.line(win, RED, [int(agent.x), int(agent.y)], 
			[int(agent.x - (sun.x - agent.x)*50/r), int(agent.y - (sun.y - agent.y)*50/r)], int(10*agent.m))


		# Render to Screen
		pygame.display.flip()


#__________________________________
#__________________________________
# Clean Up

		# Limit while loop
		# clock.tick(50)

#__________________________________
#__________________________________
# Game Failure Screen - Breakout Loop

		while fail:

			# Listen for exit button
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
					save_Qtable(q_table)
					pygame.quit()

			# Render window
			win.fill(BLACK)
			textsurface = myfont.render("Score: " + str(score), False, WHITE)
			win.blit(textsurface, (5,5))
			textsurface = myfont.render("Agent Score: " + str(agent_score), False, WHITE)
			win.blit(textsurface, (5,50))
			fail_note = pygame.font.SysFont('Comic Sans MS', 100).render("FAILED", False, WHITE)
			win.blit(fail_note, (width/2,height/2))
			pygame.display.flip()

			# Check to see if agent wants new game
			pressed = pygame.key.get_pressed()
			if pressed[pygame.K_SPACE] or controller == "Agent":

				# Set up Map
				agent, sun = setup_map(width, height)
				astroids = []

				# Reset Operating Variables
				fuel = 200
				score = 0
				quad = 3

				# Reset Agent Score
				agent_score = 0

				# Increment Episode
				episode += 1

				# Kick out of Fail Loop
				fail = False
