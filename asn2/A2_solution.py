## CS 2120 Assignment #2 -- Take Back Our World!
## Name: Me
## Student number: 3543589
## Grade: 100 %


import numpy
import matplotlib.pyplot as plt
import matplotlib

#### This stuff you just have to use, you're not expected to know how it works.
#### You just need to read the plain English function headers.
#### If you want to learn more, by all means follow along (and ask questions if
#### you're curious). But you certainly don't have to.

def make_city(name,neighbours):
    """
    Create a city (implemented as a list).
    
    :param name: String containing the city name
    :param neighbours: The city's row from an adjacency matrix.
    
    :return: [name, Infection status, List of neighbours]
    """
    
    return [name, False, list(numpy.where(neighbours==1)[0])]


def make_connections(n,density=0.35):
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

#def set_up_cities(names=['City 0', 'City 1', 'City 2', 'City 3', 
#                         'City 4', 'City 5', 'City 6', 'City 7', 
#                         'City 8', 'City 9', 'City 10', 'City 11', 
#                         'City 12', 'City 13', 'City 14', 'City 15']):
    
def set_up_cities(names=['Toronto', 'New York City', 
                         'Los Angeles', 'Mexico City', 
                         'Chicago', 'Washington DC', 
                         'Arlington County', 'Langley', 
                         'Fort Meade', 'Vancouver', 
                         'Houston', 'Ottawa',
                         'Jacksonville', 'San Francisco', 
                         'Waltham', 'Bethesda']):
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

def get_real_world():
    """
    Set up a particular collection of cities (world) for our simulator so that
    all of us have a common model of the real world to work with.
    Each city is a 3 element list, and our world will be a list of cities.
    
    :return: a list of cities
    """
    return [['Toronto', True, [0, 6, 9, 11, 14]],
            ['New York City', False, [1, 4, 7, 9, 11, 14]],
            ['Los Angeles', False, [2, 5, 7, 9, 10, 11, 12]],
            ['Mexico City', False, [3, 7, 8, 10, 14, 15]],
            ['Chicago', False, [1, 4, 8, 11, 14]],
            ['Washington DC', False, [2, 5, 8, 13, 14, 15]],
            ['Arlington County', False, [0, 6, 7, 10, 12, 14, 15]],
            ['Langley', False, [1, 2, 3, 6, 7, 14, 15]],
            ['Fort Meade', False, [3, 4, 5, 8, 9, 13]],
            ['Vancouver', False, [0, 1, 2, 8, 9, 11, 15]],
            ['Houston', False, [2, 3, 6, 10, 15]],
            ['Ottawa', False, [0, 1, 2, 4, 9, 11, 12, 14]],
            ['Jacksonville', False, [2, 6, 11, 12, 14, 15]],
            ['San Francisco', False, [5, 8, 13, 15]],
            ['Waltham', False, [0, 1, 3, 4, 5, 6, 7, 11, 12, 14, 15]],
            ['Bethesda', False, [3, 5, 6, 7, 9, 10, 12, 13, 14, 15]]]

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
    
    redlist=[]
    greenlist=[]
    
    plt.clf()
    plt.figure(num=None, figsize=(8, 6), dpi=180, facecolor='w', edgecolor='k')
    
    # For each city, add a node to the graph and figure out if
    # the node should be red (lost) or green (regained)
    for city in enumerate(world):
        if city[1][1] == False:
            G.add_node(city[0])
            redlist.append(city[0])
        else:
            G.add_node(city[0],node_color='g')
            greenlist.append(city[0])
        
        for neighbour in city[1][2]:
            G.add_edge(city[0],neighbour)
    
    # Lay out the nodes of the graph
    position = networkx.circular_layout(G)
    
    # Draw the nodes
    networkx.draw_networkx_nodes(G,position,nodelist=redlist, node_color="r")
    networkx.draw_networkx_nodes(G,position,nodelist=greenlist, node_color="g")

    # Draw the edges and labels
    networkx.draw_networkx_edges(G,position)
    networkx.draw_networkx_labels(G,position)

    # Force Python to display the updated graph
    plt.legend(['Lost','Regained'])
    plt.savefig('graph.png')
    plt.show()
    plt.draw()

def print_world(world):
    """
    In case the graphics don't work for you, this function will print
    out the current state of the world as text.

    :param world: a list of cities
    """

    print('{:19}{}'.format('City', 'Regained?'))
    print('----------------------------')
    for city in world:
        print('{:19}{}'.format(city[0], city[1]))


def get_cityno(world,city_in):
    """
    Given a world and a city within it, find the numerical index of 
    that city in the world.
    
    :param world: a list of cities
    :param city: a city
    """
    cityno = 0
    
    for i, city in enumerate(world):
        if city_in[0] == city[0]:
            cityno = i
            
    return cityno

def is_connected(world,city1,city2):
    """
    Given a world and two cities within it, determines whether the
    two cities are directly connected in the network.
    
    :param world: a list of cities
    :param city1: a city
    :param city2: another city
    """
    
    return get_cityno(world,city1) in city2[2]

def reset_world(world):
    """
    Resets a given world to the state where all cities are lost.
    
    :param world: a list of cities
    """
    
    for city in world:
        city[1] = False
    world[0][1] = True



#### That's the end of the stuff provided for you.
#### Put *your* code after this comment.
def regain(world, cityno):
    """
    Changes the 'regained' flag of the city in the supplied world with the 
    index cityno to True, so that the city is regained.
    
    :param world: a list of cities.
    :param cityno: the number (index) of a city in the world.
    
    :return: returns nothing.
    """
    world[cityno][1] = True

def lose(world, cityno):
    """
    Changes the 'regained' flag of the city in the supplied world with the 
    index cityno to False, so that the city is lost.
    
    :param world: a list of cities.
    :param cityno: the number (index) of a city in the world.
    
    :return: returns nothing.
    """
    world[cityno][1] = False

def get_connected_city(world,old_city):
    """
    Get a city that is connected to old_city according to the world network.
    
    :param world: a list of cities.
    :param old_city: the city in world for which to find a neighbouring city.
    
    :return: a city neighbouring old_city.
    """
    cityno = get_cityno(world,old_city)
    connected = world[cityno][2][:]
    connected.remove(cityno)
    
    return world[connected[numpy.random.randint(len(connected))]]

def sim_step(world, p_regain, p_lose):
    """
    A routine that takes a step of a simulation of an operation to regain a 
    collection of cities constituting the "world", depending on certain 
    probabilities of regaining a city (p_regain) and losing a city (p_lose) on
    each step of the simulation.
    
    If a given city is lost, it is regained with probability p_regain, but if 
    not, then with a probability p_lose a neighbouring city will be lost.
    
    :param world: a list of cities.
    :param p_regain: the probability of regaining a city that is lost.
    :param p_lose: the probability of losing a city that neighbours a lost 
     city.
    
    :return: returns nothing.
    """
    for city in world:
        if not city[1] and numpy.random.rand() < p_regain:
            city[1] = True
        if not city[1] and numpy.random.rand() < p_lose:
                get_connected_city(world,city)[1] = False
    world[0][1] = True

def step_draw(world,p_regain, p_lose, table):
    """
    A utitlity function that will take a step of the simulation and either 
    display the result as a printed table or as a plotted graph depending on 
    the value of a boolean flag 'table'.
    
    :param world: a list of cities.
    :param p_regain: the probability of regaining a city that is lost.
    :param p_lose: the probability of losing a city that neighbours a lost 
     city.
    :param table: a boolean flag that determines wether a table or graph will 
    be shown.
    
    :return: returns nothing.
    """
    sim_step(world,p_regain,p_lose)
    if picture:
        draw_world(world)
    else:
        print_world(world)

def is_world_saved(world):
    """
    Checks whether the world has been saved (all of the cities have been 
    regained.)
    
    :param world: a list of cities.
    
    :return: returns a boolean value indicating whether or not the world is 
     saved.
    """
    for city in world:
        if not city[1]:
            return False
    return True

def time_to_save_world(world,p_regain,p_lose):
    """
    Runs a full simulation of the operation on a given world for particular
    probabilities of regaining and losing cities and returns the number of 
    steps taken to reach a state where the world is saved.
    
    :param world: a list of cities.
    :param p_regain: the probability of regaining a city that is lost.
    :param p_lose: the probability of losing a city that neighbours a lost 
     city.
    
    :return: The number of steps taken to save the world.
    """
    reset_world(world)
    
    counter = 1
    while not is_world_saved(world):
        sim_step(world, p_regain, p_lose)
        counter += 1
    
    return counter

def save_world_many_times(world,n,p_regain,p_lose):
    """
    Runs n full simulations of the operation on a given world for particular
    probabilities of regaining and losing cities and returns a list containing 
    the number of steps each run of the simulation takes to reach a state where
    the world is saved.
    
    :param world: a list of cities.
    :param n: the number of times to run the simulation.
    :param p_regain: the probability of regaining a city that is lost.
    :param p_lose: the probability of losing a city that neighbours a lost 
     city.
    
    :return: A list of the number of steps taken to save the world for each of 
     n runs of the simulation.
    """
    times = []
    
    for i in range(n):
        times.append(time_to_save_world(world,p_regain,p_lose))
    
    return times

my_world = set_up_cities()
## QUESTION 1 ##
print('Question 1:')
# Fix the value of p_lose at zero. 
# How does varying the value of p_regain affect the time to save the world?
runs = 100

times = []
p_lose = 0
probs = list(numpy.arange(0.1,1,0.1))

for p_regain in probs:
#    print('running',p_regain)
    times.append(numpy.mean(save_world_many_times(my_world,runs,p_regain,p_lose)))

plt.plot(probs,times)
plt.title('Number of Moves to Take Back the World for p_lose = 0.0')
plt.xlabel('p_regain')
plt.savefig('p_lose-0.0.png')
plt.show()
plt.clf()
# As the plot and the following data show, doubling the probability of 
# regaining a city roughly reduces the number of steps to save the world 
# approximately a factor of two.
print('Steps for p_regain=0.1 =',times[0])
print('Steps for p_regain=0.2 =',times[1])
print('Steps for p_regain=0.4 =',times[3])
print('Steps for p_regain=0.8 =',times[7])

# Result for a sample run:
# Steps for p_regain=0.1 = 33.58
# Steps for p_regain=0.2 = 16.43
# Steps for p_regain=0.4 = 8.09
# Steps for p_regain=0.8 = 3.59


## QUESTION 2 ##
print('\nQuestion 2:')
# Fix the value of p_lose at 0.1. 
# How does varying the value of p_regain affect the time to save the world?
times = []
p_lose = 0.1
probs = list(numpy.arange(0.1,1,0.1))

for p_regain in probs:
#    print('running',p_regain)
    times.append(numpy.mean(save_world_many_times(my_world,runs,p_regain,p_lose)))

plt.plot(probs,times)
plt.title('Number of Moves to Take Back the World for p_lose = 0.1')
plt.xlabel('p_regain')
plt.savefig('p_lose-0.1.png')
plt.show()
plt.clf()
# As the plot and the following data show, in this case increasing the 
# probability of leads to a steeper drop in the number of steps to save the 
# world, now doubling the probability of regaining a city roughly reduces the 
# number of steps to save the world by roughly a factor of three.
print('Steps for p_regain=0.1 =',times[0])
print('Steps for p_regain=0.2 =',times[1])
print('Steps for p_regain=0.4 =',times[3])
print('Steps for p_regain=0.8 =',times[7])

# Result for a sample run:
# Steps for p_regain=0.1 = 55.18
# Steps for p_regain=0.2 = 19.32
# Steps for p_regain=0.4 = 8.41
# Steps for p_regain=0.8 = 3.78


## QUESTION 3 ##
print('\nQuestion 3:')
# Fix the value of p_regain at 0.5. 
# How does varying the value of p_lose affect the time to save the world?
times = []
p_regain = 0.5
probs = list(numpy.round(numpy.arange(0.1,0.9,0.1),1))

for p_lose in probs:
#    print('running',p_lose)
    times.append(numpy.mean(save_world_many_times(my_world,runs,p_regain,p_lose)))

plt.plot(probs,times)
plt.title('Number of Moves to Take Back the World for p_regain = 0.5')
plt.xlabel('p_lose')
plt.savefig('p_regain-0.5.png')
plt.show()
plt.clf()

# As the plot and the following data show, here the relationship  between the
# probability of losing a city and the number of steps taken to save the world 
# is closer to exponential, with the number of steps increasing exponentially 
# with the probability of losing a city on a given step.
print('Steps for p_lose=0.1 =',times[0])
print('Steps for p_lose=0.2 =',times[1])
print('Steps for p_lose=0.4 =',times[3])
print('Steps for p_lose=0.8 =',times[7])

# Result for a sample run:
# Steps for p_lose=0.1 = 6.56
# Steps for p_lose=0.2 = 6.72
# Steps for p_lose=0.4 = 7.87
# Steps for p_lose=0.8 = 8.59

## QUESTION 4 ##
print('\nQuestion 4:')
# Pick three pairs of p_regain and p_lose values that you think are 
# interesting. Run 500 simulations for them (e.g, 
# save_world_many_times(world, 500, your_value, your_value). 
# What does the distribution of times to save the world look like? 
# If you’ve taken a stats course: is it normal (Gaussian)? 
# (If you haven’t taken stats, just ignore that question).

# I'm generating 500 points sampled from a Gaussian distribution for 
# comparison with the data generated in the three cases I consider.
import scipy.stats as stats
gaussian_data = numpy.random.normal(10,1,500)
exponential_data = numpy.random.exponential(1,500)

runs = 500
p_regain = 0.5
p_lose = 0.9
#matplotlib.rcParams.update({'font.size': 14})
#plt.figure(num=None, figsize=(8, 6), dpi=180, facecolor='w', edgecolor='k')
data = save_world_many_times(my_world,runs,p_regain,p_lose)
plt.hist(data)
plt.xlabel('Steps to Save the World')
plt.ylabel('Number of Runs')
plt.savefig('histogram-0.5-0.5.png')
plt.show()
plt.clf()
# In this case the simulation most commonly completes in about 9 runs, but the 
# distribution is skewed to the left (as shown by a positive skewness), with 
# it being more likely to save the world in more than 9 steps than fewer. 
# Since this distribution also exhibits with a heavy right tail (as shown by 
# the large kurtosis), it is certainly not a  Gaussian distribution.
print('Sample Mean = ',numpy.mean(data))
print('Sample Median = ',numpy.median(data))
print('Gaussian skewness =',stats.skew(gaussian_data))
print('Sample skewness =',stats.skew(data))
print('Gaussian kurtosis =',stats.kurtosis(gaussian_data))
print('Sample kurtosis =',stats.kurtosis(data))

# Result of a sample run:
# Sample Mean =  9.42
# Sample Median =  9.0
# Gaussian skewness = -0.06084535123423136
# Sample skewness = 1.4326716749919048
# Gaussian kurtosis = -0.3264417578118701
# Sample kurtosis = 3.589710763042145

p_regain = 0.1
p_lose = 0.3
#matplotlib.rcParams.update({'font.size': 14})
#plt.figure(num=None, figsize=(8, 6), dpi=180, facecolor='w', edgecolor='k')
data = save_world_many_times(my_world,runs,p_regain,p_lose)
plt.hist(data)
plt.xlabel('Steps to Save the World')
plt.ylabel('Number of Runs')
plt.savefig('histogram-0.1-0.3.png')
plt.show()
plt.clf()
# In this case the data is heavily skewed to the right, with a sharp drop from 
# the median value around 500. The distribution resembles an exponential 
# distribution, so is clearly not Gaussian. The following data bears out this
# apparent similarity in that the data is skewed ( positive skewness different 
# from zero) and has a tail heaviness (kurtosis greater than zero), that is 
# similar to the exponential distribution,
print('Sample Mean = ',numpy.mean(data))
print('Sample Median = ',numpy.median(data))
print('Gaussian skewness =',stats.skew(gaussian_data))
print('Exponential skewness =',stats.skew(exponential_data))
print('Sample skewness =',stats.skew(data))
print('Gaussian kurtosis =',stats.kurtosis(gaussian_data))
print('Exponential kurtosis =',stats.kurtosis(exponential_data))
print('Sample kurtosis =',stats.kurtosis(data))

# Result of a sample run:
# Sample Mean =  930.028
# Sample Median =  663.0
# Gaussian skewness = -0.06084535123423136
# Exponential skewness = 2.2628429036425284
# Sample skewness = 2.3446986659745854
# Gaussian kurtosis = -0.3264417578118701
# Exponential kurtosis = 10.378656892756853
# Sample kurtosis = 7.631408116579834

runs = 500
p_regain = 0.95
p_lose = 0.1
#matplotlib.rcParams.update({'font.size': 14})
#plt.figure(num=None, figsize=(8, 6), dpi=180, facecolor='w', edgecolor='k')
data = save_world_many_times(my_world,runs,p_regain,p_lose)
plt.hist(data)
plt.xlabel('Steps to Save the World')
plt.ylabel('Number of Runs')
plt.savefig('histogram-0.95-0.1.png')
plt.show()
plt.clf()

# In this case the number of runs is almost always 2 or 3, with a slight 
# preference for 3. Thus, there is a slight skew to the right, 
# but more interestingly, there is very little variation in the data, with no 
# outliers (low frequency values significantly different from the other values 
# in the distribution). This gives rise to a negative kurtosis, which means 
# that there are fewer outliers than the Gaussian distriubtion, so once again  
# the distribution is not Gaussian.
print('Sample Mean = ',numpy.mean(data))
print('Sample Median = ',numpy.median(data))
print('Gaussian skewness =',stats.skew(gaussian_data))
print('Sample skewness =',stats.skew(data))
print('Gaussian kurtosis =',stats.kurtosis(gaussian_data))
print('Sample kurtosis =',stats.kurtosis(data))

# Result of a sample run:
# Sample Mean =  2.56
# Sample Median =  3.0
# Gaussian skewness = -0.06084535123423136
# Sample skewness = 0.4077286127022732
# Gaussian kurtosis = -0.3264417578118701
# Sample kurtosis = -0.7736447520184546


## QUESTION 5 ##
print('\nQuestion 5:')
# Suppose that you have received some intel on the enemy network and you want 
# to use this to plan your operation. This city network is returned by the 
# get_real_world() function (already written for you). Also suppose that the 
# time step is counted in months. If the value of p_lose is 0.9 (90% probably 
# of losing a city in a given month), then approximately what probability of 
# regaining a city (value of p_regain) must we guarantee to save the world 
# within 2 years? Justify your answer (pictures may help)

# Running the following code we obtain a range of histograms, which show that
# below p_regain = 0.5, we see runs over 24 months. Thus, we will focus on 
# p_regain = 0.5 and above to see which reliably gives no runs over 24.
my_world = get_real_world()

runs = 100
p_lose = 0.9
for i, p_regain in enumerate(probs[2:]):
    plt.clf()
    plt.hist(save_world_many_times(my_world,runs,p_regain,p_lose))
    plt.title('Run p_lose = 0.9, p_regain = '+str(p_regain))
    plt.savefig('histogram'+str(i)+'.png')
    plt.show()

# Running the following code we find that p_regain = 0.5 definitely does not 
# guarantee saving the world in 24 months, but that p_regain = 0.6 is quite 
# close though still generates some runs over 24 months. It is possible to 
# miss this using only 10 000 runs, which is why I've increased it to 40 000.
# p_regain = 0.6 is still a reasonable answer, however, because the probability
# of having a run over 24 months is a small fraction of a percent, which is 
# extremely rare. Accordingly, it would be reasonable to inform command that a
# probability of regaining a city of 0.6 is sufficient to guarantee victory 
# within 24 months, with a vanishingly small chance of error. A stronger 
# guarantee, if needed, would require p_regain = 0.7 at the level of one 
# significant figure. Thus, both 0.6 and 0.7 can be acceptable answers here.
runs = 40000
probs = [0.5,0.6,0.7]
p_lose = 0.9
for p_regain in probs:
    data = save_world_many_times(my_world,runs,p_regain,p_lose)
    plt.hist(data)
    plt.xlabel('Steps to Save the World')
    plt.ylabel('Number of Runs')
    plt.savefig('histogram'+str(p_regain)+'.png')
    plt.show()
    print('Max time to save world for p_regain = '+str(p_regain)+':',numpy.max(data))
    print('Proportion of runs above 24 months =',len([x for x in data if x > 24])/runs)

# Result of a sample run:
# Max time to save world for p_regain = 0.5: 52
# Proportion of runs above 24 months = 0.010325
# Max time to save world for p_regain = 0.6: 26
# Proportion of runs above 24 months = 2.5e-05
# Max time to save world for p_regain = 0.7: 16
# Proportion of runs above 24 months = 0.0