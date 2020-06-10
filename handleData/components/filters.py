from ..interface.component import Component
from ..interface.parameter import Parameter
from ..interface.dtype import FuncType, IntType, StrType


def build_filter_nan():
    def filter_nan(data, context):
        def filter_criterion(v):
            if isinstance(v, float) or isinstance(v, int):
                return not np.isnan(v)
            elif isinstance(v, list):
                return True
            else:
                return True
        records = context['records']
        filter_out = list(filter(lambda v: not filter_criterion(v['values'][0]), data))
        filter_in = list(filter(lambda v: filter_criterion(v['values'][0]), data))
        context['records'] = list(map(lambda x: x[1], filter(lambda item: filter_criterion(data[item[0]]['values'][0]), enumerate(records))))
        data = filter_in
        return data, context
    return filter_nan

class NanFilter(Component):
    parameters = {}
    def get_func(self):
        return build_filter_nan()
    

def build_filter_weekly(period_start=-7, period_end=0):
    def filter_weekly(records, context):
        length = len(records)
        return list(map(lambda x: x[ len(x) + period_start: len(x) + period_end], records)), context
    return filter_weekly

class WeeklyFilter(Component):
    parameters = {
        "daysStartToNow": Parameter(IntType, 7),
        "daysEndToNow": Parameter(IntType, 0)
    }
    def get_func(self):
        return build_filter_weekly(-self.args['daysStartToNow'], -self.args['daysEndToNow'])


def build_filter_records(f):
    def filter_records(records, context):
        # print(records)
        # for record in records:
            # if record['国家地区'] == "冰岛":
                # print(record)
        context_records = context['records']
        context['records'] = list(filter(f, context_records))
        return list(filter(f, records)), context
    return filter_records


class RecordsFilter(Component):
    parameters = {
        "f": Parameter(FuncType)
    }
    def get_func(self):
        return build_filter_records(self.args['f'])

def build_confirmed_condition(condition=10000):
    def confirmed_condition(records, context):
        return list(filter(lambda x: x[-1]["累计确诊"] > 10000, records)), context
    return confirmed_condition


class ConfirmedConditionFilter(Component):
    parameters = {
        "condition": Parameter(IntType, 10000)
    }
    def get_func(self):
        return build_confirmed_condition(self.args['condition'])


def build_filter_seq(l):
    def filter_seq(records, context):
        filtered = {
            "x": records['x'][-l:],
            'y': list(map(lambda x:x[-l:], records['y']))
        }
        return filtered, context
    return filter_seq


class SeqFilter(Component):
    parameters = {
        "l": Parameter(IntType)
    }
    def get_func(self):
        return build_filter_seq(self.args['l'])


def build_filter_region(region):
    def filter_region(records, context):
        return list(filter(lambda x: x['地区']==region, records)), context
    return filter_region


class RegionFilter(Component):
    parameters = {
        "region": Parameter(StrType)
    }
    def get_func(self):
        return build_filter_region(self.args['region'])

def build_filter_stage(stage):
    def filter_stage(records, context):
        return list(filter(lambda x: x['阶段']==stage, records)), context
    return filter_stage

class StageFilter(Component):
    parameters = {
        "stage": Parameter(StrType)
    }
    def get_func(self):
        return build_filter_stage(self.args['stage'])