##
# Branch and Bound Algorithm to solve Minimum Vertex Cover Problem
# Created by: Saurabh
# Team : 22 of CSE 6140, Fall 2020
# Last Modified On: 28th November, 2020
##

import argparse
import math
import sys
from sys import argv
import networkx as net
import operator
import time
import os

# Function to read in the given input file
def parse(datafile):
	# Declaring empty adjacency list
	adj_list = []
	with open(datafile) as df:
		# Reading number of vertices, number of edges and whether the graph is unidrected from the first line of data file
		num_vertices, num_edges, weighted = map(int, df.readline().split())
		# Using for loop through every vertex to find their neighbors and store in adjacency list
		for i in range(num_vertices):
			adj_list.append(map(int, df.readline().split()))
	return adj_list

# Function to create graph using adjacency list
def create_graph(adj_list):
	# Creating graph G using module Networkx 
	G = net.Graph()
	# Adding edges in the graph G as per adjacency list
	for i in range(len(adj_list)):
		for j in adj_list[i]:
			G.add_edge(i + 1, j)
	return G

# Branch and Bound Function:

def Branch_And_Bound(G,T):
	# Noting the begin and finish time

	begin_time = time.time()
	finish_time = begin_time

	#total_time = finish_time - begin_time
	
	# time_list when solution is found
	time_list = []

	# We will initialize Minimum VC, Current VC, Frontier set, and neighbor set
	MVC = []
	Current_VC = []
	Frontier = []
	neighbor = []

	# Setting Upper Bound as total number of vertices initially
	UB = G.number_of_nodes()
	print('Initial UpperBound:', UB)

	# Storing a duplicate of graph G in Current_Graph
	Current_Graph = G.copy() 

	# We will sort the vertices in Current Graph as per number of edges they carry
	a = max_degree(Current_Graph)
	

	# Adding the first element of a to Frontier
	# We will also give the possible state of the vertex along with it's parent vertex and it's state
	# Here, the first element of a is at root, hence parent vertex will be shown with (-1), and it's state too 

	Frontier.append((a[0], 0, (-1, -1)))  
	Frontier.append((a[0], 1, (-1, -1)))
	# print(Frontier)

	while Frontier!=[] and total_time < T:
		# We will select a candidate node (CN) for our solution as last element in Frontier Set
		(CN,state,parent) = Frontier.pop()

		#print('New Iteration(CN,state,parent):', CN, state, parent)
		backtrack = False

		#print(parent[0])
		# print('Neigh',CN,neighbor)
		# print('Remaining no of edges',Current_Graph.number_of_edges())


		if state == 0:  
			# CN is not present in Vertex Cover, we will select all neighbors of CN in Vertex Cover and change their states to 1
			# neighbor list will contain all neighbors of CN of current graph
			neighbor = Current_Graph.neighbors(CN) 

			# For loop will change states of neighbors of C to 1, add them in Vertec Cover list and remove from current graph list 
			for vertex in list(neighbor):
				Current_VC.append((vertex, 1))
				Current_Graph.remove_node(vertex)  

		elif state == 1:  
			# if CN is present in Vertex Cover, then it's neighbors will not be present and hence their state will be changed to 0
			# CN will be removed from current graph list
			Current_Graph.remove_node(CN) 
			#print('new Current_Graph',Current_Graph.edges())
		else:
			pass

		Current_VC.append((CN, state))
		Current_Vertex_Cover_Size = Vertex_Cover_Size(Current_VC)
		#print('Current_VC Size', Current_Vertex_Cover_Size)
		# print(Current_Graph.number_of_edges())
		# print(Current_Graph.edges())

		# print('no of edges',Current_Graph.number_of_edges())
		if Current_Graph.number_of_edges() == 0:  
			# There are no edges left in the current graph after every possibility
			if Current_Vertex_Cover_Size < UB:
				# If current vertex cover size is less than current optimal or upper bound, update upper bound and MVC
				MVC = Current_VC.copy()
				
				print('Current Optimal Vertex Cover size is', Current_Vertex_Cover_Size)
				UB = Current_Vertex_Cover_Size
		
				time_list.append((Current_Vertex_Cover_Size,time.time() - begin_time))
			# As we completed one branch, we need to return or backtrack to previous nodes, to check for other solutions
			backtrack = True
			#print('First backtrack-vertex-',CN)

		else:   
			# We can still see other options at this node: Either further solution possible or it is a dead end
			# We will update the current lower bound and check for these options
			Current_LB = Lower_Bound(Current_Graph) + Current_Vertex_Cover_Size
			#print(CurLB)
			#CurLB=297

			if Current_LB < UB:  
				# The current branch still has potential and we can check further
				# We will attach one new node with two states to our CN. CN will be the parent 
				new_node = max_degree(Current_Graph)
				Frontier.append((new_node[0], 0, (CN, state)))
				Frontier.append((new_node[0], 1, (CN, state)))
				# print('Frontier',Frontier)
			else:
				# The current branch cannot give better solution then our current best and hence we backtrack from here
				backtrack = True
				#print('Second backtrack-vertex-',CN)


		if backtrack == True:
			# When we reach a deadend or find a feasible solution, we backtrack to search for another solution
			if Frontier != []:	
				# As Frontier has elements, we can explore remaining elements
				# We will find the parent of the last element in Frontier. We will get parent and it's state
				last_parent = Frontier[-1][2]	

				# Now in our current Vertex Cover, we will rewind back to parent of last node
				if last_parent in Current_VC:
					# We will find the last_parent in our current Vertex solution
					# We will find location of last_parent	
					location = Current_VC.index(last_parent) + 1
					while location < len(Current_VC):	
						# We will reverse the changes done in Current Vertex Cover list from back till the last_parent location
						# Remove them from Current_VC list
						# Add them again in Current Graph list

						node, state = Current_VC.pop()	
						Current_Graph.add_node(node)	

						# We will find the nodes that are connected to CN through direct edges and not present in current Vertex Cover Solution
						# Current_VC is a tuple and the first element has the vertex, hence extracting that through lambda function
						Nodes_Current_VC = list(map(lambda x:x[0], Current_VC))
						
						# For loop to pass thorugh each neighbor of node
						for value in G.neighbors(node):
							# Adding the edge of CN again to Current_Graph, if the node is not present in Current Vertex Cover but in Current Graph
							if ((value in Current_Graph.nodes()) and (value not in Nodes_Current_VC)):
								Current_Graph.add_edge(value, node)	

				elif last_parent == (-1, -1):
					# We have traced back to the start or root node, hence will restore our Current Graph and clear the Vertex Cover
					Current_VC.clear()
					Current_Graph = G.copy()
				else:
					# If both of the above cases fail, then there is an error and backtracking is not possible
					print('There is an error and backtracking not possible')

		
		finish_time = time.time()
		total_time = finish_time - begin_time
		if total_time > T:
			print('We have crossed our given time for running the algorithm, hence terminating here')

	return MVC, time_list

# Function to get a vertex which has maximum degree or number of edges 
def max_degree(G):
	# First we will find degrees of all vertices of graph G and then sort them in descending order
	# Then, we can select the first element in the list, as it will have the highest degree
	degree_list = G.degree()
	# Our reverse will be true, as we want descending order.
	# Key will be the second element in tuple of (vertex, degree), as we want to sort by degree
	sorted_degree_list = sorted(degree_list, reverse = True, key = operator.itemgetter(1))  
	x = sorted_degree_list[0] 
	return x

# Intialising Lower Bound for the graph
def Lower_Bound(G):
	# We can assume maximum degree of the graph as our initial lower bound for MVC
	lb = max_degree(G)[1]
	return lb

# Function to determine size of Vertex Cover Solution at any point or the number of vertices with state as 1
def Vertex_Cover_Size(list):
	# The input list is in the form of tuples, and the second element gives us the state of the vertex
	# By adding the all the 2nd elements, we can get the size of Vertex Cover or the vertices which have state as 1  
	size = 0
	for i in list:
		size = size + i[1]
	return size


# Main Function

def main(data_file, result_file, max_time, randSeed):

	# Taking the main data file
	adj_list = parse(data_file)	

	# Making graph from the input file 
	g = create_graph(adj_list)

	MVC,time_list = Branch_And_Bound(g, max_time)

	# Removing the nodes with state = 0 condition
	for node in MVC:
		if node[1]==0:
			MVC.remove(node)


	