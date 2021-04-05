import  unittest
from domain import TonalSystemElement

class TestTonalSystemElement(unittest.TestCase):

    def setUp(self):
        self.e1 = TonalSystemElement(8, 12)
        self.e2 = TonalSystemElement(5, 12)
    
    def test_is_generator(self):
        self.assertFalse(self.e1.is_generator())
        self.assertTrue(self.e2.is_generator())

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

    def test_sub(self):
        result = self.e1 - self.e2
        e3 = TonalSystemElement(3, 12)
        self.assertEqual(e3, result)

        result2 = self.e2 - self.e1
        self.assertEqual(TonalSystemElement(9, 12), result2)

    def test_mul(self):
        result = self.e1 * self.e2
        e3 = TonalSystemElement(160, 12)
        self.assertEqual(e3, result)

    def test_lt(self):

        e3 = TonalSystemElement(8, 12)
        self.assertTrue(self.e2 < self.e1)
        self.assertFalse(e3 < self.e1)
        self.assertFalse(self.e1 < self.e2)

    def test_gt(self):
        e3 = TonalSystemElement(8, 12)
        self.assertTrue(self.e1 > self.e2)
        self.assertFalse(e3 > self.e1)
        self.assertFalse(self.e2 > self.e1)

    def test_le(self):
        e3 = TonalSystemElement(8, 12)
        self.assertTrue(self.e2 <= self.e1)
        self.assertTrue(e3 <= self.e1)
        self.assertFalse(self.e1 <= self.e2)

    def test_ge(self):
        e3 = TonalSystemElement(8, 12)
        self.assertTrue(self.e1 >= self.e2)
        self.assertTrue(e3 >= self.e1)
        self.assertFalse(self.e2 >= e3)

    def test_inverse(self):
        self.assertEqual(None, self.e1.inverse())
        self.assertEqual(self.e2, self.e2.inverse())

if __name__ == '__main__':
    unittest.main()  