#!/usr/bin/python3

# Libraries

import sys
import os
import time
import random
import math

######
#local search
#size copmrasion true fale ve 01 arasında bit farkı yok (saçmalık) 01 daha rahat , linux da da yok
######


#python solver.py "C:\Users\golat\Documents\Git\sat-solver\benchmarks\cnf-100-200-0.cnf"

def readData(name): #reads the file and returns the relevant data
    with open(name, mode='r') as cnf_file:
        i=0
        clauses = []
        for line in cnf_file:
            if (i==0):
                header = line.split(' ')
                var_count = int(header[2])
                i +=1
            else:
                temp = line.split(' ')[:3]
                temp = list(map(int,temp))
                clauses.append(temp)
        	#print(line)
    clause_count = len(clauses) 
    #print (var_count,clause_count)
    #print(clauses)
    return(var_count,clause_count,clauses)

def evaluate(clauses,solution): #returns the number of clauses this solution satisfies
    true_count = 0
    for clause in clauses:
        for var in clause:
            real = abs(var)-1 
            target = 1
            if (var<0): target =0
            if (solution[real]==target):
                true_count = true_count +1
                break

    return(true_count)

def random_guesser(var_count): #returns a random guess of a specified length
    
    poss = [0,1]
    #poss = [False,True]
    guess = []

    for i in range(0,var_count):
        guess.append(random.choice(poss))
    
    return guess

def try_endless_mindless(var_count,clause_count,clauses):
    metric = 0
    while(metric != clause_count):
        sol = random_guesser(var_count)
        metric = evaluate(clauses,sol)
        print("offset:",clause_count-metric)
    
    return sol

def try_and_remember(var_count,clause_count,clauses,start,cutoff=2,best_count=5): #returns either the solution (unlikely) or the top solutions with the wrong count
    metric = 0
    counter = 0
    #all_sol = {}
    all_sol = []
    best = []

    while(True):
        sol = random_guesser(var_count)
        metric = evaluate(clauses,sol)
        offset = clause_count-metric
        #print("offset:",clause_count-metric)
        #all_sol[clause_count-metric] = sol
        all_sol.append((offset,sol))
        best.append((offset,counter))
        counter+=1
        if (offset == 0 ):
            return(True,sol)   #not likely
        #print(time.time() - start)
        if (time.time() - start  >= cutoff): #try for x seconds
            break
    
    #print(time.time() - start)
    best = sorted(best) 
    #best = best[:math.floor(len(best)/10)]
    best = best[:best_count]
    best_sol = []
    for i in best:
        best_sol.append(all_sol[i[1]]) 
    #offsets = sorted(all_sol)
    #offsets = offsets[:math.ceil(len(offsets)/10)]
    #print(all_sol.keys())
    #print(len(all_sol))
    #print(time.time() - start)
    return (False,best_sol)

def search_local_random(var_count,sol,offset,clauses,start,cutoff=1.4):
    #print(offset,sol)
    offsets = []
    #print("hop")
    while (time.time() - start  < cutoff):
        temp = get_random_neighbour(sol.copy())
        metric = evaluate(clauses,temp)
        new_offset = clause_count-metric
        offsets.append(new_offset)
        #print(new_offset-offset)
    
    print(len(offsets))
    return offsets

def search_local_all(var_count,sol,offset,clauses):
    offsets = []
    for i in range(0,var_count):
        temp = get_specific_neighbour(sol.copy(),i)
        metric = evaluate(clauses,temp)
        new_offset = clause_count-metric
        offsets.append(new_offset)
        #print(new_offset-offset)
    print(len(offsets))
    return offsets


def get_specific_neighbour(temp,change):
    temp[change] = 1- temp[change]
    return temp

def get_random_neighbour(temp):
    
    change = random.randint(0,len(temp)-1)
    #sol[change] = not(sol[change] )
    temp[change] = 1- temp[change]
    return temp



if __name__ == '__main__' :
    random.seed(1)
    start_time = time.time()


    if len(sys.argv) != 2:
        sys.exit("Use: %s <benchmark> ")
        sys.exit()
    benchmark = sys.argv[1]
    

    var_count,clause_count,clauses = readData(benchmark)
    

    found,instances = try_and_remember(var_count,clause_count,clauses,start_time)
    if found:
        print("found")
        print(instances)
    else:
        print(instances[0][0],var_count)
        local_start_time = time.time()
        #start local search
        print (min(search_local_random(var_count,instances[0][1],instances[0][0],clauses,local_start_time)))
        #print (min(search_local_all(var_count,instances[0][1],instances[0][0],clauses)))
        #print(instances)
    
        
    
    print(time.time() - start_time)

    #init_guess = [True,True,True,True,True]
    #print(get_neighbour(init_guess))
    #init_guess = [False,False,False,False,False]
    #a = evaluate(clauses,init_guess)
    #print(a)
    

'''
    guess = random_guesser(100)
    print(guess)
    search_local(100,guess)
    print(time.time() - start_time)
    '''
    