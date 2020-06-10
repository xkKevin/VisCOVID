from datetime import datetime, timedelta
import dateutil.parser
from functools import reduce
import numpy as np
from .process.builders import build_filter_nan, build_filter_records
from .interface.dtype import FuncType

def process_global_seq(operator, preprocess, postprocess):
    def build_final_seq(db, config):
        found = list(db.global_records.find())
        found.sort(key=lambda x: x['日期'])
        truncated = list(filter(lambda x: not np.isnan(x['累计确诊']), found))
        context = {}
        def generate_default_seq():
            return {'x': [], 'y': []}
        def process(acc, c):
            return c(acc, context)[0]
        data = reduce(process, preprocess, found)
        data = reduce(operator, data, generate_default_seq())
        data = reduce(process, postprocess, data)
        return data
    return build_final_seq


# Extract country data which is accessible from the newest data
# 国家确诊数据 confirmed_data
# 国家死亡数据 death_data






# TBD: Multi-column values support
# TBD: Better support for records filtering
        




def process_country_record_last_day(f, args=dict() , preprocess=[], postprocess=[]):

    # Query the MongoDB
    
        # Build the dataset table
    def filter_2000(x):
        # if x ['国家地区'] == "冰岛":
            # print(x)
        # print(x)
        if x['累计确诊'] >= 2000.:
            return True
        else:
            return False
    preprocess.insert(0,build_filter_records(filter_2000) )
    postprocess.insert(0, build_filter_nan())
    def build_final_data(db, config, with_others = True, top = -1, with_average=False, average=None, filter_country= lambda x: True, sorted=True, average_func=None):
        countries = db.selected_countries.find({})
        check_date = dateutil.parser.parse(config['time']['end'])
        check_date -= timedelta(days=1)
        global_record = db.global_records.find_one({"日期": check_date})
        found = list(map(lambda x: db.country_records.find_one({"国家地区": x['chinese'], "日期": check_date}), countries))
        # Pre-Processing
        context = {
            "records": found,
            "global_record": global_record,
            "db": db,
        }
        def process(acc, c):
            return c(acc, context)[0]
        
        found = reduce(process, preprocess, found)
        mfound = list(filter(filter_country, found))
        # Process on the records
        values = list(map(lambda x: {"name": x['国家地区'], "values": f(x)}, mfound))
        
        values = reduce(process, postprocess, values) 
        return values
    return build_final_data

    
# Extract country data which can not be accessible from the newest data

def process_country_seq( operator, preprocess=[], postprocess=[]):
    def build_final_seq(db, config, with_others = False, period_start=-7, period_end=0, key="seq", top=-1, compare=lambda x: x['value'], sorted=False, post_filter=lambda x: True):
        countries = db.selected_countries.find({})
        check_date = dateutil.parser.parse(config['time']['end'])
        check_date -= timedelta(days=1)
        found = list(map(lambda x: list(db.country_records.find({"国家地区": x['chinese'], "日期":{"$lte": check_date, "$gt": check_date - timedelta(days=14)}})), countries))
        def extract_weekly_global():
            global_records = list(db.global_records.find({"日期":{"$lte": check_date, "$gt": check_date - timedelta(days=14)}}))
            return global_records
            global_last_records = list(db.global_records.find({"日期":{"$lte": check_date - timedelta(days=7), "$gt": check_date - timedelta(days=14)}}))
            def build_sum_func(key):
                def f_global(acc, c):
                    acc += c[key]
                    return acc
                return f_global
            global_weekly_confirmed = reduce(build_sum_func("新增确诊"), global_records, 0)
            global_weekly_death = reduce(build_sum_func("新增死亡"), global_records, 0)
            global_last_weekly_confirmed = reduce(build_sum_func("新增确诊"), global_last_records, 0)
            global_last_weekly_death = reduce(build_sum_func("新增死亡"), global_last_records, 0)
            return global_weekly_confirmed, global_weekly_death, global_last_weekly_confirmed, global_last_weekly_death
        # global_weekly_confirmed, global_weekly_death, global_last_weekly_confirmed, global_last_weekly_death = extract_weekly_global()
        global_records = extract_weekly_global()
        context = {
            "records": found,
            "record": found,
            "global_record": global_records,
            "db": db,
        }
        def process(acc, c):
            return c(acc, context)[0]
        preprocess.insert(0,build_filter_records(lambda x: x[-1]['累计确诊']>=2000) )
        mfound = reduce(process, preprocess, found)
        # mfound = list(filter(filter_country, mfound))
        # Process on the records

        data = list(map(lambda x: {"name": x[0]['国家地区'], "values": operator(x)}, mfound))
        data = reduce(process, postprocess, data) 

        return data

    return build_final_seq



def process_region_records(operator, preprocess=[], postprocess=[]):
    def build_final_data(db, config):
        def generate_default_seq():
            return {'x': [], 'y': [[],[]]}
        records = db.region_records.find({})
        context = {}
        check_date = dateutil.parser.parse(config['time']['end'])
        # check_date -= timedelta(days=1)
        def process(acc, c):
            return c(acc, context)[0]
        data = reduce(process, preprocess, records)
        data = reduce(operator, data, generate_default_seq())
        data = reduce(process, postprocess, data)
        return data
    return build_final_data



def process_stage_records(operator, preprocess=[], postprocess=[]):
    def build_final_data(db, config):
        def generate_default_seq():
            return {'x': [], 'y': [[],[]]}
        records = db.stage_records.find({})
        context = {}
        check_date = dateutil.parser.parse(config['time']['end'])
        # check_date -= timedelta(days=1)
        def process(acc, c):
            return c(acc, context)[0]
        data = reduce(process, preprocess, records)
        data = reduce(operator, data, generate_default_seq())
        data = reduce(process, postprocess, data)
        return data
    return build_final_data


class Compiler():
    def __init__(self, db, config):
        self.db = db
        self.config = config

    def preprocess(self, description):
        description['operator'] = FuncType(description['operator']).value
        description['preprocess'] = list(map(lambda x: x.get_func(), description['preprocess']))
        description['postprocess'] = list(map(lambda x: x.get_func(), description['postprocess']))
        return description
    def compile(self, description):
        db = self.db
        config = self.config
        description = self.preprocess(description)
        if description['process'] == "global":
            data = process_global_seq(description['operator'], description['preprocess'], description['postprocess'])(db, config)
        elif description['process'] == "last_day":
            data = process_country_record_last_day( description['operator'], preprocess=description['preprocess'],postprocess=description['postprocess'])(db, config)
        elif description['process'] == "seq":
            data = process_country_seq(description['operator'], preprocess=description['preprocess'],postprocess=description['postprocess'])(db, config)
        elif description['process'] == "region":
            data = process_region_records(description['operator'], preprocess=description['preprocess'],postprocess=description['postprocess'])(db, config)
        elif description['process'] == "stage":
            data = process_stage_records(description['operator'], preprocess=description['preprocess'],postprocess=description['postprocess'])(db, config)
        else:
            data = None
            print("Invalid process specified")
        return {
            "id": description['id'],
            "data": data
        }
    def get_compile_func(self):
        def compile(description):
            return self.compile(description)
        return compile
 