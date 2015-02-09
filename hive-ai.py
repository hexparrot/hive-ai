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

if __name__ == '__main__':
    board = HiveBoard(queen_opening_allowed=True)
    
    gp = GamePieces()

    board.perform(Placement(gp.grab(Color.White, Insect.Queen), (0,0)))
    board.perform(Placement(gp.grab(Color.Black, Insect.Queen), (0,1)))

    from itertools import cycle
    from random import choice, shuffle
    
    action = {
        Color.White: 'grab',
        Color.Black: 'grab'
        }
    
    cycler = cycle([Color.White, Color.Black])
    player_color = next(cycler)
        
    while board.winner is None:
        if not board.can_act(player_color):
            player_color = next(cycler)
        elif action[player_color] == 'grab':
            try:
                grabbed = gp.grab_random(player_color)
            except IndexError:
                print('placing over')
                action[player_color] = 'move'
            else:
                new_loc = choice(list(board.valid_placements(player_color)))
                placement_action = Placement(grabbed, new_loc)
                board.perform(placement_action)
                print(placement_action)
                player_color = next(cycler)
        elif action[player_color] == 'move':
            move_made = False
            current_positions = list(board.free_pieces(player_color))
            shuffle(current_positions)
            
            for actor_coord in current_positions:
                if move_made:
                    break
                p = board.piece_at(actor_coord)
                if p.color == player_color:
                    vm_set = list(board.valid_moves(actor_coord))
                    shuffle(vm_set)
                    #print(board)
                    #print(p, '@', actor_coord, 'considering', vm_set)
                    #print(board._pieces[actor_coord])

                    for considered_move in vm_set:
                        try:
                            considered_ply = Movement(actor_coord, considered_move)
                            board.perform(considered_ply)
                        except IllegalMove as e:
                            #print(e, board._pieces[actor_coord])
                            continue
                        else:
                            print('performed:', p, actor_coord, considered_move)
                            move_made = True
                            #player_color = next(cycler)
                            break

            player_color = next(cycler)

            
    print('ended')    
    print(board)
    