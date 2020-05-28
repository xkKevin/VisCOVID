import pandas as pd
def format_data(name, data):
    def format_confirmed_english_all(data):
        t = pd.DataFrame(map(lambda x: [x['name'], x['value']], data))
        t.columns = ['国家', "累计确诊人数"]
        return t, "2-1.csv"

    def format_death_english_all(data):
        t = pd.DataFrame(map(lambda x: [x['name'], x['value']], data))
        t.columns = ['国家', "累计病死人数"]
        return t, "2-2.csv"

    def format_confirmed(data):
        t = pd.DataFrame(map(lambda x: [x['name'], x['values'][0]], data))
        t.columns = ['国家', "累计确诊人数"]
        return t, "2-5.csv"

    def format_death(data):
        t = pd.DataFrame(map(lambda x: [x['name'], x['values'][0]], data))
        t.columns = ['国家', "累计病死人数"]
        return t, "2-6.csv"

    def format_global_death_seq(data):
        t = [data['x'], data['y']]
        t = pd.DataFrame(t).T
        t.columns = ['日期', '全球累计病死人数']
        t['日期'] = t["日期"].apply(lambda x: x.strftime('"%Y-%m-%d"'))
        return t, '2-3-b.csv'

    def format_global_confirmed_seq(data):
        t = [data['x'], data['y']]
        t = pd.DataFrame(t).T
        t.columns = ['日期', '全球累计确诊人数']
        t['日期'] = t["日期"].apply(lambda x: x.strftime('"%Y-%m-%d"'))
        return t, '2-3-a.csv'
    
    def format_global_death_rate_seq(data):
        t = [data['x'], data['y']]
        t = pd.DataFrame(t).T
        t.columns = ['日期', '全球病死率']
        t['日期'] = t["日期"].apply(lambda x: x.strftime('"%Y-%m-%d"'))
        return t, '2-4-b.csv'

    def format_global_confirmed_per_million_seq(data):
        y_seq = list(map(lambda x: x/1000000, data['y']))
        t = [data['x'], y_seq]
        t = pd.DataFrame(t).T
        t.columns = ['日期', '全球确诊率']
        t['日期'] = t["日期"].apply(lambda x: x.strftime('"%Y-%m-%d"'))
        return t, '2-4-a.csv'

    def _format_weekly_confirmed_data(data):
        t = pd.DataFrame(map(lambda x: [x['name'], x['value']], data))
        t.columns = ['国家', "累计确诊人数"]
        return t, '2-5.csv'

    def _format_weekly_death_data(data):
        t = pd.DataFrame(map(lambda x: [x['name'], x['value']], data))
        t.columns = ['国家', "累计病死人数"]
        return t, '2-7.csv'

    def format_confirmed_rate_data(data):
        t = pd.DataFrame(map(lambda x: [x['name'], x['values'][0]], data))
        t.columns = ['国家', "确诊率"]
        return t, '2-7.csv'
    
    def format_death_rate_data(data):
        t = pd.DataFrame(map(lambda x: [x['name'], x['values'][0]], data))
        t.columns = ['国家', "病死率"]
        return t, '2-8.csv'
    
    def format_test_rate_data(data):
        t = pd.DataFrame(map(lambda x: [x['name'], x['values'][0]], data))
        t.columns = ['国家', "检测率"]
        return t, '2-10.csv'
    
    def format_positive_rate_data(data):
        t = pd.DataFrame(map(lambda x: [x['name'], x['values'][0]], data))
        t.columns = ['国家', "阳性率"]
        return t, '2-11.csv'
    
    def format_global_newly_confirmed_seq(data):
        x_seq = data['x']
        y_seq = data['y']
        t = map(lambda x: [x_seq[x], y_seq[x][0]], range(len(x_seq)))
        t = pd.DataFrame(list(t))
        t.columns = ['日期', '新增确诊人数']
        t['日期'] = t["日期"].apply(lambda x: x.strftime('"%Y-%m-%d"'))
        return t, '2-17-a.csv'

    def format_global_newly_death_seq(data):
        x_seq = data['x']
        y_seq = data['y']
        t = map(lambda x: [x_seq[x], y_seq[x][1]], range(len(x_seq)))
        t = pd.DataFrame(list(t))
        t.columns = ['日期', '新增病死人数']
        t['日期'] = t["日期"].apply(lambda x: x.strftime('"%Y-%m-%d"'))
        return t, '2-17-b.csv'


    def format_global_confirmed_weekly_seq(data):
        print(data)
        x_seq = data['x'][-7:]
        y_seq = data['y'][-7:]
        t = map(lambda x: [x_seq[x], y_seq[x]], range(len(x_seq)))
        t = pd.DataFrame(list(t))
        t.columns = ['日期', '新增确诊人数']
        t['日期'] = t["日期"].apply(lambda x: x.strftime('"%Y-%m-%d"'))
        return t, '2-12-a.csv'
    def format_global_death_weekly_seq(data):
        print(data)
        x_seq = data['x'][-7:]
        y_seq = data['y'][-7:]
        t = map(lambda x: [x_seq[x], y_seq[x]], range(len(x_seq)))
        t = pd.DataFrame(list(t))
        t.columns = ['日期', '新增病死人数']
        t['日期'] = t["日期"].apply(lambda x: x.strftime('"%Y-%m-%d"'))
        return t, '2-12-b.csv'
    # Deprecated
    def format_global_confirmed_week_seq(data):
        x_seq = data['x'][-7:]
        y_seq = data['y'][-7:]
        t = map(lambda x: [x_seq[x], y_seq[x][0], y_seq[x][1]], range(len(x_seq)))
        t = pd.DataFrame(list(t))
        t.columns = ['日期', '新增确诊人数', '新增病死人数']
        t['日期'] = t["日期"].apply(lambda x: x.strftime('"%Y-%m-%d"'))
        return t, '2-12.csv'
    
    def format_weekly_confirmed_data(data):
        t = pd.DataFrame(map(lambda x: [x['name'], x['values'][0]], data))
        t.columns = ['国家', "本周新增确诊人数"]

        return t, '2-13.csv'
    
    def format_weekly_death_data(data):
        t = pd.DataFrame(map(lambda x: [x['name'], x['values'][0]], data))
        t.columns = ['国家', "本周新增病死人数"]
        return t, '2-14.csv'
    
    def format_weekly_confirmed_growth(data):
        t = pd.DataFrame(map(lambda x: [x['name'], x['values'][0]], data))
        t.columns = ['国家', "本周较上周新增确诊人数增速"]
        return t, '2-15.csv'

    def format_weekly_death_growth(data):
        t = pd.DataFrame(map(lambda x: [x['name'], x['values'][0]], data))
        t.columns = ['国家', "本周较上周新增病死人数增速"]
        return t, '2-16.csv'
    
    def format_weekly_confirmed_growth_condition_1(data):
        t = pd.DataFrame(map(lambda x: [x['name'], x['values'][0]], data))
        t.columns = ['国家', "本周较上周新增确诊人数增速"]
        return t, 'appendix-1.csv'

    def format_weekly_death_growth_condition_1(data):
        t = pd.DataFrame(map(lambda x: [x['name'], x['values'][0]], data))
        t.columns = ['国家', "本周较上周新增病死人数增速"]
        return t, 'appendix-2.csv'

    def format_test_num_data(data):
        t = pd.DataFrame(map(lambda x: [x['name'], x['values'][0]], data))
        t.columns = ['国家', "累计检测数"]
        return t, 'appendix-3.csv'


    def format_recovery_rate_data(data):
        t = pd.DataFrame(map(lambda x: [x['name'], x['values'][0]], data))
        t.columns = ['国家', "治愈率"]
        return t, '2-9.csv'

    if name == "confirmed_data":
        return format_confirmed(data)
    elif name == "death_data":
        return format_death(data)
    elif name == "global_death_seq":
        return format_global_death_seq(data)
    elif name == "global_confirmed_seq":
        return format_global_confirmed_seq(data)
    elif name == "global_death_rate_seq":
        return format_global_death_rate_seq(data)
    elif name == "global_confirmed_per_million_seq":
        return format_global_confirmed_per_million_seq(data)
    elif name == "confirmed_rate_data":
        return format_confirmed_rate_data(data)
    elif name == "death_rate_data":
        return format_death_rate_data(data)
    elif name == "test_rate_data":
        return format_test_rate_data(data)
    elif name == "positive_rate_data":
        return format_positive_rate_data(data)
    elif name == "recovery_rate_data":
        return format_recovery_rate_data(data)
    # Deprecated branch
    # elif name == "global_confirmed_death_seq":
    #     return format_global_confirmed_week_seq(data)
    elif name == "global_confirmed_weekly_seq":
        return format_global_confirmed_weekly_seq(data)
    elif name == "global_death_weekly_seq":
        return format_global_death_weekly_seq(data)
    elif name == "weekly_confirmed_data":
        return format_weekly_confirmed_data(data)
    elif name == "weekly_death_data":
        return format_weekly_death_data(data)
    elif name == "weekly_confirmed_growth":
        return format_weekly_confirmed_growth(data)
    elif name == "weekly_death_growth":
        return format_weekly_death_growth(data)
    elif name == "confirmed_map":
        return format_confirmed_english_all(data)
    elif name == "death_map":
        return format_death_english_all(data)
    elif name == "test_num_data":
        return format_test_num_data(data)
    elif name == "weekly_confirmed_growth_condition_1":
        return format_weekly_confirmed_growth_condition_1(data)
    elif name == "weekly_death_growth_condition_1":
        return format_weekly_death_growth_condition_1(data)
    elif name == "global_newly_confirmed_seq":
        return format_global_newly_confirmed_seq(data)
    elif name == "global_newly_death_seq":
        return format_global_newly_death_seq(data)
    else:
        return None, None
