import math
import copy
from typing import Tuple, Union
from utils import check_or_create_folder
import numpy as np 
import matplotlib.pyplot as plt
from fractions import Fraction


#TODO: CHECAGEM DE TIPOS
#TODO: Adicionar informações sonoras no TonalSystemElement (para utilização conjunta com SCAMP e outros)
class TonalSystemElement:
    def __init__(self, value, module):
        self.value = value % module
        self.module = module

        self.cents = self.value * (1200/self.module)
        self.midi = (self.cents/100)
    
    def is_generator(self):
        return math.gcd(self.value, self.module)==1

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
    
    def __str__(self):
        return str(self.value)

class BalzanoDiagram:
    def __init__(self, cardinality: int, x: TonalSystemElement, y: TonalSystemElement):
        self.cardinality = cardinality
        self.matrix = self.build_matrix(cardinality, x, y)
    
    def build_matrix(self, cardinality, x, y):
        matrix = []
        for i in range(-2, y.value-1):
            row = []
            for j in range(-1, x.value):
                row.append(TonalSystemElement(i*x.value + j*y.value, cardinality))
            matrix.append(row)
        return matrix
    
    def contains_scale(self, scale):
        pos = [0,0]
        actual = self.matrix[pos[0]][pos[1]]
        region = []
        step = 0
        while actual.value != self.matrix[0][0].value or len(region)==0:
            if len(region)>len(scale): return False

            region.append(actual)
            pos[step]+=1
            step = (step+1)%2
            actual = self.matrix[pos[0]][pos[1]]
        
        if len(region)!=len(scale): return False
        region.sort()
        region.append(region[0])

        r_struct = list((region[i]-region[i-1]).value for i in range(1, len(region)))
        s_struct = list(scale.interval_struct)
        for i in range(len(s_struct)):
            if (r_struct[i:]+r_struct[:i]) == s_struct: return True
        
        return False
    
    def show(self):
        print(self)
        fig, ax = plt.subplots()
        
        i,j = 0.5, 0.5
        p = 0.08
        h = False
        while i<=len(self.matrix) and j<=len(self.matrix[0]):
            dest = (i+1, j) if h else (i, j+1)
            px = 0.1 if h else 0
            py = 0.1-px
            color = 'r' if h else 'b'
            plt.plot([i+px, dest[0]-px], [j+py+0.05, dest[1]-py], color=color)
            if i+1<=len(self.matrix[0]):
                plt.plot([i+p, i+1-p], [j+p, j+1-p], color='g')
            h = not h
            i, j = dest

        
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                el = self.matrix[i][j]
                ax.text(j+0.5, i+0.5, str(el), va='center', ha='center')

        ax.set_xlim(0, len(self.matrix[0]))
        ax.set_ylim(0, len(self.matrix))
        ax.set_xticks(np.arange(len(self.matrix[0])))
        ax.set_yticks(np.arange(len(self.matrix)))

        plt.axis('off')

        ax.grid()
        plt.show()

    def __str__(self):
        return str([[str(x) for x in row] for row in self.matrix])


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

    #TODO: garantir que file_name tenha .scl e que o kbm substitua.
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
        if not isinstance(o, Scale):
            return False
        return (sorted(self.elements) == sorted(o.elements)) and (self.system_size==o.system_size)
    
    def __len__(self):
        return len(self.elements)
    
    def __str__(self):
        output_str = self.name
        output_str += f'\nElements: {[e.value for e in self.elements]}'
        output_str += f'\nInterval Vector: {self.interval_vector}'
        output_str += f'\nInterval Struct: {self.interval_struct}\n'
        return output_str
    
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

        return Scale(self.generator.module, struct, tonic=tonic, name="Diatonic Scale")

    def next(self, elem: Union[TonalSystemElement, int], steps: int):
        real_elem = TonalSystemElement(elem, self.generator.module) if isinstance(elem, int) else elem
        next_index = (self.elements.index(real_elem) + steps) % len(self.elements)
        return copy.deepcopy(self.elements[next_index])
    
    def __str__(self):
        return f'Cycle: {[str(e) for e in self.elements]}'

    ## show
    def show(self):
        pass

class TonalSystem:
    def __init__(self, n):
        assert n>1, "Tonal System must have more than one element"
        self.cardinality = n
        self.generator = TonalSystemElement(1, n)


    def scale(self, elements, struct=[]):
        assert (len(elements)==0) ^ (len(struct)==0), "argument must be either elements or struct"
        if len(elements)!=0:
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

    def get_generators(self):
        n = self.cardinality
        return [TonalSystemElement(x, n) for x in range(n) if math.gcd(x, n)==1]

    def set_generator(self, g: Union[TonalSystemElement, int]):
        if isinstance(g, int):
            assert math.gcd(g, self.cardinality)==1, "Element must be a generator"
            self.generator = TonalSystemElement(g, self.cardinality)
        elif isinstance(g, TonalSystemElement):
            assert g.is_generator(), "Element must be a generator"
            self.generator = g
    
    def get_midi_pitch_classes(self):
        n = self.cardinality
        return [TonalSystemElement(i, n).midi for i in range(n)]

    def balzano_diagram(self, minor, major):
        n = self.cardinality
        assert TonalSystemElement(minor+major, n)==self.generator, "thirds must sum up to generator"
        return BalzanoDiagram(n, TonalSystemElement(minor, n), TonalSystemElement(major, n))

    def __str__(self):
        return f'{self.cardinality}-Fold Tonal System with generator {self.generator}'





