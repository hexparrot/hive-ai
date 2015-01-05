import unittest
import hive

class TestHive(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_board(self):
        board = hive.HiveBoard()
        self.assertEqual(len(board), 0)
    
    def test_tiles(self):
        piece = hive.Tile(hive.Color.White, hive.Insect.Queen)
        
        self.assertEqual(piece.color, hive.Color.White)
        self.assertEqual(piece.insect, hive.Insect.Queen)
        
    def test_place(self):
        board = hive.HiveBoard()
        piece = hive.Tile(hive.Color.White, hive.Insect.Queen)
        
        board.place(piece, (0,0) )
        self.assertEqual(board.piece_at((0,0)).color, hive.Color.White)
        self.assertEqual(board.piece_at((0,0)).insect, hive.Insect.Queen)
        
        piece_2 = hive.Tile(hive.Color.Black, hive.Insect.Ant)
        with self.assertRaises(RuntimeError):
            board.place(piece_2, (0,0) )
            
    def test_pop(self):
        board = hive.HiveBoard()
        piece = hive.Tile(hive.Color.White, hive.Insect.Queen)
        
        board.place(piece, (0,0) )
        p = board.pop( (0,0) )
        
        self.assertIs(piece, p)
        
        with self.assertRaises(KeyError):
            board.piece_at( (0,0) )

    def test_piece_at(self):
        board = hive.HiveBoard()
        piece = hive.Tile(hive.Color.White, hive.Insect.Queen)
        
        board.place(piece, (0,0) )
        self.assertEqual(board.piece_at((0,0)).color, hive.Color.White)
        self.assertEqual(board.piece_at((0,0)).insect, hive.Insect.Queen)
    
    def test_stack_at(self):
        board = hive.HiveBoard()
        piece = hive.Tile(hive.Color.White, hive.Insect.Queen)
        piece_2 = hive.Tile(hive.Color.Black, hive.Insect.Ant)

        board.place(piece, (0,0) )
        with self.assertRaises(RuntimeError):
            board.place(piece_2, (0,0) )

if __name__ == '__main__':
    unittest.main()