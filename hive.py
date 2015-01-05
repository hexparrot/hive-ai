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
        if coords in self._pieces:
            raise RuntimeError
        self._pieces[coords] = [tile]
    
    def pop(self, coords):
        p = self._pieces[coords].pop()
        if not self._pieces[coords]:
            del self._pieces[coords]
        return p
        
    def piece_at(self, coords):
        return self._pieces[coords][-1]
        
    def stack_at(self, coords):
        return self._pieces[coords]

Tile = namedtuple('Tile', ['color', 'insect'])