## CS 2120 Assignment #2 -- Take Back Our World!
## Name: Brett Petch
## Student number: 251038051

import numpy as np
import numpy
import matplotlib.pyplot as plt


#### This stuff you just have to use, you're not expected to know how it works.
#### You just need to read the plain English function headers.
#### If you want to learn more, by all means follow along (and ask questions if
#### you're curious). But you certainly don't have to.


def make_city(name, neighbours):
    """
    Create a city (implemented as a list).
    
    :param name: String containing the city name
    :param neighbours: The city's row from an adjacency matrix.
    
    :return: [name, Infection status, List of neighbours]
    """

    return [name, False, list(numpy.where(neighbours == 1)[0])]


def make_connections(n, density=0.35):
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
    a = numpy.int32(numpy.triu((numpy.random.random_sample(size=(n, n)) < density)))
    G = networkx.from_numpy_matrix(a)

    # If the network is 'not connected' (i.e., there are isolated nodes)
    # generate a new one. Keep doing this until we get a connected one.
    # Yes, there are more elegant ways to do this, but I'm demonstrating
    # while loops!
    while not networkx.is_connected(G):
        a = numpy.int32(numpy.triu((numpy.random.random_sample(size=(n, n)) < density)))
        G = networkx.from_numpy_matrix(a)

    # Cities should be connected to themselves.
    numpy.fill_diagonal(a, 1)

    return a + numpy.triu(a, 1).T


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
        city_list += [make_city(n[1], con[n[0]])]

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

    redlist = []
    greenlist = []

    plt.clf()
    plt.clf()
    # plt.figure(num=None, figsize=(8, 6), dpi=180, facecolor='w', edgecolor='k')

    # For each city, add a node to the graph and figure out if
    # the node should be red (lost) or green (regained)
    for city in enumerate(world):
        if city[1][1] == False:
            G.add_node(city[0])
            redlist.append(city[0])
        else:
            G.add_node(city[0], node_color='g')
            greenlist.append(city[0])

        for neighbour in city[1][2]:
            G.add_edge(city[0], neighbour)

    # Lay out the nodes of the graph
    position = networkx.circular_layout(G)

    # Draw the nodes
    networkx.draw_networkx_nodes(G, position, nodelist=redlist, node_color="r")
    networkx.draw_networkx_nodes(G, position, nodelist=greenlist, node_color="g")

    # Draw the edges and labels
    networkx.draw_networkx_edges(G, position)
    networkx.draw_networkx_labels(G, position)

    # Force Python to display the updated graph
    plt.legend(['Lost', 'Regained'])
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


def get_cityno(world, city_in):
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


def is_connected(world, city1, city2):
    """
    Given a world and two cities within it, determines whether the
    two cities are directly connected in the network.
    
    :param world: a list of cities
    :param city1: a city
    :param city2: another city
    """

    return get_cityno(world, city1) in city2[2]


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


def lose(world, cityno):
    """
    :param world: accepts a list of cities.
    :param cityno: accepts an integer representing a city.
    Sets a city to be lost.
    """
    world[cityno][1] = False


def regain(world, cityno):
    """
    :param world:
    :param cityno:
    :return: Sets city to be regained.
    """
    world[cityno][1] = True


def sim_step(world, p_regain, p_lose):
    """
    Runs one time step of the simulation. If a city is lost, a random number generator picks a number between 0,1.
    If it is less than p_lose, then one randomly selected neighbour is lost. Random number generator is repeated
    and if it is less than p_regain then the city itself gets regained.

    :param world: Accepts list of cities
    :param p_regain: Accepts a float to dictate the percentage chance of regaining a city.
    :param p_lose: Accepts a float to dictate the percentange change of losing city.
    """
    for n, city in enumerate(world):
        if city[1] is False and numpy.random.rand() < p_regain:
            city[1] = True
        if city[1] is False and numpy.random.rand() < p_lose:
            is_connected = numpy.random.randint(0, len(city[2]))
            lose(world, city[2][is_connected])
    regain(world, 0)


def is_world_saved(world):
    """
    Determines if all cities in the world are regained. The first element of each city's list(regained) is looped over
    to see if the regained flag is raised.
    :param world: Accepts list of cities
    :return: returns if world has been regained or not
    """
    regained = True  # variable to be returned at the end to state if all cities are infected
    for n, city in enumerate(world):  # indexes the cities and loops over all of them
        if not world[n][1]:  # checks to see if the city's inflection flag is raised or not
            regained = False  # if not raised then it sets the variable is_it_the_end to False
    return regained


def time_to_save_world(world, p_regain, p_lose):
    """
    Runs is_world_saved function to determine if all cities are regained and if it returns False,
    it runs one time step of the sim_step function. Then the function checks if all cities are regained through
    is_is_world_saved function after each time step until is_is_world_saved function returns True.
    :param world:
    :param p_regain:
    :param p_lose:
    :return:
    """
    regained_counter = 0
    reset_world(world)
    while not is_world_saved(world):
        sim_step(world, p_regain, p_lose)
        regained_counter += 1
    return regained_counter


def save_world_many_times(world, n, p_regain, p_lose):
    """
    Creates an empty list and runs time_to_save_world n number of times. After each time the function returns
    how long it took to end the world and adds it to the list.
    :param world: accepts a list of cities
    :param n: amount of times for trial to be run
    :param p_regain: percentage chance of regaining city
    :param p_lose: percentage chance of losing city.
    :return:
    """
    list_of_results = []
    ntimes = 0
    while ntimes < n:
        list_of_results.append(time_to_save_world(world, p_regain, p_lose))
        ntimes += 1
    return list_of_results


my_world = set_up_cities()

ttl = save_world_many_times(my_world, 500, 0.9, 0.1)
# save_world_many_times(my_world, 500, 0.9, 0)  # stored into a variable with chosen numbers to plot histogram
plt.hist(ttl)                                       # make a histogram
plt.show()

print(time_to_save_world(my_world, 0.5, 0))      # Question 1
print(time_to_save_world(my_world, 0.6, 0.1))    # Question 2
print(time_to_save_world(my_world, 0.5, 0.2))    # Question 3

# Question 4

ttl41 = save_world_many_times(my_world, 500, 0.7, 0.1)     # Dataset 1 (4.1)
ttl42 = save_world_many_times(my_world, 500, 0.9, 0.3)     # Dataset 2 (4.2)
ttl43 = save_world_many_times(my_world, 500, 0.8, 0.2)     # Dataset 3 (4.3)

plt.hist(ttl41)
plt.show()

plt.hist(ttl42)
plt.show()

plt.hist(ttl43)
plt.show()

# Question 5:

ttl5 = save_world_many_times(my_world, 10000, 0.7, 0.9)
plt.hist(ttl5)
plt.show()
