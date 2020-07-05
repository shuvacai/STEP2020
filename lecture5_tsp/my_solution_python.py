import sys
import math
import time
import numpy as np
import multiprocessing
from multiprocessing import Pool
from multiprocessing import Process
from common import print_tour, read_input, format_tour
global cities

def distance(city1, city2): # Caculates distance between two points
    return np.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def total_distance(cities_order, dist):  # Calculates total distance for the given order
    distance = 0
    for i in range(len(cities_order)-2):
        distance += dist[i][i+1]
    distance += dist[len(cities_order)-1][0]
    return distance

def distance_matrix(cities):  # Calculates distance matrix
    n_cities = len(cities)
    dist = [[0] * n_cities for i in range(n_cities)]
    for i in range(n_cities):
        for j in range(i, n_cities):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    return dist


def calculate_swapping_cost(cities_order, i, j, dist): # Calculates cost (change in distance) of swapping two points
    n_cities = len(cities_order)
    p1, p2 = cities_order[i], cities_order[(i + 1) % n_cities]
    q1, q2 = cities_order[j], cities_order[(j + 1) % n_cities]
    dist_before = dist[p1][p2] + dist[q1][q2]
    dist_after = dist[p1][q1] + dist[p2][q2]
    return dist_after - dist_before

def swap_order(cities_order, i, j):  # Swaps order at the given two points
    tmp = cities_order[i+1:j+1]
    tmp.reverse()
    cities_order[i+1:j+1] = tmp
    return cities_order


def optimal_swap(cities_order, dist):  # Finds the best pair of points to swap for Opt2
    n_cities = len(cities_order)
    dist_diff_best = 0.0
    i_best, j_best = None, None
    for i in range(0, n_cities - 2): # Tests swapping for all possible combinations
        for j in range(i+2, n_cities):
            if i == 0 and j == n_cities -1:  # fix first and last point
                continue
            
            dist_diff = calculate_swapping_cost(cities_order, i, j, dist)
            
            if dist_diff < dist_diff_best:   # Updates the candidate points if the cost is smaller
                dist_diff_best = dist_diff
                i_opt, j_opt = i, j
    
    if dist_diff_best < 0.0:     # Swaps two points if the optimal order found is better than the original order
        new_order = swap_order(cities_order, i_opt, j_opt)
        return new_order
    else:
        return None

def twoOpt_local_solver(subset_cities):   # Opt2 method
    best_score = float('inf')
    best_order = []
    j = 0
    current_score = 0

    for i in range(1):   # Try with different initial order  // For large number of nodes, decrease this number
        cities_order = subset_cities

        while True:   # Swap two points until no improvement can be made
            j = j+1
            improved = optimal_swap(cities_order, dist)
            if not improved:
                break
            cities_order = improved
            current_score = total_distance(cities_order, dist)

        if current_score < best_score:
            best_order = cities_order
            best_score = current_score

    return best_order

def divide_quadrants(cities):   # Divides the cities into four quadrants based on their position
    n_cities = len(cities)
    x_list = []
    y_list = []
    global x_mean, y_mean
    for i in range(n_cities):
        x_list.append(cities[i][0])
        y_list.append(cities[i][1])

    x_mean = np.mean(x_list)
    y_mean = np.mean(y_list)

    first_quadrant = []
    second_quadrant = []
    third_quadrant = []
    forth_quadrant = []

    for i in range(n_cities):
        if(cities[i][1] >= y_mean):
            if(cities[i][0] < x_mean):
                first_quadrant.append(i)
            else:
                second_quadrant.append(i)
        else:
            if(cities[i][0]< x_mean):
                third_quadrant.append(i)
            else:
                forth_quadrant.append(i)
    return first_quadrant, second_quadrant, third_quadrant, forth_quadrant

def nearest_to_mean(route):  # Find the point that is the nearest to the center (mean position)
    min_dis = float('inf')
    nearest_to_mean = route[0]
    for i in range(len(route)):
        current_dis = distance(cities[i], (x_mean, y_mean))
        if current_dis < min_dis:
            min_dis = current_dis
            nearest_to_mean = i
    return nearest_to_mean

def join_routes(routes):  # Joins the optimal routes of the four quadrants
    nearest_to_mean_1 = nearest_to_mean(routes[0])
    nearest_to_mean_2 = nearest_to_mean(routes[1])
    nearest_to_mean_3 = nearest_to_mean(routes[2])
    nearest_to_mean_4 = nearest_to_mean(routes[3])
    
    final_route = routes[0][:nearest_to_mean_1] + routes[1][nearest_to_mean_2:] + routes[1][:nearest_to_mean_2] + routes[2][nearest_to_mean_3:] + routes[2][:nearest_to_mean_3] + routes[3][nearest_to_mean_4:] + routes[3][:nearest_to_mean_4] + routes[0][nearest_to_mean_1:]
    return final_route


def concat_maps(cities):  # Apply 2-Opt method for each quadrant while multiprocessing them

    first_quadrant, second_quadrant, third_quadrant, forth_quadrant = divide_quadrants(cities)
    
    with multiprocessing.Pool() as pool:
        pr1 = pool.apply_async(twoOpt_local_solver, (first_quadrant,))
        pr2 = pool.apply_async(twoOpt_local_solver, (second_quadrant,))
        pr3 = pool.apply_async(twoOpt_local_solver, (third_quadrant,))
        pr4 = pool.apply_async(twoOpt_local_solver, (forth_quadrant,))
        route1 = pr1.get()
        route2 = pr2.get()
        route3 = pr3.get()
        route4 = pr4.get()
        route_final = join_routes([route1, route2, route3, route4])
    return total_distance(route_final, dist)


         
if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input('input_{}.csv'.format(sys.argv[1]))
    dist = distance_matrix(cities)

    start = time.time()
    result = concat_maps(cities)
    end = time.time()
    
    print('2out distance: ', result)
    print('2opt time: ', (end-start)*1e6)

    with open(f'output_{sys.argv[1]}.csv', 'w') as f:
        f.write(format_tour(tour_improved) + '\n')