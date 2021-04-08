from .tonal_system_element import TonalSystemElement
from .utils import check_or_create_folder
import copy

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
    