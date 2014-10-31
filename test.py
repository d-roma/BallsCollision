#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author: D. Roma
#
# 2014/10/29    First issue

import numpy as np
from Box import Box
import matplotlib.pyplot as plt
import matplotlib.animation as animation

dt = 0.01

#positions = np.array([[5, 5], [6, 6], [4, 6], [3, 6]])
#velocity = np.array([[1, 1], [2, 0], [3, 2], [1, 2]])
#masses = np.array([1, 1, 1, 1])
#radius = np.array([0.2, 0.5, 1, 0.1])

positions = np.array([[5, 5], [6, 6]])
velocity = np.array([[1, 3], [2, 0]])
masses = np.array([1, 1])
radius = np.array([0.2, 1])

box = Box(positions, velocity, masses, radius, dt = dt, debug=False)

positions = np.array([[5, 5], [6, 6], [4, 4]])
velocity = np.array([[1, 3], [2, 0], [0, 2]])
masses = np.array([1, 1, 1])
radius = np.array([0.2, 1, 1])

box = Box(positions, velocity, masses, radius, dt = dt, debug=False)
print(box.getPositions())
print(box.getVelocities())