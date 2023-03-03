# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 14:51:20 2023

@author: Linne
"""

import numpy as np
import itertools
from matplotlib import animation
import matplotlib.pyplot as plt
class Particle:
    def __init__(self, position, func, searchspace, weights):
        '''
        

        Parameters
        ----------
        position : Array
            Initial position of the particle
        func : function
            Function with which to calculate the particles goodness value.

        Returns
        -------
        None.

        '''
        self.searchspace = searchspace
        self.func = func
        self.position = position
        self.velocity = np.zeros(position.shape)
        self.current_value = func(position)
        self.personal_best = self.current_value
        self.personal_best_pos = self.position
        self.weights = weights
    def position_in_searchspace(self):
        no = 0
        for i in range(len(self.position)):
            if self.searchspace[i][0]<=self.position[i] and self.position[i] <= self.searchspace[i][1]:
                no += 0
            else:
                no += 1
        return (no == 0)
    def update_current_value(self):
        self.current_value =  self.func(self.position)
        if self.current_value < self.personal_best and self.position_in_searchspace():
            self.personal_best = self.current_value
            self.personal_best_pos = self.position
            
    def update_velocity(self, global_best_pos):
        inertia = self.weights[0]*self.velocity
        personal_influence = self.weights[1]*np.random.rand()*(self.personal_best_pos - self.position)
        social_influence = self.weights[2]*np.random.rand()*(global_best_pos - self.position)
        self.velocity = inertia + personal_influence + social_influence
        
    def move(self, global_best_pos):
        self.update_velocity(global_best_pos)
        self.position = self.position + self.velocity
        self.update_current_value()
    
        
    
class PSO:
    def __init__(self, NperDimension, dimension, searchspace, func, weights = [0.7, 0.6, 0.5]):
        '''
        

        Parameters
        ----------
        size : int
            Number of particles to initialize.
        dimension : int
            Number of dimensions in search space.
        searchspace : tuple
            tuple with [min, max] for each dimension

        Returns
        -------
        None.

        '''
        self.size = NperDimension**dimension
        self.dimension = dimension
        self.searchspace = searchspace
        self.particles = []
        self.func = func
        self.global_best = None
        self.iteration = 0
        self.weights = weights
        self.ave_position = None
        
        iterables = []
        positions = []
        for i in range(dimension):
            iterables.append(np.linspace(searchspace[i][0], searchspace[i][1], NperDimension))
        for t in itertools.product(*iterables):
            positions.append(t)
        pos_sum = np.zeros(np.array(positions[i]).shape)
        for i in range(self.size):
            self.particles.append(Particle(np.array(positions[i]), self.func, self.searchspace, self.weights))
            pos_sum = pos_sum + self.particles[-1].position
            if self.global_best == None:
                self.global_best = self.particles[-1].current_value 
                self.global_best_pos = self.particles[-1].position
            if self.particles[-1].current_value < self.global_best:
                self.global_best = self.particles[-1].current_value 
                self.global_best_pos = self.particles[-1].position
        self.ave_position = pos_sum/self.size
        self.global_best_list = []
        
    def move_particles(self):
        self.iteration += 1
        print(self.iteration)
        acting_global_best_pos = self.global_best_pos
        pos_sum = np.zeros(self.particles[-1].position.shape)
        for i in self.particles:
            i.move(acting_global_best_pos)
            pos_sum = pos_sum + i.position
            if i.current_value < self.global_best and i.position_in_searchspace():
                self.global_best = i.current_value
                self.global_best_pos = i.position
        self.ave_position = pos_sum/self.size
        # print(self.global_best)
    def minimise(self):
        self.move_particles()
        n = 0
        while np.linalg.norm(self.ave_position) <0.01:
            self.move_particles()
            n+= 1
            if n > 1000000:
                print('no valid minimum')
                break
        return self.global_best_pos()    
        
    def run(self, num_frames, func_plotting, animate=False, filename = 'PSO'):        
        if animate:
            x = np.linspace(self.searchspace[0][0], self.searchspace[0][1], 100)
            y = np.linspace(self.searchspace[1][0], self.searchspace[1][1], 100)
            X, Y= np.meshgrid(x, y)
            Z = np.zeros(X.shape)
            for i in range(len(x)):
                for j in range(len(y)):
                    Z = np.flip(func_plotting(X, Y), axis = 0)                
            
        # Plotting preparation
            fig = plt.figure(figsize=(10, 10))
            ax = fig.add_subplot()
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.imshow(Z, extent = [X[0,0], X[-1,-1], Y[0,0], Y[-1,-1]])
            # Animation image placeholder
            images = []
            #initial positions
            image = ax.scatter([n.position[0] for n in self.particles],
                                 [n.position[1] for n in self.particles], c='r')
                                 # [n.current_value for n in self.particles], c='r')
            images.append([image])
            
            if num_frames:
                for i in range(num_frames):
                    self.move_particles()
                    image = ax.scatter([n.position[0] for n in self.particles],
                                         [n.position[1] for n in self.particles], c = 'r')
                                         # [n.current_value for n in self.particles], c='r')
                    images.append([image])
            else:
                while np.linalg.norm(self.ave_position - self.global_best_pos)>1e-3:
                    self.move_particles()
                    image = ax.scatter([n.position[0] for n in self.particles],
                                         [n.position[1] for n in self.particles], c = 'r')
                    images.append([image])
            # Generate the animation image and save
            animated_image = animation.ArtistAnimation(fig, images)
            animated_image.save(f'./{filename}.gif', writer='pillow') 
            plt.close()
        