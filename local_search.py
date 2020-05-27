#!/usr/bin/python3

# Libraries

import sys
import os
import time
import random
import math

######


######


#python local_search.py "C:\Users\golat\Documents\Git\sat-solver\benchmarks\cnf-100-200-0.cnf"

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
            #print(real,end=" ")
            target = 1
            if (var<0): target =0
            if (solution[real]==target):
                true_count = true_count +1
                break
    #print(" ")
    return(true_count)

def random_guesser(var_count): #returns a random guess of a specified length
    
    poss = [0,1]
    #poss = [False,True]
    guess = []

    for i in range(0,var_count):
        guess.append(random.choice(poss))
    
    return guess

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
            print_sol(sol)
            sys.exit()   #not likely
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
    return (best_sol)

def search_local_random(var_count,sol,offset,clauses,limit):
    local_start_time = time.time()
    old = var_count
    #print(offset)
    while (time.time()-local_start_time < limit):
        vars =list( range(0,len(sol)))
        random.shuffle(vars)
        #input("-")
        best = [clause_count,var_count]
        changed = False


        for i in vars:
            
            new_sol = get_specific_neighbour(sol.copy(),i)
            metric = evaluate(clauses,new_sol)
            new_offset = clause_count-metric
            #print(offset,best[0])
            #print(new_offset)
            #print(i)
            #input("--")
            if (new_offset == 0):
                print_sol(new_sol)
                sys.exit()
            
            if (new_offset < offset) and (i != old):
                offset = new_offset
                sol = new_sol.copy()
                changed = True
                break
            
            else:
                 if (new_offset <= best[0])  and (i != old): 
                    #print("bbb")
                    best[0] = new_offset
                    best[1] = i
        if (changed):
            continue
        temp = get_specific_neighbour(sol.copy(),best[1])
        sol = temp.copy()
        offset = best[0]
        old = best[1]
        #print("aaa",old)

            

    return (sol,offset)

def search_local_all(var_count,sol,offset,clauses,limit):
    local_start_time = time.time()
    
    while (time.time()-local_start_time < limit):
    #while (True):
        vars =list( range(0,len(sol)))
        random.shuffle(vars)

        changed = False
        better = (offset,var_count)

        for i in vars:

            temp = get_specific_neighbour(sol.copy(),i)
            metric = evaluate(clauses,temp)
            new_offset = clause_count-metric

            if (new_offset == 0):
                print_sol(temp)
                sys.exit()
            
            if (new_offset < better[0]):
                changed = True
                better = (new_offset,i)

        if changed:

            temp = get_specific_neighbour(sol.copy(),better[1])
            sol = temp.copy()
            offset = better[0]
            continue


        return (True,sol,offset)

    #print("---")
    return (False,sol,offset)

def get_specific_neighbour(temp,change):
    temp[change] = 1- temp[change]
    return temp

def get_random_neighbour(temp):
    
    change = random.randint(0,len(temp)-1)
    #sol[change] = not(sol[change] )
    temp[change] = 1- temp[change]
    return temp

def print_sol(sol):
    #print(sol)
    print("c Turkish Muscle")
    print("s SATISFIABLE")
    print("v",end=" ")
    for i in range(0,len(sol)):
        if (sol[i]==1):
            print(i+1,end=" ")
        else:
            print(-1*(i+1),end=" ")
    print("0\n")
    sys.exit()

def unlikely(offset,clause_count):
    print("c Turkish Muscle")
    print("s UNSATISFIED")
    print("c", offset,"clauses not satisfied out of", clause_count, "clauses in total")
    sys.exit()

if __name__ == '__main__' :
    #random.seed(1)
    start_time = time.time()
    time_limit = 10

    if len(sys.argv) != 2:
        sys.exit("Use: %s <benchmark> ")
        sys.exit()
    benchmark = sys.argv[1]
    
    #read data
    var_count,clause_count,clauses = readData(benchmark)
    
    #find first guesses
    num_of_first_guesses = 1
    instances = try_and_remember(var_count,clause_count,clauses,start_time,cutoff=0.5,best_count=num_of_first_guesses)
    
    second_guesses = []
    for i in range(0,num_of_first_guesses):
        second_guesses.append(instances[i])
    
    
    for i in range(0,num_of_first_guesses):
        remaining_time = 10  - (time.time()- start_time) - 0.1
        #print(remaining_time)
        sol,offset = search_local_random(var_count,instances[i][1],instances[i][0],clauses,remaining_time/(num_of_first_guesses-i))
        #print(offset,clause_count)
        #print(time.time() - start_time)
        second_guesses[i] = (offset,sol.copy())
    
    

    unlikely(min(second_guesses)[0],clause_count)