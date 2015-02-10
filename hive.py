"""A python AI for Hive, by John Yianni
"""

__author__ = "William Dizon"
__license__ = "Simplified BSD License"
__version__ = "0.0.1"
__email__ = "wdchromium@gmail.com"

from enum import Enum

class Ply(object):
    def __init__(self, rule, tile):
        self.rule = rule
        self.tile = tile
        
class Placement(Ply):
    def __init__(self, tile, dest):
        super().__init__(Rule.Place, tile)
        self.dest = dest
    
    def __str__(self):
        return 'Placing {0} {1} at {2}'.format(self.tile.color.name,
                                               self.tile.insect.name,
                                               self.dest) 

class Movement(Ply):
    def __init__(self, origin, dest, leech_from=None):
        if leech_from:
            super().__init__(Rule.Leech_Move, None)
        else:
            super().__init__(Rule.Move, None)
            
        self.origin = origin
        self.dest = dest
        self.leech_from = leech_from
    
    def __str__(self):
        retval = 'Movement from {0} to {1}'.format(self.origin, self.dest)
        if self.leech_from:
            retval += ' leeching power from {0}'.format(self.leech_from)
        
        return retval

class Relocation(Ply):
    def __init__(self, origin, dest, actor_loc, leech_from=None):
        if leech_from:
            super().__init__(Rule.Leech_Relocate, None)
        else:
            super().__init__(Rule.Relocate, None)
        
        self.origin = origin
        self.dest = dest
        self.actor_loc = actor_loc
        self.leech_from = leech_from
    
    def __str__(self):
        retval = 'Movement from {0} to {1}'.format(self.origin, self.dest)
        retval += ' via {0}'.format(self.actor_loc)
        
        if self.leech_from:
            retval += ' leeching power from {0}'.format(self.leech_from)
        
        return retval

class Tile(object):
    def __init__(self, color, insect):
        self._color = color
        self._insect = insect
        
    def __eq__(self, other):
        return self.color == other.color and self.insect == other.insect
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        return '{0} {1}'.format(self.color.name, self.insect.name)
    
    @property
    def color(self):
        return self._color
        
    @property
    def insect(self):
        return self._insect

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
    Relocate = 2
    Leech_Move = 3
    Leech_Relocate = 4
    
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
    Freedom_of_Movement = 'Piece unable to slide physically through this path'
    One_Hive_Rule = 'Movement/placement may not split hive into separate pieces, even in-transit'
    Pillbug_Adjacent = 'Origin and dest must both be adjacent to pillbug'
    Mosquito_Adjacent = 'Mosquito must both be adjacent to pillbug'
    Pillbug_Cannot_Touch_Stacks = 'Pillbugs may not grab from or place onto stacks'
    Unavailable_Action = 'The active tile does not have access to this action'
    May_Not_Place_On_Other_Pieces = 'Pieces may not initially be placed on other pieces'
    Cannot_Jump_Gaps = 'Pieces may not temporarily be separated from the hive'

class HiveBoard(object):
    BLOCKING = {
        'FLAT': {
            Flat_Directions.N: (Flat_Directions.NW, Flat_Directions.NE),
            Flat_Directions.NE: (Flat_Directions.N, Flat_Directions.SE),
            Flat_Directions.SE: (Flat_Directions.NE, Flat_Directions.S),
            Flat_Directions.S: (Flat_Directions.SW, Flat_Directions.SE),
            Flat_Directions.SW: (Flat_Directions.NW, Flat_Directions.S),
            Flat_Directions.NW: (Flat_Directions.SW, Flat_Directions.N)
        },
        'POINTED': {
            Pointed_Directions.NE: (Pointed_Directions.NW, Pointed_Directions.E),
            Pointed_Directions.E: (Pointed_Directions.NE, Pointed_Directions.SE),
            Pointed_Directions.SE: (Pointed_Directions.E, Pointed_Directions.SW),
            Pointed_Directions.SW: (Pointed_Directions.W, Pointed_Directions.SE),
            Pointed_Directions.W: (Pointed_Directions.NW, Pointed_Directions.SW),
            Pointed_Directions.NW: (Pointed_Directions.NE, Pointed_Directions.W)
        }
    }
        
    def __init__(self,
                 tile_orientation=Flat_Directions,
                 queen_opening_allowed=False):
        self._pieces = {}
        self._log = []
        self.tile_orientation = tile_orientation
        self.queen_opening_allowed = queen_opening_allowed

    def __str__(self):
        """Produces an ASCII-based map of all the tiles"""
        import hexgrid
        
        hg = hexgrid.HexGrid()
        for coords, stack in self._pieces.items():
            hg.annotate(coords, stack[-1].color.value + stack[-1].insect.value)

        return str(hg)
        
    def quick_setup(self, arrangement):
        """Provides an intuitive way to lay out tiles"""
        for coord, piece in arrangement.items():
            c = next(k for k in Color if k.value==piece[0])
            i = next(k for k in Insect if k.value==piece[1])
            
            self.place(Tile(c,i), coord)
        
    def move(self, origin, dest):
        """
        Naively removes the top tile in a stack (or single)
        and places it in the new destination.  This method
        does not do any game-rule checking and assumes the move
        has already been properly validated
        """
        t = self._pieces[origin].pop()
        if not self._pieces[origin]:
            del self._pieces[origin]

        if dest in self._pieces:
            self._pieces[dest].append(t)
        else:
            self._pieces[dest] = [t]
        
    def place(self, tile, coords):
        """
        Places a tile at the coordinates specified.  Since placing
        may never happen atop an existing tile (that's instead
        a move), it throws an error if attempting to.
        """
        if coords in self._pieces:
            raise IllegalMove(Violation.May_Not_Place_On_Other_Pieces)
        self._pieces[coords] = [tile]
        
    def piece_at(self, coords):
        """Returns the tile (or topmost tile) at a given coordinate"""
        return self._pieces[coords][-1]
        
    def stack_at(self, coords):
        """Returns a list of all tiles at a given coordinate"""
        return self._pieces[coords]
    
    def perform(self, ply):
        """
        Convenience function for all game logic.  Accepts a ply
        (with or without the tile attribute) and checks it against
        all known rules.  If an invalid move is detected, it will
        raise the exception, else it will complete the move
        with the inner functions and add it to the game log.
        """
        assert(ply.rule in Rule)
        
        try:
            ply = self.validate(ply)
            assert(ply)
        except IllegalMove:
            raise
        else:
            if ply.rule == Rule.Place:
                self.place(ply.tile, ply.dest)
            elif ply.rule in [Rule.Move, Rule.Leech_Move,
                              Rule.Relocate, Rule.Leech_Relocate]:
                self.move(ply.origin, ply.dest)
    
            self._log.append(ply)
    
    def validate(self, ply):
        """
        Accepts a play and tests it against all known game rules.
        If an invalid move is detected, it will raise an exception.
        If all is well, it will return a (possibly) new ply,
        but with the .tile attribute properly populated.
        """
        def queen_placed(color):
            """Checks if queen is placed for the current color."""
            q = Tile(color, Insect.Queen)
            for stack in self._pieces.values():
                if q in stack:
                    return True
            return False
            
        def placed_adjacent_to_opponent(color):
            """Checks if tile is ilegally placed next to opponent"""
            for c in self.hex_neighbors(self.tile_orientation, ply.dest):
                if c in self._pieces:
                    if self.piece_at(c).color != color:
                        return True
            return False
            
        def check_queen_opening():
            """
            If the tournament rule is in effect, disallow
            placing the Queen on either players first ply.
            """
            if self.ply_number in [0,1] and \
                not self.queen_opening_allowed and \
                ply.tile.insect == Insect.Queen:
                raise IllegalMove(Violation.Queen_Bee_Opening_Prohibited)
            
        def check_queen_down_by_fourth_turn():
            """
            If the player's first 3 plies did not place a Queen,
            force the player's 4th ply to be a Queen.
            """
            if self.ply_number in [6,7] and \
                not queen_placed(ply.tile.color) and \
                ply.tile.insect != Insect.Queen:
                raise IllegalMove(Violation.Queen_Bee_Must_Be_Played)
            
        def check_climbing_permitted():
            """
            If the destination of a piece is atop another piece,
            ensure the piece is or has the power of a beetle.
            """
            if ply.dest in self._pieces and \
                ply.tile.insect != Insect.Beetle:
                raise IllegalMove(Violation.Insect_Cannot_Climb)
        
        def check_correct_distance_for_single_hex_insects():
            """Ensure that pieces that may move only one hex do so"""
            if ply.tile.insect in [Insect.Queen,
                                   Insect.Beetle,
                                   Insect.Pillbug] and \
                self.hex_distance(ply.origin, ply.dest) != 1:
                raise IllegalMove(Violation.Distance_Must_Be_Exactly_One)
        
        def check_correct_distance_for_spiders(start, end):
            """
            Ensure spiders never land farther than 3 spaces
            away from their starting position
            """
            if ply.tile.insect == Insect.Spider and \
                self.hex_distance(start, end) > 3:
                raise IllegalMove(Violation.Invalid_Distance_Attempted)

        def check_insect_moved():
            """Ensure no tile ends up where it started"""
            if self.hex_distance(ply.origin, ply.dest) == 0:
                raise IllegalMove(Violation.Did_Not_Move)
                
        def check_not_isolated():
            """
            Checks that a piece doesn't simply move off the hive.
            This check is necessary because the one_hive_rule
            method only checks the CURRENT state, not the future
            state."""
            neighbors = self.hex_neighbors(self.tile_orientation, ply.dest)
            origin_will_be_vacated = False            
            
            if ply.origin in neighbors:            
                neighbors.remove(ply.origin)
                if len(self.stack_at(ply.origin)) <= 1:
                    origin_will_be_vacated = True
            
            if not any(p in self._pieces for p in neighbors) and \
                origin_will_be_vacated:
                raise IllegalMove(Violation.One_Hive_Rule)      
                
        def freedom_of_movement(path):
            """
            Checks that a piece can physically slide into
            a position each step of the way.
            """
            if self.piece_at(path[0]).insect in [Insect.Grasshopper, Insect.Beetle]:
                return

            path_copy = path[:]
            blockers = self.BLOCKING['FLAT'] if self.tile_orientation == Flat_Directions else self.BLOCKING['POINTED']
            
            while path_copy:
                try:
                    current = path_copy.pop(0)
                    direction = self.get_direction(current, path_copy[0], self.tile_orientation)
                    
                    if self.go_direction(current, blockers[direction][0]) in self._pieces and \
                        self.go_direction(current, blockers[direction][1]) in self._pieces:
                        raise IllegalMove(Violation.Freedom_of_Movement)
                except IndexError:
                    break
        
        def beetle_gate_freedom_of_moment(start, end):
            '''
            Very specific rule: Blocking tiles still restrict 
            climbing if the lower of the two blocking tiles
            is higher than the higher of origin/dest.
            
            For full specifics see the hive faq:            
            http://boardgamegeek.com/wiki/page/Hive_FAQ#toc9'''
            def height_of(cc):
                try:
                    return len(self.stack_at(cc))
                except KeyError:
                    return 0
            
            if self.piece_at(start).insect != Insect.Beetle:
                return
                
            blockers = self.BLOCKING['FLAT'] if self.tile_orientation == Flat_Directions else self.BLOCKING['POINTED']
            direction = self.get_direction(start, end, self.tile_orientation)
            
            gate_1 = self.go_direction(start, blockers[direction][0])
            gate_2 = self.go_direction(start, blockers[direction][1])

            if min(height_of(gate_1), height_of(gate_2)) > max(height_of(start)-1, height_of(end)):
                raise IllegalMove(Violation.Freedom_of_Movement)
        
        def check_origin_dest_empty_adjacency(pillbug_coords):
            """
            Checks that a pillbugs relocation move is:
            a) adjacent to the pillbug itself and
            b) not originating or ending on a stack
            """
            neighbors = self.hex_neighbors(self.tile_orientation, pillbug_coords)
            if ply.origin not in neighbors or \
                ply.dest not in neighbors:
                raise IllegalMove(Violation.Pillbug_Adjacent)
            elif ply.dest in self._pieces or \
                len(self.stack_at(ply.origin)) > 1:
                raise IllegalMove(Violation.Pillbug_Cannot_Touch_Stacks)
                
        def jumping_gap(start, end):
            """
            Checks that even in transit, a piece is always
            physically adjacent to another piece of the hive.
            """
            if self.piece_at(start).insect not in [Insect.Beetle, Insect.Queen]:
                return
            elif end in self._pieces:
                return #if climbing, not jumping gap
            elif len(self.stack_at(start)) > 1:
                return #if climbing down, gap irrelevant
                
            direction = self.get_direction(start, end, self.tile_orientation)            
            helpers = self.BLOCKING['FLAT'] if self.tile_orientation == Flat_Directions else self.BLOCKING['POINTED']
            if self.go_direction(start, helpers[direction][0]) not in self._pieces and \
               self.go_direction(start, helpers[direction][1]) not in self._pieces:
                raise IllegalMove(Violation.Cannot_Jump_Gaps)

        if ply.rule == Rule.Place:
            assert(isinstance(ply.tile, Tile))
            assert(isinstance(ply.dest, tuple))
            
            check_queen_opening()
            check_queen_down_by_fourth_turn()
            
            if self.ply_number == 0:
                return ply
            elif self.ply_number == 1:
                if placed_adjacent_to_opponent(ply.tile.color):
                    return ply
                else:
                    raise IllegalMove(Violation.Must_Place_Adjacent)
            else:
                if placed_adjacent_to_opponent(ply.tile.color):
                    raise IllegalMove(Violation.May_Not_Place_Adjacent)
                elif not any(c in self._pieces for c in self.hex_neighbors(self.tile_orientation, ply.dest)):
                    raise IllegalMove(Violation.One_Hive_Rule)
                else:
                    return ply
        elif ply.rule == Rule.Move:
            assert(isinstance(ply.origin, tuple))
            assert(isinstance(ply.dest, tuple))
            
            ply.tile = self.piece_at(ply.origin)

            if not queen_placed(ply.tile.color):
                raise IllegalMove(Violation.No_Movement_Before_Queen_Bee_Placed)
            if not self.one_hive_rule(ply.origin):
                raise IllegalMove(Violation.One_Hive_Rule)
                
            check_not_isolated()
            
            check_insect_moved()
            check_climbing_permitted()
            check_correct_distance_for_single_hex_insects()
            check_correct_distance_for_spiders(ply.origin, ply.dest)
            
            freedom_of_movement(self.valid_path(ply.origin, ply.dest))
            beetle_gate_freedom_of_moment(ply.origin, ply.dest)
            
            jumping_gap(ply.origin, ply.dest)

            return ply
        elif ply.rule == Rule.Relocate:
            assert(isinstance(ply.origin, tuple))
            assert(isinstance(ply.dest, tuple))
            assert(isinstance(ply.actor_loc, tuple) and ply.actor_loc)
            
            ply.tile = self.piece_at(ply.actor_loc)
            
            if self.piece_at(ply.actor_loc).insect != Insect.Pillbug:
                raise IllegalMove(Violation.Unavailable_Action)

            check_origin_dest_empty_adjacency(ply.actor_loc)
            
            if not self.one_hive_rule(ply.origin):
                raise IllegalMove(Violation.One_Hive_Rule)
            
            return ply
        elif ply.rule == Rule.Leech_Relocate:
            assert(isinstance(ply.origin, tuple))
            assert(isinstance(ply.dest, tuple))
            assert(isinstance(ply.actor_loc, tuple) and ply.actor_loc)
            assert(isinstance(ply.leech_from, tuple) and ply.leech_from)
            
            ply.tile = self.piece_at(ply.actor_loc)
            
            if self.piece_at(ply.leech_from).insect != Insect.Pillbug:
                raise IllegalMove(Violation.Unavailable_Action)
            elif ply.leech_from not in self.hex_neighbors(self.tile_orientation, ply.actor_loc):
                raise IllegalMove(Violation.Mosquito_Adjacent)
            
            check_origin_dest_empty_adjacency(ply.actor_loc)
            
            return ply
        elif ply.rule == Rule.Leech_Move:
            assert(isinstance(ply.origin, tuple))
            assert(isinstance(ply.dest, tuple))
            assert(isinstance(ply.leech_from, tuple) and ply.leech_from)
            
            if ply.dest in set(self.valid_moves(ply.origin, self.piece_at(ply.leech_from).insect)):
                return ply
            #else:
            #    raise IllegalMove(Violation.Unavailable_Action)
        else:
            raise RuntimeError
        
    def valid_moves(self, coords, acting_as=None):
        """Return a generator containing all the hexes
        which a tile could move to in one turn. This funciton,
        however, does not take any rules into account so many
        of them may still throw IllegalMove.
        
        This is just a quick method to check plausible moves,
        and should be less expensive than running all rules against
        all potential moves. This way, validation can occur at
        execution of the ply, rather than prior to execution.
        """
        def adjacent_to_something(ignored_origin, dest):
            """Check destination has another tile adjacent"""
            for c in self.hex_neighbors(self.tile_orientation, dest):
                if c in self._pieces and c != ignored_origin:
                    return True
                        
        def queen_bee():
            """Check destination is empty and adjacent"""
            for direction in self.tile_orientation:
                c = self.go_direction(coords, direction)
                if c not in self._pieces and adjacent_to_something(coords, c):
                    yield c
        
        def beetle():
            """Check destination is adjacent"""
            for direction in self.tile_orientation:
                c = self.go_direction(coords, direction)
                if adjacent_to_something(coords, c):
                    yield c
                    
        def grasshopper():
            """
            Check destination is a straight line over
            at least one tile
            """
            for direction in self.tile_orientation:
                c = self.go_direction(coords, direction)
                if c in self._pieces:
                    while c in self._pieces:
                        c = self.go_direction(c, direction)
                    yield c
        
        def ant():
            """
            Returns roughly all tiles around perimeter.
            Note, some may be FOM-violating
            """
            valid = set()

            for p in [k for k in self._pieces.keys() if k != coords]:
                valid.update(self.hex_neighbors(self.tile_orientation, p))

            valid.difference_update([k for k in self._pieces.keys()])
            for i in valid:
                yield i
        
        def spider():
            """
            Check destination is truly 3 hexes worth of movement,
            but does not ever revisit a hex.
            """
            checked = set()
            s1 = set() #1 tile out
            s2 = set() #2 tiles out
            s3 = set() #3 tiles out

            for c in self.hex_neighbors(self.tile_orientation, coords):
                if c not in self._pieces and adjacent_to_something(coords, c):
                    s1.add(c)
                    checked.add(c)

            for i in s1:
                for c in self.hex_neighbors(self.tile_orientation, i):
                    if c not in self._pieces and adjacent_to_something(coords, c) and c not in checked:
                        s2.add(c)
                        checked.add(c)
            
            for i in s2:
                for c in self.hex_neighbors(self.tile_orientation, i):
                    if c not in self._pieces and adjacent_to_something(coords, c) and c not in checked:
                        s3.add(c)

            for i in s3:
                yield i
                
        def ladybug():
            """
            Check first two tiles are climbed onto, and third tile
            is climbing down to the base level.
            """
            checked = set()
            s1 = set() #1 tile out
            s2 = set() #2 tiles out
            s3 = set() #3 tiles out
            
            checked.add(coords) 
            #add initial space because it cannot be crawled back upon

            for c in self.hex_neighbors(self.tile_orientation, coords):
                if c in self._pieces:
                    s1.add(c)
                    checked.add(c)

            for i in s1:
                for c in self.hex_neighbors(self.tile_orientation, i):
                    if c in self._pieces and c not in checked:
                        s2.add(c)
                        checked.add(c)
            
            for i in s2:
                for c in self.hex_neighbors(self.tile_orientation, i):
                    if c not in self._pieces and adjacent_to_something(coords, c) and c not in checked:
                        s3.add(c)

            for i in s3:
                yield i
                
        def mosquito():
            """Doesn't do anthing--likely will be removed"""
            valid_dests = set()
            neighbors = self.hex_neighbors(self.tile_orientation, coords)
            gained_movement = set(self.piece_at(n).insect for n in neighbors if n in self._pieces)
            
            insect_map = {
                Insect.Queen: queen_bee,
                Insect.Beetle: beetle,
                Insect.Grasshopper: grasshopper,
                Insect.Ant: ant,
                Insect.Spider: spider,
                Insect.Ladybug: ladybug,
                Insect.Pillbug: queen_bee #shared movement logic with bee,
                #mosquito left out deliberately--would recurse indefinitely
            }
            
            if Insect.Mosquito in gained_movement:
                gained_movement.remove(Insect.Mosquito)

            for insect in gained_movement:
                for j in insect_map[insect]():
                    valid_dests.add(j)
            
            for i in valid_dests:
                yield i
                
        insect = acting_as or self.piece_at(coords).insect
        
        return {
            Insect.Queen: queen_bee,
            Insect.Beetle: beetle,
            Insect.Grasshopper: grasshopper,
            Insect.Ant: ant,
            Insect.Spider: spider,
            Insect.Ladybug: ladybug,
            Insect.Pillbug: queen_bee, #shared movement logic with bee,
            Insect.Mosquito: mosquito
            }[insect]()

    def valid_path(self, origin, dest):
        '''this function will find a valid path for the tiles from A->B.
        However, it makes limited assumptions about the piece it is moving.
        For example, the spider movement heuristic is the same as the ant's,
        but the spider can only move 3 tiles--this movement restriction
        is not part of hb.valid_path. This function should operate as if
        the tile itself has unlimited moves (and thus it can create a beetle
        path that extends long beyond one tile).
        
        thanks amit patel
        http://www.redblobgames.com/pathfinding/a-star/introduction.html
        '''
        def freedom_of_movement_violated(start, end):
            blockers = self.BLOCKING['FLAT'] if self.tile_orientation == Flat_Directions else self.BLOCKING['POINTED']
            direction = self.get_direction(start, end, self.tile_orientation)
            
            if self.go_direction(start, blockers[direction][0]) in self._pieces and \
                self.go_direction(start, blockers[direction][1]) in self._pieces:
                return True

        from queue import Queue
        
        frontier = Queue()
        frontier.put(origin)
        
        came_from = {}
        came_from[origin] = None
        
        limit = ((self.radius + 1)*2) * 6
        #includes radius, plus one padding for the boundaries
        #multiplies by two, for the diameter
        #multiplied by six, for how many new hexagons introduced per radius
        counter = 0
        
        insect = self.piece_at(origin).insect

        while not frontier.empty():
            counter += 1
            if counter > limit: break
            current = frontier.get()
            
            if current not in self._pieces and \
                not any(c in self._pieces for c in self.hex_neighbors(self.tile_orientation, current)):
                continue
            
            for n in self.hex_neighbors(self.tile_orientation, current):
                if n not in came_from:
                    if insect in [Insect.Spider, Insect.Ant, Insect.Queen, Insect.Pillbug]:                        
                        if n not in self._pieces and \
                            not freedom_of_movement_violated(current, n):
                            frontier.put(n)
                            came_from[n] = current
                    elif insect == Insect.Beetle:
                        frontier.put(n)
                        came_from[n] = current
                    elif insect == Insect.Grasshopper:
                        if n in self._pieces and n!= dest:
                            frontier.put(n)
                            came_from[n] = current
                        elif n not in self._pieces and n == dest:
                            frontier.put(n)
                            came_from[n] = current
                    elif insect == Insect.Ladybug:
                        if n == dest:
                            frontier.put(n)
                            came_from[n] = current
                        elif n in self._pieces:
                            frontier.put(n)
                            came_from[n] = current

        current = dest
        path = [current]
        
        try:
            came_from[current]
        except KeyError:
            raise IllegalMove(Violation.Freedom_of_Movement)
        
        while current != origin:
            current = came_from[current]
            path.append(current)
        return list(reversed(path))
        
    def valid_placements(self, color):
        """
        Finds all hexes where a new, unused piece can be placed"""
        def adjacent_to_opponent(friendly_color, coord):
            for c in self.hex_neighbors(self.tile_orientation, coord):
                if c in self._pieces and self.piece_at(c).color != friendly_color:
                    return True
            return False
        
        valid = set()
        checked = set()
        
        for coords in self._pieces.keys():
            for n in self.hex_neighbors(self.tile_orientation, coords):
                if n not in checked and \
                   n not in self._pieces and \
                   not adjacent_to_opponent(color, n):
                    valid.add(n)
                checked.add(n)
                
        return valid

    def one_hive_rule(self, ignored_coord=None):
        """
        Checks if hive is contiguous. ignored_coord, when provided,
        should be the moving tile (not the acting tile).
        
        If the hive is incomplete while the moving tile is ignored,
        then it means that the hive is broken 'in transit' and 
        the move is illegal.
        """
        from queue import Queue
        
        frontier = Queue()
        checked = set()
        
        all_pieces = list(self._pieces.keys())
        
        if ignored_coord and len(self.stack_at(ignored_coord)) == 1:
            all_pieces.remove(ignored_coord)
        
        start = all_pieces[0]
        frontier.put(start)
        
        while not frontier.empty():
            current = frontier.get()
            for n in self.hex_neighbors(self.tile_orientation, current):
                if n in all_pieces and n not in checked:
                    frontier.put(n)
                    checked.add(n)

        return checked == set(all_pieces)

    def free_pieces(self, color):
        """
        Returns a set of all pieces that will not violate
        the 'one hive rule' if moved.
        """
        free = set()
        
        for coords in self._pieces:
            if self.piece_at(coords).color == color:
                if self.one_hive_rule(coords):
                    free.add(coords)
        
        return free
    
    def can_act(self, color):
        """
        Checks all possibilities for placing or moving.
        If this returns False, the player will forego his or her
        turn
        """
        if len(self._pieces) == 0:
            return True
        elif len(self._pieces) == 1:
            if self.piece_at(list(self._pieces.keys())[0]).color == color:
                return False
            else:
                return True
        else:
            if self.free_pieces(color) or self.valid_placements(color):
                return True
            else:
                return False

    @property
    def winner(self):
        """
        Checks if the board has a winner.  If a single move
        simultaneously surrounds both Queens, instead of returning
        a color (signifying the winner), it will return False,
        as in 'it is False there will be a winner'.  All other
        circumstances return None, to indicate not yet a winner.
        """
        white_surrounded, black_surrounded = False, False
        
        for coords, stack in self._pieces.items():
            if not white_surrounded and Tile(Color.White, Insect.Queen) in stack:
                white_surrounded = all(p in self._pieces for p in self.hex_neighbors(self.tile_orientation, coords))
            if not black_surrounded and Tile(Color.Black, Insect.Queen) in stack:
                black_surrounded = all(p in self._pieces for p in self.hex_neighbors(self.tile_orientation, coords))
        
        if white_surrounded and black_surrounded:
            return False
        elif white_surrounded:
            return Color.Black
        elif black_surrounded:
            return Color.White     
        else:
            return None
        
    @property
    def ply_number(self):
        """
        Returns the number of plies performed, as only
        plies get added to the log (manual move/place does not)
        """
        return len(self._log)
    
    @staticmethod
    def get_direction(origin, dest, tile_orientation):
        """
        Given a start and end, return the respective direction
        the two hexes are in relation to eachother.
        
        If the two hexes are not adjacent, will except
        RuntimeError, as it does not make logical sense to
        have a direction that is a distance > 1.
        """
        delta = (dest[0] - origin[0], dest[1] - origin[1])
        for d in tile_orientation:
            if d.value == delta:
                return d
        else:
            raise RuntimeError
    
    @staticmethod
    def go_direction(coord, direction):
        """
        Returns the hex coordinate of a hex one distance away
        from a given coordinate, in the given direction.
        """
        return tuple(map(sum, zip(coord, direction.value)))

    @classmethod
    def hex_neighbors(cls, tile_orientation, origin):
        """Returns a set of all hex coords adjacent to a given coord"""
        return set(cls.go_direction(origin, d) for d in tile_orientation)
                        
    @staticmethod
    def hex_distance(origin, dest):
        """
        Calculates the distance between two hex coordinates. This
        number signifies the number of single-hex movements
        required to get from start to end
        
        http://www.redblobgames.com/grids/hexagons/#distances
        """
        return (abs(origin[0] - dest[0]) + abs(origin[1] - dest[1]) + \
                abs(origin[0] + origin[1] - dest[0] - dest[1])) / 2
    
    @property
    def radius(self):
        """Returns the max distance of all pieces from 0,0"""
        maximum = 0
        
        for k in self._pieces:
            maximum = max(self.hex_distance((0,0), k), maximum)
        
        return maximum
            

class IllegalMove(Exception):
    def __init__(self, violation):
        self.violation = violation
        self.message = violation.value
