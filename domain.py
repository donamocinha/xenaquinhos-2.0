import math
import copy
from typing import Tuple, Union
from utils import check_or_create_folder
from fractions import Fraction


#TODO: CHECAGEM DE TIPOS
#TODO: __repr__(self, o), __str__
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
            #TODO: Exceção?

class BalzanoDiagram:
    def __init__(self, matrix):
        self.matrix = matrix



class Scale:
    def __init__(self, system_size, interval_struct, tonic=0, name="Generic Scale"):
        self.system_size = system_size
        self.interval_struct = interval_struct
        self.set_tonic(tonic)
        self.name = name
        self.interval_vector = self.vector()

    def set_tonic(self, tonic):
        self.elements = []
        actual = tonic
        for i in self.interval_struct:
            self.elements.append(TonalSystemElement(actual, self.system_size))
            actual += i

    def next(self, elem, steps):
        real_elem = TonalSystemElement(elem, self.system_size) if isinstance(elem, int) else elem
        next_index = (self.elements.index(real_elem) + steps) % len(self.elements)
        return copy.deepcopy(self.elements[next_index])

    def export_scala_files(self, file_name, kbm_pattern=None):
        chroma_cents = 1200/self.system_size
        check_or_create_folder('scala_files')
        f = open(f'scala_files/{file_name}', 'w')

        #Escrevendo cabeçalho
        f.write(f'! {file_name}\n!\n {self.name}\n {len(self.elements)}\n!')

        sum_interval = 0
        for interval in self.interval_struct:
            sum_interval+=interval
            format_value = "{:.5f}".format(sum_interval*chroma_cents)
            f.write(f'\n {format_value}')
        f.close()

        kbm_name = file_name[:-3]+'kbm'
        kbm = open(f'scala_files/{kbm_name}', 'w')

        if kbm_pattern==None:
            kbm_pattern = [i for i in range(len(self.elements))]
        
        if len(kbm_pattern)<=12:
            length = 12
            kbm.write(f'! {kbm_name}\n{length}\n{0}\n{127}\n{60+self.elements[0].value}\n{69}\n440.00000\n{len(self.elements)}\n')
            kbm.write('! Mapping.')
            for e in (kbm_pattern+['x' for _ in range(12-len(kbm_pattern))]):
                kbm.write(f'\n{e}')
            
        else:
            length = len(kbm_pattern)
            kbm.write(f'! {kbm_name}\n{length}\n{0}\n{127}\n{60+self.elements[0].value}\n{69}\n440.00000\n{len(self.elements)}\n')
            kbm.write('! Mapping.')
            for e in kbm_pattern:
                kbm.write(f'\n{e}')
        
        kbm.close()

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
    
    def __eq__(self, o):
        assert isinstance(o, Scale)
        return (sorted(self.elements) == sorted(o.elements)) and (self.system_size==o.system_size)
    
class GCycle:

    def __init__(self, generator: TonalSystemElement):
        self.generator = generator
        self.elements = self.generate_cycle()

    def generate_cycle(self):
        elements = [TonalSystemElement(0, self.generator.module)]
        for _ in range(self.generator.module - 1):
            elements.append(elements[-1] + self.generator)
        return elements

    def diatonic_scale(self, tonic):
        length = self.generator.inverse().value

        start_element = TonalSystemElement(-self.generator.value, self.generator.module)
        
        sc_elements = [start_element]
        for _ in range(length-1):
            sc_elements.append(sc_elements[-1]+self.generator)
        sc_elements.sort()
        sc_elements.append(sc_elements[0])
        

        struct = tuple((sc_elements[i]-sc_elements[i-1]).value for i in range(1, len(sc_elements)))

        return Scale(self.generator.module, struct, tonic=tonic)

    def next(self, elem: Union[TonalSystemElement, int], steps: int):
        real_elem = TonalSystemElement(elem, self.generator.module) if isinstance(elem, int) else elem
        next_index = (self.elements.index(real_elem) + steps) % len(self.elements)
        return copy.deepcopy(self.elements[next_index])

    ## show
    def show(self):
        pass

class TonalSystem:
    def __init__(self, n):
        assert n>1, "Tonal System must have more than one element"
        self.cardinality = n
        self.generator = TonalSystemElement(1, n)

    #TODO: Debater a possibilidade de passar aqui diretamente a estrutura ao invés dos elementos
    def scale(self, elements):
        elements.sort()
        if all(isinstance(e, TonalSystemElement) for e in elements):
            circle_elements = elements + [elements[0]]
        elif all(isinstance(e, int) for e in elements):
            circle_elements = [TonalSystemElement(e, self.cardinality) for e in elements] + [TonalSystemElement(elements[0], self.cardinality)]

        struct = tuple((circle_elements[i]-circle_elements[i-1]).value for i in range(1, len(circle_elements)))
        return Scale(self.cardinality, struct)

    def diatonic_scale(self):
        cycle = GCycle(self.generator)
        return cycle.diatonic_scale(0)

    #TODO: Função que retorna possibilidades de geradores
    def set_generator(self, g: Union[TonalSystemElement, int]):
        assert math.gcd(g, self.cardinality)==1, "Element must be a generator"
        self.generator = TonalSystemElement(g, self.cardinality) if isinstance(g, int) else g

    def balzano_diagram(self, minor, major):
        pass



