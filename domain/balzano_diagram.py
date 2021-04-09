from .tonal_system_element import TonalSystemElement
import matplotlib.pyplot as plt
import numpy as np

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
