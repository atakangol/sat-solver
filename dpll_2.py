#!/usr/bin/python3

# Libraries

import sys
import os
import time
import random
import math
from copy import deepcopy

######


######
def readnprob(name): #reads and looks and more 0s or 1s
    with open(name, mode='r') as cnf_file:
        i=0
        clauses = []
        probs = []
        positives = []
        #negatives = []
        #var_map = {}
        for line in cnf_file:
            if (i==0):
                header = line.split(' ')
                var_count = int(header[2])
                i +=1
                for c in range(0,var_count):
                    #var_map[c] = 0
                    probs.append(0)
            else:
                temp = line.split(' ')[:3]
                temp = list(map(int,temp))
                clauses.append(temp)
                for c in temp:
                    #var_map[abs(c)-1] += 1
                    if (c>0):
                        probs[abs(c)-1] +=1
                    elif( (c<0)):
                        probs[abs(c)-1] -=1    



    for i in range(0,len(probs)):
        if (probs[i]>0):
            positives.append(i+1)
        #elif(probs[i]<=0):
            #negatives.append(i)
        #else:
            #x = random.choice([0,1])
            #if (x == 0):
                #negatives.append(i)
            #else:
                #positives.append(i)

    #var_map = dict(sorted(var_map.items(), key = lambda kv:(kv[1], kv[0])))
    #var_map = dict(sorted(var_map.items(), key = lambda kv:(kv[1], kv[0]),reverse =True))
    #var_map = list(var_map.keys())
    
    clause_count = len(clauses)

    return(var_count,clause_count,clauses,positives)

def evaluate(clauses,solution): #returns the number of clauses this solution satisfies
    true_count = 0
    #print(solution)
    for clause in clauses:
        for var in clause:
            real = abs(var)
            #print(clause, var, true_count)
            #target = 1
            #if (var<0): target =0
            if (solution[real]==(real/var +1)/2):
                true_count += 1
                break
    #print(" ")
    return(true_count)

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

def remove_clauses(clauses_set,var):
    to_return = []
    
    i=0
    while(i<len(clauses_set)):
        clause = clauses_set[i].copy()
        if (var  in clause):
            #to_return.append(clause)
            clauses_set.pop(i)
            continue

        i += 1
    return (clauses_set)

def remove_literals(clauses_set,var):
    var = (-1)* var
    to_return = []
    for clause in clauses_set:
        c = clause.copy()
        if (var in c):
            c.pop(c.index(var))
        to_return.append(c)
            

    return (to_return)

def check_empty(clauses_set):
    for clause in clauses_set:
        if (len(clause) == 0):
            return True
    return False


def dpll(clauses,var_count,limit):
    start_time = time.time()
    current_sol = {}
    step = 0
    old_clauses = {}
    current_clauses = deepcopy(clauses)
    assigned = []
    not_assigned = []
    for i in range(1,var_count+1):
        not_assigned.append(i)


    while (True):
        old_clauses[step] = deepcopy(current_clauses)

        i = random.randint(0,len(not_assigned))
        var = not_assigned.pop(i-1)
        
        guess = 0
        if (var in positives): 
            guess = 1
            actual_var = -1*var
        




        step += 1




def ahead(var,current_sol,clauses_set,g=True):
    #print("----cs",clauses_set)
    guess=0
    if(var in positives):guess=1

    if(g): x = guess
    else: x = 1-guess

    current_sol[var] = x

    x = var
    if(not g): x =-1*var
    #print("----2cs",clauses_set)
    clauses_set = remove_clauses(clauses_set.copy(),var)
    clauses_set = remove_literals(clauses_set.copy(),var)

    return(current_sol,clauses_set)





if __name__ == '__main__' :
    #random.seed(5)
    start_time = time.time()
    time_limit = 10

    if len(sys.argv) != 2:
        sys.exit("Use: %s <benchmark> ")
        sys.exit()
    benchmark = sys.argv[1]
    
    #read data
    var_count,clause_count,clauses,positives = readnprob(benchmark)
    


    remaining_time = 10 -(time.time()-start_time) -0.001

    #print(clauses)
    #print("---")
    #test(clauses,var_count)


    dpll(clauses.copy(),var_count,remaining_time)
    #unsolved()
    