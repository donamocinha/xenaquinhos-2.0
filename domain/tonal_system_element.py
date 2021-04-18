import math

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

    def symmetrical(self):
        return TonalSystemElement(-self.value, self.module)

    def subgroup(self):
        i = 1
        value = self.value
        while value!=0:
            i+=1
            value = (value+self.value)%self.module
        return i
    
    def __str__(self):
        return str(self.value)
