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
            
    def test_pop(self):
        board = hive.HiveBoard()
        t = hive.Tile(hive.Color.White, hive.Insect.Queen)
        
        with self.assertRaises(KeyError):
            board.pop((0,0))
        
        board.place(t, (0,0))
        p = board.pop((0,0))
        
        self.assertIs(t, p)
        
        with self.assertRaises(KeyError):
            board.piece_at((0,0))

        with self.assertRaises(KeyError):
            board.pop((0,0))

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
        
        with self.assertRaises(hive.IllegalMovement):
            board.perform(p3)
            
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
        
        with self.assertRaises(hive.IllegalPlacement):
            board.perform(p3_a)
            
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
        
        board.perform(p1)
        board.perform(p2)
        board.perform(p3)
        board.perform(p4)
        board.perform(p5)
        board.perform(p6)
        with self.assertRaises(hive.IllegalPlacement):
            board.perform(p7_a)
        
        board.perform(p7_b)
        
        with self.assertRaises(hive.IllegalPlacement):
            board.perform(p8_a)
        
        board.perform(p8_b)
        
    def test_special_rules_queen_opening_prohibited(self):
        '''tourney rules about queen not available on move 1'''
        board = hive.HiveBoard(queen_opening_allowed=False)
        
        t1_a = hive.Tile(hive.Color.White, hive.Insect.Queen)
        p1_a = hive.Ply(hive.Rule.Place, t1_a, None, (0,0))
        
        with self.assertRaises(hive.IllegalPlacement):
            board.perform(p1_a)
            
        t1_z = hive.Tile(hive.Color.White, hive.Insect.Ant)
        p1_z = hive.Ply(hive.Rule.Place, t1_z, None, (0,0))
        
        board.perform(p1_z)
        
        t2_a = hive.Tile(hive.Color.Black, hive.Insect.Queen)
        p2_a = hive.Ply(hive.Rule.Place, t2_a, None, (0,1))
        
        with self.assertRaises(hive.IllegalPlacement):
            board.perform(p2_a)
    
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
    
    def test_only_beetles_can_climb(self):
        board = hive.HiveBoard(queen_opening_allowed=True)
        
        t = hive.Tile(hive.Color.White, hive.Insect.Queen)
        p = hive.Ply(hive.Rule.Place, t, None, (0,0))
        t2 = hive.Tile(hive.Color.Black, hive.Insect.Queen)
        p2 = hive.Ply(hive.Rule.Place, t2, None, (0,1))
        t3 = hive.Tile(hive.Color.White, hive.Insect.Beetle)
        p3 = hive.Ply(hive.Rule.Place, t3, None, (0,-1))
        t4 = hive.Tile(hive.Color.Black, hive.Insect.Spider)
        p4 = hive.Ply(hive.Rule.Place, t4, None, (0,2))
        
        for e in [p, p2, p3, p4]:
            board.perform(e)

        p5 = hive.Ply(hive.Rule.Move, None, (0,-1), (0,0))
        p6 = hive.Ply(hive.Rule.Move, None, (0,2), (0,1))
        
        board.perform(p5)
        with self.assertRaises(hive.IllegalMovement):
            board.perform(p6)
            
    def test_hex_distance(self):
        self.assertEqual(hive.HiveBoard.hex_distance((0,0), (0,1)), 1)
        self.assertEqual(hive.HiveBoard.hex_distance((0,0), (-1,1)), 1)
        self.assertEqual(hive.HiveBoard.hex_distance((0,0), (-5,5)), 5)
        self.assertEqual(hive.HiveBoard.hex_distance((0,0), (5,-5)), 5)
        self.assertEqual(hive.HiveBoard.hex_distance((0,0), (2,-3)), 3)
        
    def test_hex_neighbors(self):
        board = hive.HiveBoard(hive.Flat_Directions)
        self.assertSetEqual(board.hex_neighbors(board.tile_orientation, (0,0)),
                            set([(0,-1), (1,-1), (1,0), 
                                 (0,1), (-1,1), (-1,0)]))

if __name__ == '__main__':
    unittest.main()