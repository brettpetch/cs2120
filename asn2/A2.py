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
    Sets a city to not be lost.
    """
    world[cityno][1] = False


def regain(world, cityno):
    """
    :param world:
    :param cityno:
    :return: Sets city to be lost.
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
        if world[n][1] == True and np.random.rand() < p_regain:
            x = len(world[n][2])
            city_lost = np.random.randint(0, x)
            regain(world, world[n][2][city_lost])
        if world[n][1] == True and np.random.rand() < p_lose:
            lose(world, n)
    world[0][1] = True


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
ttl = save_world_many_times(my_world, 500, 0.7, 0.1)
print(ttl)
plt.hist(ttl)
plt.show()

"""
Analysis:

1. Fix the value of p_lose at zero. How does varying the value of p_regain affect the time to save the world? :var 
p_lose = 0 :var p_regain = n If p_lose is set to zero, p_regain affects the time to save the world positively, 
as there is less of a chance for the world to become more infected. p_lose set to 0 results in most results being 
between 12-23 tries, with a peak at 20 times. 
        
        Data From: # ttl = save_world_many_times(my_world, 100, 0.5, 0) #1 
            Dataset 1.1: 
                [18, 26, 15, 22, 31, 17, 20, 18, 35, 11, 11, 14, 21, 15, 18, 14, 22, 19, 15, 25, 13, 15, 16, 14,  16, 
                19, 12, 46, 12, 30, 5, 20, 21, 21, 30, 19, 17, 28, 20, 16, 31, 26, 15, 14, 22, 19, 14, 10, 8, 24, 20, 
                20, 24, 31, 24, 16 ,19, 38, 18, 48, 10, 17, 15, 10, 1 5, 16, 13, 14, 13, 42, 13, 24, 18, 28, 33, 24, 
                9, 19, 18, 18, 18, 12, 15, 20, 21, 17, 18, 18, 13, 34, 14, 29, 25, 17, 36, 22, 22 , 12, 20, 14] 


2. Fix the value of p_lose at 0.1. How does varying the value of p_regain affect the time to save the world?
    :var p_lose = 0.1
    :var p_regain = n
    If p_regain is changed to a higher value with p_lose set to 0.1, it is more likely to run x amount of times.
    
        Data From: # ttl = save_world_many_times(my_world, 100, 0.6, 0.1) #2 
            Dataset 2.1: 
                [94, 60, 19, 21, 143, 159, 47, 28, 35, 27, 230, 46, 24, 132, 76, 16, 29, 81, 21, 53, 90, 84, 71, 61, 
                120, 30, 49, 110, 18, 71, 3 3, 215, 32, 62, 54, 99, 38, 99, 49, 19, 70, 43, 41, 54, 48, 58, 40, 43, 
                79, 54, 21, 57, 10, 107, 30, 24, 10, 41, 25, 44, 25, 16, 22, 17, 58, 47, 52, 85, 127, 41, 31, 29, 63, 
                57, 61, 46, 33, 57, 15, 61, 46, 42, 44, 64, 46, 16, 28, 107, 52, 17, 58, 68, 71, 1 9, 26, 16, 90, 11, 
                91, 31] 


3. Fix the value of p_regain at 0.5. How does varying the value of p_lose affect the time to save the world? 
    Fixing p_regain to 0.5 results in a slower time in regaining world, if p_lose is higher than p_regain, 
    then it takes a very long time for world to be regained. 

    Data From: # ttl = save_world_many_times(my_world, 100, 0.5, 0.2) #3 
        Dataset 3.1: 
            [2228, 2254, 3272, 6454, 576, 3022, 735, 969, 7543, 13015, 6648, 1856, 6927, 6514, 122, 17313, 3205, 
            3912, 2315, 4577, 917, 898, 4622, 8870, 709, 4574, 450, 8303, 1253, 11650, 1196, 755, 3940, 2161, 5664, 
            1213, 13763, 9482, 2045, 4255, 5998, 16264, 6874, 3 660, 2484, 816, 2148, 782, 2660, 10751, 1119, 2819, 
            1611, 5352, 1343, 2429, 2993, 4257, 3839, 4700, 2982, 1174, 8202, 486, 813, 8300, 4982, 1404, 10331, 
            2400, 2647, 4613, 468, 11860, 2294, 173, 1495, 437, 11055, 427, 8796, 4047, 1366, 8213, 5565, 175, 6929 , 
            1706, 2484, 8311, 2891, 9864, 2180, 292, 1669, 6854, 1041, 2575, 2810, 9809] 

4. Pick three pairs of p_regain and p_lose values that you think are interesting. Run 500 simulations for them (e.g, 
    end_world_many_times(500, your_value, your_value). What does the distribution of times to the end of the world look 
    like? If you’ve taken a stats course: is it normal (Gaussian)? (If you haven’t taken stats, just ignore that 
    question). 
    The simulations seem to have a range of how many steps it takes to complete is based on the 
       
    Data from: 
        # ttl = save_world_many_times(my_world, 500, 0.7, 0.1)     # Dataset 1 (4.1) 
        # ttl = save_world_many_times(my_world, 500, 0.9, 0.3)     # Dataset 2 (4.2) 
        # ttl = save_world_many_times(my_world, 500, 0.8, 0.2)     # Dataset 3 (4.3) 

        Dataset 1: 
            [20, 54, 64, 142, 18, 115, 53, 33, 30, 77, 32, 14, 70, 33, 38, 102, 55, 78, 18, 53, 17, 34, 43, 110, 13, 
            48, 30, 43, 73, 115, 45 , 16, 40, 56, 11, 117, 98, 59, 65, 92, 29, 120, 21, 76, 219, 61, 23, 38, 201, 
            120, 61, 22, 112, 43, 10, 54, 34, 51, 13, 17, 133, 13, 48, 63, 65, 99, 76, 58, 79, 46, 21, 54, 71, 26, 
            35, 14, 43, 16, 175, 46, 25, 61, 32, 54, 39, 44, 58, 29, 47, 89, 54, 27, 11 8, 73, 30, 33, 43, 128, 31, 
            42, 70, 184, 55, 73, 34, 62, 49, 34, 15, 52, 23, 88, 23, 25, 47, 29, 14, 10, 111, 18, 35, 76, 13, 64 , 
            27, 66, 58, 86, 66, 21, 40, 17, 25, 44, 75, 18, 34, 21, 50, 43, 32, 101, 54, 86, 22, 63, 47, 31, 10, 34, 
            25, 16, 30, 28, 20, 1 07, 113, 41, 57, 53, 35, 30, 28, 66, 22, 61, 51, 68, 23, 26, 34, 92, 41, 21, 6, 16, 
            56, 40, 49, 36, 40, 30, 86, 39, 31, 41, 73, 60, 74, 14, 48, 42, 44, 34, 48, 24, 43, 108, 46, 14, 39, 23, 
            32, 16, 18, 30, 30, 99, 225, 23, 62, 28, 31, 65, 32, 79, 118, 48, 1 6, 51, 46, 22, 37, 119, 69, 82, 15, 
            21, 25, 38, 59, 21, 134, 23, 55, 53, 24, 50, 29, 20, 121, 11, 20, 74, 45, 17, 102, 75, 109, 53, 32, 26, 
            44, 161, 102, 103, 78, 66, 15, 30, 36, 52, 94, 43, 24, 23, 53, 50, 39, 50, 39, 29, 108, 105, 14, 56, 83, 
            78, 109, 19 0, 16, 96, 29, 38, 16, 67, 72, 128, 12, 41, 177, 46, 80, 26, 79, 115, 45, 37, 25, 24, 161, 
            109, 44, 58, 53, 44, 112, 59, 28, 39, 71, 35, 15, 80, 13, 37, 23, 66, 26, 34, 203, 29, 14, 36, 23, 78, 
            67, 85, 212, 133, 82, 52, 27, 38, 60, 43, 19, 22, 130, 140, 35 , 34, 14, 51, 51, 52, 80, 163, 33, 46, 91, 
            40, 37, 91, 21, 28, 58, 25, 108, 16, 203, 58, 31, 46, 119, 389, 36, 40, 163, 14, 29, 34, 187, 57, 45, 40, 
            30, 51, 22, 44, 149, 47, 25, 65, 41, 31, 177, 154, 12, 214, 33, 22, 20, 50, 89, 30, 34, 68, 61, 43, 106, 
            22 , 90, 18, 161, 163, 95, 168, 30, 195, 93, 29, 152, 36, 33, 24, 80, 34, 73, 24, 12, 18, 68, 21, 99, 91, 
            91, 71, 72, 84, 61, 26, 1 8, 53, 20, 60, 81, 164, 85, 25, 37, 48, 66, 38, 114, 110, 40, 75, 28, 10, 26, 
            19, 202, 40, 48, 96, 26, 82, 20, 43, 79, 40, 19, 1 00, 31, 47, 30, 34, 54, 67, 25, 12, 62, 63, 114, 27, 
            25, 53, 45, 30, 21, 158, 33, 42, 32, 107, 11, 110, 66, 74, 51, 11, 50, 40, 51, 17, 76, 16, 85, 67] 
                    
        Dataset 2: 
            [479, 711, 1857, 3873, 1321, 526, 1901, 1460, 530, 710, 292, 690, 1892, 553, 3330, 2030, 2466, 1692, 
            1123, 530, 634, 1660, 1748, 238, 97, 2429, 76, 817, 806, 230, 2088, 2546, 1096, 1216, 135, 816, 175, 22, 
            3516, 164, 866, 248, 140, 114, 1529, 1060, 352, 13 61, 386, 99, 1199, 473, 506, 1718, 569, 1549, 589, 
            3074, 545, 313, 2326, 2901, 505, 1241, 2017, 79, 2168, 708, 651, 1662, 1067, 195, 79, 1980, 202, 2307, 
            487, 45, 1589, 282, 5866, 395, 2923, 1348, 1763, 2166, 1047, 67, 1053, 113, 780, 59, 1945, 192, 620, 
            2 195, 355, 1668, 1608, 750, 2274, 2266, 847, 96, 178, 1992, 4016, 193, 514, 204, 3748, 44, 206, 477, 
            153, 1208, 555, 2213, 2751, 2839, 1548, 1864, 5547, 4285, 422, 1557, 3122, 643, 1561, 863, 146, 144, 484, 
            271, 2092, 579, 1049, 4989, 4052, 1203, 5224, 174, 947, 560, 243, 2329, 810, 89, 3038, 1216, 1744, 1887, 
            744, 625, 686, 2407, 393, 427, 1198, 1509, 696, 1658, 1415, 847, 1213, 19 0, 418, 50, 230, 220, 3695, 
            5097, 195, 1482, 283, 619, 2551, 192, 532, 860, 2043, 398, 826, 153, 1908, 6861, 985, 552, 569, 294, 
            1364, 108, 2936, 573, 1737, 158, 3803, 668, 62, 2583, 391, 354, 144, 2182, 328, 635, 1075, 2599, 201, 
            840, 154, 4038, 907, 901, 7937, 1246, 4466, 606, 227, 1467, 657, 54, 848, 473, 1404, 982, 2489, 631, 
            2381, 1189, 1203, 81, 4910, 3437, 19, 3151, 4445, 12 31, 415, 756, 142, 2028, 1166, 439, 4788, 648, 990, 
            957, 3147, 1796, 439, 1305, 1473, 29, 626, 324, 2153, 142, 2025, 3018, 1559, 1260, 3008, 406, 357, 101, 
            298, 699, 328, 156, 3058, 80, 1637, 930, 4890, 779, 1635, 450, 3432, 300, 4317, 486, 664, 202, 81, 1 78, 
            357, 3404, 641, 1391, 86, 1329, 967, 1454, 1164, 361, 3159, 1684, 701, 1105, 1652, 26, 3149, 2018, 473, 
            2369, 1040, 541, 381 , 463, 1091, 488, 220, 6356, 3931, 812, 1516, 782, 1459, 220, 684, 1171, 707, 6149, 
            4981, 1024, 229, 1104, 1011, 877, 4330, 196, 531, 665, 1292, 362, 2309, 4137, 955, 731, 52, 1967, 213, 
            3975, 5627, 377, 1168, 1334, 971, 1409, 837, 501, 65, 1500, 1554, 737 , 150, 835, 2419, 2051, 423, 498, 
            454, 1734, 4490, 1958, 3454, 1934, 2410, 48, 7020, 2475, 1008, 35, 654, 233, 433, 413, 273, 68 , 970, 26, 
            1643, 2406, 748, 3483, 449, 2011, 3261, 524, 1651, 580, 4187, 7502, 2191, 1066, 7140, 781, 14, 1625, 584, 
            483, 597, 6 15, 1342, 880, 2370, 2232, 1429, 282, 2606, 5291, 472, 716, 339, 587, 2176, 1614, 5319, 706, 
            1461, 337, 1525, 71, 2016, 3888, 30 95, 2723, 1037, 2707, 163, 632, 1127, 2820, 581, 226, 1187, 2192, 
            721, 1261, 1966, 214, 849, 221, 1697, 208, 4621, 159, 709, 740 , 1657, 986, 1262, 262, 76, 903, 433, 158, 
            1162, 1350, 1561, 418, 1776, 142, 8904, 1504, 448, 276, 1388, 1263, 582, 1417, 179, 4 46, 367, 946, 213, 
            301, 3479, 331, 1246, 106, 1461, 783, 2706, 415, 1750, 597, 77, 125, 639, 709, 2130, 3444, 185, 2450, 
            3947, 3 324, 1924, 2038] 
           
        Dataset 3: 
            [64, 244, 337, 64, 662, 74, 144, 28, 528, 156, 1101, 198, 253, 140, 359, 743, 102, 21, 426, 1091, 48, 
            905, 699, 235, 202, 563, 8 1, 137, 320, 2615, 25, 570, 21, 333, 133, 56, 439, 162, 30, 187, 945, 51, 24, 
            88, 639, 241, 297, 94, 466, 95, 317, 415, 576, 16, 144, 123, 52, 950, 527, 177, 573, 171, 162, 274, 1106, 
            21, 435, 243, 567, 395, 271, 33, 581, 146, 530, 467, 55, 110, 293, 762, 204, 435, 68, 42, 821, 64, 125, 
            319, 217, 53, 388, 60, 33, 24, 246, 1658, 620, 36, 266, 149, 405, 956, 86, 49, 88, 17, 50, 264, 546, 306, 
            463, 88, 1021, 161, 233, 1257, 279, 53, 95, 269, 149, 362, 359, 298, 371, 195, 267, 722, 691, 286, 764, 
            103, 126, 202, 750, 428, 130, 855, 162, 250, 169, 534, 210, 104, 570, 168, 450, 17, 233, 45, 252, 42, 
            528, 147, 86, 122, 619, 163, 497, 73, 10 2, 1321, 9, 476, 160, 57, 419, 57, 182, 34, 127, 482, 198, 601, 
            260, 859, 660, 754, 674, 17, 527, 186, 38, 472, 157, 226, 452, 4 6, 398, 112, 436, 90, 550, 2026, 718, 
            59, 28, 579, 64, 825, 320, 16, 627, 31, 148, 390, 414, 417, 73, 235, 426, 94, 249, 100, 11 2, 557, 248, 
            372, 1239, 46, 154, 65, 337, 427, 263, 507, 764, 323, 582, 24, 13, 254, 182, 646, 214, 100, 339, 67, 216, 
            180, 307, 62, 150, 110, 41, 265, 654, 121, 289, 622, 47, 908, 8, 288, 132, 219, 176, 26, 69, 97, 1170, 
            31, 434, 68, 58, 361, 992, 388, 20 6, 146, 228, 399, 43, 106, 531, 12, 123, 26, 926, 105, 697, 383, 501, 
            727, 19, 33, 183, 503, 15, 423, 515, 248, 27, 61, 297, 61, 544, 662, 26, 192, 103, 220, 83, 268, 300, 
            128, 108, 1697, 502, 68, 572, 204, 38, 378, 646, 623, 280, 489, 40, 829, 14, 187, 28 9, 586, 365, 655, 
            52, 311, 293, 142, 174, 1247, 151, 162, 154, 36, 39, 235, 33, 199, 314, 194, 1513, 844, 232, 233, 256, 
            218, 11 7, 69, 49, 354, 244, 183, 70, 299, 163, 68, 18, 48, 1373, 265, 24, 268, 190, 209, 263, 174, 94, 
            16, 105, 49, 375, 316, 203, 701, 143, 217, 9, 580, 1019, 289, 582, 969, 23, 363, 964, 819, 544, 738, 151, 
            221, 134, 44, 60, 33, 741, 218, 100, 151, 114, 226, 26 1, 315, 404, 46, 897, 66, 564, 188, 67, 290, 1683, 
            583, 98, 379, 143, 58, 169, 377, 285, 24, 136, 473, 800, 671, 468, 1490, 15, 356, 477, 57, 835, 90, 115, 
            55, 468, 356, 359, 288, 300, 375, 24, 223, 267, 199, 86, 915, 230, 47, 505, 574, 502, 79, 238, 109, 708, 
            225, 524, 72, 415, 37, 828, 297, 231, 155, 488, 177, 243, 272, 115, 402, 50, 111, 827, 801, 344, 108, 86, 
            77, 288, 469, 118 , 463, 731, 115, 270, 264, 483, 51, 126, 134, 185, 691, 739, 370, 186, 411, 285, 145] 


    I have not taken a stats course.
"""
