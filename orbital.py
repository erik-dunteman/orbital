import os
import platform

import pygame
from pygame.locals import *

from physics import accelerate, bounce
from map import setup_map, check_quadrant, random_astroid

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
fuel = 500
quad = 3
done = False # This holds the game in a loop
fail = False # This navigates to the fail screen


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
astroids = [random_astroid(width,height)]



#__________________________________
#__________________________________
# Game Logic

while not done:
	
	# Set default variables
	thrust = "None"

	# Move the circle
	agent = accelerate(agent, sun)
	agent.x += agent.v_x
	agent.y += agent.v_y

	# Move any astroids:
	for astroid in astroids:
		astroid = accelerate(astroid, sun)
		astroid.x += astroid.v_x
		astroid.y += astroid.v_y


	# Increment score per orbit (threashold directly below sun)
	print(quad)
	new_quad = check_quadrant(agent.x, agent.y, sun.x, sun.y)
	if new_quad == 3 and quad == 4:
		# Then it has passed a lap below the sun
		score += 1
		if score % 1 == 0:
			astroids.append(random_astroid(width,height))
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
		print("UP")
		agent = bounce("UP", agent, sun)
		thrust = "UP"
		fuel -= 1

	# Respond to Down (Thrust Toward Sun)
	if pressed[pygame.K_DOWN]:
		print("DOWN")
		agent = bounce("DOWN", agent, sun)
		thrust = "DOWN"
		fuel -= 1

#__________________________________
#__________________________________
# Draw
	
	# The Game Window
	win.fill(BLACK)
	scoretext = myfont.render("Score: " + str(score), False, WHITE)
	win.blit(scoretext, (5,5))
	fueltext = myfont.render("Fuel: " + str(fuel), False, WHITE)
	win.blit(fueltext, (5,100))
	pygame.draw.rect(win, GREEN,(10, 150, 30, fuel))
	pygame.draw.rect(win, RED, (0,0,width,height), 5)


	# The Features
	pygame.draw.circle(win, WHITE, 
		[int(agent.x), int(agent.y)], int(20*agent.m), 0)
	pygame.draw.circle(win, RED, [sun.x,sun.y], 50, 0)
	for astroid in astroids:
		pygame.draw.circle(win, RED, 
		[int(astroid.x), int(astroid.y)], int(20*astroid.m), 0)
	
	if thrust == "UP":
		# Draw a thrust flame toward sun
		pygame.draw.line(win, RED, 
			[int(agent.x),int(agent.y)], 
			[int(agent.x) + (int(sun.x)-int(agent.x))/5, 
			int(agent.y) + (int(sun.y)-int(agent.y))/5], 
			10)
	if thrust == "DOWN":
		# Draw a thrust flame away from sun
		pygame.draw.line(win, RED, 
			[int(agent.x),int(agent.y)], 
			[int(agent.x) - (int(sun.x)-int(agent.x))/5, 
			int(agent.y) - (int(sun.y)-int(agent.y))/5], 
			10)

	# Render to Screen
	pygame.display.flip()


#__________________________________
#__________________________________
# Clean Up

	# Set Game Failure Conditions
	if agent.x < 0 or agent.x > width or agent.y < 0 or agent.y > height or fuel <= 0:
		fail = True

	clock.tick(50)

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

			# Kick out of Fail Loop
			fail = False