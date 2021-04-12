from .tonal_system_element import TonalSystemElement
from .scale import Scale
from typing import Union
import copy
import numpy as np
import matplotlib.pyplot as plt

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

    def show(self):
        r = 10
        angulo = 2 * np.pi / self.generator.module
        ciclo = self.elements
        x = [ciclo[0].value]
        y = [r]

        for i in range(1, self.generator.module + 1):
            x.append(r * np.sin(i * angulo))
            y.append(r * np.cos(i * angulo))

        # plt.plot(x, y, 'bo', markersize=20)
        plt.plot(x, y, markersize=20)
        for i in range(self.generator.module):
            #plt.annotate(ciclo[i], (x[i], y[i]))
            plt.text(x[i], y[i],ciclo[i])
        plt.axis('off')
        plt.show()