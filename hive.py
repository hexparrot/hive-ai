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
    Queen = 'Q'
    Ant = 'A'
    Beetle = 'B'
    Grasshopper = 'G'
    Spider = 'S'
    Mosquito = 'M'
    Ladybug = 'L'
    Pillbug = 'P'
    
class Color(Enum):
    White = 'w'
    Black = 'b'
    
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
    
class Violation(Enum):
    Queen_Bee_Opening_Prohibited = 'Current rules disallow Queen Bee opening'
    Queen_Bee_Must_Be_Played = 'Queen Bee must be placed by turn 4'
    No_Movement_Before_Queen_Bee_Placed = 'Queen Bee must be placed before attempting to move other pieces'
    Insect_Cannot_Climb = 'Piece may not climb atop other pieces'
    Distance_Must_Be_Exactly_One = 'Piece must move exactly one space'
    Invalid_Distance_Attempted = 'Piece moved an incorrect number of spaces'
    Did_Not_Move = 'No piece may end where it started its turn'
    Must_Place_Adjacent = 'First placement must be adjacent to opponent'
    May_Not_Place_Adjacent = 'Moves after the first may not be adjacent to opponent'

class HiveBoard(object):
    def __init__(self,
                 tile_orientation=Flat_Directions,
                 queen_opening_allowed=False,
                 show_reduced_grid=True):
        self._pieces = {}
        self._log = []
        self.tile_orientation = tile_orientation
        self.queen_opening_allowed = queen_opening_allowed
        self.show_reduced_grid = show_reduced_grid

    def __str__(self):
        import hexgrid
        
        hg = hexgrid.HexGrid(reduced=self.show_reduced_grid)
        for coords, stack in self._pieces.items():
            hg.annotate(coords, stack[-1].color.value + stack[-1].insect.value)

        return str(hg)
        
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
                raise IllegalMove(Violation.Queen_Bee_Opening_Prohibited)
            
        def check_queen_down_by_fourth_turn():
            if self.ply_number in [6,7] and \
                not queen_placed(ply.tile.color) and \
                ply.tile.insect != Insect.Queen:
                raise IllegalMove(Violation.Queen_Bee_Must_Be_Played)
            
        def check_climbing_permitted():
            if ply.dest in self._pieces and \
                ply.tile.insect != Insect.Beetle:
                raise IllegalMove(Violation.Insect_Cannot_Climb)
        
        def check_correct_distance_for_single_hex_insects():
            if ply.tile.insect in [Insect.Queen,
                                   Insect.Beetle,
                                   Insect.Pillbug] and \
                self.hex_distance(ply.origin, ply.dest) != 1:
                raise IllegalMove(Violation.Distance_Must_Be_Exactly_One)

        def check_insect_moved():
            if self.hex_distance(ply.origin, ply.dest) == 0:
                raise IllegalMove(Violation.Did_Not_Move)

        if ply.rule == Rule.Place:
            check_queen_opening()
            check_queen_down_by_fourth_turn()
            
            if self.ply_number == 1:
                if placed_adjacent_to_opponent(ply.tile.color):
                    self.place(ply.tile, ply.dest)
                else:
                    raise IllegalMove(Violation.Must_Place_Adjacent)
            else:
                if placed_adjacent_to_opponent(ply.tile.color):
                    raise IllegalMove(Violation.May_Not_Place_Adjacent)
                else:
                    self.place(ply.tile, ply.dest)
        elif ply.rule == Rule.Move:
            if ply.tile is None:
                ply = Ply(ply.rule,
                          self.piece_at(ply.origin),
                          ply.origin,
                          ply.dest)
                          
            if not queen_placed(ply.tile.color):
                raise IllegalMove(Violation.No_Movement_Before_Queen_Bee_Placed)
            
            check_insect_moved()
            check_climbing_permitted()
            check_correct_distance_for_single_hex_insects()

            self.move(ply.origin, ply.dest)

        self._log.append(ply)
        
    def valid_moves(self, coords):
        def adjacent_to_something(origin, dest):
            for c in self.hex_neighbors(self.tile_orientation, dest):
                if c in self._pieces and c != origin:
                    return True
                        
        def queen_bee():
            for direction in self.tile_orientation:
                c = (coords[0] + direction.value[0], coords[1] + direction.value[1])
                if c not in self._pieces and adjacent_to_something(coords, c):
                    yield c
        
        def beetle():
            for direction in self.tile_orientation:
                c = (coords[0] + direction.value[0], coords[1] + direction.value[1])
                if adjacent_to_something(coords, c):
                    yield c
        
        return {
            Insect.Queen: queen_bee,
            Insect.Beetle: beetle
            }[self.piece_at(coords).insect]()

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
    def __init__(self, violation):
        self.violation = violation
        self.message = violation.value
