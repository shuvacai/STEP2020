import sys
import math
import time
import numpy as np

from common import print_tour, read_input, format_tour

def distance(city1, city2): # Caculates distance between two points
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def total_distance(cities_order, dist):  # Calculates total distance for the given order
    idx_from = np.array(cities_order)
    idx_to = np.array(cities_order[1:])
    idx_to = np.append(idx_to,cities_order[0])
    distance = 0
    for i,j in zip(idx_from, idx_to):
        distance += dist[i][j]
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


def solver_greedy(cities):   # Greedy method
    n_cities = len(cities)
         
    current_city = 0
    unvisited = set(range(1, n_cities))
    tour = [current_city]
    while unvisited:
        next_city = min(unvisited, key=lambda city: dist[current_city][city])
        unvisited.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour


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

def two_opt_solve(cities):   # Opt2 method
    best_score = float('inf')
    best_order = []
    j = 0

    for i in range(1):   # Try with different initial order
        print(i)
        cities_order = list(np.random.permutation(len(cities)))

        while True:   # Swap two points until no improvement can be made
            j = j+1
            print(j)
            improved = optimal_swap(cities_order, dist)
            if not improved:
                break
            cities_order = improved
            current_score = total_distance(cities_order, dist)

        if current_score < best_score:
            best_order = cities_order
            best_score = current_score

    
    return best_order



         
if __name__ == '__main__':
    assert len(sys.argv) > 1
    input_data = read_input('input_{}.csv'.format(sys.argv[1]))
    dist = distance_matrix(input_data)

    start = time.time()
    tour = solver_greedy(input_data)
    end = time.time()
    print('Greedy distance: ', total_distance(tour, dist))
    print('Greedy time: ', (end-start)*1e6)

    start = time.time()
    tour_improved = two_opt_solve(input_data)
    end = time.time()
    print('2out distance: ', total_distance(tour_improved, dist))
    print('2opt time: ', (end-start)*1e6)

    with open(f'output_{sys.argv[1]}.csv', 'w') as f:
        f.write(format_tour(tour_improved) + '\n')