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
        
        with self.assertRaises(KeyError): 
            board[(0,0)]
    
    def test_tiles(self):
        piece = hive.Tile(hive.Color.White, hive.Insect.Queen)
        
        self.assertEqual(piece.color, hive.Color.White)
        self.assertEqual(piece.insect, hive.Insect.Queen)
        
    def test_place(self):
        board = hive.HiveBoard()
        piece = hive.Tile(hive.Color.White, hive.Insect.Queen)
        
        board.place(piece, (0,0) )
        self.assertIsInstance(board[(0,0)], hive.Tile)
        self.assertEqual(board[(0,0)].color, hive.Color.White)
        self.assertEqual(board[(0,0)].insect, hive.Insect.Queen)
        
        piece_2 = hive.Tile(hive.Color.Black, hive.Insect.Ant)
        board.place(piece_2, (0,0) )
        self.assertIsInstance(board[(0,0)], hive.Tile)
        self.assertEqual(board[(0,0)].color, hive.Color.Black)
        self.assertEqual(board[(0,0)].insect, hive.Insect.Ant)

if __name__ == '__main__':
    unittest.main()