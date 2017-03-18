import json
from pprint import pprint

class library(object):
  library = dict()
  filename = ""
  
  def __init__(self, filename):
    self.filename = filename
    with open(self.filename) as data_file:
      self.library = json.load(data_file)
  
  def add(self, book):
    new_number = len(self.library["list"]) + 1
    new_book = dict()
    new_book[str(new_number)] = book
    self.library["list"].append(new_book)

  def show(self):
    pprint(self.library)

  def bookInfo(self, num):
    return(self.library["list"][num - 1][str(num)][0] + "\n\n" + self.library["list"][num - 1][str(num)][1])

  def list(self):
    ind = 0
    for item in self.library["list"]:
      ind += 1
      yield("/" + str(ind) + ": " + item[str(ind)][0])

  def dump(self):
    with open(self.filename, 'w') as outfile:
      json.dump(self.library, outfile)

  def __del__(self):
    self.dump()

    


