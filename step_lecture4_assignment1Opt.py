# Tokyo Train Map (HW 1 Optional)

from collections import defaultdict
import heapq as hq


def addEdge(graph, u, v, dist):  # Appends a new edge with two vertices and distance inbetween
  if u in graph.keys():
    if v in graph[u]:
      return
  graph[u].append((v, int(dist)))
  return

def showGraph(graph):  # Prints out all connections
  for key in graph:
    print(key, " :  ",  graph[key])

def trackPath(path, station, origin):  # To trace back the shortest path
  track = []
  current_station = station
  track.append(current_station)
  while current_station!=origin:
    track.append(path[current_station])
    current_station = path[current_station]
  return list(reversed(track))


def dijkstra(graph, origin, target):   # Dijkstra's algorithm to find the shortest path
  stations = stations_name_map.values()
  queue = []
  path = {name: None for name in stations} 
  dist_from_origin = {name: float('inf') for name in stations} 

  dist_from_origin[origin] = 0
  hq.heappush(queue, (0, origin))

  while queue:
    last_dist, current_station = hq.heappop(queue)
    for neigbor, new_dist in graph[current_station]:
      if neigbor == target:
        dist_from_origin[neigbor] = last_dist + new_dist
        path[neigbor] = current_station
        return dist_from_origin[neigbor], trackPath(path, neigbor, origin)
      elif dist_from_origin[neigbor] == float('inf'):
        cand_dist = last_dist + new_dist
        if cand_dist < dist_from_origin[neigbor]:
          dist_from_origin[neigbor] = cand_dist
          path[neigbor] = current_station
          hq.heappush(queue, (cand_dist, neigbor))
    
  print("not connected")
  return



# Read files
stations_file = open("stations.txt", 'r')
stations_list = list(stations_file.read().split('\n'))
stations_file.close()
edges_file = open("edges.txt", 'r')
edges_list = list(edges_file.read().split('\n'))
edges_file.close()

# Create a dict which maps the name and the index
stations_name_map = {}
for item in stations_list:
  idx, name = item.split()
  stations_name_map[idx] = name

# Initialize a graph and add links of people to it
graph = defaultdict(list)
for item in edges_list:
  fro, to, dist = item.split()
  addEdge(graph,  stations_name_map[fro], stations_name_map[to], dist)



# Test
def test():
  print(dijkstra(graph, '東京', '渋谷'))
  print(dijkstra(graph, '渋谷', '高輪ゲートウェイ'))
  print(dijkstra(graph, '東京', '御茶ノ水'))

test()


