import os
import platform

import pygame
from pygame.locals import *
import math

from physics import accelerate, bounce
from map import setup_map, check_quadrant, random_astroid
from rl_utils import observe
from db_utils import write
from classes import Agent, Sun, Astroid

#__________________________________
#__________________________________
# Global Variables

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
fuel = 500
quad = 3
done = False # This holds the game in a loop
fail = False # This navigates to the fail screen


# Log Variables for Reinforcement Learning
observation = [None, None, None, None, None, None]
reward = 0
episode = 1

# Agent Rewards
frame_reward = -1
lap_reward = 100
wall_reward = -10000



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

	# Set reward for frame
	reward = frame_reward

	# Move the circle
	agent = accelerate(agent, sun)
	agent.x += agent.v_x
	agent.y += agent.v_y

	# Move any astroids:
	# for astroid in astroids:
	# 	astroid = accelerate(astroid, sun)
	# 	astroid.x += astroid.v_x
	# 	astroid.y += astroid.v_y


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

	# Check User Input
	pressed = pygame.key.get_pressed()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
			pygame.quit()
			sys.exit()

	# Respond to Up (Thrust Away From Sun)
	if pressed[pygame.K_UP]:
		# print("UP")
		agent = bounce("UP", agent, sun)
		thrust = "UP"
		fuel -= 1

	# Respond to Down (Thrust Toward Sun)
	if pressed[pygame.K_DOWN]:
		# print("DOWN")
		agent = bounce("DOWN", agent, sun)
		thrust = "DOWN"
		fuel -= 1

	# Add score
	agent_score += reward


#__________________________________
#__________________________________
# Observation and Reward Logging
	
	observation = observe(agent, sun, fuel, width, height)

	print('{:<15s}{:<15s}{:<20s}{:<15s}{:<15s}{:<15s}'.format("V_x: " + str(observation[0]), 
		"V_y: " + str(observation[1]), 
		"Radius: " + str(observation[2]), 
		"To Wall: " + str(observation[3]), 
		"Mass: " + str(observation[4]), 
		"Fuel: " + str(observation[5])))

	write(episode, observation, reward)


#__________________________________
#__________________________________
# Draw
	
	# The Game Window
	win.fill(BLACK)
	scoretext = myfont.render("Score: " + str(score), False, WHITE)
	win.blit(scoretext, (5,5))
	scoretext = myfont.render("Agent Score: " + str(agent_score), False, WHITE)
	win.blit(scoretext, (5,50))
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

	# Set Game Failure Conditions
	if agent.x < 0 or agent.x > width or agent.y < 0 or agent.y > height or fuel <= 0:
		reward = wall_reward
		agent_score += reward
		observation = observe(agent, sun, fuel, width, height)
		write(episode, observation, reward)
		fail = True

	# Limit while loop
	clock.tick(80)

#__________________________________
#__________________________________
# Game Failure Screen - Breakout Loop

	while fail:

		# Listen for exit button
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
				pygame.quit()
				sys.exit()

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
		if pressed[pygame.K_SPACE]:
			
			# Set up Map
			agent, sun = setup_map(width, height)
			astroids = []

			# Reset Operating Variables
			fuel = 500
			score = 0
			quad = 3

			# Reset Agent Score
			agent_score = 0

			# Increment Episode
			episode += 1

			# Kick out of Fail Loop
			fail = False