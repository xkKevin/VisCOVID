import pandas as pd
from datetime import timedelta
import dateutil.parser
from functools import reduce
def build_report(r, config):
    report =[]
    if r['due'] == None:
        r['due'] = {
            'hour': None,
            'minute': None,
        }
    report.append(["开始日期", dateutil.parser.parse(config['time']['start']).strftime('"%Y-%m-%d"')])
    report.append(["结束日期", (dateutil.parser.parse(config['time']['end']) - timedelta(days=1)).strftime('"%Y-%m-%d"')])
    report.append(["当前全球确诊数量", r['global_confirmed_seq']['y'][-1]])
    report.append(["当前全球死亡数量", r['global_death_seq']['y'][-1]])
    report.append(["当前全球确诊率", r['global_confirmed_per_million_seq']['y'][-1]/1000000])
    report.append(["当前全球病死率", r['global_death_rate_seq']['y'][-1]])
    report.append(["当前全球确诊最多国家", r["confirmed_data"][0]['name']])
    report.append(["当前全球确诊最多国家确诊数", r['confirmed_data'][0]['values'][0]])
    report.append(["当前全球确诊第二多国家", r['confirmed_data'][1]['name']])
    report.append(["当前全球确诊第二多国家确诊数", r['confirmed_data'][1]['values'][0]])
    report.append(["当前全球死亡最多国家", r['death_data'][0]['name']])
    report.append(["当前全球死亡最多国家死亡数", r['death_data'][0]['values'][0]])
    report.append(["当前全球死亡第二多国家", r['death_data'][1]['name']])
    report.append(["当前全球死亡第二多国家死亡数", r['death_data'][1]['values'][0]])
    

    # Calculate the weekly confirmed and death data
    def count_global_confirmed_death(acc, c):
        acc['confirmed'] += c[0]
        acc['death'] += c[1]
        return acc
    global_confirmed_death_count = reduce(count_global_confirmed_death, r['global_confirmed_death_seq']['y'][-7:], {"confirmed": 0, 'death': 0})
    last_global_confirmed_death_count = reduce(count_global_confirmed_death, r['global_confirmed_death_seq']['y'][-14:-7], {"confirmed": 0, 'death': 0})
    report.append(["上周全球确诊病例", global_confirmed_death_count['confirmed']])
    report.append(["上周全球确诊较前一周", global_confirmed_death_count['confirmed']/last_global_confirmed_death_count['confirmed'] - 1])
    report.append(["上周全球死亡病例", global_confirmed_death_count['death']])
    report.append(["上周全球死亡较前一周", global_confirmed_death_count['death']/last_global_confirmed_death_count['death'] - 1])
    report.append(["上周确诊最多国家", r['weekly_confirmed_data'][0]['name']])
    report.append(["上周确诊最多国家确诊数", r['weekly_confirmed_data'][0]['values'][0]])
    report.append(["上周确诊第二多国家", r['weekly_confirmed_data'][1]['name']])
    report.append(["上周确诊第二多国家确诊数", r['weekly_confirmed_data'][1]['values'][0]])
    report.append(["上周死亡最多国家", r['weekly_death_data'][0]['name']])
    report.append(["上周死亡最多国家死亡数", r['weekly_death_data'][0]['values'][0]])
    report.append(["上周死亡第二多国家", r['weekly_death_data'][1]['name']])
    report.append(["上周死亡第二多国家死亡数", r['weekly_death_data'][1]['values'][0]])
    report.append(["上周确诊增速最快国家", r['weekly_confirmed_growth'][1]['name']])
    report.append(["上周确诊增速最快国家增速值", r['weekly_confirmed_growth'][1]['values'][0]])
    report.append(["上周确诊增速第二快国家", r['weekly_confirmed_growth'][2]['name']])
    report.append(["上周确诊增速第二快国家增速值", r['weekly_confirmed_growth'][2]['values'][0]])
    report.append(["上周死亡增速最快国家", r['weekly_death_growth'][1]['name']])
    report.append(["上周死亡增速最快国家增速值", r['weekly_death_growth'][1]['values'][0]])
    report.append(["上周死亡增速第二快国家", r['weekly_death_growth'][2]['name']])
    report.append(["上周死亡增速第二快国家增速值", r['weekly_death_growth'][2]['values'][0]])
    report.append(["当前全球确诊第三多国家", r['confirmed_data'][2]['name']])
    report.append(["当前全球确诊第三多国家确诊数", r['confirmed_data'][2]['values'][0]])
    report.append(["所有疫情数据截止小时", r['due']['hour']]) 
    report.append(["所有疫情数据截止分钟", r['due']['minute']])
    report = pd.DataFrame(report)
    report.columns = ['name', 'value']
    return report