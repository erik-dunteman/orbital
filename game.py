import os
import platform

import pygame
from pygame.locals import *
import math

from physics import accelerate, bounce
from map import setup_map, check_quadrant, random_astroid
from rl_utils import observe, get_action, get_state, load_Qtable, init_Qtable, update_Qtable, save_Qtable, save_logs, read_logs, track_stats
from db_utils import write
from classes import Agent, Sun, Astroid


def run(controller, screen, session_len, statespace, mode, alpha, gamma, epsilon, 
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
	
	episode = 0

	# Global Variables for Reinforcement Learning
	if controller == "Agent":
		
		#construct identifying string for hyperparameters
		hyperstring = "a" + str(alpha) + "_g" + str(gamma) + "_e" + str(epsilon)

		try:
			q_table = load_Qtable(statespace, mode, hyperstring)
		except:
			q_table = init_Qtable(statespace)

		episode = read_logs(statespace, mode, hyperstring)
		episode_session_start = episode

		# Variables for counting the amount of frames per episode where the agent is acting "blindly"
		blind_frames = 0
		episode_frames = 0

		

#__________________________________
#__________________________________
# Fire-up
	if screen == "ScreenOn": 
		print('Display Setup, as Screen is True')
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
	if mode == "Astroids":
		astroids = [random_astroid(width,height)]



#__________________________________
#__________________________________
# Game Logic

	while not done:
		
		# Set default variables
		thrust = "None"

	#__________________________________
	#__________________________________
	# Loop break conditions
		
		# Give User [X] override ability to kill game
		if screen == "ScreenOn":
			for event in pygame.event.get():
					if event.type == pygame.QUIT:
						done = True
						if controller == "Agent":
							save_Qtable(q_table, statespace, mode, hyperstring)
							save_logs(statespace, mode, hyperstring, episode)
						pygame.quit()

	#__________________________________
	#__________________________________
	# Observe pre_action_state

		if controller == "Agent" and pre_action_state == None:
			observation = observe(agent, sun, fuel, width, height)
			pre_action_state = get_state(observation, statespace)

		
	#__________________________________
	#__________________________________
	# Get Action

		action = None

		if controller == "Agent": #The Agent is in control
			action, blind_frames = get_action(q_table, pre_action_state, epsilon, blind_frames)
		
		else: #The User is in control
			# Check User Input
			pressed = pygame.key.get_pressed()
			# Respond to Up (Thrust Away From Sun)
			if pressed[pygame.K_UP]:
				# print("UP")
				action = 1
			# Respond to Down (Thrust Toward Sun)
			if pressed[pygame.K_DOWN]:
				# print("DOWN")
				action = 2

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
		if screen == "ScreenOn":
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
# Frame End Functions (Cleanup)

		# Limit while loop
		if controller == "Self":
			clock.tick(50)

		# Increment frames per episode
		if controller == "Agent":
			episode_frames += 1

#__________________________________
#__________________________________
# Game Failure Screen - Breakout Loop

		while fail:

			if screen == "ScreenOn":
				# Listen for exit button
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						done = True
						if controller == "Agent":
							save_Qtable(q_table, statespace, mode, hyperstring)
							save_logs(statespace, mode, hyperstring, episode)
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


			# Save that Episode's stats
			if controller == "Agent":
				if episode % 1000 == 0:
					print("Episode: ", episode)
				blind_fraction = round(blind_frames/episode_frames, 5)
				track_stats(statespace, mode, hyperstring, episode, agent_score, blind_fraction)

				# Kill the game if limited training session is done
				if session_len != None:
					if episode + 1 - episode_session_start >= session_len:
						done = True
						save_Qtable(q_table, statespace, mode, hyperstring)
						save_logs(statespace, mode, hyperstring, episode)



			# Check to see if agent wants new game
			if controller == "Self":
				pressed = pygame.key.get_pressed()
				pressed_space = pressed[pygame.K_SPACE]
			else:
				pressed_space = True

			if pressed_space:

				# Set up Map
				agent, sun = setup_map(width, height)
				astroids = []

				# Reset Operating Variables
				fuel = 200
				score = 0
				quad = 3

				# Reset Agent Score
				agent_score = 0

				# Reset Frames per Episode
				episode_frames = 0

				# Reset Blind Frames per Episode
				blind_frames = 0

				# Increment Episode
				episode += 1
				

				# Kick out of Fail Loop
				fail = False
