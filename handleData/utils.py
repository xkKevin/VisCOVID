import json
import datetime
from bson import json_util
from functools import reduce
import numpy as np
from datetime import timedelta
import dateutil.parser
class BsonEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%m/%d")
        else:
            return obj
def load_config(config_path = "./handleData/config.json" ):
    fp = open(config_path)
    config_data = json.load(fp)
    return config_data
class ConfigEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        else:
            return obj
def save_config(config, config_path="./handleData/config.json"):
    fp = open(config_path, 'w', encoding='utf-8')
    json.dump(config, fp, cls=ConfigEncoder, ensure_ascii=False)

    
def save_data(path, data):
    fp = open(path, 'w', encoding='utf-8')
    json.dump(data, fp,cls=BsonEncoder,  ensure_ascii=False)   


def save_world_map(path, data):
    fp = open(path, "w")
    r = {
        "data": data
    }
    json.dump( r, fp)

def find_population_by_chinese_name(db, chinese):
    if chinese == "刚果":
        chinese = "刚果(金)"
    if chinese == "全球":
        return 7594270356.
        populations = list(db.populations.find({}))
        def f(acc, c):
            p = 0
            try :
               p = float(c['2018 [YR2018]'])
            except ValueError:
                pass
            if np.isnan(p):
                return acc
            acc += p
            return acc
        global_population = reduce(f, populations, 0)
        print(global_population)
        return global_population
    t = db.chinese_conversion.find_one({"sheet": chinese})
    if t:
        chinese = t['formal']
    
    country = db.countries.find_one({"country_name_chinese_short": chinese})
    t = db.populations.find_one({"Country Code": country['country_code3']})
    if not t:
        print(chinese)
    return float(t['2018 [YR2018]'])


def build_time_range(time_range):
    start = dateutil.parser.parse(time_range['start'])
    end = dateutil.parser.parse(time_range['end'])
    c = start
    dates = []    
    while c < end:
        dates.append(c)
        c += timedelta(days=1)
    return dates