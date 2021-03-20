import unittest

from domain import TonalSystemElement, Scale


class TestScale(unittest.TestCase):

    # preparacenario
    def setUp(self):
        diatonic = (2, 2, 1, 2, 2, 2, 1)
        self.s1 = Scale(12, diatonic)

    def test_set_tonic(self):
        diatonic = [0, 2, 4, 5, 7, 9, 11]
        elements = [TonalSystemElement(e, 12) for e in diatonic]
        self.assertEqual(elements, self.s1.elements)
        elements = [TonalSystemElement(e + 3, 12) for e in diatonic]
        self.s1.set_tonic(3)
        self.assertEqual(elements, self.s1.elements)

    def test_next(self):
        diatonic = [0, 2, 4, 5, 7, 9, 11]
        elements = [TonalSystemElement(e+1, 12) for e in diatonic]
        self.assertEqual(TonalSystemElement(2,12).value, self.s1.next(elements[6], 2).value)

    def test_export_scala_files(self):
        pass

    def test_show(self):
        pass

    def test_vector(self):
        diatonic = [0, 2, 4, 5, 7, 9, 11]
        elements = [TonalSystemElement(e, 12) for e in diatonic]
        self.s1.elements = elements
        vector_int = [2, 5, 4, 3, 6, 1]
        self.assertEqual(vector_int, self.s1.vector())


if __name__ == '__main__':
    unittest.main()
