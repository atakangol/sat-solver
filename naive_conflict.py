#!/usr/bin/python3

# Libraries

import sys
import os
import time
import random
import math

######


######


#python naive_conflict.py "C:\Users\golat\Documents\Git\sat-solver\benchmarks\cnf-100-200-0.cnf"

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

old_evaluate_assumption='''def evaluate_assumption(clauses,solution,assumed):
    #true_count = 0
    
    for clause in clauses:
        next_clause = False
        variables = []
        for var in clause:
            variables.append(abs(var))
        print(variables)
        for var in clause:
            real = abs(var)-1 #index
            #print(real,end=" ")
            target = 1
            if (var<0): target =0
            if (solution[real]==target):
                #satisfied
                #true_count += 1
                #next clause
                print("hop")
                next_clause = True

        #end for
        if (next_clause):
            print("hop")
            continue
        else:
            #not satisfied
            if (max(variables) <= assumed):
                #assumption wrong 
                return(False)
    return(True)

                '''

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
        if (max(variables) <= assumed): #in assumption
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

def first_guesses(index):
    first_assumptions = [ 
    [0,0,0],[0,0,1],
    [0,1,0],[0,1,1],
    [1,0,0],[1,0,1],
    [1,1,0],[1,1,1]]
    
    
    return first_assumptions[index]

def ahead(guess):
    guess.append(0)
    return guess

def backtrack(guess):
    if (len(guess) <= 3):
        return(False,guess)
    wrong = guess.pop()
    if (wrong==0):
        guess.append(1)
        return(True,guess)
    else:
        return(backtrack(guess))

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
    var_count,clause_count,clauses = readData(benchmark)
    guess = []
    i = 0
    state = 0
    while (len(guess)<=var_count):
        #print(len(guess),end=" ")
        #input()
        if (len(guess)<3 or state == 0):
            guess = first_guesses(i)
            i += 1
            state = 1
        else:
            #print("__")
            a = evaluate_assumption(clauses,guess,len(guess))
            #print(a)
            if (a == True):
                guess = ahead(guess.copy())
                
                if (len(guess)>=var_count):
                    break
                continue

            else:
                
                s,guess = backtrack(guess.copy())
                if(s):
                    continue
                else: 
                    state = 0
        
    print(clause_count-evaluate(clauses,guess))
    print(guess)



    '''
    first_assumptions = [ 
    [0,0,0],[0,0,1],
    [0,1,0],[0,1,1],
    [1,0,0],[1,0,1],
    [1,1,0],[1,1,1],]

    
    state = 0
    #assumed = 3
    i = 0
    k=-1
    guess = []
    #while (time.time()-start_time < time_limit):
    #print(var_count)
    #while (True):
    while (len(guess)<var_count):
        print("eval",evaluate_assumption(clauses,guess,len(guess)))
        k += 1
        print("s",state)
        print("k",k)
        print("i",i)
        print(len(guess),guess)
        input("")
        
        if (state == 0): #first 3
            
            assumption = first_assumptions[i]
            guess = assumption.copy()
            if(evaluate_assumption(clauses,guess,len(guess))):
                state = 1
                continue
                
            else:
                i += 1
                state=1
                continue


        elif (state==1): #new var
            guess.append(0)
            if(evaluate_assumption(clauses,guess,len(guess))):
                state = 1
                continue
            else:
                state = 2
                continue
        
        elif (state == 2): #change var to 1
            guess.pop()
            guess.append(1)
            if(evaluate_assumption(clauses,guess,len(guess))):
                state = 1
                continue
            else:
                state = 3
                continue
        
        elif (state == 3): #backtrack
            a = guess.pop()
            if (len(guess) > 3 ):
                if (guess[-1] == 1):
                    state = 3
                    continue
                if (guess[-1] == 0):
                    state = 2
                    continue

            else: #baktrack to first assumptions
                i += 1
                state = 0
                continue
    print(evaluate(clauses,guess)-var_count)
    print(guess)


    '''
    print(time.time() - start_time)

   
    

