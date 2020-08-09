import json
import pandas as pd
import numpy as np
from pymongo import MongoClient
from .utils import load_config, save_config
import datetime
import dateutil.parser
import urllib.request
from functools import reduce
import os



def extract_region_sheet(sheet, name):
    sheet = sheet[1:]
    objs = []
    print("here")
    sheet[0:1] = sheet[0:1].replace(np.nan, 0)
    sheet = sheet.replace(pd.NaT, np.nan)
    
    for index, row in sheet.iterrows():
        if type(row[1]) == pd._libs.tslibs.nattype.NaTType:
            break
        print(row[1])
        obj = {
            "日期": row[0],
            "新增确诊": row[1],
            "新增治愈": row[2],
            "地区": name
        }
        objs.append(obj)
    return objs

def extract_stage_sheet(sheet):
    sheet = sheet[1:]
    stages = ["上行", "下行", "震荡", "尾期"]
    def f(acc, c):
        acc[c] = [],
        return acc
    stage_records_index = reduce(f, stages, {})
    
    def build_obj(item):
        # index = item[0]
        # stage = item[1]
        print( item['split'][0])
        obj = {
            "日期": item['split'][0],
            "新增确诊": item['split'][1],
            "新增治愈": item['split'][2],
            "阶段": item['stage'] 
        }
        return obj
    all_stages = []
    for index, row in sheet.iterrows():
        if type(row[1]) == pd._libs.tslibs.nattype.NaTType:
            break
        splits = list(map(lambda i: {"split": row[3*i: 3*i+3], "stage": stages[i]}, range(4)))
        objs = list(map(build_obj, splits))
        all_stages.extend(objs)
    return all_stages

def store_region_records(db, config):
    db.region_records.remove({})
    db.stage_records.remove({})
    # region_files = os.listdir(config['path']['regions'])
    # for filename in region_files:
    fp = open(config['path']['regions'], "rb")
    excel_df = pd.read_excel(fp, None)
    region_names = ["全球", "非洲", "周边", "一带一路"]
    for sheet_name in excel_df.keys():
        if sheet_name in region_names:
            objs = extract_region_sheet(excel_df[sheet_name], sheet_name)
            db.region_records.insert_many(objs)
        elif sheet_name == "四个阶段分别合计":
            objs = extract_stage_sheet(excel_df[sheet_name])
            db.stage_records.insert_many(objs)


def store_ineffective_countries(db, ineffective):
    db['ineffective_countries'].remove({})
    if len(ineffective) == 0:
        return False

    ineffective = list(map(lambda x: {"chinese": x}, ineffective))
    db['ineffective_countries'].insert_many(ineffective)
def store_selected_countries(db, selected):
    selected_countries = db["selected_countries"]
    selected_countries.remove({})
    # selected = list(filter(lambda x:  x not in ["全球", "全球2", "法国CDC", "澳门", "台湾", "香港", "中国大陆", "Sheet1"] and x[:2]!='Sh',excel.keys()))
    # selected = list(filter(lambda x: x not in excluded, selected))
    selected = list(map(lambda x: {"chinese": x}, selected))
    selected_countries.insert_many(selected)

def extract_sheet(excel, check_date, sheet_name=None):
    df = excel[sheet_name]
    objs = []
    df = df.replace(pd.NaT, np.nan)
    columns = ['累计确诊', '新增确诊', '累计死亡', '新增死亡', '百万人口确诊率', '百万人口死亡率']
    # necessary_columns = ['累计确诊', '新增确诊', '累计死亡', "新增死亡", '累计治愈',  '百万人口确诊率'， '百万人口死亡率' ]
    base_date = datetime.datetime(2020, 2, 1)
    for index, row in df.iterrows():
        obj = dict(row)
        obj['sheet_name'] = sheet_name
        obj['国家地区'] = sheet_name
        if '日期' not in obj.keys():
            pass
        date = obj['日期']
        if(pd.isnull(date)):
            print(sheet_name)
            print("NAT Detected")
            continue
        
        if type(date) == int:
            date = base_date + datetime.timedelta(days = date - 43862)
            # continue
            # pass
        else:
            date = datetime.datetime(date.year, date.month, date.day)
        obj['日期'] = date
        check_datetime = dateutil.parser.parse(check_date) - datetime.timedelta(days=1)
        c = datetime.datetime(check_datetime.year, check_datetime.month, check_datetime.day)
        if date >  c:
            continue
        for key in obj.keys():
            if type(obj[key]) ==  pd._libs.tslibs.nattype.NaTType:
                obj[key] = np.nan
        for column in columns:
            if column not in obj.keys():
                if sheet_name == "全球":
                    obj['column'] = np.nan
                else:
                    obj[column] = 0.
            if np.isnan(obj[column]):
                if sheet_name == "全球":
                    obj['column'] = np.nan
                else:
                    obj[column] = 0.
        objs.append(obj)
    return objs


def check_country_missing(db, country):
    t = db.chinese_conversion.find_one({"sheet": country})
    chinese = country
    if t:
        chinese = t['formal']
    country = db.countries.find_one({"country_name_chinese_short": chinese})
    if not country:
        return False
    else:
        return True


def get_sheet_type(db, sheet_name):
    if sheet_name == "Sheet1" or sheet_name[:2] == "Sh" or sheet_name[0] == "S":
        return "Sheet" 
    elif sheet_name in ["全球2","法国CDC", "澳门", "台湾", "香港", "中国大陆" , "Sheet1"]:
        return "Excluded"
    elif sheet_name == "全球":
        return "Global"
    elif not check_country_missing(db, sheet_name):
        return "Missing"
    else:
        return "Country"

def store_excel_data(db, config):
    country_records = db["country_records"]
    global_records = db["global_records"]
    country_records.remove({})
    global_records.remove({})
    db.missing_countries.remove({})
    fp = open(config['path']['excel'], "rb")
    excel_df = pd.read_excel(fp, None)
    
    def extract_end_date(excel):
        df = excel["全球"]
        df = df.replace(pd.NaT, np.nan)
        records = []
        for index, row in df.iterrows():
            obj = dict(row)
            records.append(obj)
        t = filter(lambda x: x['日期'] > datetime.datetime(2020,5,2), records)

        # reduce(lambda x: )
        def f(acc, c):
            all_fields = list(filter(lambda x:not np.isnan(x) and x!=0
            , list(c.values())[2:]))
            if len(all_fields) == 0:
                return acc
            else:
                return c
        t = reduce(f, t, {})
        return t['日期']
    # def extract_end_date(excel):
    #     usa_sheet = excel['美国']
    #     usa_end = extract_sheet_end_date(usa_sheet)
    #     global_sheet = excel['全球']
    #     global_end = extract_sheet_end_date(global_sheet)
        
    #     return global_end
    #     print(global_end)
    #     print(usa_end)
    #     if global_end < usa_end:
    #         return global_end
    #     else:
    #         return usa_end
    
    end_date = extract_end_date(excel_df)
    end_date += datetime.timedelta(days=1)
    start_date = end_date - datetime.timedelta(days=7)
    config['time']['end'] = end_date.isoformat()
    config['time']['start'] = start_date.isoformat()
    save_config(config)
    effective_countries = []
    error_countries = []
    for sheet_name in excel_df.keys():
        sheet_type = get_sheet_type(db, sheet_name)
        if sheet_type == "Sheet" or sheet_type == "Excluded":
            continue
        elif sheet_type == "Missing":
            db.missing_countries.insert_one({"chinese": sheet_name})
            continue
        else:
            if sheet_type == "Global":
                records = extract_sheet(excel_df, config['time']['end'], sheet_name)
                global_records.insert_many(records)
            else:
                try: 
                    records = extract_sheet(excel_df, config['time']['end'], sheet_name)
                    country_records.insert_many(records)
                    effective_countries.append(sheet_name)
                except:
                    error_countries.append(sheet_name)

    store_selected_countries(db, effective_countries)
    store_ineffective_countries(db, error_countries)

def store_country_info(db, config):
    path = config['path']['conrties_info']
    db.countries.remove({})
    fp = open(path, encoding="utf-8")
    json_data = json.load(fp)
    def process_country(item):
        if 'phone_code' in item.keys():
            if item['phone_code'] == "642": # Romania
                item['country_code3'] = "ROU"
            elif item['phone_code'] == "688":
                item['country_code3'] = "SRB"
            elif item['phone_code'] == "191":
                item['country_code3'] = "HRV"
        
        db.countries.insert_one(item)
    list(map(process_country, json_data))
# def replace_nan_by_none(obj):
    
def float_population(db, config):
    for obj in db.populations.find():
        p = 0
        try:
            p = float(obj['2018 [YR2018]'])
        except ValueError:
            pass
        db.populations.update_one({"_id": obj["_id"]}, {"$set":{"value": p}})


def check_populations(db, config):
    countries = list(db.selected_countries.find())
    timedeltas = list(range(20))
    
    dates = map(lambda x: datetime.datetime(2020, 4, 5) + datetime.timedelta(days=x), timedeltas)
    def f(record):
        population = 1000000. * record['累计死亡']/record['百万人口死亡率']
        return population
    def calculate_population(date):
        records = list(map(lambda x: db.country_records.find_one({"国家地区": x['chinese'], '日期': date}), countries))
        values = map(f, records )
        values = list(values)
        values.insert(0, date)
        return values 
    data = list(map(calculate_population, dates))
    data = pd.DataFrame(data)
    country_names = list(map(lambda x: x['chinese'], countries))
    country_names.insert(0, "Date")
    data.columns = country_names
    v = list(data.var())
    v.insert(0, 'Var')
    v = pd.DataFrame(v)
    v = v.T
    v.columns = country_names
    a = list(data.mean())

    a.insert(0, 'Avg')
    a = pd.DataFrame(a)
    a = a.T
    a.columns = country_names
    data = pd.concat([data, v, a], axis=0)


    data.to_csv("./population.csv")
    # list(map(f, lastest_records))




def store_population(db, config, check=False):
    db.populations.remove({})
    fp = open(config['path']['population'], "r")
    csv = pd.read_csv(fp)
    # countries = db.selected_countries.find()
    # lastest_records = map(lambda x: db.country_records.find_one({"国家地区": x['chinese'], '日期': datetime.datetime(2020, 4, 2)}), countries)
    def f(record):
        population = 1000000. * record['累计确诊']/record['百万确诊率']
    # list(map(f, lastest_records))
    for index, row in csv.iterrows():
        obj = dict(row)
        db.populations.insert_one(obj)
    float_population(db, config)
# 

def prepare_country_chinese_conversion(db, config):
    db.chinese_conversion.insert_one({"sheet": "刚果民主共和国", "formal": "刚果(金)"})
    db.chinese_conversion.insert_one({"sheet": "刚果", "formal": "刚果(布)"})
    db.chinese_conversion.insert_one({"sheet": "孟加拉", "formal": "孟加拉国"})

def prepare_dxy_data(db ,config):
    fp = open(config['path']['dxy_data'], 'r')
    dxy = json.load(fp)
    db.dxy.insert_many(dxy['results'])
def prepare_owd_data(db, config):
    # cases = pd.read_csv(config['path']['owd_cases'])
    # death = pd.read_csv(config['path']['owd_death'])
    owd_all = pd.read_csv(config['path']['owd_all'])
    # db.owd_confirmed.remove({})
    # db.owd_death.remove({})
    db.owd_all.remove({})
    # for index, row in cases.iterrows():
    #     obj = dict(row)
    #     t = dateutil.parser.parse(obj['Date'])
    #     obj['Date'] = t
    #     db.owd_confirmed.insert_one(obj)
    # for index, row in death.iterrows():
    #     obj = dict(row)
    #     t = dateutil.parser.parse(obj['Date'])
    #     obj['Date'] = t
    #     db.owd_death.insert_one(obj)
    for index, row in owd_all.iterrows():
        obj = dict(row)
        t = dateutil.parser.parse(obj['date'])
        obj['date'] = t
        db.owd_all.insert_one(obj)
def fetch_owd_data(config, db):
    urllib.request.urlretrieve(config['resource']['owd_cases'], config['path']['owd_cases'])
    urllib.request.urlretrieve(config['resource']['owd_death'], config['path']['owd_death'])

def prepare(config_path="./handleData/config.json"):
    config = load_config(config_path)
    
    client = MongoClient()
    db = client['coronavirus_analysis']
    # fetch_owd_data(db, config)
    
    store_region_records(db, config)

    store_country_info(db, config)
    store_population(db, config)
    prepare_country_chinese_conversion(db, config)

    store_excel_data(db, config)
    prepare_owd_data(db, config)
    # store_selected_countries(db, config)

    
    
    
    
    # check_populations(db, config)
    # prepare_dxy_data(db, config)

# Weekly Updates:
# Store EXCEL Data
# Prepare_owd_data




if __name__ == "__main__":
    prepare(config_path="./config_run.json")