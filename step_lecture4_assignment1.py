# Assignment 1 SNS

from collections import defaultdict


def addEdge(graph, u, v):  # Appends a new edge with two vertices
  if u in graph.keys():
    if v in graph[u]:
      return
  graph[u].append(v)
  return


def showGraph(graph):  # Prints out all connections
  for key in graph:
    print(key, " :  ",  graph[key])


def dfs(origin, target): # Finds a path from origin to target using DFS

  visited = []
  stack = []

  stack.append((origin, [origin]))
  visited.append(origin)

  while stack:
    (vertex, path)= stack.pop() 
    for neigbor in graph[vertex]:
      if neigbor not in visited:
        if neigbor == target:
          return path + [neigbor]
        visited.append(neigbor)
        stack.append((neigbor, path + [neigbor])) 
  return "not connected"
      

def bfs(origin, target): # Finds a path from origin to target using BFS
  visited = []
  queue = []

  queue.append((origin, [origin]))
  visited.append(origin)

  while queue:
    (vertex, path)= queue.pop(0)    
    for neigbor in graph[vertex]:
      if neigbor not in visited:
        if neigbor == target:
          return path + [neigbor]
        visited.append(neigbor)
        queue.append((neigbor, path + [neigbor])) 
  return "not connected"


def getFarthestPerson(origin):   # To find the person with the longest distance
  names_others = names.copy()
  names_others.remove(origin)
  dist_list = {}
  for name in names_others:
    path = bfs(origin, name)
    if path and path!= "not connected":
      dist = len(path)
      dist_list[name] = dist
  farthest_person = max(dist_list, key = lambda k: dist_list[k])

  return farthest_person


# Read files
nickname_file = open("nickname.txt", 'r')
nickname_list = list(nickname_file.read().split('\n'))
nickname_file.close()
links_file = open("links.txt", 'r')
links_list = list(links_file.read().split('\n'))
links_file.close()

# Create a dictionary which maps the index to the nickname
nickname_map = {}
for item in nickname_list:
  idx, name = item.split()
  nickname_map[idx] = name

names = list(nickname_map.values())
graph = defaultdict(list)

for item in links_list:
  followed, follower = item.split()
  addEdge(graph, nickname_map[followed], nickname_map[follower])


# Test Cases

def test():
  print(bfs('janice', 'adrian'))
  print(dfs('janice', 'adrian'))
  print(bfs('betty', 'janice'))
  print(dfs('betty', 'janice'))
  print(dfs('', 'adrian'))
  print("The least related person from me (;_;)/ ", getFarthestPerson('janice'))



test()
