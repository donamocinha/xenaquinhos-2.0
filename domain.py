import math
from typing import Tuple


class BalzanoDiagram:
    def __init__(self, matrix):
        self.matrix = matrix



class Scale:
    def __init__(self, system_size, interval_struct, tonic=0):
        self.system_size = system_size
        self.interval_struct = interval_struct
        self.set_tonic(tonic)
        # self.interval_vector = self.vector()

    def set_tonic(self, tonic):
        self.elements = []
        actual = tonic
        for i in self.interval_struct:
            self.elements.append(TonalSystemElement(actual, self.system_size))
            actual += i

    def next(self, elem, step):
        return TonalSystemElement(self.elements.index(elem) + step, len(self.elements))

    def export_scala_files(self, file_name):
        pass

    def show(self):
        pass

    def vector(self):
        v = [0 for _ in range(int(self.system_size / 2))]
        scale = self.elements
        for i, pivot in enumerate(scale):
            for el in scale[i + 1:]:
                dist = min((el - pivot).value % self.system_size, (pivot - el).value % self.system_size)
                v[dist - 1] += 1
        return v


class TonalSystem:
    def __init__(self, n):
        self.cardinality = n

    def scale(self, elements):
        pass

    def set_generator(self, g):
        pass

    def balzano_diagram(self, minor, major):
        pass


class TonalSystemElement:
    def __init__(self, value, module):
        self.value = value % module
        self.module = module

    def __add__(self, o):
        assert isinstance(o, TonalSystemElement), f"Cannot add TonalSystemElement to {type(o)}"
        assert self.module == o.module, "Cannot add elements of different modules"
        return TonalSystemElement(self.value + o.value, self.module)

    def __sub__(self, o):
        assert isinstance(o, TonalSystemElement), f"Cannot subtract TonalSystemElement to {type(o)}"
        assert self.module == o.module, "Cannot subtract elements of different modules"
        return TonalSystemElement(self.value - o.value, self.module)

    def __mul__(self, o):
        assert isinstance(o, TonalSystemElement), f"Cannot multiply TonalSystemElement to {type(o)}"
        assert self.module == o.module, "Cannot multiply elements of different modules"
        return TonalSystemElement(self.value * o.value, self.module)

    def __eq__(self, o):
        return isinstance(o, TonalSystemElement) and self.value == o.value and self.module == o.module

    def __gt__(self, o):
        return isinstance(o, TonalSystemElement) and (self.value > o.value) and self.module == o.module

    def __lt__(self, o):
        return isinstance(o, TonalSystemElement) and self.value < o.value and self.module == o.module

    def __le__(self, o):
        return isinstance(o, TonalSystemElement) and self.value <= o.value and self.module == o.module

    def __ge__(self, o):
        return isinstance(o, TonalSystemElement) and self.value >= o.value and self.module == o.module

    def inverse(self):
        if math.gcd(self.value, self.module) != 1:
            return None
        else:
            for i in range(self.module):
                if (i * self.value) % self.module == 1:
                    return TonalSystemElement(i, self.module)
            # excecao


class GCycle:

    def __init__(self, generator: TonalSystemElement):
        self.elements = self.generate_cycle(generator)

    def generate_cycle(self, g):
        elements = [TonalSystemElement(0, g.module)]
        for _ in range(g.module - 1):
            elements.append(elements[-1] + g)
        return elements

    def diatonic_scale(self, tonic):
        pass

    def next(self, elem: TonalSystemElement, steps: int):
        pass

    ## show
    def show(self):
        pass
