import sys

# Cache is a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.
#
# Note: Please do not use a library (e.g., collections.OrderedDict).
#       Implement the data structure yourself.


class Link:
  def __init__(self):
    self.url = None
    self.contents = None
    self.left = None
    self.right = None


class Cache:

  # Contains a Hash map to store the Link objects.
  # Sets maximum size of the Hash map.
  # Keeps track of start and end items.

  def __init__(self, n):

    self.max_size = n
    self.start = Link()
    self.end = Link()
    self.cache_map = {}


  # Access a page and update the cache so that it stores the most
  # recently accessed N pages. This needs to be done with mostly O(1).
  # |url|: The accessed URL
  # |contents|: The contents of the URL
  def access_page(self, url, contents):
    
    # If the item is already in the cache, bring it to the top.
    if url in self.cache_map:
      item = self.cache_map[url]
      item.contents = contents
      self.removeItem(item)
      self.addItemAtTop(item)
      self.cache_map.pop(url)
      self.cache_map[url] = item

    # If item not in the cache, create a new link and add to the top.
    else:
      new_cache_link = Link()
      new_cache_link.contents = contents
      new_cache_link.url = url

      if len(self.cache_map)>=self.max_size: # If  chache is full, pop the oldest item.
        self.cache_map.pop(self.end.url)
        self.removeItem(self.end)
        self.addItemAtTop(new_cache_link)
            
      else:
        self.addItemAtTop(new_cache_link)

      self.cache_map[url] = new_cache_link

  

  def get_pages(self):
    cache_list = list(self.cache_map.keys())[::-1]
    return cache_list
  

  # Remove item from the Hashmap. Corrects the links.
  def removeItem(self, item):
    if item.left != None:
      item.left.right = item.right  # (Link  Left -> Right)
    else:
      self.start = item.right
    if item.right.url != None:
      item.right.left = item.left   # (Link  Left <- Right)
    else:
      self.end = item.left

  # Add item to the hash map, so that the item comes to the top of the linked list.
  def addItemAtTop(self, item): 
    item.right = self.start   # (Link  Item -> start)
    item.left = None
    if self.start != None:
      self.start.left = item    #(Link  Item <- start)
    self.start = item           # Sets item as a new start
    if self.end.url == None:
      self.end = self.start
      






# Does your code pass all test cases? :)
def cache_test():
  # Set the size of the cache to 4.
  cache = Cache(4)
  # Initially, no page is cached.
  equal(cache.get_pages(), [])
  # Access "a.com".
  cache.access_page("a.com", "AAA")
  # "a.com" is cached.
  equal(cache.get_pages(), ["a.com"])
  # Access "b.com".
  cache.access_page("b.com", "BBB")
  # The cache is updated to:
  #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
  equal(cache.get_pages(), ["b.com", "a.com"])
  # Access "c.com".
  cache.access_page("c.com", "CCC")
  # The cache is updated to:
  #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
  equal(cache.get_pages(), ["c.com", "b.com", "a.com"])
  # Access "d.com".
  cache.access_page("d.com", "DDD")
  # The cache is updated to:
  #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
  equal(cache.get_pages(), ["d.com", "c.com", "b.com", "a.com"])
  # Access "d.com" again.
  cache.access_page("d.com", "DDD")
  # The cache is updated to:
  #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
  equal(cache.get_pages(), ["d.com", "c.com", "b.com", "a.com"])
  # Access "a.com" again.
  cache.access_page("a.com", "AAA")
  # The cache is updated to:
  #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
  equal(cache.get_pages(), ["a.com", "d.com", "c.com", "b.com"])
  cache.access_page("c.com", "CCC")
  equal(cache.get_pages(), ["c.com", "a.com", "d.com", "b.com"])
  cache.access_page("a.com", "AAA")
  equal(cache.get_pages(), ["a.com", "c.com", "d.com", "b.com"])
  cache.access_page("a.com", "AAA")
  equal(cache.get_pages(), ["a.com", "c.com", "d.com", "b.com"])
  # Access "e.com".
  cache.access_page("e.com", "EEE")
  # The cache is full, so we need to remove the least recently accessed page "b.com".
  # The cache is updated to:
  #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
  equal(cache.get_pages(), ["e.com", "a.com", "c.com", "d.com"])
  # Access "f.com".
  cache.access_page("f.com", "FFF")
  # The cache is full, so we need to remove the least recently accessed page "c.com".
  # The cache is updated to:
  #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
  equal(cache.get_pages(), ["f.com", "e.com", "a.com", "c.com"])
  print("OK!")

# A helper function to check if the contents of the two lists is the same.
def equal(list1, list2):
  assert(list1 == list2)
  for i in range(len(list1)):
    assert(list1[i] == list2[i])
    pass

if __name__ == "__main__":
  cache_test()
