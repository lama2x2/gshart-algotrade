import time
import requests
import data
import bot


def get_time():
    r = requests.get('https://dapi.binance.com/dapi/v1/time')
    return r.json()['serverTime']


def check_tenpct(klines):
    ch_ind = 4
    kline_now = klines[-1]
    price_now = float(kline_now[ch_ind])
    pct = data.PCT
    f = False
    prices = [float(kline[ch_ind]) for kline in klines[:-1]]
    if min(prices) * pct <= price_now:
        f = True
    return f


def check_tenpct10m(klines):
    high_ind = 2
    low_ind = 3
    prices_now = [float(kline_now[high_ind]) for kline_now in klines[-10:]]
    pct = data.PCT
    f = False
    prices = [float(kline[low_ind]) for kline in klines]
    for i in range(10):
        if min(prices[:-10 + i]) * pct <= max(prices_now[i:]):
            f = True
            break
    return f


def check_pair(pair_name, pair_cd, time_now):
    if pair_cd + data.CDmin * 60 * 1000 > time_now:
        return False
    get = '/fapi/v1/markPriceKlines'
    params = {
        'symbol': pair_name,
        'interval': '1m',
        'limit': 120
    }
    r = requests.get(url=data.URL + get, params=params).json()
    return check_tenpct10m(r)


def create_new_symbols():
    with open('smbs.txt') as f:
        smbs_t = [i.replace('\n', '') for i in f]
        dc = {}
        for i in smbs_t:
            dc[i] = 0
    print(dc)


def start():
    bot.send_pr(f'#START +{int((data.PCT - 1) * 100)}% {data.CDmin}min cd\n@Shaiba_123')
    bot.send_pr(f'{time.localtime().tm_hour}:{time.localtime().tm_min}')
    bot.send_ph_net('https://kartinki.pibig.info/uploads/posts/2023-04/1681713030_kartinki-pibig-info-p-bot-kartinka-arti-pinterest-16.png')
    while True:
        time_now = get_time()
        print(time_now / 1000 / 60)
        for i in data.smbs:
            v = check_pair(i, data.smbs[i], time_now)
            if v:
                data.smbs[i] = time_now
                name = i + '.P'
                print(name)
                time.sleep(5)
                while True:
                    try:
                        bot.send_pr(name + ' @Shaiba_123 ' + '\n' + data.CHARTURL + name)
                        break
                    except:
                        time.sleep(5)


while True:
    try:
        start()
    except:
        bot.send_pr('что-то сломалось, но я перезагружаюсь!')
        continue
