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
    
    for clause in clauses:
        false_count = 0
        #next_clause = False
        #print(clause)
        #print()
        variables = []
        for var in clause:
            variables.append(abs(var))
        if (max(variables) <= assumed): #in assumption
            print(clause)
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

def merge_lists(litem1,litem2):
    
    merged = []
    l = min(len(litem1),len(litem2))
    for i in range(0,l):
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
    
    litem = [1,2,3,4,5,6,7,8,9,10,11]
    litem = merge_lists(litem[0:int(len(litem)/2)],litem[int(len(litem)/2):])
    #print(llll)
    print(litem)