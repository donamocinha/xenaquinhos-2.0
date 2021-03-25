import  unittest
from domain import TonalSystem, TonalSystemElement, Scale

class TestTonalSystem(unittest.TestCase):
    
    #preparacenario    
    def setUp(self):
        self.t1 = TonalSystem(12)
        self.diatonic_values = [0, 2, 4, 5, 7, 9, 11]
        self.diatonic_struct = (2, 2, 1, 2, 2, 2, 1)
    
    def test_set_generator(self):
        self.t1.set_generator(7)
        self.assertEqual(TonalSystemElement(7, 12), self.t1.generator)

        self.t1.set_generator(TonalSystemElement(7, self.t1.cardinality))
        self.assertEqual(TonalSystemElement(7, 12), self.t1.generator)
    
    def test_scale(self):
        new_scale = self.t1.scale(self.diatonic_values)
        self.assertEqual(Scale(12, self.diatonic_struct), new_scale)
    
    def test_diatonic_scale(self):
        self.t1.set_generator(7)
        self.assertEqual(Scale(12, self.diatonic_struct), self.t1.diatonic_scale())

if __name__ == '__main__':  
    unittest.main()  