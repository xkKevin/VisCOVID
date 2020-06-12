from ..interface.component import Component
from ..interface.parameter import Parameter
from ..interface.dtype import FuncType, IntType, StrType

def build_topk(k=15, compare=lambda x: x['values'][0]):
    def topk(data, context):
        data_sorted = sorted(data, key=compare, reverse = True)
        data_sorted = data_sorted[:k]
        topk_names = list(map(lambda x: x['name'], data_sorted))
        return list(filter(lambda x:x['name'] in topk_names, data)), context
    return topk

def build_sort(compare=lambda x: x['values'][0]):
    def sort(data, context):
        data_sorted = sorted(data, key=compare, reverse=True)
        return data_sorted, context
    return sort

class TopK(Component):
    parameters = {
       "k": Parameter(IntType, 15) 
    }
    def get_func(self):
        return build_topk(self.args['k'])



class Sort(Component):
    parameters = {
        "order": Parameter(StrType, "decrease")
    }
    def get_func(self):
        return build_sort()

