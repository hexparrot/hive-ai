"""A python AI for Hive, by John Yianni
"""

__author__ = "William Dizon"
__license__ = "Simplified BSD License"
__version__ = "0.0.1"
__email__ = "wdchromium@gmail.com"

import itertools
import random
from hive import *
from ai import GamePieces
from collections import deque

opponent = {
    Color.White: Color.Black,
    Color.Black: Color.White
}

def random_game():
    board = HiveBoard(queen_opening_allowed=True)
    
    gp = GamePieces()

    board.perform(Placement(gp.grab(Color.White, Insect.Queen), (0,0)))
    board.perform(Placement(gp.grab(Color.Black, Insect.Queen), (0,1)))

    action = {
        Color.White: 'grab',
        Color.Black: 'grab'
        }
    
    cycler = itertools.cycle([Color.White, Color.Black])
    player_color = next(cycler)
        
    while board.winner is None:
        if not board.can_act(player_color):
            player_color = next(cycler)
        elif action[player_color] == 'grab':
            try:
                grabbed = gp.grab_random(player_color)
            except IndexError:
                print('%s ALL PIECES PLACED' % (str(player_color).ljust(20)))
                action[player_color] = 'move'
            else:
                new_loc = random.choice(list(board.valid_placements(player_color)))
                placement_action = Placement(grabbed, new_loc)
                board.perform(placement_action)
                print(placement_action)
                player_color = next(cycler)
        elif action[player_color] == 'move':
            move_made = False
            current_positions = list(board.free_pieces(player_color))
            random.shuffle(current_positions)
            
            for actor_coord in current_positions:
                if move_made:
                    break
                p = board.piece_at(actor_coord)
                if p.color == player_color:
                    vm_set = list(board.valid_moves(actor_coord))
                    random.shuffle(vm_set)
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
                            print('%s %s' % (str(p).ljust(20), considered_ply))
                            move_made = True
                            #player_color = next(cycler)
                            break

            player_color = next(cycler)

    print('ended')    
    print(board)
    
def naive_ai():
    board = HiveBoard(queen_opening_allowed=True)
    
    gp = GamePieces()

    board.perform(Placement(gp.grab(Color.White, Insect.Queen), (0,0)))
    board.perform(Placement(gp.grab(Color.Black, Insect.Queen), (0,1)))
    
    cycler = itertools.cycle([Color.White, Color.Black])
    player_color = next(cycler)
    
    moved_recently = deque([],4)
        
    while board.winner is None:
        move_made = False
        opposing_queen = next(board.find(opponent[player_color], Insect.Queen))[0]
        ply = None
        print('turn', player_color)
        print(board)
        for c, t in board.neighbors(opposing_queen):
            if not t:
                for candidate in board.free_pieces(player_color):
                    if board.piece_at(candidate) in moved_recently:
                        continue
                    elif board.piece_at(candidate).insect is Insect.Queen:
                        continue
                    elif c in set(board.valid_moves(candidate)):
                        ply = Movement(candidate, c)
                        try:
                            board.validate(ply)
                        except IllegalMove:
                            continue
                        else:
                            move_made = True
                            break
                        
                if move_made:
                    print(board.piece_at(ply.origin), ply)
                    moved_recently.append(board.piece_at(ply.origin))
                    board.perform(ply)
                    player_color = next(cycler)
                    break
        else:
            print('got there')
            try:
                grabbed = gp.grab_random(player_color)
            except IndexError:
                moved_recently.clear()
                #player_color = next(cycler)
                #happens if it seems nothing can fill
                #the last remaining adjacent tile
                print('bah')
                
                for candidate in board.free_pieces(player_color):
                    for c in set(board.valid_moves(candidate)):
                        ply = Movement(candidate, c)
                        try:
                            board.validate(ply)
                        except IllegalMove:
                            continue
                        else:
                            move_made = True
                            break
                if move_made:
                    print(board.piece_at(ply.origin), ply)
                    moved_recently.append(board.piece_at(ply.origin))
                    try:
                        board.perform(ply)
                    except IllegalMove:
                        #why would this happen?
                        pass
                    finally:
                        player_color = next(cycler)
                    
            else:
                new_loc = random.choice(list(board.valid_placements(player_color)))
                placement_action = Placement(grabbed, new_loc)
                board.perform(placement_action)
                print(placement_action)
                player_color = next(cycler)
    
    print(board)
    print('winner', board.winner)

if __name__ == '__main__':
    #random_game()
    naive_ai()