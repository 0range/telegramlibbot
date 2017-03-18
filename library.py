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
    #ToDo

  def show(self):
    pprint(self.library)

  def __del__(self):
    with open(self.filename, 'w') as outfile:
      json.dump(self.library, outfile)
    


