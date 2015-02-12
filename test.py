import unittest
import hive

class TestHive(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_board(self):
        board = hive.HiveBoard()
        self.assertIs(board.tile_orientation, hive.Flat_Directions)
        
        board = hive.HiveBoard(hive.Flat_Directions)
        self.assertIs(board.tile_orientation, hive.Flat_Directions)
        
        board = hive.HiveBoard(hive.Pointed_Directions)
        self.assertIs(board.tile_orientation, hive.Pointed_Directions)
    
    def test_tiles(self):
        piece = hive.Tile(hive.Color.White, hive.Insect.Queen)
        
        self.assertEqual(piece.color, hive.Color.White)
        self.assertEqual(piece.insect, hive.Insect.Queen)
        
        self.assertEqual(piece, piece)
        
        piece2 = hive.Tile(hive.Color.Black, hive.Insect.Queen)
        self.assertNotEqual(piece, piece2)
        
    def test_place(self):
        board = hive.HiveBoard()
        
        t = hive.Tile(hive.Color.White, hive.Insect.Queen)
        
        board.place(t, (0,0))
        self.assertEqual(board.piece_at((0,0)).color, t.color)
        self.assertEqual(board.piece_at((0,0)).insect, t.insect)
        
        t2 = hive.Tile(hive.Color.Black, hive.Insect.Ant)

        with self.assertRaises(hive.IllegalMove) as e:
            board.place(t2, (0,0))
        self.assertEqual(e.exception.violation, hive.Violation.May_Not_Place_On_Other_Pieces)

    def test_piece_at(self):
        board = hive.HiveBoard()
        piece = hive.Tile(hive.Color.White, hive.Insect.Queen)
        
        board.place(piece, (0,0))
        self.assertEqual(board.piece_at((0,0)).color, hive.Color.White)
        self.assertEqual(board.piece_at((0,0)).insect, hive.Insect.Queen)
    
    def test_stack_at(self):
        board = hive.HiveBoard()
        
        pieces = {
            (0,0): 'wQ',
            (0,1): 'bQ',
            (0,-1): 'wB'   
        }
        
        board.quick_setup(pieces)
        board.move((0,-1), (0,0))

        self.assertEqual(board.stack_at((0,0)),
                         [hive.Tile(hive.Color.White, hive.Insect.Queen),
                          hive.Tile(hive.Color.White, hive.Insect.Beetle) ])
            
    def test_move(self):
        board = hive.HiveBoard()
        piece = hive.Tile(hive.Color.White, hive.Insect.Queen)
        
        board.place(piece, (0,0))
        board.move((0,0), (0,1))
        
        with self.assertRaises(KeyError):
            board.piece_at((0,0))
            
        self.assertEqual(board.piece_at((0,1)).color, hive.Color.White)
        self.assertEqual(board.piece_at((0,1)).insect, hive.Insect.Queen)
        
    def test_perform(self):
        board = hive.HiveBoard()
        
        t = hive.Tile(hive.Color.White, hive.Insect.Ant)
        p = hive.Placement(t, (0,0))
        
        board.perform(p)
        
        self.assertIsInstance(board._log[0], hive.Ply)
        self.assertEqual(board._log[0].tile, t)
        
        t2 = hive.Tile(hive.Color.Black, hive.Insect.Ant)
        p2 = hive.Placement(t2, (0,1))
        board.perform(p2)
        
        self.assertIsInstance(board._log[1], hive.Ply)
        self.assertEqual(board._log[1].tile, t2)
        
    def test_rule_movement_before_queen_placed(self):
        board = hive.HiveBoard()

        p = hive.Placement(hive.Tile(hive.Color.White, hive.Insect.Ant), (0,0))
        board.perform(p)
        
        p2 = hive.Placement(hive.Tile(hive.Color.Black, hive.Insect.Ant), (0,1))
        board.perform(p2)
        
        p3 = hive.Movement((0,0), (1,0))
        
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(p3)
        
        self.assertEqual(e.exception.violation, hive.Violation.No_Movement_Before_Queen_Bee_Placed)
            
    def test_rule_adjacency_to_opponent(self):
        board = hive.HiveBoard()
        
        p = hive.Placement(hive.Tile(hive.Color.White, hive.Insect.Ant), (0,0))
        board.perform(p)
        
        p2 = hive.Placement(hive.Tile(hive.Color.Black, hive.Insect.Ant), (0,1))
        board.perform(p2)
        
        t3 = hive.Tile(hive.Color.White, hive.Insect.Ant)
        p3_a = hive.Placement(t3, (0,2))
        
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(p3_a)
        
        self.assertEqual(e.exception.violation, hive.Violation.May_Not_Place_Adjacent)
            
        p3_b = hive.Placement(t3, (0,-1))
        board.perform(p3_b)
    
    def test_rule_placed_queen_by_fourth_action(self):
        board = hive.HiveBoard()
        
        p1 = hive.Placement(hive.Tile(hive.Color.White, hive.Insect.Ant), (0,0))
        p2 = hive.Placement(hive.Tile(hive.Color.Black, hive.Insect.Ant), (0,1))
        p3 = hive.Placement(hive.Tile(hive.Color.White, hive.Insect.Ant), (0,-1))
        p4 = hive.Placement(hive.Tile(hive.Color.Black, hive.Insect.Ant), (0,2))
        p5 = hive.Placement(hive.Tile(hive.Color.White, hive.Insect.Ant), (0,-2))
        p6 = hive.Placement(hive.Tile(hive.Color.Black, hive.Insect.Ant), (0,3))
        p7_a = hive.Placement(hive.Tile(hive.Color.White, hive.Insect.Spider), (0,-3))
        p7_b = hive.Placement(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,-3))
        p8_a = hive.Placement(hive.Tile(hive.Color.Black, hive.Insect.Spider), (0,4))
        p8_b = hive.Placement(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,4))
        
        for e in [p1, p2, p3, p4, p5, p6]:
            board.perform(e)

        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(p7_a)
        
        self.assertEqual(e.exception.violation, hive.Violation.Queen_Bee_Must_Be_Played)
        
        board.perform(p7_b)
        
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(p8_a)
        
        self.assertEqual(e.exception.violation, hive.Violation.Queen_Bee_Must_Be_Played)
        
        board.perform(p8_b)
        
    def test_special_rules_queen_opening_prohibited(self):
        '''tourney rules about queen not available on move 1'''
        board = hive.HiveBoard(queen_opening_allowed=False)
 
        p1_a = hive.Placement(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        
        with self.assertRaises(hive.IllegalMove):
            board.perform(p1_a)

        p1_z = hive.Placement(hive.Tile(hive.Color.White, hive.Insect.Ant), (0,0))
        board.perform(p1_z)
        
        p2_a = hive.Placement(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(p2_a)
        
        self.assertEqual(e.exception.violation, hive.Violation.Queen_Bee_Opening_Prohibited)
    
    def test_special_rules_queen_opening_permitted(self):
        '''tourney rules about queen not available on move 1'''
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        p1_a = hive.Placement(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.perform(p1_a)
        
        p2_a = hive.Placement(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        board.perform(p2_a)
        
    def test_ply_number_property(self):
        board = hive.HiveBoard()
        
        self.assertEqual(board.ply_number, 0)
        
        p = hive.Placement(hive.Tile(hive.Color.White, hive.Insect.Ant), (0,0))
        board.perform(p)
        
        self.assertEqual(board.ply_number, 1)
    
    def test_beetle_movement(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Beetle), (0,-1))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Spider), (0,2))

        p5 = hive.Movement((0,-1), (0,0))
        p6 = hive.Movement((0,2), (0,1))
        p7 = hive.Movement((0,0), (1,-1))
        
        board.perform(p5)
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(p6)
        
        self.assertEqual(e.exception.violation, hive.Violation.Insect_Cannot_Climb)
        
        board.perform(p7)
            
    def test_single_hex_movement_checked(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Beetle), (0,-1))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Spider), (0,2))
        
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Movement((0,-1), (0,2)))
        self.assertEqual(e.exception.violation, hive.Violation.Distance_Must_Be_Exactly_One)
        
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Movement((0,-1), (0,1)))
        self.assertEqual(e.exception.violation, hive.Violation.Distance_Must_Be_Exactly_One)
            
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Movement((0,-1), (0,-1)))
        self.assertEqual(e.exception.violation, hive.Violation.Did_Not_Move)
    
    def test_insect_did_move(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Beetle), (0,-1))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Spider), (0,2))

        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Movement((0,-1), (0,-1)))
        self.assertEqual(e.exception.violation, hive.Violation.Did_Not_Move)

    def test_board_quicksetup(self):
        board = hive.HiveBoard()
        
        pieces = {
            (0,0): 'wQ',
            (0,1): 'bQ'      
        }
        
        board.quick_setup(pieces)
        
        self.assertEqual(board.piece_at((0,0)).color, hive.Color.White)
        self.assertEqual(board.piece_at((0,0)).insect, hive.Insect.Queen)
        
        self.assertEqual(board.piece_at((0,1)).color, hive.Color.Black)
        self.assertEqual(board.piece_at((0,1)).insect, hive.Insect.Queen)

    def test_queen_valid_moves(self):
        board = hive.HiveBoard(queen_opening_allowed=True)

        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))

        self.assertSetEqual(set(board.valid_moves( (0,0) )),
                            set([(-1,1), (1,0)]))
                                 
    def test_beetle_valid_moves(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Beetle), (-1,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Beetle), (0,2))

        self.assertSetEqual(set(board.valid_moves( (-1,0) )),
                            set([(0,-1), (0,0), (-1,1)]))
                            
    def test_grasshopper_valid_moves(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Grasshopper), (-1,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Grasshopper), (0,2))
            
        self.assertSetEqual(set(board.valid_moves( (-1,0) )),
                            set([(1,0)]))
                            
        board.perform(hive.Movement((-1,0), (1,0)))
        
        self.assertSetEqual(set(board.valid_moves( (1,0) )),
                            set([(-1,0), (-1,2)]))
                            
    def test_ant_valid_moves(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Ant), (-1,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Ant), (0,2))
            
        self.assertSetEqual(set(board.valid_moves( (-1,0) )),
                            set([(0,-1), (1,-1), (1,0), (1,1),
                                 (1,2), (0,3), (-1,3), (-1,2), (-1,1)]))
    
    def test_spider_valid_moves(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Spider), (-1,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Spider), (0,2))
        
        self.assertSetEqual(set(board.valid_moves( (-1,0) )),
                            set([(-1,3), (1,0)]))
    
    def test_ladybug_valid_moves(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Ladybug), (-1,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Ladybug), (0,2))

        self.assertSetEqual(set(board.valid_moves( (-1,0) )),
                            set([(-1,1), (-1,2), (1,0), (1,1)]))
    
    def test_pillbug_valid_moves(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Pillbug), (-1,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Pillbug), (0,2))
        
        self.assertSetEqual(set(board.valid_moves( (-1,0) )),
                            set([(0,-1), (-1,1)]))
        
    def test_pillbug_forced_relocation(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Pillbug), (-1,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Pillbug), (0,2))

        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Relocation((0,0), (-1,1), (-1,0)))
        self.assertEqual(e.exception.violation, hive.Violation.One_Hive_Rule)
        
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Relocation((0,0), (0,-1), (-1,0)))
        self.assertEqual(e.exception.violation, hive.Violation.One_Hive_Rule)

        board.move((-1,0), (-1,2)) #illegal move for the sake of brevity
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Relocation((0,2), (5,5), (-1,2)))
        self.assertEqual(e.exception.violation, hive.Violation.Pillbug_Adjacent)
        
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Relocation((0,2), (0,1), (-1,2)))
        self.assertEqual(e.exception.violation, hive.Violation.Pillbug_Cannot_Touch_Stacks)
        
        board.perform(hive.Relocation((0,2), (-2,2), (-1,2)))
        
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Beetle), (-2,1))
        board.move((-2,1), (-2,2))
        
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Relocation((-2,2), (-2,3), (-1,2)))
        self.assertEqual(e.exception.violation, hive.Violation.Pillbug_Cannot_Touch_Stacks)

        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Relocation((0,-1), (1,0), (0,1)))
        self.assertEqual(e.exception.violation, hive.Violation.Unavailable_Action)
        
    def test_mosquito_leech_relocate(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        pb = hive.Tile(hive.Color.White, hive.Insect.Pillbug)
        board.place(pb, (-1,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Ant), (0,2))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Mosquito), (0,-1))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Mosquito), (0,3))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Spider), (-1,3))

        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Relocation((-1,3), (1,2), (0,3), (0,2)))
        self.assertEqual(e.exception.violation, hive.Violation.Unavailable_Action)

        board.perform(hive.Relocation((-1,0), (1,-1), (0,-1), (-1,0)))
        self.assertEqual(board._pieces[(1,-1)][0], pb)

        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Relocation((-1,3), (1,2), (0,3), (1,-1)))
        self.assertEqual(e.exception.violation, hive.Violation.Mosquito_Adjacent)
        
    def test_mosquito_leech_move(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Mosquito), (-1,0))

        self.assertSetEqual(set(board.valid_moves( (-1,0) )),
                            set([(0,-1), (-1,1)]))
        
        board.place(hive.Tile(hive.Color.White, hive.Insect.Ant), (0,-1))

        self.assertSetEqual(set(board.valid_moves( (-1,0) )),
                            set([(-1,-1), (0,-2), (1,-2), (1,-1), (1,0), 
                                 (1,1), (0,2), (-1,2), (-1,1)]))

        board.place(hive.Tile(hive.Color.Black, hive.Insect.Mosquito), (-1,-1))
        
        self.assertSetEqual(set(board.valid_moves( (-1,-1) )),
                            set([(0,-2), (1,-2), (1,-1), (1,0), 
                                 (1,1), (0,2), (-1,2), (-1,1),
                                 (-2,1), (-2,0)]))
                                 
    def test_mosquito_leech_climb(self):
        board = hive.HiveBoard()
        
        pieces = {
            (0,0): 'wQ',
            (0,1): 'bQ',
            (0,-1): 'wB',
            (0,-2): 'bM'  
        }
        
        board.quick_setup(pieces)
        
        p = hive.Movement((0,-2), (0,-1), (0,-1))
        board.perform(p)
        
        self.assertEqual(board.stack_at((0,-1)),
                         [hive.Tile(hive.Color.White, hive.Insect.Beetle),
                          hive.Tile(hive.Color.Black, hive.Insect.Mosquito)])
                            
    def test_valid_path(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Spider), (0,-1))

        #testing spider
        self.assertEqual(board.valid_path((0,-1), (-1,2)),
                         [(0,-1), (-1,0), (-1,1), (-1,2)])
        self.assertEqual(board.valid_path((0,-1), (1,1)),
                         [(0,-1), (1,-1), (1,0), (1,1)])
        
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Beetle), (0,2))
        #testing beetle
        self.assertEqual(board.valid_path((0,2), (-1,2)),
                         [(0,2), (-1,2)])
        self.assertEqual(board.valid_path((0,2), (1,1)),
                         [(0,2), (1,1)])
        self.assertEqual(board.valid_path((0,2), (0,1)),
                         [(0,2), (0,1)])
        
        #testing queen
        self.assertEqual(board.valid_path((0,0), (-1,0)),
                         [(0,0), (-1,0)])
        self.assertEqual(board.valid_path((0,0), (1,-1)),
                         [(0,0), (1,-1)])
        self.assertEqual(board.valid_path((0,0), (1,0)),
                         [(0,0), (1,0)])
        
        board.place(hive.Tile(hive.Color.White, hive.Insect.Ant), (0,-2))
        #testing ant
        self.assertEqual(board.valid_path((0,-2), (-1,1)),
                         [(0,-2), (-1,-1), (-1,0), (-1,1)])
        self.assertEqual(board.valid_path((0,-2), (1,0)),
                         [(0,-2), (1,-2), (1,-1), (1,0)])
        
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Grasshopper), (1,1))
        #testing grasshopper
        self.assertEqual(board.valid_path((1,1), (-1,1)),
                         [(1,1), (0,1), (-1,1)])
        self.assertEqual(board.valid_path((1,1), (-1,3)),
                         [(1,1), (0,2), (-1,3)])

        board.place(hive.Tile(hive.Color.White, hive.Insect.Ladybug), (0,-3))
        
        self.assertEqual(board.valid_path((0,-3), (-1,0)),
                         [(0,-3), (0,-2), (0,-1), (-1,0)])
        self.assertEqual(board.valid_path((0,-3), (1,-1)),
                         [(0,-3), (0,-2), (0,-1), (1,-1)])
        
        #testing pillbug
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Pillbug), (0,3))
        self.assertEqual(board.valid_path((0,3), (1,0)),
                         [(0,3), (1,2), (2,1), (2,0), (1,0)])
        self.assertEqual(board.valid_path((0,3), (-1,0)),
                         [(0,3), (-1,3), (-1,2), (-1,1), (-1,0)])
    
    def test_invalid_paths(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        pieces = {
            (0,0): 'wQ',
            (0,1): 'bQ',
            (1,-1): 'wB',
            (1,1): 'bM',
            (2,-1): 'wG',
            (2,0): 'bG',
            (0,-1): 'wA'
        }
        
        board.quick_setup(pieces)
        
        with self.assertRaises(hive.IllegalMove) as e:
            board.valid_path((0,-1), (1,0))
        self.assertEqual(e.exception.violation, hive.Violation.Freedom_of_Movement)
        
    def test_spider_three_space_limit(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        pieces = {
            (0,0): 'wQ',
            (0,1): 'bQ',
            (-1,-1): 'bS',
            (0,-1): 'wA',
            (0,2): 'bA'
        }
        
        board.quick_setup(pieces)
        
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Movement((-1,-1), (-1,3)))
        self.assertEqual(e.exception.violation, hive.Violation.Invalid_Distance_Attempted)
        
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        pieces = {
            (0,0): 'wQ',
            (0,1): 'bQ',
            (-1,0): 'bS',
            (0,-1): 'wA',
            (-1,-1): 'bA'
        }
        
        board.quick_setup(pieces)
        board.perform(hive.Movement((-1,0), (-1,-2)))
    
    def test_not_isolated(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        pieces = {
            (0,0): 'wQ',
            (0,1): 'bQ',
            (0,-1): 'wA',
            (-1,-1): 'bA'
        }
        
        board.quick_setup(pieces)

        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Movement((-1,-1), (-1,-2)))
        self.assertEqual(e.exception.violation, hive.Violation.One_Hive_Rule)
    
            
    def test_invalid_paths_physical_slide(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        pieces = {
            (0,0): 'wQ',
            (0,1): 'bQ',
            (1,-1): 'wB',
            (1,1): 'bM',
            (2,0): 'bG',
            (0,-1): 'wA'
        }
        
        board.quick_setup(pieces)

        with self.assertRaises(hive.IllegalMove) as e:
            board.valid_path((0,-1), (1,0))
        self.assertEqual(e.exception.violation, hive.Violation.Freedom_of_Movement)
    
    def test_beetle_jump_gaps(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        pieces = {
            (0,0): 'wQ',
            (0,1): 'bQ',
            (1,-1): 'wB',
            (1,1): 'bM',
            (2,0): 'bB',
            (0,-1): 'wA'
        }
        
        board.quick_setup(pieces)
        
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Movement((2,0), (2,-1)))
        
        self.assertEqual(e.exception.violation, hive.Violation.Cannot_Jump_Gaps)
    
    def test_queen_jump_gaps(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        pieces = {
            (0,0): 'wQ',
            (0,1): 'bQ',
            (1,-1): 'wB',
            (2,-1): 'bM',
            (2,0): 'bB',
            (0,-1): 'wA'
        }
        
        board.quick_setup(pieces)

        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Movement((0,1), (1,1)))
        
        self.assertEqual(e.exception.violation, hive.Violation.Cannot_Jump_Gaps)

    def test_valid_placements(self):
        board = hive.HiveBoard()
        
        pieces = {
            (0,0): 'wQ',
            (0,1): 'bQ',
            (0,-1): 'wB',
            (0,2): 'bM'  
        }
        
        board.quick_setup(pieces)
        
        self.assertEqual(board.valid_placements(hive.Color.White),
                         set([(-1,0), (-1,-1), (0,-2), (1,-2), (1,-1)]))
        self.assertEqual(board.valid_placements(hive.Color.Black),
                         set([(-1,2), (-1,3), (0,3), (1,2), (1,1)]))

    def test_freedom_of_movement(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Spider), (1,-1))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Spider), (1,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Ant), (2,-1))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Ant), (0,2))

        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Movement((0,2), (1,0)))
        self.assertEqual(e.exception.violation, hive.Violation.Freedom_of_Movement)

    def test_beetle_gate_restriction(self):
        #http://www.boardgamegeek.com/thread/332467/how-are-beetles-affected-sliding-rule-when-crawlin
    
        board = hive.HiveBoard(queen_opening_allowed=True)
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Spider), (1,-1))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Spider), (1,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Ant), (2,-1))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Beetle), (2,0))

        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Movement((2,0), (1,0)))
        self.assertEqual(e.exception.violation, hive.Violation.Freedom_of_Movement)
        
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Ant), (1,0))
        board.perform(hive.Movement((2,0), (1,0)))
    
    def test_one_hive_rule_move(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Spider), (1,-1))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Spider), (1,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Ant), (2,-1))

        self.assertTrue(board.one_hive_rule())
        
        board.move((1,-1), (1,2))
        self.assertFalse(board.one_hive_rule())
        board.move((1,2), (1,-1))

        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Movement((1,-1), (2,-2)))
        self.assertEqual(e.exception.violation, hive.Violation.One_Hive_Rule)
        
    def test_one_hive_rule_place(self):
        board = hive.HiveBoard()
        
        t1 = hive.Tile(hive.Color.White, hive.Insect.Ant)
        p1 = hive.Placement(t1, (0,0))

        t2 = hive.Tile(hive.Color.Black, hive.Insect.Ant)
        p2 = hive.Placement(t2, (0,1))

        t3 = hive.Tile(hive.Color.White, hive.Insect.Ant)
        p3 = hive.Placement(t3, (4,4))
        
        board.perform(p1)
        board.perform(p2)
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(p3)
            
        self.assertEqual(e.exception.violation, hive.Violation.One_Hive_Rule)
        
    def test_free_pieces(self):
        board = hive.HiveBoard()
        self.assertIsNone(board.winner)
        
        pieces = {
            (0,0): 'wQ',
            (0,1): 'bQ',
            (0,-1): 'wB',
            (0,2): 'bM'  
        }
        
        board.quick_setup(pieces)
        
        self.assertEqual(set(board.free_pieces(hive.Color.White)), {(0,-1)})
        self.assertEqual(set(board.free_pieces(hive.Color.Black)), {(0,2)})
        
    def test_winner_found(self):
        board = hive.HiveBoard()
        self.assertIsNone(board.winner)
        
        pieces = {
            (0,0): 'wQ',
            (0,1): 'bQ',
            (0,-1): 'wB',
            (0,-2): 'bM'  
        }
        
        board.quick_setup(pieces)
        self.assertIsNone(board.winner)
        
        pieces = {
            (1,0): 'wA',
            (1,1): 'bA',
            (0,2): 'wB',
            (-1,2): 'bB',
            (-1,1): 'bG'
        }
        
        board.quick_setup(pieces)
        self.assertEqual(board.winner, hive.Color.White)
        
        pieces = {
            (1,-1): 'wA',
            (-1,0): 'bA'
        }
        
        board.quick_setup(pieces)
        self.assertFalse(board.winner)
    
    def test_can_act(self):
        board = hive.HiveBoard()
        self.assertTrue(board.can_act(hive.Color.White))
        self.assertTrue(board.can_act(hive.Color.Black))
        
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        
        self.assertFalse(board.can_act(hive.Color.White))
        self.assertTrue(board.can_act(hive.Color.Black))
        
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        
        self.assertTrue(board.can_act(hive.Color.White))
        self.assertTrue(board.can_act(hive.Color.Black))
                         
    def test_get_direction(self):
        self.assertEqual(hive.HiveBoard.get_direction((0,0), (-1,0), hive.Flat_Directions), hive.Flat_Directions.NW)
        self.assertEqual(hive.HiveBoard.get_direction((0,0), (1,-1), hive.Flat_Directions), hive.Flat_Directions.NE)
        
        with self.assertRaises(RuntimeError):
            hive.HiveBoard.get_direction((0,0), (-3,0), hive.Flat_Directions)
        with self.assertRaises(RuntimeError):
            hive.HiveBoard.get_direction((0,0), (1,-3), hive.Flat_Directions)

    def test_hex_distance(self):
        self.assertEqual(hive.HiveBoard.hex_distance((0,0), (0,1)), 1)
        self.assertEqual(hive.HiveBoard.hex_distance((0,0), (-1,1)), 1)
        self.assertEqual(hive.HiveBoard.hex_distance((0,0), (-5,5)), 5)
        self.assertEqual(hive.HiveBoard.hex_distance((0,0), (5,-5)), 5)
        self.assertEqual(hive.HiveBoard.hex_distance((0,0), (2,-3)), 3)
    
    def test_radius(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        self.assertEqual(board.radius, 0)
        
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        self.assertEqual(board.radius, 1)
        
        board.place(hive.Tile(hive.Color.White, hive.Insect.Spider), (0,-1))
        self.assertEqual(board.radius, 1)
        
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Spider), (0,2))
        self.assertEqual(board.radius, 2)

        board.place(hive.Tile(hive.Color.Black, hive.Insect.Spider), (1,0))
        self.assertEqual(board.radius, 2)

    def test_go_direction(self):
        board = hive.HiveBoard(hive.Flat_Directions)
        self.assertEqual(board.go_direction((0,0), hive.Flat_Directions.N), (0,-1))
        self.assertEqual(board.go_direction((0,0), hive.Flat_Directions.NE), (1,-1))
        self.assertEqual(board.go_direction((0,0), hive.Flat_Directions.SE), (1,0))
        self.assertEqual(board.go_direction((0,0), hive.Flat_Directions.S), (0,1))
        self.assertEqual(board.go_direction((0,0), hive.Flat_Directions.SW), (-1,1))
        self.assertEqual(board.go_direction((0,0), hive.Flat_Directions.NW), (-1,0))
        
    def test_hex_neighbors(self):
        board = hive.HiveBoard(hive.Flat_Directions)
        self.assertSetEqual(board.hex_neighbors(board.tile_orientation, (0,0)),
                            set([(0,-1), (1,-1), (1,0), 
                                 (0,1), (-1,1), (-1,0)]))
                                 
    def test_find_tiles(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        pieces = {
            (0,0): 'wQ',
            (0,1): 'bQ',
            (0,-1): 'wB',
            (0,-2): 'bM'  
        }
        
        board.quick_setup(pieces)
        self.assertEqual(dict(board.find(hive.Color.White, hive.Insect.Queen)),
                         {(0,0): {0}})
        self.assertEqual(dict(board.find(hive.Color.Black, hive.Insect.Mosquito)),
                         {(0,-2): {0}})
        self.assertEqual(dict(board.find(hive.Color.Black, hive.Insect.Ant)), {})
        
        board.quick_setup({(0,-3): 'wB'})
        
        self.assertEqual(dict(board.find(hive.Color.White, hive.Insect.Beetle)),
                         {
                          (0,-1): {0},
                          (0,-3): {0}
                         })
        
        board.move((0,-3), (0,-2))
        board.move((0,-2), (0,-1))
        
        self.assertEqual(dict(board.find(hive.Color.White, hive.Insect.Beetle)),
                         {(0,-1): {0, 1}})
    
    def test_neighbors(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        pieces = {
            (0,0): 'wQ',
            (0,1): 'bQ',
            (0,-1): 'wB'
        }
        
        board.quick_setup(pieces)
        
        self.assertDictEqual(dict(board.neighbors((0,0))), 
                             {
                                 (0,-1): hive.Tile(hive.Color.White,
                                                   hive.Insect.Beetle),
                                 (1,-1): None,
                                 (1,0): None,
                                 (0,1): hive.Tile(hive.Color.Black,
                                                  hive.Insect.Queen),
                                 (-1,1): None,
                                 (-1,0): None
                             })


if __name__ == '__main__':
    unittest.main()