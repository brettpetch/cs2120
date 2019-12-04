## CS 2120 Assignment #2 -- Take Back Our World!
## Name: PLEASE FILL THIS IN
## Student number: SERIOUSLY


import numpy
import matplotlib.pyplot as plt

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
    # plt.figure(num=None, figsize=(8, 6), dpi=180, facecolor='w', edgecolor='k')
    
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
