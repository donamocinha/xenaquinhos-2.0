import  unittest

from domain import GCycle, TonalSystemElement, Scale


class TestGCycle(unittest.TestCase):

    def setUp(self):
        diatonic = (2, 2, 1, 2, 2, 2, 1)
        self.s1 = GCycle(diatonic)

        diatonic = (2, 2, 1, 2, 2, 2, 1)
        self.s1 = Scale(12, diatonic)

    def test_diatonic_scale(self):
        scale = Scale(12, self.s1.cur_struct, 0)
        self.assertEqual(scale.elements, self.s1.diatonic_scale(0).elements)
        self.assertEqual(scale.system_size, self.s1.diatonic_scale(0).system_size)
        self.assertEqual(scale.interval_struct, self.s1.diatonic_scale(0).interval_struct)
  
if __name__ == '__main__':  
    unittest.main()  