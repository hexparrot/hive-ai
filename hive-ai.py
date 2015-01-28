"""A python AI for Hive, by John Yianni
"""

__author__ = "William Dizon"
__license__ = "Simplified BSD License"
__version__ = "0.0.1"
__email__ = "wdchromium@gmail.com"

from hive import *

if __name__ == '__main__':
    quantities = {
        Insect.Queen: 1,
        Insect.Ant: 3,
        Insect.Beetle: 1,
        Insect.Grasshopper: 2,
        Insect.Ladybug: 1,
        Insect.Mosquito: 0,
        Insect.Pillbug: 0,
        Insect.Spider: 2
    }
    
    board = hive.HiveBoard()
    
    pieces = {
        Color.White: [],
        Color.Black: []  
    }
    
    for k, count in quantities.items():
        pieces[Color.White].extend([k for _ in range(count)])
        pieces[Color.Black].extend([k for _ in range(count)])
        
    