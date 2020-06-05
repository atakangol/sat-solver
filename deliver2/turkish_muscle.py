#!/usr/bin/python3

# Libraries

import sys
import os
import time
import random
import math
from copy import deepcopy

#python dpll_new.py "C:\Users\golat\Documents\Git\sat-solver\benchmarks\cnf-100-200-0.cnf"
class  Problem:
    def __init__(self,benchmark = None, var_count= None,clause_count= None,clauses= None):
        if (benchmark is not None):
            self.var_count,self.clause_count,temp = readData(benchmark)
            #self.var_count,self.clause_count,temp,v  =readnanalize(benchmark)
            #global var_map 
            #var_map = v
            self.clauses = deepcopy(temp)
            self.sol = {}
            self.init()
        else:
            self.clauses = deepcopy(clauses)
            self.var_count = var_count
            self.clause_count = clause_count
            self.sol = {}
            self.init()

    def init(self):
        for i in range(1,self.var_count+1):
            self.sol[i] = None
    def add_clause(self,c):
        self.clauses.append(c)
    def copy(self):
        new_prob = Problem(var_count=self.var_count,clause_count=self.clause_count,clauses=self.clauses)
        return new_prob
    def not_assigned(self):
        global var_map
        not_ass = []
        m = max(var_map.values())
        #var_map = dict(sorted(var_map.items(), key = lambda kv:(kv[1], kv[0])))
        for i in list(var_map.keys()):
            if (self.sol[i] == None) and var_map[i]==m:
                not_ass.append(i)

        return not_ass

    def empty_clause_check(self):
        for clause in self.clauses:
            if (len(clause) == 0):
                return True
        return False
    
    def pure_literals(self):
        found = []
        for clause in self.clauses:
            if (len(clause)==1):
                #print(clause[0])
                v = clause[0]
                found.append(v)
                self.sol[abs(v)] = int((abs(v)/v + 1)/2)
                
        for v in found:
            self.remove_literals(-1*v)
            self.remove_clauses(v)
        if len(found)>0:
            self.pure_literals()
            return True
        return False

    def unit_propagation(self):
        found = False
        for var in self.sol:
            not_pure = False
            #print("--")
            if (self.sol[var] == None):
                positive = None
                for clause in self.clauses:
                    if var in clause:
                        positive = True
                        break
                for clause in self.clauses:
                    if -1*var in clause:
                        if positive:
                            #not pure
                            not_pure = True
                            pass
                        else:
                            positive = False
                            break
                if (not_pure):
                    continue
                #print(var)
                if positive:
                    self.sol[var] = 1
                    v = var
                else:
                    self.sol[var] = 0
                    v = var * -1
                self.remove_literals(-1*v)
                self.remove_clauses(v)
                
                found = True
                break
        if found and (len(self.clauses) > 0):
            #print(self.clauses)
            self.unit_propagation()
            return True
        return False

    def remove_clauses(self,var):
        i=0
        while i < len(self.clauses):
            if (var in self.clauses[i]):
                self.clauses.remove(self.clauses[i])
                continue
            i += 1

    def remove_literals(self,var):
        for c in self.clauses:
            if var in c:
                c.remove(var)

    def assign_empty(self):
        if (len(self.clauses) !=0 ):
            return
        for var in self.sol:
            if self.sol[var] == None:
                self.sol[var] = 0


def dpll_rec(problem,var):
    
    if problem.empty_clause_check():
        #failed
        return False
    if len(problem.clauses) == 0:
        #succes
        problem.assign_empty()
        print_sol(problem.sol)
        return True
    old_problem = problem.copy()
    
    #assumption 1
    problem.sol[var] = 1
    problem.remove_clauses(var)
    problem.remove_literals(-1*var)

    p = u =  True
    while p or u :
        p = problem.pure_literals()
        u = problem.unit_propagation()
        #print(p,u)
    
    try:
        new_var = random.sample(problem.not_assigned(),1)[0]
        
    except :
        var_map[var] += 1
        return False
    

    dpll_rec(problem,new_var)
    
    #reset
    problem = old_problem.copy()
    #assumption 0
       
    problem.sol[var] = 0
    problem.remove_clauses(-1*var)
    problem.remove_literals(var)

    p = u =  True
    while p or u :
        p = problem.pure_literals()
        u = problem.unit_propagation()
        #print(p,u)
    
    try:
        new_var = random.sample(problem.not_assigned(),1)[0]
       
    except :
        
        var_map[var] += 1
        return False
    
    dpll_rec(problem,new_var)
    var_map[var] += 1
    return False

def dpll_init(problem):
    global var_map
    a = list(range(1,problem.var_count+1))
    random.shuffle(a)
    for k in a:
        var_map[k] = 0
    
    #print(var_map.keys())
    i = random.randint(1,problem.var_count)
    dpll_rec(problem,i)

def print_sol(sol):
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
    print(time.time() - start_time)  
    sys.exit()

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

def unsatif():
    print(  "UNSATISFAIBLE")
    sys.exit()

if __name__ == '__main__' :
    #random.seed(1)
    start_time = time.time()
    time_limit = 10

    var_map = {}

    if len(sys.argv) != 2:
        sys.exit("Use: %s <benchmark> ")
        sys.exit()
    benchmark = sys.argv[1]
    
    orig_problem = Problem(benchmark)
    if orig_problem.var_count>=sys.getrecursionlimit() * 0.85:
        sys.setrecursionlimit(int(orig_problem.var_count * 1.15))
    
    a = dpll_init(orig_problem)

    
    unsatif()
    print(time.time() - start_time)

    
