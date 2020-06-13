from functools import reduce
class Engine:
    def __init__(self):
        self.index = {}
        self.rindex = {}

    def add_to_index(self, variables):
        def f(acc, c):
            acc[c[0]] = c[1]
            return acc
        def rf(acc, c):
            acc[c[1]] = c[0]
            return acc
        self.index = reduce(f, variables, self.index) 
        self.rindex = reduce(rf, variables, self.rindex)