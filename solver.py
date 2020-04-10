#!/usr/bin/python3

# Libraries

import sys
import os
import time
import random
import math

######


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

def search_local_random(var_count,sol,offset,clauses,start,cutoff=300,per = 75):
    #print(offset,sol)
    #print(offset,sol)
    limit = int(var_count*per/100)
    #print(limit)
    count = 0
    #offsets = []
    #print("hop")
    #while(True):
    while (time.time() - start  < cutoff):
        count = 0
        #print("aaaaaa")
        #while(True):
        #print(offset,sol)
        #print("yeni",count)
        while (time.time() - start  < cutoff):
            count += 1
            temp = get_random_neighbour(sol.copy())
            metric = evaluate(clauses,temp)
            new_offset = clause_count-metric
            #offsets.append(new_offset)
            #print(new_offset,end=" ")
            if (new_offset == 0):
                #print ("FOUND",sol)
                return (True,temp,new_offset)

            
            if (count >= limit):
                #print ("-------")
                #break
                return (False,sol,offset)
            
            
            if (new_offset < offset):
                #print("hop")

                sol = temp.copy()
                offset = new_offset
                #print(offset)
                break
                #continue
            #print(new_offset-offset)
    
    return (False,sol,offset)

def search_local_all(var_count,sol,offset,clauses,start):
    #print(offset,sol)
    #print(offset,sol)
    #limit = int(var_count*per/100)
    #print(limit)
    #count = 0
    #offsets = []
    #print("hop")
    #while(True):
    
    while (True):
        #count = 0
        changed = False
        #print("aaaaaa")
        #while(True):
        #print(offset,sol)
        #print("yeni",count)
        better = (offset,var_count)
        for i in range(0,len(sol)):
            #count += 1
            #temp = get_random_neighbour(sol.copy())
            temp = get_specific_neighbour(sol.copy(),i)
            metric = evaluate(clauses,temp)
            new_offset = clause_count-metric
            #offsets.append(new_offset)
            #print(new_offset,end=" ")
            if (new_offset == 0):
                if (offset == 0 ):
                    print_sol(sol)
                    sys.exit()
            
            if (new_offset < better[0]):
                #print("hop",i)
                changed = True
                better = (new_offset,i)
                #sol = temp.copy()
                #offset = new_offset
                #print(offset)
                #break
                #continue
            #print(new_offset-offset)
        
        if changed:
            temp = get_specific_neighbour(sol.copy(),better[1])
            sol = temp.copy()
            offset = better[0]
            continue
        return (sol,offset)


    return (sol,offset)

def get_specific_neighbour(temp,change):
    temp[change] = 1- temp[change]
    return temp

def get_random_neighbour(temp):
    
    change = random.randint(0,len(temp)-1)
    #sol[change] = not(sol[change] )
    temp[change] = 1- temp[change]
    return temp

def get_random_neighbourhood(temp,changes):
    
    for i in range(0,changes):

        change = random.randint(0,len(temp)-1)
        temp[change] = 1- temp[change]
    return temp

def neighbourhood_search(var_count,sol,offset,clauses,limit,per = 20):
    start = time.time()
    to_change = math.floor((var_count/100)*per)
    while (time.time() - start  < limit):
        while (time.time() - start  < limit):
            temp = get_random_neighbourhood(sol.copy(),random.randint(2,to_change))
            metric = evaluate(clauses,temp)
            new_offset = clause_count-metric
            #print(new_offset,end = " ")
            if (new_offset == 0):
                #print ("FOUND",sol)
                return (True,temp,new_offset)
            
            if (new_offset < offset):
                    print("hop")

                    sol = temp.copy()
                    offset = new_offset
                    #print(offset)
                    break
    return

def print_sol(sol):
    print(sol)
    print("c Turkish Muscle")
    print("s SATISFIABLE")
    print("v",end=" ")
    for i in range(0,len(sol)):
        if (sol[i]==1):
            print(i+1,end=" ")
        else:
            print(-1*(i+1),end=" ")
    print("0\n")


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
    instances = try_and_remember(var_count,clause_count,clauses,start_time,cutoff=2,best_count=5)


    #for i in instances:
        #print(i[0])
    #print("\n")
    second_guesses = []
    for i in range(0,len(instances)):

        local_start_time = time.time()
        #start local search
        sol,offset = search_local_all(var_count,instances[i][1],instances[i][0],clauses,local_start_time)
        #stat,sol,offset = search_local_random(var_count,instances[i][1],instances[i][0],clauses,local_start_time)
        second_guesses.append((offset,sol))
    
    #for i in second_guesses:
        #print(i)
    best = (min(second_guesses))
    print(best[0])
    #remaining_time = math.floor(time_limit-time.time() + start_time)

    #neighbourhood_search(var_count,best[1],best[0],clauses,remaining_time)

    
    print(time.time() - start_time)

   
    

