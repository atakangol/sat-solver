#!/usr/bin/python3

# Libraries

import sys
import os
import time
import random
import math

######


######


def get_random_neighbourhood(temp,changes):
    change = random.sample(range(0,len(temp)-1),changes)
    for i in change:
        temp[i] = 1- temp[i]
    return temp



sol = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
sol1  = get_random_neighbourhood(sol.copy(),4)
print(sol)
print(sol1)
