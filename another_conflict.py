#!/usr/bin/python3

# Libraries

import sys
import os
import time
import random
import math

######


######


#python conflict_final.py "C:\Users\golat\Documents\Git\sat-solver\benchmarks\cnf-100-200-0.cnf"

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

def readnprob(name): #reads and looks and more 0s or 1s
    with open(name, mode='r') as cnf_file:
        i=0
        clauses = []
        probs = []
        positives = []
        negatives = []
        var_map = {}
        for line in cnf_file:
            if (i==0):
                header = line.split(' ')
                var_count = int(header[2])
                i +=1
                for c in range(0,var_count):
                    var_map[c] = 0
                    probs.append(0)
            else:
                temp = line.split(' ')[:3]
                temp = list(map(int,temp))
                clauses.append(temp)
                for c in temp:
                    var_map[abs(c)-1] += 1
                    if (c>0):
                        probs[abs(c)-1] +=1
                    elif( (c<0)):
                        probs[abs(c)-1] -=1    



    for i in range(0,len(probs)):
        if (probs[i]>0):
            positives.append(i)
        elif(probs[i]<=0):
            negatives.append(i)
        #else:
            #x = random.choice([0,1])
            #if (x == 0):
                #negatives.append(i)
            #else:
                #positives.append(i)

    #var_map = dict(sorted(var_map.items(), key = lambda kv:(kv[1], kv[0])))
    var_map = dict(sorted(var_map.items(), key = lambda kv:(kv[1], kv[0]),reverse =True))
    var_map = list(var_map.keys())
    
    clause_count = len(clauses)

    return(var_count,clause_count,clauses,var_map,positives,negatives)

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

def ahead(assumed,var_map,positives,guess):
    new = var_map[len(assumed)]
    if (new in positives ):
        guess[new] = 1
    
    assumed.append(var_map[len(assumed)]+1)  

    return assumed

def backtrack(solution,assumed,var_map,positives):
    last = assumed[-1]
    if (last-1 in positives):
        target = 1
    else:
        target =0
    if(solution[last-1]==target):
        solution[last-1] = 1-target
        return()
    else:
        solution[last-1]=0
        a = assumed.pop()
        #print("a",a)
        return(backtrack(solution,assumed,var_map,positives))

def m_backtrack(solution,assumed,back,var_map,positives):
    last = back[-1]
    if (last-1 in positives):
        target = 1
    else:
        target =0
    if(solution[last-1]==target):
        solution[last-1] = 1-target
        return()
    else:
        solution[last-1]=0
        a = back.pop()
        i = assumed.index(a)
        a = assumed.pop(i)
        #print("a",a)
        return(backtrack(solution,assumed,var_map,positives))


def search_local_random(var_count,sol,offset,clauses,start,cutoff=5,per = 75):
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
    var_count,clause_count,clauses,var_map,positives,negatives = readnprob(benchmark)
    
    #print(var_map)
    #print(positives)
    #print(negatives)
    #print()
    guess = []
    for i in range(0,var_count):
        guess.append(0)
    assumed = []
    x = int(var_count*10/100)
    #print(x)
    old =[]
    for i in range(0,x):
        old.append(-10)
    #print(old)
    counter = 0
    best = [0,guess.copy()]
    temp_best = guess.copy()
    back = []
    #while (len(assumed)<=var_count):
    while(len(assumed) >= old[counter]):
        #input()
        
        back = assumed.copy()
        #back = assumed.reverse()
        if len(assumed) > 0:
            if (len(assumed) >= max(old)):
                #print(len(assumed) , max(assumed))
                #print(guess)
                #print(temp_best)
                temp_best = guess.copy()
            if (len(assumed)>best[0]):
                #print("______")
                #print(len(assumed),best[0])
                #print(guess)
                #print(best[1])
                best[0]= len(assumed)
                best[1] = guess.copy()
        old[counter] = len(assumed)
        counter += 1
        counter %= x
        #if (len(assumed)>=70):
        #    break
        
        #print(len(assumed) , end = " ")
        a = evaluate_assumption(clauses,guess,assumed)

        if (a == True):
            if(len(assumed)>=var_count):
                break
            ahead(assumed,var_map,positives,guess)
        else:
            #random.shuffle(back)
            back.reverse()
            #backtrack(guess,assumed,var_map,positives)

            m_backtrack(guess,assumed,back,var_map,positives)


    '''
    print("guess")
    #print(guess)
    print(clause_count-evaluate(clauses,guess))
    start = time.time()
    
    print(time.time() - start_time)
    stat,sol,offset = search_local_random(var_count,guess,clause_count-evaluate(clauses,guess),clauses,start,cutoff = 10-(start-start_time)-0.01)
    #stat,sol,offset = search_local_all(var_count,guess,clause_count-evaluate(clauses,guess),clauses,start)
    #print(offset,sol)
    print(offset, 100*offset/var_count)
    print()
    
    
    print("best")
    #print(best[1])
    print(clause_count-evaluate(clauses,best[1]))
    start = time.time()
    stat,sol,offset = search_local_random(var_count,guess,clause_count-evaluate(clauses,guess),clauses,start,cutoff = 10-(start-start_time)-0.01)
    #print(offset,sol)
    print(offset, 100*offset/var_count)
    print()
    '''
    
    print()
    print("local")
    #print(temp_best)
    print(clause_count-evaluate(clauses,temp_best))
    start = time.time()
    stat,sol,offset = search_local_random(var_count,guess,clause_count-evaluate(clauses,guess),clauses,start,cutoff = 10-(start-start_time)-0.01)
    #print(offset,sol)
    print(offset, 100*offset/var_count)
    print()

    '''
    '''
    print(time.time() - start_time)

