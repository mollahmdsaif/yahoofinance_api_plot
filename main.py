from matplotlib import pyplot as plt

def deep_copy(lst):
    ret = []
    for ele in lst:
        if isinstance(ele,list):
            ret.append(deep_copy(ele))
        else:
            ret.append(ele)
    return ret


def utc_time_diff_gen(date_str):
    from datetime import datetime as dt
    dt_utc0 = dt(1970,1,1)
    date_time_lst = list(map(int,date_str.split('-')))
    dt_time = dt(*date_time_lst)
    return str(int((dt_time - dt_utc0).total_seconds()))


#parameters -> initial='NAME', start='Y-m-d', end='Y-m-d'
def yahoo_fin_link_genarator(**data):
    url = ['https://query1.finance.yahoo.com/v7/finance/download/', None,
           '?period1=', None,
           '&period2=', None,
           '&interval=1d&events=history&includeAdjustedClose=trued']
    
    utc_0_start_diff = utc_time_diff_gen(data['start'])
    utc_0_end_diff = utc_time_diff_gen(data['end'])
    
    url[1], url[3], url[5] = data['initial'], utc_0_start_diff, utc_0_end_diff
    
    return ''.join(url)
   
 
def csv_reader(link):
    lst_data = None
    import requests, csv
    from contextlib import closing
    with closing(requests.get(link, stream=True)) as r:
        f = (line.decode('utf-8') for line in r.iter_lines())
        reader = csv.reader(f, delimiter=',', quotechar='"')
        lst_data = list(reader)
    return lst_data


def distribute_nums(l, parts = 50):
    parts += 1
    lst = list(range(1, l+1))
    multiple = len(lst)/parts
    n_lst = list(map(lambda x: round(x), [i * multiple for i in range(1,parts)]))
    return n_lst


def main():
     
    url = yahoo_fin_link_genarator(initial='TSLA', start='2019-1-10', end='2021-1-10')
    data = list(map(lambda x: [x[0]] + x[2:4], csv_reader(url)))
    
    #print(csv_reader(url))
    
    
    plt.xlabel(data[0][0])
    plt.ylabel(data[0][1] + '/' + data[0][2])
    
    dates, high, low = [], [], []
    for i in data[1:]:
        dates.append(i[0])
        high.append(float(i[1]))
        low.append(float(i[2]))
    
    plt.rcParams['figure.dpi'] = 300
    
    x_axis = list(range(len(high)))
    index = distribute_nums(len(x_axis)) if len(x_axis) > 50 else x_axis
    dates = [dates[i] for i in range(len(dates)) if i in index] if len(x_axis) > 50 else dates
    
    plt.xticks(index, dates, rotation='vertical', fontsize=5)

    #plt.yticks([float(i)/20 for i in range(0, 30)])
    
    plt.plot(x_axis, high)
    plt.plot(x_axis, low)
    
    plt.show()


if __name__ == "__main__":
    main()
























    