import  unittest
from domain import TonalSystemElement

class TestTonalSystemElement(unittest.TestCase):

    def setUp(self):
        self.e1 = TonalSystemElement(8, 12)
        self.e2 = TonalSystemElement(5, 12)

    def test_eq(self):
        e3 = TonalSystemElement(8, 12)
        self.assertTrue(self.e1 == e3)
        
        e4 = TonalSystemElement(20, 12)
        self.assertTrue(self.e1 == e4)

        self.assertFalse(self.e1 == self.e2)
        self.assertFalse(self.e1 == 'uff')

    def test_add(self):
        result = self.e1 + self.e2
        e3 = TonalSystemElement(1, 12)
        self.assertEqual(e3, result)
        
      #  s = e1 + e2
    #  assertEqual()  
    
    #def test_
    def test_mul(self):  
  
if __name__ == '__main__':  
    unittest.main()  