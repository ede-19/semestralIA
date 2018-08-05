import gym
import numpy
#import gym_pull
import retro
import random
from random import randint


def reset(self, **kwargs):
        self.action_history = []
        self.reward_history = []
        self.total_reward = 0
        return self.env.reset(**kwargs)


def move(x):
        #["B", "A", "MODE", "START", "UP", "DOWN", "LEFT", "RIGHT", "C", "Y", "X", "Z"]
        # action = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	r = random.randrange(2)
	if r == 0:
                return  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]  # Right
	
	if r == 1:
                return  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Up

	if r == 3:
		return  [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]

	if r == 4:
		return  [0,0,0,1,1,0]

	if r == 5:
		return  [0,0,0,1,0,0]

	if r == 6:
		return  [0,0,0,1,0,0]

a = numpy.append([[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]],[[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]], axis = 0 )
intera = 0
for i_episode in range(1000):
	env = retro.make(game='SonicTheHedgehog-Genesis', state='GreenHillZone.Act1')
	observation = env.reset()
	distance=0
	i = 0
	contador = 0
	condi = True 
	while condi:
            env.render()
            contador = contador + 1

            if contador >= intera:
                action = move(random.randint(0, 3))
	    	#action = numpy.random.randint(2, size=6)
                a = numpy.insert(a,contador,action,axis = 0)
            else:
                action = a[contador]
               
            #print (%action
	    #print i
            old_observation = observation
            observation, reward, done, info = env.step(action)
            if info['x'] <= distance:
                i = i + 1
            else:
                i = 0
            if info['x'] > distance:
		#print old_observation
                print ('---------------------------------------------------------')
		#print contador
		#print intera
		#print info['distance']
		#print i
		#spamwriter.writerow(action)
		#aqui tiene que  llnar la variable 
                distance = info['x']
            if i >= 100:
                intera = contador
                intera = intera - 150 
               	#condi = False 
#                if done:
 #                      break
