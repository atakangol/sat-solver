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

#/home/atakan/Desktop/race/cnf-100-200-0.cnf

#python solver.py "C:\Users\golat\Dropbox\udl2\advane programmingfor ai\race\project\benchmarks\cnf-100-200-0.cnf"

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

def random_guesser(var_count):
    
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

def try_and_remember(var_count,clause_count,clauses,start,cutoff=2,best_count=5):
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
    
    print(time.time() - start)
    best = sorted(best) 
    #best = best[:math.floor(len(best)/10)]
    best = best[:best_count]
    best_sol = []
    for i in best:
        best_sol.append(all_sol[i[1]]) 
    #offsets = sorted(all_sol)
    #offsets = offsets[:math.ceil(len(offsets)/10)]
    #print(all_sol.keys())
    print(len(all_sol))
    print(time.time() - start)
    return (False,best_sol)

def search_local(var_count,sol,offset,clause,solution):
    
    
    pass

def get_specific_neighbour(sol,var_num):
    sol [var_num-1] = 1- sol[var_num-1]
    return sol

def get_random_neighbour(sol):
    change = random.randint(0,len(sol)-1)
    #sol[change] = not(sol[change] )
    sol [change] = 1- sol[change]
    return sol



if __name__ == '__main__' :
    start_time = time.time()
    if len(sys.argv) != 2:
        sys.exit("Use: %s <benchmark> ")
        sys.exit()
    benchmark = sys.argv[1]
    

    var_count,clause_count,clauses = readData(benchmark)
    

    #CHANGE VARIABLE NAME
    found,SOMETHING = try_and_remember(var_count,clause_count,clauses,start_time)
    if found:
        print(SOMETHING)
    
        
    
    print(time.time() - start_time)
'''
    init_guess = [True,True,True,True,True]
    print(get_neighbour(init_guess))
    #init_guess = [False,False,False,False,False]
    #a = evaluate(clauses,init_guess)
    #print(a)'''