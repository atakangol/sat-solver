#!/usr/bin/python3

# Libraries

import sys
import os
import time
import random
import math

######


######


#python trial.py "C:\Users\golat\Documents\Git\sat-solver\benchmarks\cnf-100-200-0.cnf"

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

def readnanalize(name):
    with open(name, mode='r') as cnf_file:
        i=0
        clauses = []
        var_map = {}
        for line in cnf_file:
            if (i==0):
                header = line.split(' ')
                var_count = int(header[2])
                i += 1
                for c in range(0,var_count):
                    var_map[c] = 0
                #print(counts)
            else:
                temp = line.split(' ')[:3]
                temp = list(map(int,temp))
                clauses.append(temp)
                for c in temp:
                    var_map[abs(c)-1] += 1

    #print(counts)
    var_map = dict(sorted(var_map.items(), key = lambda kv:(kv[1], kv[0])))
    #var_map = dict(sorted(var_map.items(), key = lambda kv:(kv[1], kv[0]),reverse=True))
    print(var_map)
    var_map = list(var_map.keys())
    #var_map = merge_lists(var_map[0:int(len(var_map)/2)],var_map[int(len(var_map)/2):])
    clause_count = len(clauses)
    return(var_count,clause_count,clauses,var_map)

def merge_lists(litem1,litem2):
    
    merged = []
    l = min(len(litem1),len(litem2))
    for i in range(0,int(l/3)):
        a = litem1.pop(0)
        merged.append(a)
        a = litem1.pop(0)
        merged.append(a)
        a = litem1.pop(0)
        merged.append(a)


        a = litem2.pop()
        merged.append(a)
    if(len(litem1)>0):
        l=len(litem1)
        for i in range(0,l):
            a = litem1.pop(0)
            merged.append(a)
    if(len(litem2)>0):
        l=len(litem2)
        for i in range(0,l):
            a = litem2.pop(0)
            merged.append(a)
    return(merged)



def evaluate_assumption(clauses,solution,assumed):
    #true_count = 0
    #print(solution)
    for clause in clauses:
        false_count = 0
        #next_clause = False
        #print(clause)
        #print()
        variables = []
        for var in clause:
            variables.append(abs(var))
        if (compare_lists(variables,assumed)): #in assumption
            #print("hop",clause)
            for var in clause:
                real = abs(var)-1 
                #print(real)
                target = 1
                if (var<0): target =0
                if (solution[real]!=target):
                    #satisfied
                    #print("-")
                    false_count += 1
                    #return(True)
            if(false_count==3):
                return(False)
    return (True)

def compare_lists(small,big):
    for i in small:
        if (i not in big):
            return False
    return True

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

def ahead(assumed,var_map):
    
    assumed.append(var_map[len(assumed)]+1)  

    return assumed

def backtrack(solution,assumed,var_map):
    last = assumed[-1]
    if(solution[last-1]==0):
        solution[last-1] = 1
        return()
    else:
        solution[last-1]=0
        a = assumed.pop()
        #print("a",a)
        return(backtrack(solution,assumed,var_map))

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
                #print ("FOUND")
                return (True,temp,new_offset)
            
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
        return (False,sol,offset)


    return (False,sol,offset)

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
                print ("FOUND",sol)
                return (True,temp,new_offset)
            
            if (new_offset < offset):
                    print("hop")

                    sol = temp.copy()
                    offset = new_offset
                    #print(offset)
                    break
    return

def print_sol(sol):
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
    var_count,clause_count,clauses,var_map = readnanalize(benchmark)
    #print(var_map)
    assumed = []
    guess = []
    for i in range(0,var_count):
        guess.append(0)


    #print(assumed,len(assumed))
    while (len(assumed)<=var_count):
        #print(len(assumed), end = " ")
        if (len(assumed)>=60):
            break
        a = evaluate_assumption(clauses,guess,assumed)
        #print(a)
        if (a == True):
            if(len(assumed)==var_count):
                break
            ahead(assumed,var_map)
        else:
            
            backtrack(guess,assumed,var_map)

           # print(guess)
            #print(assumed)
        
            
    print(guess)
    print(clause_count-evaluate(clauses,guess))
    print(time.time() - start_time)
    start = time.time()
    #stat,sol,offset = search_local_random(var_count,guess,clause_count-evaluate(clauses,guess),clauses,start)
    stat,sol,offset = search_local_all(var_count,guess,clause_count-evaluate(clauses,guess),clauses,start)
    print(offset,sol)
    print(time.time() - start_time)

   
    

