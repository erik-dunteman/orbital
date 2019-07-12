# Orbital
#### An Astrophysics game embedded with Reinforcement Learning.
![](https://media.giphy.com/media/f4DCd1I1AOe8oNMdAY/giphy.gif)

## Objective:
- Maximize orbit laps

## Control:
- Trust toward sun
- Thrust away from sun

## Constraints:
- Stay within bounds of game window
- Do not hit the sun
- Do not hit the astroids
- Do not run out of fuel

## Under the Hood:
 - Game Environment coded from scratch using Pygame
 - Q-Learning RL Algorithm coded from scratch using Numpy
 - Functions to:
    - Reduce continuous statespace to discrete
    - Handle hyperparameter selection from terminal
    - Train independently in AWS EC2 environments
    - Log relevant learning metrics

## Current Project Status:
The agent has trained against itself for 50 million episodes (games) using one set of Q-Learning hyperparameters. Currently, I am refining the algorithm hyperparameters through programatic training, evaluation, and selection.
