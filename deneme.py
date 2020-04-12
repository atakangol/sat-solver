#!/usr/bin/python3

# Libraries

import sys
import os
import time
import random
import math

######


######
def print_sol(sol): #dict(1-100)
    #print(sol)
    print("c Turkish Muscle")
    print("s SATISFIABLE")
    print("v",end=" ")
    for i in range(1,len(sol)+1):
        if (sol[i]==1):
            print(i,end=" ")
        else:
            print(-1*(i),end=" ")
    print("0\n")
    sys.exit()


f = []
for i in f:
    print(f)