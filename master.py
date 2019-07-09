from game import run
import sys

#__________________________________
#__________________________________
# Reinforcement Learning Control
try:
	controller = sys.argv[1]
except:
	controller = "Self"
	# controller = "Agent"

if controller == "Agent":
	#Choose how we want to run the agent.

	# Visual on? Pass in Parameter "ScreenOn"
	try:
		screen = sys.argv[2]
	except:
		# screen = "ScreenOn"
		screen = "ScreenOff"
	
	# Limit Number of Training Episodes in this Session.
	# Pass in as Parameter
	try:
		session_len = int(sys.argv[3])
	except:
		session_len = 10
else:
	screen = "ScreenOn"
	session_len = None


# Hyperparameters
alpha = 0.7
gamma = 0.8
epsilon = 0.1


statespace = "Tiny"
# statespace = "Small"
# statespace = "Large"
# statespace = "LargeSmoothed"
mode = "NoAstroids"
# mode = "Astroids"


# Agent Rewards
frame_reward = -1
lap_reward = 100
wall_reward = -10000

# print(screen, session_len)

run(controller, screen, session_len, statespace, mode, alpha, gamma, epsilon, frame_reward, lap_reward, wall_reward)