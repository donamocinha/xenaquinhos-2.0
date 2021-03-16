import  unittest

class TestBalzanoDiagram(unittest.TestCase):

    
    #preparacenario    
    def setUp(self):
        pass
    
    def test_add(self): 
        self.assertEqual((1 + 2), 3)  
        self.assertEqual(0 + 1, 1)  
    
    def test_multiply(self):  
        self.assertEqual((0 * 10), 0)  
        self.assertEqual((5 * 8), 40)  
  
if __name__ == '__main__':  
    unittest.main()  