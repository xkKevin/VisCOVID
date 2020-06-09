from functools import reduce
class Engine:
    def __init__(self):
        self.index = {}

    def add_to_index(self, variables):
        def f(acc, c):
            acc[c[0]] = c[1]
            return acc
        self.index = reduce(f, variables, self.index) 