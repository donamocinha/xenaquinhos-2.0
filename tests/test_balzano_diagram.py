import  unittest
from domain import TonalSystemElement, BalzanoDiagram

class TestBalzanoDiagram(unittest.TestCase):

    #preparacenario    
    def setUp(self):
        self.b1 = BalzanoDiagram(12, TonalSystemElement(3,12), TonalSystemElement(4, 12))
    
    def test_build_matrix(self):
        m = [[0, 4, 8, 0],
                [3, 7, 11, 3],
                [6, 10, 2, 6],
                [9, 1, 5, 9],
                [0, 4, 8, 0]]
        
        el_matrix = [[TonalSystemElement(e, 12) for e in row] for row in m]
        self.assertEqual(el_matrix, self.b1.matrix)
  
if __name__ == '__main__':  
    unittest.main()  