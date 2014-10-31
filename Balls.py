#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author: D. Roma
#
# 2014/10/29    First issue
# TODO:
#    - Fix collision_vector for resolve_collision() 

import numpy as np

class Balls():
    ''' This class implements a ball.
    
    Propierties:
    position -- x,y vector defining the position of the ball
    velocity -- x,y vector defining the velocity of the ball
    mass     -- mass of the ball
    radius   -- radius of the ball
    
    dt       -- static propierty which define the time step 
    
    '''
    dt  = 1e-3
    wall_height = 10
    wall_length = 10
    Cr = 1.0
    
    def __init__(self, position = np.zeros(2), velocity = np.zeros(2), mass = 1, \
                 radius = 1):
        self.position = position
        self.velocity = velocity
        self.mass = mass    
        self.radius = radius
        
    def updatePosition(self):
        '''
        Updates the current ball position using the class parameter dt. Returns 
        the new position of the ball
        '''
        self.position = self.position + self.velocity * self.dt
        self.check_wall_collision()
        return(self.position)
    
    def updateOffsets(self):
        offset = self.velocity * self.dt
        self.position = self.position + offset
        self.check_wall_collision()
        return(offset)
        
    def getPosition(self):
        '''
        Returns the current position of the ball
        '''
        return(self.position)
        
    def check_wall_collision(self):
        '''
        Checks if the ball is colliding with the wall.
        '''
        if (self.position[0] < self.radius or 
            (self.position[0] + self.radius) > self.wall_length):
            x = True
        else:
            x = False
        if (self.position[1] < self.radius or 
            (self.position[1] + self.radius) > self.wall_height):
            y = True
        else:
            y = False
        self.wall_collision(x, y)
        return (x, y)
    
    def wall_collision(self, x, y):
        '''
        When a collision with the walls appears, invert the component sense.
        '''
        if x:
            self.velocity[0] = -self.velocity[0]
        if y:
            self.velocity[1] = -self.velocity[1]
            
    def check_ball_collision(self, ball):
        '''
        Check if this object collides with another ball
        '''
        distance_centers = np.linalg.norm(self.position - ball.position)
        if distance_centers < (ball.radius + self.radius):
            return True
        else:
            return False
    
    def resolve_collision(self, ball, use_delta=False):
        '''
        Calculate the new velocity vector after collision with ball
        '''
        # Find time of collision and "go back", e.g, 
        # resolve mtd (minimum translation distance) 
        if use_delta:    
            collision_vector = self.position - ball.position
            distance_centers = np.linalg.norm(collision_vector)
            if (distance_centers == 0):
                print("ERROR, objects at the same spot!")    
            #Project velocity in the direction of the collision vector
            collision_unity_vector = collision_vector/distance_centers
            vel1 = np.sum(self.velocity*collision_unity_vector)
            vel2 = np.sum(ball.velocity*collision_unity_vector)
            #Colision delta time
            collision_dt = (self.radius + ball.radius - distance_centers)/(vel1 - vel2)
    
            #Move back
            self.position -= self.velocity * collision_dt
            ball.position -= ball.velocity * collision_dt
        
        # Ideally, at this point, the distance between centers is self.radius + ball.radius
        collision_vector = self.position - ball.position
        distance_centers = np.linalg.norm(collision_vector)
        #Projection of the velocities to resolve 1D problem
        collision_unity_vector = collision_vector/distance_centers
        ax, ay = collision_unity_vector
        va1 = np.sum(self.velocity*collision_unity_vector)
        va2 = np.sum(ball.velocity*collision_unity_vector)
        vb1 = -self.velocity[0]*ax + self.velocity[1]*ay
        vb2 = -ball.velocity[0]*ax + ball.velocity[1]*ay
        #New velocities in these axes
        ed = self.Cr * ball.Cr
        vaP1 = va1 + (1+ed)*(va2-va1)/(1+self.mass/ball.mass)
        vaP2 = va2 + (1+ed)*(va1-va2)/(1+ball.mass/self.mass)
        #Undo the projectiosn
        self.velocity = np.array([vaP1*ax - vb1*ay, vaP1*ax - vb2*ay])
        ball.velocity = np.array([vaP1*ax + vb1*ay, vaP1*ax + vb2*ay])

        #Move the object to the apropiate time instant
        if use_delta:
            self.position += self.velocity * collision_dt
            ball.position += ball.velocity * collision_dt
        
        if (self.position[0] < self.radius or 
            (self.position[0] + self.radius) > self.wall_length or 
            self.position[1] < self.radius or 
            (self.position[1] + self.radius) > self.wall_height):
            print("Error, ball falls outside of the box")
            print(collision_dt)
            print(self.position, ball.position)
            print(self. velocity, ball.velocity)
        