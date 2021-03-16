class BalzanoDiagram:
    def __init__(self,matrix):
        self.matrix = matrix

class Scale:
    def __init__(self, system_size, interval_struct, tonic = 0):
        self.system_size = system_size
        self.interval_struct = interval_struct
        self.set_tonic(tonic) 
      #  self.interval_vector = self.vector()

    def set_tonic(self, tonic):
        self.elements = []
        actual = tonic
        for i in self.interval_struct:
            self.elements.append(TonalSystemElement(actual, self.system_size))
            actual += i

    def next(self, elem, step):
        pass
    
    def export_scala_files(self, file_name):
        pass
    
    def show(self):
        pass
    
    def vector(self):
        v = [0 for _ in range(int(self.system_size/2))]
        scale = self.elements
        for i, pivot in enumerate(scale):
            for el in scale[i+1:]:
                dist = min((el - pivot)%self.system_size, (pivot-el)%self.system_size)
                v[dist-1] += 1
        return v

class GCycle:
    def __init__(self, cur_struct, elements):
        self.cur_struct = cur_struct
        self.elements = elements

    def diatonic_scale(self, tonic):
        self.elements = [tonic+x for x in self.cur_struct]
        self.elements.sort()
        return Scale(self.elements, len(self.elements), tonic)

class TonalSystem:
    def __init__(self, n):
        self.cardinality = n
    def scale(self,elements):
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

    def __sub__(self, other):
        pass

    def __mul__(self, o):
        pass
    
    def __eq__(self, o):
        return isinstance(o, TonalSystemElement) and self.value == o.value and self.module == o.module

    def __gt__(self, other):
        pass

    def __lt__(self, other):
        pass
    def __le__(self, other):
        pass
    def __ge__(self, other):
        pass