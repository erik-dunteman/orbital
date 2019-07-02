from game import run

#__________________________________
#__________________________________
# Reinforcement Learning Control
# controller = "Self"
controller = "Agent"

# Hyperparameters
alpha = 0.1
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

run(controller, statespace, mode, alpha, gamma, epsilon, frame_reward, lap_reward, wall_reward)