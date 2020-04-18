import numpy as np
from ple import PLE

from ple.games.waterworld import WaterWorld
import time
import os

class MyAgent():

    def __init__(self, actions):
        self.actions = actions
        self.eatState = 0
        self.negStep = -1

    def pickAction(self, reward, state):
        myVelo = [state['player_velocity_x'], state['player_velocity_y']]
        myPos  = [state['player_x'] + myVelo[0]*3/29.25, state['player_y'] + myVelo[1]*3/29.25]
        creeps = state['creep_pos']['G'] + state['creep_pos']['R'] + state['creep_pos']['Y']
        dist   = state['creep_dist']['G'] + state['creep_dist']['R'] + state['creep_dist']['Y']
        minIdx = dist.index(min(dist))
        fwd    = np.subtract(creeps[minIdx], myPos)

        if self.eatState == 0:
            if minIdx // 3 == 1: self.eatState = 1
        elif self.eatState == 1:
            if reward < 0: 
                self.eatState = 2
                self.negStep = state['step']
            elif minIdx // 3 != 1: self.eatState = 0
        elif self.eatState == 2:
            if state['step'] - self.negStep > 300:
                self.eatState = 3
        elif self.eatState == 3:
            if minIdx // 3 == 1: self.eatState = 4
        else:
            if reward > 0: self.eatState = 0
            elif minIdx // 3 != 1: self.eatState = 3

        if self.eatState == 2:
            return self.actions[4]
        elif fwd[1] > 0 and abs(fwd[1]) > abs(fwd[0]):
            return self.actions[0]
        elif fwd[0] > 0 and abs(fwd[0]) > abs(fwd[1]):
            return self.actions[1]
        elif fwd[1] < 0 and abs(fwd[1]) > abs(fwd[0]):
            return self.actions[2]
        elif fwd[0] < 0 and abs(fwd[0]) > abs(fwd[1]):
            return self.actions[3]
        else:
            return self.actions[4]

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.environ["SDL_VIDEODRIVER"] = "dummy"

# create our game
force_fps = True  # slower speed
display_screen = False
game = WaterWorld()

# make a PLE instance.
p = PLE(game,force_fps=force_fps)

# init agent and game.
p.init()
p.display_screen = True

reward = 0
agent = MyAgent(p.getActionSet())
while p.game_over() == False:
    state = p.getGameState()
    action = agent.pickAction(reward, state)
    reward = p.act(action)
print p.score()
