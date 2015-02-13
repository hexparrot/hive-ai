import unittest
import hive, ai

class TestHive(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_board(self):
        board = hive.HiveBoard()
        hivemind = ai.HiveAI(board)
        
        self.assertIs(board, hivemind.board)
        
    def test_opponent_queen(self):
        board = hive.HiveBoard()
        hivemind = ai.HiveAI(board)
        
        self.assertIsNone(hivemind.opponent_queen(hive.Color.Black))
        self.assertIsNone(hivemind.opponent_queen(hive.Color.White))
        
        pieces = {
            (0,0): 'wQ',
            (0,1): 'bQ'
        }
        
        board.quick_setup(pieces)
        
        self.assertEqual(hivemind.opponent_queen(hive.Color.Black), (0,0) )
        self.assertEqual(hivemind.opponent_queen(hive.Color.White), (0,1) )
    
    def test_empty_hexes_surrounding(self):
        board = hive.HiveBoard()
        hivemind = ai.HiveAI(board)

        pieces = {
            (0,0): 'wQ',
            (0,1): 'bQ'
        }
        
        board.quick_setup(pieces)
        print(board)
        
        self.assertEqual(set(hivemind.empty_hexes_surrounding((0,0))), 
                         { (1,0), (1,-1), (0,-1), (-1,0), (-1,1) })

if __name__ == '__main__':
    unittest.main()