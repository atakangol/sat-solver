#!/usr/bin/python3

########
#Turkish Muscle


#Atakan GÖL
#Hatice Hüma Kalaycı
########


# Libraries

import sys
import os
import time
import random
import math

######


######


#python turkish_muscle.py "C:\Users\golat\Documents\Git\sat-solver\benchmarks\uf100-01.cnf"

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

def remove_clauses(clauses_set,var):
    i=0
    while(i<len(clauses_set)):
        clause = clauses_set[i]
        if (var in clause):
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

def unit_propagation(clauses_set):
    for clause in clauses_set:
        if (len(clause) == 1):
            #found unit
            return (clause[0])
    return(None)
      
def check_empty(clauses_set):
    for clause in clauses_set:
        if (len(clause) == 0):
            return True
    return False

def dpll(clauses,var_count,limit):
    start_time = time.time()


    clauses_backtrack=[]
    clauses_set = clauses.copy()
    not_assigned = []
    for i in range(1,var_count+1):
        not_assigned.append(i)
    current_sol = {}
    x = 0
    #while(True):
    while(time.time()-start_time < limit):    
       
        #1
        if (len(not_assigned) == 0):
            print_sol(current_sol)
        clauses_backtrack.append(clauses_set.copy())
        #print(i)
        i = random.randint(0,len(not_assigned))
        #print(i)
        x = not_assigned.pop(i-1)
        

        
        #for i in clauses_backtrack:
            #print(i)
        #print(current_sol)
        #input()
        


        guess = -1
        if (x in positives):

            guess = 1
        
        current_sol[x] = int((guess+1)/2) #0 or 1
        #2/3
        clauses_set = remove_clauses(clauses_set.copy(),x*guess)
        clauses_set = remove_literals(clauses_set.copy(),x*guess)
        
        #4
        unit = 0
        while (unit):
            unit = unit_propagation(clauses_set)
            #var = clause[0]
            avar = abs(unit)
            not_assigned.pop(not_assigned.index(avar))
            current_sol[avar] = int((avar/unit +1)/2)
            clauses_set = remove_clauses(clauses_set,unit)
            clauses_set = remove_literals(clauses_set,unit)
        
        #print()
        '''
        while():
            a = pure_literal(clauses_set.copy())
            if (a):
                remove_literals
                remove_clauses
                current sol
            else: break
        '''
        #pure literal
        #5
        if check_empty(clauses_set):
            #bactrack once , change 1 assumption
            current_sol[x] = 1-current_sol[x]
            guess = -1*guess
            clauses_set = clauses_backtrack.pop().copy()

            clauses_set = remove_clauses(clauses_set.copy(),x*guess)
            clauses_set = remove_literals(clauses_set.copy(),x*guess)
            
            unit = 0
            while (unit):
                unit = unit_propagation(clauses_set)
                #var = clause[0]
                avar = abs(unit)
                not_assigned.pop(not_assigned.index(avar))
                current_sol[avar] = int((avar/unit +1)/2)
                clauses_set = remove_clauses(clauses_set,unit)
                clauses_set = remove_literals(clauses_set,unit)
        
            if check_empty(clauses_set):
                #backtrack more , delete assumption
                current_sol.pop(x)
                not_assigned.append(x)
                clauses_set = clauses_backtrack.pop().copy()
                continue
        
        else:
            #go ahead
            continue

def unsatif():
    print(  "UNSATISFAIBLE")
    sys.exit()

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
    


    remaining_time = 10 -(time.time()-start_time) -0.005
    dpll(clauses,var_count,remaining_time)
    unsatif()