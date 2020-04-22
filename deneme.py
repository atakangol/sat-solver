#!/usr/bin/python3

# Libraries

import sys
import os
import time
import random
import math
from copy import deepcopy,copy

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
    for i in range(0,len(clauses_set)):
        clause = clauses_set[i]
        if var in clause:
            clauses_set.pop(i)
            return(remove_clauses(deepcopy(clauses_set),var))

    return(clauses_set)

def remove_literals(clauses_set,var):
    var = -1*var
    for clause in clauses_set:
        if (var in clause):
            
            clause.pop(clause.index(var))
            
    return(clauses_set)

def check_empty(clauses_set):
    for clause in clauses_set:
        if (len(clause) == 0):
            return True
    return False

def dpll(clauses,var_count,limit):
    start_time = time.time()
    current_sol = {}
    #step = 0
    old_clauses = []
    current_clauses = deepcopy(clauses)
    assigned = []
    not_assigned = []
    old_na = []
    for i in range(1,var_count+1):
        not_assigned.append(i)
    #extra = []
    old_sol=[]
    old_sol.append(deepcopy(current_sol))
    old_clauses.append(deepcopy(current_clauses))
    old_na.append(not_assigned.copy())
    while (True):
        if(len(old_na) != len(old_clauses)):
            print("-----------------------------------------------")
        #extra = []
        '''
        print(assigned)
        print(not_assigned)
        print(current_clauses)
        print(current_sol)
        print()
        #for c in old_clauses:
            #print(c)
        print("__")
        input()
        '''

        a = check_empty(current_clauses)
        
        if (a == False):
            if(len(not_assigned)==0):
                print(evaluate(clauses,current_sol),clause_count)
                print_sol(current_sol)
            #old_clauses.append(deepcopy(current_clauses))
            current_clauses = ahead(assigned,not_assigned,deepcopy(current_clauses),current_sol)
            
            #unit propagation
            unit = 0
            
            while (unit != None):
                unit = unit_propagation(current_clauses)
                if (unit == None): break
                aunit = abs(unit)
                if(aunit not in not_assigned):
                    #print(aunit)
                    #print(sorted(current_sol))
                    #print(sorted(get_unique(current_clauses)))
                    #print(current_clauses)
                    print(aunit in current_sol)
                    #print(sorted(not_assigned))
                    #print(sorted(get_unique(current_clauses)))
                    #print()
                    break
                not_assigned.pop(not_assigned.index(aunit))
                current_clauses = remove_clauses(deepcopy(current_clauses),unit)
                current_clauses = remove_literals(deepcopy(current_clauses),unit)
                
                aunit = abs(unit)
                current_sol[aunit] = int((aunit/unit +1)/2)
            
            old_sol.append(deepcopy(current_sol))
            old_na.append(copy(not_assigned))
            old_clauses.append(deepcopy(current_clauses))
        else:
            
            current_clauses,current_sol = backtrack(old_clauses,assigned,not_assigned,deepcopy(current_clauses),current_sol,old_na,old_sol)
            continue
    
    
    
    return

def ahead(assigned,not_assigned,current_clauses,current_sol):
    #i = random.randint(0,len(not_assigned)-1)
    #var = not_assigned.pop(i)
    var = random.choice(not_assigned)
    not_assigned.pop(not_assigned.index(var))
    #print(var)
    assigned.append(var)

    #first guess is 0
    current_sol[var] = 0

    current_clauses = remove_clauses(deepcopy(current_clauses),-1*var)
    current_clauses = remove_literals(deepcopy(current_clauses),-1*var)
    #print(current_clauses)
    

    return(current_clauses)

def backtrack(old_clauses,assigned,not_assigned,current_clauses,current_sol,old_na,old_sol):
    #print(old_clauses)
    last = assigned[-1]
    #print(last,current_sol[last],current_sol)
    if (current_sol[last]==0):
        
        
        (old_clauses.pop())
        current_clauses = deepcopy(old_clauses[-1])
        (old_na.pop())
        not_assigned = copy(old_na[-1])
        (old_sol.pop())
        current_sol = deepcopy(old_sol[-1])
        
        #print(last in current_sol)
        #print(last in not_assigned)
        current_sol[last] = 1
        not_assigned.pop(not_assigned.index(last))
        #print(last in current_sol)
        #print(last in not_assigned)
        #print(sorted(not_assigned))
        #print(sorted(get_unique(current_clauses)))
        #print()
        
        current_clauses = remove_clauses(deepcopy(current_clauses),last)
        current_clauses = remove_literals(deepcopy(current_clauses),last)
        '''
        unit=0
        while (unit != None):
                unit = unit_propagation(current_clauses)
                if (unit == None): break
                aunit = abs(unit)
                if(aunit not in not_assigned):
                    print("2")
                    print(aunit in not_assigned)
                    #print(sorted(not_assigned))
                    #print(sorted(get_unique(current_clauses)))
                    #print()
                    break
                not_assigned.pop(not_assigned.index(aunit))
                current_clauses = remove_clauses(deepcopy(current_clauses),unit)
                current_clauses = remove_literals(deepcopy(current_clauses),unit)
                
                aunit = abs(unit)
                current_sol[aunit] = int((aunit/unit +1)/2)
        '''

        old_sol.append(deepcopy(current_sol))
        old_clauses.append(deepcopy(current_clauses))
        old_na.append(copy(not_assigned))
        return(current_clauses,current_sol)

    else:
        (old_clauses.pop())
        current_clauses = deepcopy(old_clauses[-1])
        (old_na.pop())
        not_assigned = copy(old_na[-1])
        (old_sol.pop())
        current_sol = deepcopy(old_sol[-1])
        
        assigned.pop()
        '''
        not_assigned.append(last)
        current_sol.pop(last)
        '''
        #print("__")
        #print(sorted(not_assigned))
        #print(sorted(get_unique(current_clauses)))
        #print()
        
        return (backtrack(old_clauses,assigned,not_assigned,deepcopy(current_clauses),current_sol,old_na,old_sol))

def unit_propagation(clauses_set):
    for clause in clauses_set:
        if (len(clause) == 1):
            #found unit
            #print(clauses_set)
            return (clause[0])
    return(None)

def get_unique(clauses_set):
    vars = []
    for clause in clauses_set:
        for c in clause:
            if(abs(c) not in vars):
                vars.append(abs(c))
    return (vars)


def test(clauses,var_count,limit):
    start_time = time.time()
    current_sol = {}
    #step = 0
    old_clauses = []
    current_clauses = deepcopy(clauses)
    assigned = []
    not_assigned = []
    old_na = []
    for i in range(1,var_count+1):
        not_assigned.append(i)
    #extra = []
    old_sol=[]
    old_sol.append(deepcopy(current_sol))
    old_clauses.append(deepcopy(current_clauses))
    old_na.append(not_assigned.copy())
    
    
    
    current_clauses = ahead(assigned,not_assigned,deepcopy(current_clauses),current_sol)

    old_sol.append(deepcopy(current_sol))
    old_na.append(copy(not_assigned))
    old_clauses.append(deepcopy(current_clauses))

    current_clauses = ahead(assigned,not_assigned,deepcopy(current_clauses),current_sol)

    old_sol.append(deepcopy(current_sol))
    old_na.append(copy(not_assigned))
    old_clauses.append(deepcopy(current_clauses))
    '''
    unit = unit_propagation(current_clauses)
    aunit = abs(unit)
               
    not_assigned.pop(not_assigned.index(aunit))
    current_clauses = remove_clauses(deepcopy(current_clauses),unit)
    current_clauses = remove_literals(deepcopy(current_clauses),unit)
    
    aunit = abs(unit)
    current_sol[aunit] = int((aunit/unit +1)/2)
    '''
    print(assigned)
    print(not_assigned)
    print(current_clauses)
    print(current_sol)
    print()
    #for c in old_clauses:
        #print(c)
    print("__")


    
    current_clauses,current_sol = backtrack(old_clauses,assigned,not_assigned,deepcopy(current_clauses),deepcopy(current_sol),
                                    old_na,old_sol)
         
    print(assigned)
    print(not_assigned)
    print(current_clauses)
    print(current_sol)
    print()
    #for c in old_clauses:
    for c in old_sol:
    #for c in old_na:
        print(c)
    print("__")

    
    
    return


if __name__ == '__main__' :
    random.seed(5)
    start_time = time.time()
    time_limit = 10

    if len(sys.argv) != 2:
        sys.exit("Use: %s <benchmark> ")
        sys.exit()
    benchmark = sys.argv[1]
    
    #read data
    var_count,clause_count,clauses,positives = readnprob(benchmark)
    
    #test(clauses,var_count,10)

    dpll(clauses,var_count,10)




    
    remaining_time = 10 -(time.time()-start_time) -0.001


