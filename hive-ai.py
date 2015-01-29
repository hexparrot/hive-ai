"""A python AI for Hive, by John Yianni
"""

__author__ = "William Dizon"
__license__ = "Simplified BSD License"
__version__ = "0.0.1"
__email__ = "wdchromium@gmail.com"

from hive import *

class GamePieces(object):
    QUANTITIES = {
        Insect.Queen: 1,
        Insect.Ant: 3,
        Insect.Beetle: 1,
        Insect.Grasshopper: 2,
        Insect.Ladybug: 1,
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

if __name__ == '__main__':
    board = HiveBoard(queen_opening_allowed=True)
    
    gp = GamePieces()

    board.perform(Placement(gp.grab(Color.White, Insect.Queen), (0,0)))
    board.perform(Placement(gp.grab(Color.Black, Insect.Queen), (0,1)))

    from itertools import cycle
    from random import choice
    
    action = {
        Color.White: 'grab',
        Color.Black: 'grab'
        }
    
    for player_color in cycle([Color.White, Color.Black]):
        try:
            grabbed = gp.grab_random(player_color)
        except IndexError:
            print('placing over')
            break
        else:
            new_loc = choice(list(board.valid_placements(player_color)))
            board.perform(Placement(grabbed, new_loc))
            
    print(board)
    