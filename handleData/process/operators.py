def f_death(acc, current):
        acc['x'].append(current['日期'])
        acc['y'].append(current['累计死亡'])
        return acc

def f_confirmed(acc, current):
    acc['x'].append(current['日期'])
    acc['y'].append(current['累计确诊'])
    return acc

def f_newly_confirmed(acc, current):
    acc['x'].append(current['日期'])
    acc['y'].append(current['新增确诊'])
    return acc
    
def f_newly_death(acc, current):
    acc['x'].append(current['日期'])
    acc['y'].append(current['新增死亡'])
    return acc


def f_confirmed_per_million(acc, current):
    acc['x'].append(current['日期'])
    acc['y'].append(current['百万人口确诊率'])
    return acc

def f_death_rate(acc, current):
    acc['x'].append(current['日期'])
    if current['累计确诊'] == 0.:
        acc['y'].append(0.)
    else:
        acc['y'].append(current['累计死亡']/current['累计确诊'])
    return acc

def f_newly_confirmed_death(acc, current):
    acc['x'].append(current['日期'])
    acc['y'].append([current['新增确诊'], current['新增死亡']])
    return acc


# Operators Used in Country Data
def calculate_test_rate(x):
        # return x['总检测数'] / float(find_population_by_chinese_name(db, x['国家地区']))
        return [x['百万人口检测率'] / 1000000]
def calculate_confirmed_rate(x):
    # return x['累计确诊'] / float(find_population_by_chinese_name(db, x['国家地区']))
    return [x['百万人口确诊率'] / 1000000.]

def calculate_death_rate(x):
    return [x['累计死亡']/x['累计确诊']]

def calculate_positive_rate(x):
    if x['总检测数'] == 0:
        return [0]
    return [x['累计确诊'] / x['总检测数']]
    
def calculate_recovery_rate(x):
    return [x['累计治愈']/x['累计确诊']]

def add_to_seq(acc, c):
        acc['x'].append(c['日期'])
        acc['y'][0].append(c['新增确诊'])
        acc['y'][1].append(c['新增治愈'])
        return acc

