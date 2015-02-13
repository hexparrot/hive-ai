"""A python AI for Hive, by John Yianni
"""

__author__ = "William Dizon"
__license__ = "Simplified BSD License"
__version__ = "0.0.1"
__email__ = "wdchromium@gmail.com"

from hive import Insect, Tile, Color

class GamePieces(object):
    QUANTITIES = {
        Insect.Queen: 1,
        Insect.Ant: 3,
        Insect.Beetle: 1,
        Insect.Grasshopper: 2,
        Insect.Ladybug: 0,
        Insect.Mosquito: 0,
        Insect.Pillbug: 0,
        Insect.Spider: 2
    }
    
    def __init__(self):
        self._pieces = []
        for k, count in self.QUANTITIES.items():
            self._pieces.extend([Tile(Color.White, k) for _ in range(count)])
            self._pieces.extend([Tile(Color.Black, k) for _ in range(count)])
    
    def grab(self, color, insect):
        return self._pieces.pop(self._pieces.index(Tile(color, insect)))
    
    def grab_random(self, color):
        from random import choice
        
        friendly = choice([p for p in self._pieces if p.color == color])
        return self._pieces.pop(self._pieces.index(friendly))

class HiveAI(object):
    OPPONENT = {
        Color.White: Color.Black,
        Color.Black: Color.White
    }
    
    def __init__(self, board):
        self.board = board
    
    def opponent_queen(self, color):
        try:
            return next(self.board.find(self.OPPONENT[color], Insect.Queen))[0]
        except StopIteration:
            return None
    
    def empty_hexes_surrounding(self, coord):
        for c,t in self.board.neighbors(coord):
            if not t:
                yield c