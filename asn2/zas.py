import numpy

def make_city(name,neighbours):
	"""
	Create a city (implemented as a list).
	
	:param name: String containing the city name
	:param neighbours: The city's row from an adjacency matrix.
	
	:return: [name, Infection status, List of neighbours]
	"""
	
	return [name, False, list(numpy.where(neighbours==1)[0])]
	

def make_connections(n,density=0.25):
	"""
	This function will return a random adjacency matrix of size
	n x n. You read the matrix like this:
	
	if matrix[2,7] = 1, then cities '2' and '7' are connected.
	if matrix[2,7] = 0, then the cities are _not_ connected.
	
	:param n: number of cities
	:param density: controls the ratio of 1s to 0s in the matrix
	
	:returns: an n x n adjacency matrix
	"""
	
	import networkx
	
	# Generate a random adjacency matrix and use it to build a networkx graph
	a=numpy.int32(numpy.triu((numpy.random.random_sample(size=(n,n))<density)))
	G=networkx.from_numpy_matrix(a)
	
	# If the network is 'not connected' (i.e., there are isolated nodes)
	# generate a new one. Keep doing this until we get a connected one.
	# Yes, there are more elegant ways to do this, but I'm demonstrating
	# while loops!
	while not networkx.is_connected(G):
		a=numpy.int32(numpy.triu((numpy.random.random_sample(size=(n,n))<density)))
		G=networkx.from_numpy_matrix(a)
	
	# Cities should be connected to themselves.
	numpy.fill_diagonal(a,1)
	
	return a + numpy.triu(a,1).T

def set_up_cities(names=['City 0', 'City 1', 'City 2', 'City 3', 'City 4', 'City 5', 'City 6', 'City 7', 'City 8', 'City 9', 'City 10', 'City 11', 'City 12', 'City 13', 'City 14', 'City 15']):
	"""
	Set up a collection of cities (world) for our simulator.
	Each city is a 3 element list, and our world will be a list of cities.
	
	:param names: A list with the names of the cities in the world.
	
	:return: a list of cities
	"""
	
	# Make an adjacency matrix describing how all the cities are connected.
	con = make_connections(len(names))
	
	# Add each city to the list
	city_list = []
	for n in enumerate(names):
		city_list += [ make_city(n[1],con[n[0]]) ]
	
	return city_list

def draw_world(world):
	"""
	Given a list of cities, produces a nice graph visualization. Infected
	cities are drawn as red nodes, clean cities as blue. Edges are drawn
	between neighbouring cities.
	
	:param world: a list of cities
	"""
	
	import networkx
	import matplotlib.pyplot as plt
	
	G = networkx.Graph()
	
	bluelist=[]
	redlist=[]
	
	plt.clf()
	
	# For each city, add a node to the graph and figure out if
	# the node should be red (infected) or blue (not infected)
	for city in enumerate(world):
		if city[1][1] == False:
			G.add_node(city[0])
			bluelist.append(city[0])
		else:
			G.add_node(city[0],node_color='r')
			redlist.append(city[0])
			
		for neighbour in city[1][2]:
			G.add_edge(city[0],neighbour)
	
	# Lay out the nodes of the graph
	position = networkx.circular_layout(G)
	
	# Draw the nodes
	networkx.draw_networkx_nodes(G,position,nodelist=bluelist, node_color="b")
	networkx.draw_networkx_nodes(G,position,nodelist=redlist, node_color="r")

	# Draw the edges and labels
	networkx.draw_networkx_edges(G,position)
	networkx.draw_networkx_labels(G,position)

	# Force Python to display the updated graph
	plt.show()
	plt.draw()
	
def print_world(world):
	"""
	In case the graphics don't work for you, this function will print
	out the current state of the world as text.
	
	:param world: a list of cities
	"""
	
	import string
	
	print string.ljust('City',15), 'Zombies?'
	print '------------------------'
	for city in world:
		print string.ljust(city[0],15), city[1]



#### That's the end of the stuff provided for you.
#### Put *your* code after this comment.
def zombify (cities,cityno):
	"""
	Infects one city from a list of cities. Sets the second element (infection) in the city's list to True 
	and this raises the inflection flag.
	
	:param cities: a list containing all cities
	:param cityno: The city's index number in the list of cities
	"""
	cities[cityno][1] = True 
def cure(cities,cityno):
	"""
	Cures one city from a list of cities.Sets the second element (infection) in the city's list 
	to False and lowers the inflection flag. 
	
	:param cities: a list containing all cities
	:param cityno: The city's index number in the list of cities
	"""
	cities[cityno][1] = False 
	
def sim_step(cities,p_spread,p_cure):
	"""
	Runs one time step of the simulation. If a city is infected, a random number generator picks a number between 0,1.
	If it is less than p_spread, then one randomly selected neighbour is infected. Random number generator is repeated 
	and if it is less than p_cure then the city itself gets cured. 
	
	:param cities: a list containing all cities
	:param p_spread: probability of the plague spreading to other cities 
	:param p_cure: probability of the plague being cured within city 
	"""
	for n, city in enumerate(cities): 
	 
		if cities[n][1]== True and numpy.random.rand() < p_spread: 
			x=len(cities[n][2]) # finds length of the neighbours list and stores into a variable  
			victim_infected=numpy.random.randint(0,x) #picks a neighbour from 0 to length of neighbour's list and stores into a variable
			zombify(cities,cities[n][2][victim_infected]) # uses last variable as an index or the neighbour list, raises infection flag for neighbour chosen through zombify()
				
		if cities[n][1] == True and numpy.random.rand() < p_cure:
			cure(cities,n) #cured so it lowers its own infection flag 
			
	cities[0][1] = True # to have city 0 always infected even if it is cured 
	
def is_end_of_world(cities):
	"""
	Determines if all cities in the world are infected. The second element of each city's list(infection) is looped over 
	to see if the infection flag is raised. 
	
	:param cities: a list containing all cities
	:return: variable containing boolean indicating if all cities are infected 
	"""
	is_it_the_end = True  #variable to be returned at the end to state if all cities are infected 
	for n, city in enumerate(cities): # indexes the cities and loops over all of them
		if cities[n][1] == False: #checks to see if the city's inflection flag is raised or not  
			is_it_the_end = False #if not raised then it sets the variable is_it_the_end to False 
	return is_it_the_end 
def time_to_end_of_world(p_spread,p_cure):
	"""
	Runs is_end_of_world function to determine if all cities are infected and if it returns False,
	it runs one time step of the sim_step function. Then the function checks if all cities are infected through
	is_end_of_world function after each time step until is_end_of_world function returns True. 
	
	
	:param p_spread: probability of the plague spreading to other cities 
	:param p_cure: probability of the plague being cured within city 
	
	:return: a counter showing how many time steps it took for all cities to be infected 
	"""

	end_of_world_counter = 0 #initializing a counter 
	my_world = set_up_cities() #setting up all the cities and storing them into a variable 
	my_world[0][1] == True # setting city 0 to always be infected 
	while is_end_of_world(my_world) == False:  #while loop runs sim_step repeatedly until all cities are infected 
		sim_step(my_world,p_spread,p_cure)
		end_of_world_counter = end_of_world_counter + 1 # increment the counter to keep track of how many time steps 
	return end_of_world_counter
		
def end_world_many_times(n,p_spread,p_cure):
	"""
	Creates an empty list and runs time_to_end_of_world n number of times. After each time the function returns 
	how long it took to end the world and adds it to the list. 
	
	:param n: The number of times you want to end the world 
	:param p_spread: probability of the plague spreading to other cities 
	:param p_cure: probability of the plague being cured within city 
	
	:return: variable containing a list of how many time steps it took to end the world each time for n number of times 

	"""
	list_of_results = [] #initialized an empty list
	ntimes = 0 #initialize a counter 
	my_world = set_up_cities() #set up all cities and store into a variable 
	while ntimes < n: # while loop ensures it run n times 
		list_of_results.append(time_to_end_of_world(p_spread,p_cure)) #runs time_to_end_world and adds what the function returns to the empty list
		ntimes = ntimes + 1 #increment the counter so it runs n times 
	return list_of_results 

import numpy as np
import matplotlib.pyplot as plt
ttl = end_world_many_times(500,0.9,0) #stored into a variable with chosen numbers to plot histogram 
plt.hist(ttl) # make a histogram 
plt.show() #to show the histogram 
