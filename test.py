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
        
    def test_place(self):
        board = hive.HiveBoard()
        
        t = hive.Tile(hive.Color.White, hive.Insect.Queen)
        
        board.place(t, (0,0))
        self.assertEqual(board.piece_at((0,0)).color, t.color)
        self.assertEqual(board.piece_at((0,0)).insect, t.insect)
        
        t2 = hive.Tile(hive.Color.Black, hive.Insect.Ant)

        with self.assertRaises(RuntimeError):
            board.place(t2, (0,0))

    def test_piece_at(self):
        board = hive.HiveBoard()
        piece = hive.Tile(hive.Color.White, hive.Insect.Queen)
        
        board.place(piece, (0,0))
        self.assertEqual(board.piece_at((0,0)).color, hive.Color.White)
        self.assertEqual(board.piece_at((0,0)).insect, hive.Insect.Queen)
    
    def test_stack_at(self):
        board = hive.HiveBoard()
        piece = hive.Tile(hive.Color.White, hive.Insect.Queen)
        piece_2 = hive.Tile(hive.Color.Black, hive.Insect.Ant)

        board.place(piece, (0,0))
        with self.assertRaises(RuntimeError):
            board.place(piece_2, (0,0))
            
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
        p = hive.Ply(hive.Rule.Place, t, None, (0,0))
        
        board.perform(p)
        
        self.assertIsInstance(board._log[0], hive.Ply)
        self.assertEqual(board._log[0].tile, t)
        
        t2 = hive.Tile(hive.Color.Black, hive.Insect.Ant)
        p2 = hive.Ply(hive.Rule.Place, t2, None, (0,1))
        board.perform(p2)
        
        self.assertIsInstance(board._log[1], hive.Ply)
        self.assertEqual(board._log[1].tile, t2)
        
    def test_rule_movement_before_queen_placed(self):
        board = hive.HiveBoard()

        t = hive.Tile(hive.Color.White, hive.Insect.Ant)
        p = hive.Ply(hive.Rule.Place, t, None, (0,0))
        board.perform(p)
        
        t2 = hive.Tile(hive.Color.Black, hive.Insect.Ant)
        p2 = hive.Ply(hive.Rule.Place, t2, None, (0,1))
        board.perform(p2)
        
        p3 = hive.Ply(hive.Rule.Move, None, (0,0), (1,0))
        
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(p3)
        
        self.assertEqual(e.exception.violation, hive.Violation.No_Movement_Before_Queen_Bee_Placed)
            
    def test_rule_adjacency_to_opponent(self):
        board = hive.HiveBoard()
        
        t = hive.Tile(hive.Color.White, hive.Insect.Ant)
        p = hive.Ply(hive.Rule.Place, t, None, (0,0))
        board.perform(p)
        
        t2 = hive.Tile(hive.Color.Black, hive.Insect.Ant)
        p2 = hive.Ply(hive.Rule.Place, t2, None, (0,1))
        board.perform(p2)
        
        t3 = hive.Tile(hive.Color.White, hive.Insect.Ant)
        p3_a = hive.Ply(hive.Rule.Place, t3, None, (0,2))
        
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(p3_a)
        
        self.assertEqual(e.exception.violation, hive.Violation.May_Not_Place_Adjacent)
            
        p3_b = hive.Ply(hive.Rule.Place, t3, None, (0,-1))
        board.perform(p3_b)
    
    def test_rule_placed_queen_by_fourth_action(self):
        board = hive.HiveBoard()
        
        t1 = hive.Tile(hive.Color.White, hive.Insect.Ant)
        p1 = hive.Ply(hive.Rule.Place, t1, None, (0,0))

        t2 = hive.Tile(hive.Color.Black, hive.Insect.Ant)
        p2 = hive.Ply(hive.Rule.Place, t2, None, (0,1))

        t3 = hive.Tile(hive.Color.White, hive.Insect.Ant)
        p3 = hive.Ply(hive.Rule.Place, t3, None, (0,-1))
        
        t4 = hive.Tile(hive.Color.Black, hive.Insect.Ant)
        p4 = hive.Ply(hive.Rule.Place, t4, None, (0,2))

        t5 = hive.Tile(hive.Color.White, hive.Insect.Ant)
        p5 = hive.Ply(hive.Rule.Place, t5, None, (0,-2))
        
        t6 = hive.Tile(hive.Color.Black, hive.Insect.Ant)
        p6 = hive.Ply(hive.Rule.Place, t6, None, (0,3))
        
        t7_a = hive.Tile(hive.Color.White, hive.Insect.Spider)
        p7_a = hive.Ply(hive.Rule.Place, t7_a, None, (0,-3))
        
        t7_b = hive.Tile(hive.Color.White, hive.Insect.Queen)
        p7_b = hive.Ply(hive.Rule.Place, t7_b, None, (0,-3))
        
        t8_a = hive.Tile(hive.Color.Black, hive.Insect.Spider)
        p8_a = hive.Ply(hive.Rule.Place, t8_a, None, (0,4))
        
        t8_b = hive.Tile(hive.Color.Black, hive.Insect.Queen)
        p8_b = hive.Ply(hive.Rule.Place, t8_b, None, (0,4))
        
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
        
        t1_a = hive.Tile(hive.Color.White, hive.Insect.Queen)
        p1_a = hive.Ply(hive.Rule.Place, t1_a, None, (0,0))
        
        with self.assertRaises(hive.IllegalMove):
            board.perform(p1_a)
            
        t1_z = hive.Tile(hive.Color.White, hive.Insect.Ant)
        p1_z = hive.Ply(hive.Rule.Place, t1_z, None, (0,0))
        
        board.perform(p1_z)
        
        t2_a = hive.Tile(hive.Color.Black, hive.Insect.Queen)
        p2_a = hive.Ply(hive.Rule.Place, t2_a, None, (0,1))
        
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(p2_a)
        
        self.assertEqual(e.exception.violation, hive.Violation.Queen_Bee_Opening_Prohibited)
    
    def test_special_rules_queen_opening_permitted(self):
        '''tourney rules about queen not available on move 1'''
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        t1_a = hive.Tile(hive.Color.White, hive.Insect.Queen)
        p1_a = hive.Ply(hive.Rule.Place, t1_a, None, (0,0))
        board.perform(p1_a)
        
        t2_a = hive.Tile(hive.Color.Black, hive.Insect.Queen)
        p2_a = hive.Ply(hive.Rule.Place, t2_a, None, (0,1))
        board.perform(p2_a)
        
    def test_ply_number_property(self):
        board = hive.HiveBoard()
        
        self.assertEqual(board.ply_number, 0)
        
        t = hive.Tile(hive.Color.White, hive.Insect.Ant)
        p = hive.Ply(hive.Rule.Place, t, None, (0,0))
        board.perform(p)
        
        self.assertEqual(board.ply_number, 1)
    
    def test_beetle_movement(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Beetle), (0,-1))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Spider), (0,2))

        p5 = hive.Ply(hive.Rule.Move, None, (0,-1), (0,0))
        p6 = hive.Ply(hive.Rule.Move, None, (0,2), (0,1))
        p7 = hive.Ply(hive.Rule.Move, None, (0,0), (1,-1))
        
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
            board.perform(hive.Ply(hive.Rule.Move, None, (0,-1), (0,2)))
        self.assertEqual(e.exception.violation, hive.Violation.Distance_Must_Be_Exactly_One)
        
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Ply(hive.Rule.Move, None, (0,-1), (0,1)))
        self.assertEqual(e.exception.violation, hive.Violation.Distance_Must_Be_Exactly_One)
            
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Ply(hive.Rule.Move, None, (0,-1), (0,-1)))
        self.assertEqual(e.exception.violation, hive.Violation.Did_Not_Move)
    
    def test_insect_did_move(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Beetle), (0,-1))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Spider), (0,2))

        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Ply(hive.Rule.Move, None, (0,-1), (0,-1)))
        self.assertEqual(e.exception.violation, hive.Violation.Did_Not_Move)

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
                            
        board.perform(hive.Ply(hive.Rule.Move, None, (-1,0), (1,0)))
        
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

    def test_freedom_of_movement(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Queen), (0,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Spider), (1,-1))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Spider), (1,1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Ant), (2,-1))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Ant), (0,2))
        
        with self.assertRaises(hive.IllegalMove) as e:
            board.perform(hive.Ply(hive.Rule.Move, None, (0,2), (1,0)))
        self.assertEqual(e.exception.violation, hive.Violation.Freedom_of_Movement)
        
        #test grasshopper
        board.place(hive.Tile(hive.Color.White, hive.Insect.Grasshopper), (-1,2))
        board.perform(hive.Ply(hive.Rule.Move, None, (-1,2), (1,0)))
        board.perform(hive.Ply(hive.Rule.Move, None, (1,0), (-1,2)))
        
        #test beetle
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Beetle), (2,0))
        board.perform(hive.Ply(hive.Rule.Move, None, (2,0), (1,0)))
                         
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

if __name__ == '__main__':
    unittest.main()