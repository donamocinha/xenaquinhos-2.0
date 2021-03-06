from .tonal_system_element import TonalSystemElement
from .utils import check_or_create_folder
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Scale:
    def __init__(self, system_size, interval_struct, tonic=0, name="Generic Scale"):
        self.system_size = system_size
        self.interval_struct = interval_struct
        self.tonic = tonic
        self.elements = self.build_elements(tonic)
        self.name = name
        self.interval_vector = self.vector()
    
    def build_elements(self, tonic):
        elements = []
        actual = tonic
        for i in self.interval_struct:
            elements.append(TonalSystemElement(actual, self.system_size))
            actual += i
        return elements

    def set_tonic(self, tonic):
        self.tonic = tonic
        self.elements = self.build_elements(tonic)

    # TODO central_note
    def next(self, elem, steps):
        if isinstance(elem, int):
            real_elem = TonalSystemElement(elem, self.system_size)
            octave = int(elem // self.system_size)
        else:
            real_elem = elem
            octave = 0

        next_index = (self.elements.index(real_elem) + steps) % len(self.elements)
        if steps > 0 and self.elements[next_index].pitch_class < real_elem.pitch_class:
            octave += 1
        elif steps < 0 and self.elements[next_index].pitch_class > real_elem.pitch_class:
            octave -= 1
        return self.elements[next_index].pitch_class + (octave * self.system_size)

    # TODO: usar algoritmo de Manacher para otimizar
    def find_symmetric_rotation(self):
        struct = list(self.interval_struct)
        for i in range(0, len(struct)):
            rotated = struct[i:] + struct[:i]
            if rotated == rotated[::-1]:
                return i
        return -1

    # TODO: garantir que file_name tenha .scl e que o kbm substitua.
    def export_scala_files(self, file_name, kbm_pattern=None):
        chroma_cents = 1200 / self.system_size
        check_or_create_folder('scala_files')
        f = open(f'scala_files/{file_name}', 'w')

        # Headers
        f.write(f'! {file_name}\n!\n {self.name}\n {len(self.elements)}\n!')

        sum_interval = 0
        for interval in self.interval_struct:
            sum_interval += interval
            format_value = "{:.5f}".format(sum_interval * chroma_cents)
            f.write(f'\n {format_value}')
        f.close()

        kbm_name = file_name[:-3] + 'kbm'
        kbm = open(f'scala_files/{kbm_name}', 'w')

        if kbm_pattern == None:
            kbm_pattern = [i for i in range(len(self.elements))]

        if len(kbm_pattern) <= 12:
            length = 12
            kbm.write(
                f'! {kbm_name}\n{length}\n{0}\n{127}\n{60 + self.elements[0].pitch_class}\n{69}\n440.00000\n{len(self.elements)}\n')
            kbm.write('! Mapping.')
            for e in (kbm_pattern + ['x' for _ in range(12 - len(kbm_pattern))]):
                kbm.write(f'\n{e}')

        else:
            length = len(kbm_pattern)
            kbm.write(
                f'! {kbm_name}\n{length}\n{0}\n{127}\n{60 + self.elements[0].pitch_class}\n{69}\n440.00000\n{len(self.elements)}\n')
            kbm.write('! Mapping.')
            for e in kbm_pattern:
                kbm.write(f'\n{e}')

        kbm.close()

    def show(self):
        r = 5
        angle = 2 * np.pi / self.system_size
        i = 0
        ascending_chromatic = [i for i in range(self.system_size)]
        x = [ascending_chromatic[0]]
        y = [r]

        for i in range(1, self.system_size + 1):
            x.append(r * np.sin(i * angle))
            y.append(r * np.cos(i * angle))

        # plt.plot(x, y, 'wo', markersize=20)

        figure, axes = plt.subplots()
        cycle = plt.Circle((0, 0), r, fill=False)
        axes.add_artist(cycle)

        x_line = []
        y_line = []
        #        for i in range(self.system_size):
        for i in self.elements:
            x_line.append(x[i.pitch_class])
            y_line.append(y[i.pitch_class])
            plt.text(x[i.pitch_class], y[i.pitch_class], i.pitch_class, ha='center', va='center')

        x_line.append(x[0])
        y_line.append(y[0])
        plt.plot(x_line, y_line, markersize=20)
        plt.plot(x_line, y_line, 'wo', markersize=20)
        plt.axis('equal')
        plt.axis('off')

        plt.show()

    def vector(self):
        v = [0 for _ in range(int(self.system_size / 2))]
        scale = self.elements
        for i, pivot in enumerate(scale):
            for el in scale[i + 1:]:
                dist = min((el - pivot).pitch_class % self.system_size, (pivot - el).pitch_class % self.system_size)
                v[dist - 1] += 1
        return v

    def get_midi_pitch_classes(self):
        return [e.midi for e in self.elements]

    def get_elements(self):
        return [e.pitch_class for e in self.elements]

    def __eq__(self, o):
        if not isinstance(o, Scale):
            return False
        return (self.interval_struct == o.interval_struct) and (self.system_size == o.system_size)

    def __len__(self):
        return len(self.elements)

    def __str__(self):
        output_str = self.name
        output_str += f'\nElements: {[e.pitch_class for e in self.elements]}'
        output_str += f'\nInterval Vector: {self.interval_vector}'
        output_str += f'\nInterval Struct: {self.interval_struct}\n'
        return output_str
