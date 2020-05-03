import json
import pandas as pd
import numpy as np
from pymongo import MongoClient
from handleData.utils import load_config
import datetime
import dateutil.parser
import urllib.request



def extract_sheet(fp, check_date, sheet_name=None):
    df = pd.read_excel(fp, sheet_name)
    objs = []
    df = df.replace(pd.NaT, np.nan)
    columns = ['累计确诊', '新增确诊', '累计死亡', '新增死亡', '百万人口确诊率', '百万人口死亡率']
    
    # necessary_columns = ['累计确诊', '新增确诊', '累计死亡', "新增死亡", '累计治愈',  '百万人口确诊率'， '百万人口死亡率' ]
    for index, row in df.iterrows():
        # print(row)
        obj = dict(row)
        obj['sheet_name'] = sheet_name
        if '日期' not in obj.keys():
            print(sheet_name)
        date = obj['日期']
        date = datetime.datetime(date.year, date.month, date.day)
        # print(type(check_date))
        check_datetime = dateutil.parser.parse(check_date) - datetime.timedelta(days=1)
        c = datetime.datetime(check_datetime.year, check_datetime.month, check_datetime.day)
        if date >  c:
            continue
        for key in obj.keys():
            if type(obj[key]) ==  pd._libs.tslibs.nattype.NaTType:
                obj[key] = np.nan
        # print(type(row['重症病例']))
        for column in columns:
            if column not in obj.keys():
                obj[column] = 0.
            if np.isnan(obj[column]):
                obj[column] = 0.
        objs.append(obj)
    return objs

def store_excel_data(db, config):
    country_records = db["country_records"]
    global_records = db["global_records"]
    country_records.remove({})
    global_records.remove({})
    fp = open(config['path']['excel'], "rb")
    excel_df = pd.read_excel(fp, None)
    
    for sheet_name in excel_df.keys():
        if sheet_name == "Sheet1":
            continue
        records = extract_sheet(fp, config['time']['end'], sheet_name)
        if sheet_name == "全球":
            global_records.insert_many(records)
        elif sheet_name in ["全球2","法国CDC", "澳门", "台湾", "香港", "中国大陆" , "Sheet1"]:
            continue
        else:
            country_records.insert_many(records)
            

def store_country_info(db, config):
    path = config['path']['conrties_info']
    db.countries.remove({})
    fp = open(path)
    json_data = json.load(fp)
    def process_country(item):
        if 'phone_code' in item.keys():
            if item['phone_code'] == "642": # Romania
                item['country_code3'] = "ROU"
            elif item['phone_code'] == "688":
                item['country_code3'] = "SRB"
            elif item['phone_code'] == "191":
                print(item)
                item['country_code3'] = "HRV"
        
        db.countries.insert_one(item)
    list(map(process_country, json_data))
# def replace_nan_by_none(obj):
    

def store_selected_countries(db, config):
    selected_countries = db["selected_countries"]
    selected_countries.remove({})
    fp = open(config['path']['excel'], "rb")
    excel_df = pd.read_excel(fp, None)
    selected = list(filter(lambda x:  x not in ["全球", "全球2", "法国CDC", "澳门", "台湾", "香港", "中国大陆", "Sheet1"],excel_df.keys()))
    selected = list(map(lambda x: {"chinese": x}, selected))
    selected_countries.insert_many(selected)

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
    print(data.shape)
    a = list(data.mean())

    a.insert(0, 'Avg')
    a = pd.DataFrame(a)
    a = a.T
    a.columns = country_names
    print(a.shape)
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
        print(record)
        population = 1000000. * record['累计确诊']/record['百万确诊率']
        print(population)
    # list(map(f, lastest_records))
    for index, row in csv.iterrows():
        print(row)
        obj = dict(row)
        print(obj)
        db.populations.insert_one(obj)
    float_population(db, config)
# 

def prepare_country_chinese_conversion(db, config):

    db.chinese_conversion.insert_one({"sheet": "孟加拉", "formal": "孟加拉国"})

def prepare_dxy_data(db ,config):
    fp = open(config['path']['dxy_data'], 'r')
    dxy = json.load(fp)
    db.dxy.insert_many(dxy['results'])
def prepare_owd_data(db, config):
    # cases = pd.read_csv(config['path']['owd_cases'])
    # death = pd.read_csv(config['path']['owd_death'])
    owd_all = pd.read_csv(config['path']['owd_all'])
    db.owd_confirmed.remove({})
    db.owd_death.remove({})
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

def prepare():
    config = load_config()
    
    client = MongoClient()
    db = client['coronavirus_analysis']
    # fetch_owd_data(db, config)
    
    # store_excel_data(db, config)
    # prepare_owd_data(db, config)
    # store_selected_countries(db, config)
    
    
    
    # store_country_info(db, config)
    # store_population(db, config)
    prepare_country_chinese_conversion(db, config)
    # check_populations(db, config)
    # prepare_dxy_data(db, config)

# Weekly Updates:
# Store EXCEL Data
# Prepare_owd_data




if __name__ == "__main__":
    prepare()