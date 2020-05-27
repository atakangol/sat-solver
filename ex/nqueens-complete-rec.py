#!/usr/bin/python
#######################################################################
# Copyright 2019 Josep Argelich

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################

# Libraries

import sys
import random

# Classes 

class Interpretation():
	"""An interpretation is an assignment of the possible values to variables"""

	def __init__(self, N):
		"""
		Initialization
		N: The problem to solve
		num_vars: Number of variables to encode the problem
		vars: List of variables from 0 to num_vars - 1. The value in position [i]
	          of the list is the value that the variable i takes for the current
	          interpretation
		"""
		self.num_vars = N
		self.vars = [None] * self.num_vars

	def safe_place(self, n, row):
		""" Detects if a position in the board is a safe place for a queen"""
		for num_queen in xrange(n + 1, self.num_vars): # Iterate over the columns on the right of num_queen
			if row == self.vars[num_queen] or abs(n - num_queen) == abs(row - self.vars[num_queen]): # If they are in the same row or they are in the same diagonal
				return False
		return True

	def copy(self):
		"""Copy the values of this instance of the class Interpretation to another instance"""
		c = Interpretation(self.num_vars)
		c.vars = list(self.vars)
		return c

	def show(self):
		"""Show the solution that represents this interpretation"""
		print "Solution for %i queens" % (self.num_vars)
		print self.vars
		# First line
		sys.stdout.write("+")
		for c in xrange(self.num_vars):
			sys.stdout.write("---+")
		sys.stdout.write("\n")
		# Draw board rows
		for r in xrange(self.num_vars):
			sys.stdout.write("|")
			# Draw column position
			for c in xrange(self.num_vars):
				if r == self.vars[c]: # If the row == to the value of the variable
					sys.stdout.write(" X |")
				else:
					sys.stdout.write("   |")
			sys.stdout.write("\n")
			# Middle lines
			sys.stdout.write("+")
			for c in xrange(self.num_vars):
				sys.stdout.write("---+")
			sys.stdout.write("\n")

class Solver():
	"""The class Solver implements an algorithm to solve a given problem instance"""

	def __init__(self, problem):
		"""
		Initialization
		problem: An instance of a problem
		sol: Solution found
		"""
		self.problem = problem
		self.sol = None

	def solve(self):
		"""
		Implements a recursive algorithm to solve the instance of a problem
		"""
		curr_sol = Interpretation(self.problem) # Empty interpretation
		self.place_nqueens(curr_sol, self.problem - 1) # From column N - 1 to 0
		return self.sol

	def place_nqueens(self, curr_sol, n):
		"""
		Recursive call that places one queen each time
		"""
		if n < 0: # Base case: all queens are placed
			self.sol = curr_sol # Save solution
			return True # Solution found
		else: # Recursive case
			for row in xrange(self.problem): # We will try each row in column n
				if curr_sol.safe_place(n, row): # Is it safe to place queen n at row?
					# Without undo steps after recursive call
					new_sol = curr_sol.copy() # Copy solution
					new_sol.vars[n] = row # Place queen
					if self.place_nqueens(new_sol, n - 1): # Recursive call for column n - 1
						return True # Solution found
					# With undo steps after recursive call
					# curr_sol.vars[n] = row # Place queen
					# if self.place_nqueens(curr_sol, n - 1): # Recursive call for column n - 1
					# 	return True
					# curr_sol.vars[n] = None # Undo place queen
		return False

# Main

if __name__ == '__main__' :
	"""
	A basic complete recursive solver for the N queens problem
	"""

	# Check parameters
	if len(sys.argv) != 2:
		sys.exit("Use: %s <N>" % sys.argv[0])
	
	try:
		N = int(sys.argv[1])
	except:
		sys.exit("ERROR: Number of queens not an integer (%s)." % sys.argv[1])
	if (N < 4):
		sys.exit("ERROR: Number of queens must be >= 4 (%d)." % N)

	# Create a solver instance with the problem to solve
	solver = Solver(N)
	# Solve the problem and get the best solution found
	best_sol = solver.solve()
	# Show the best solution found
	best_sol.show()
