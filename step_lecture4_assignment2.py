# Wilipedia links

from collections import defaultdict
from collections import deque

class Graph:

  def __init__(self):
    self.graph = defaultdict(list)

  def addEdge(self, u, v):  # Appends a new edge with two vertices
    if u in self.graph.keys():
      if v in self.graph[u]:
        return
    self.graph[u].append(v)
    #self.graph[v].append(u)

  def showGraph(self):  # Prints out all connections
    for key in self.graph:
      print(key, " :  ",  self.graph[key])

        

  def BFS(self, origin, target): # Finds a path from origin to target using BFS

    visited = []
    queue = deque()

    queue.append((origin, [origin]))
    visited.append(origin)

    while queue:
      (vertex, path)= queue.popleft()
         
      for neigbor in self.graph[vertex]:
        if neigbor not in visited:
          if neigbor == target:
            print(path + [neigbor])
            return
          visited.append(neigbor)
          queue.append((neigbor, path + [neigbor])) 
    print("not connected")
    return



if __name__ == '__main__':

 
  # Read files (* Takes a lot of time so I recommend you to comment out once they are read.)
  
  pages_file = open("wikipedia_links/pages.txt", 'r')
  pages_list = list(pages_file.read().split('\n'))
  links_file = open("wikipedia_links/links.txt", 'r')
  links_list = list(links_file.read().split('\n'))

  links_file.close()
  pages_file.close()
  

  # Create a dict which maps the name and the index
  page_map = {}
  pages_list.pop()
  for item in pages_list:
    idx, title = item.split('\t')
    page_map[idx] = title


  # Initialize a graph and add links of people to it
  wikipediaGraph = Graph()
  links_list.pop()
  for item in links_list:
    followed, follower = item.split()
    wikipediaGraph.addEdge(page_map[followed], page_map[follower])

  del pages_list
  del links_list

  
  # I will add more test cases later.

  wikipediaGraph.BFS('東京', '栃木')
