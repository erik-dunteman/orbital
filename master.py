from game import run
import sys, getopt

#__________________________________
#__________________________________
# Command Line Parameter Control
args = sys.argv[1:]
opts,args = getopt.getopt(args,'s:m:c:d:a:g:e:l:')
'''
s : statespace	 	options: ["Tiny"]
m : mode			options: ["NoAstroids"]
c : controller	 	options: ["Self", "Agent"]
d : screen/display	options: ["ScreenOn", "ScreenOff"]
a : alpha			options: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
g : gamma			options: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
e : epsilon			options: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
l : session length	options: Any int
'''

# Set Default Parameters
statespace = "Tiny"
mode = "NoAstroids"
controller = "Self"
screen = "ScreenOff"
alpha = 0.1
gamma = 0.8
epsilon = 0.1
session_len = 10


for opt in opts:
	if opt[0] == "-s":
		statespace = opt[1]
	if opt[0] == "-m":
		mode = opt[1]
	if opt[0] == "-c":
		controller = opt[1]
	if opt[0] == "-d":
		screen = opt[1]
	if opt[0] == "-a":
		alpha = round(float(opt[1]),1)
	if opt[0] == "-g":
		gamma = round(float(opt[1]),1)
	if opt[0] == "-e":
		epsilon = round(float(opt[1]),1)
	if opt[0] == "-l":
		session_len = int(opt[1])


# Agent Rewards
frame_reward = -1
lap_reward = 100
wall_reward = -10000

print(statespace, mode, controller, screen, alpha, gamma, epsilon, session_len)

run(controller, screen, session_len, statespace, mode, alpha, gamma, epsilon, frame_reward, lap_reward, wall_reward)