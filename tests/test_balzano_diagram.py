import  unittest
from domain import TonalSystemElement, BalzanoDiagram, Scale

class TestBalzanoDiagram(unittest.TestCase):

    #preparacenario    
    def setUp(self):
        self.b1 = BalzanoDiagram(12, TonalSystemElement(3,12), TonalSystemElement(4, 12))
        self.diatonic_struct = [2, 2, 1, 2, 2, 2, 1]
    
    def test_build_matrix(self):
        m = [[2, 6, 10, 2],
                [5, 9, 1, 5],
                [8, 0, 4, 8],
                [11, 3, 7, 11],
                [2, 6, 10, 2]]
        
        el_matrix = [[TonalSystemElement(e, 12) for e in row] for row in m]
        self.assertEqual(el_matrix, self.b1.matrix)
    
    def test_contains_scale(self):
        diatonic = Scale(12, tuple(self.diatonic_struct), tonic=6)
        self.assertTrue(self.b1.contains_scale(diatonic))

        rotated_scale = Scale(12, tuple(self.diatonic_struct[:2]+self.diatonic_struct[2:]))
        self.assertTrue(self.b1.contains_scale(rotated_scale))
  
if __name__ == '__main__':  
    unittest.main()  