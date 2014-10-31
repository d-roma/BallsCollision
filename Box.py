#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author: D. Roma
#
# 2014/10/29    First issue
# TODO:
#    - Balls hang between them 
#    - Balls "hangs" on the wall

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from Balls import Balls

class Box():
    '''
    Container for the balls.
    
    Propierties:
    balls -- list of balls
    '''
    line = None
    wall_height = 10
    wall_length = 10
    
    def __init__(self, initial_positions, initial_velocities, masses, radius, \
                  dt = 1e-3, debug = False):
        self.balls = []
        for i, item in enumerate(initial_positions):
            self.balls.append(Balls(item, initial_velocities[i], masses[i], radius[i])) 
        Balls.dt = dt
        Balls.wall_height = self.wall_height
        Balls.wall_length = self.wall_length
        self.number_of_balls = initial_positions.shape[0]
        self.debug = debug
        self.radius = radius
        
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(0, self.wall_length), ylim=(0, self.wall_height))
        self.colors = np.random.random([self.number_of_balls, 3])
        self.patches = self.setup_plot()
        #Using setup_plot as parameter for init_func from FuncAnimation 
        #let to strange results
        self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=dt*1000, 
                                           blit=True)
        plt.show()

        
    def setup_plot(self):      
        pos = self.getPositions()
        if self.debug:
            print(pos)
        patches = []
        for i, item in enumerate(self.radius):
            patch = plt.Circle(pos[i], item, color=self.colors[i])
            self.ax.add_patch(patch)
            patches.append(patch)
        self.ax.clear()
        self.ax.grid(True)
        self.ax.set_title('Elastic collision')
        self.patches = tuple(patches)
        return tuple(patches)
    
    def getPositions(self):
        pos = np.empty([self.number_of_balls, 2])
        for i, item in enumerate(self.balls):
            pos[i, 0], pos[i, 1]  = item.getPosition()
        return pos
    
    def getVelocities(self):
        vel = np.empty([self.number_of_balls, 2])
        for i, item in enumerate(self.balls):
            vel[i] = item.velocity
        return vel
              
    def nextInstant(self):
        pos = np.empty([self.number_of_balls, 2])
        for i, item in enumerate(self.balls):
            pos[i, 0], pos[i, 1]  = item.updatePosition()
            for ball in self.balls[i+1:self.number_of_balls + 1]:
                colision = item.check_ball_collision(ball)
                if colision:
                    item.resolve_collision(ball)
        return pos
    
    def update_plot(self, counter):
        pos = self.nextInstant()
        if self.debug:
            print(pos)
        for i, patch in enumerate(self.patches):
            patch.center = pos[i]

        # We need to return the updated artist for FuncAnimation to draw.
        return self.patches
        