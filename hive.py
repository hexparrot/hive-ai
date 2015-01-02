"""A python AI for Hive, by John Yianni
"""

__author__ = "William Dizon"
__license__ = "Simplified BSD License"
__version__ = "0.0.1"
__email__ = "wdchromium@gmail.com"

from enum import Enum
from collections import namedtuple

class Insect(Enum):
    Queen = 0
    Ant = 1
    Beetle = 2
    Grasshopper = 3
    Spider = 4
    Mosquito = 5
    Ladybug = 6
    Pillbug = 7
    
class Color(Enum):
    White = 0
    Black = 1

class HiveBoard(object):
    def __init__(self):
        self._pieces = {}
        
    def __len__(self):
        return 0
        
    def __getitem__(self, key):
        return self._pieces[key]
        
    def place(self, tile, coords):
        self._pieces[coords] = tile

Tile = namedtuple('Tile', ['color', 'insect'])