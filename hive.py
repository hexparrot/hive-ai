"""A python AI for Hive, by John Yianni
"""

__author__ = "William Dizon"
__license__ = "Simplified BSD License"
__version__ = "0.0.1"
__email__ = "wdchromium@gmail.com"

from enum import Enum
from collections import namedtuple

Tile = namedtuple('Tile', 'color insect')
Ply = namedtuple('Ply', 'rule tile origin dest')

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
    
class Pointed_Directions(Enum):
    NE = (1,-1)
    E = (1,0)
    SE = (0,1)
    SW = (-1,1)
    W = (-1,0)
    NW = (0,-1)
    
class Flat_Directions(Enum):
    N = (0,-1)
    NE = (1,-1)
    SE = (1,0)
    S = (0,1)
    SW = (-1,1)
    NW = (-1,0)
    
class Rule(Enum):
    Place = 0
    Move = 1
    External_Move = 2

class HiveBoard(object):
    def __init__(self,
                 tile_orientation=Flat_Directions,
                 queen_opening_allowed=False):
        self._pieces = {}
        self._log = []
        self.tile_orientation = tile_orientation
        self.queen_opening_allowed = queen_opening_allowed
        
    def move(self, origin, dest):
        t = self.pop(origin)
        if dest in self._pieces:
            self._pieces[dest].append(t)
        else:
            self._pieces[dest] = [t]
        
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
        
    def perform(self, ply):    
        def queen_placed(color):
            for stack in self._pieces.values():
                if Tile(color, Insect.Queen) in stack:
                    return True
            return False
            
        def placed_adjacent_to_opponent(color):
            for c in self.hex_neighbors(self.tile_orientation, ply.dest):
                if c in self._pieces:
                    if self.piece_at(c).color != color:
                        return True
            return False
            
        def check_queen_opening():
            if self.ply_number in [0,1] and \
                not self.queen_opening_allowed and \
                ply.tile.insect == Insect.Queen:
                raise IllegalMove('Current rules disallow Queen Bee opening')
            
        def check_queen_down_by_fourth_turn():
            if self.ply_number in [6,7] and \
                not queen_placed(ply.tile.color) and \
                ply.tile.insect != Insect.Queen:
                raise IllegalMove('Your Queen Bee must be placed by turn 4')
            
        def check_climbing_permitted():
            if ply.dest in self._pieces and \
                ply.tile.insect != Insect.Beetle:
                raise IllegalMove('Your {0} may not climb atop other pieces'.format(ply.tile.insect))
        
        def check_correct_distance_for_single_hex_insects():
            if ply.tile.insect in [Insect.Queen,
                                   Insect.Beetle,
                                   Insect.Pillbug] and \
                self.hex_distance(ply.origin, ply.dest) != 1:
                raise IllegalMove('Your {0} must move at least one space'.format(ply.tile.insect))

        if ply.rule == Rule.Place:
            check_queen_opening()
            check_queen_down_by_fourth_turn()
            if self.ply_number == 1:
                if placed_adjacent_to_opponent(ply.tile.color):
                    self.place(ply.tile, ply.dest)
                else:
                    raise IllegalMove('First placement must be adjacent to opponent')
            else:
                if placed_adjacent_to_opponent(ply.tile.color):
                    raise IllegalMove('Moves after the first may not be adjacent to opponent')
                else:
                    self.place(ply.tile, ply.dest)
        elif ply.rule == Rule.Move:
            if ply.tile is None:
                ply = Ply(ply.rule,
                          self.piece_at(ply.origin),
                          ply.origin,
                          ply.dest)
                          
            if not queen_placed(ply.tile.color):
                raise IllegalMove('Queen Bee must be placed before attempting to move other pieces')
            
            check_climbing_permitted()
            check_correct_distance_for_single_hex_insects()

            self.move(ply.origin, ply.dest)

        self._log.append(ply)
        
    @property
    def ply_number(self):
        return len(self._log)

    @staticmethod
    def hex_neighbors(tile_orientation, origin):
        return set([tuple(sum(x) for x in zip(origin, d.value))
                    for d in tile_orientation])
                        
    @staticmethod
    def hex_distance(origin, dest):
        #http://www.redblobgames.com/grids/hexagons/#distances
        return (abs(origin[0] - dest[0]) + abs(origin[1] - dest[1]) + \
                abs(origin[0] + origin[1] - dest[0] - dest[1])) / 2

class IllegalMove(Exception):
    def __init__(self, message):
        self.message = message
