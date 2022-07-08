import pandas as pd
import csv

from pgcopy import CopyManager
import psycopg2

APIKEY = "MFW47C0DFITAED0J"

with open('symbols.csv') as f:
    reader = csv.reader(f)
    symbols = [row[0] for row in reader]
    print(symbols)


def fetch_stock_data(symbol, month):
    interval = '1min'

    slice = "year1month" + str(month) if month <= 12 else "year2month1" + str(month)

    apikey = APIKEY

    CSV_URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&' \
              'symbol={symbol}&interval={interval}&slice={slice}&apikey={apikey}' \
              .format(symbol=symbol, slice=slice, interval=interval,apikey=apikey)

    df = pd.read_csv(CSV_URL)
    print (df)

    df['symbol'] = symbol

    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')

    df = df.rename(columns={'time': 'time',
                            'open': 'price_open',
                            'high': 'price_high',
                            'low': 'price_low',
                            'close' : 'price_close',
                            'volume': 'trading_volume'})
    df = df[['time', 'symbol', 'price_open', 'price_close', 'price_low', 'price_high', 'trading_volume']]

    return [row for row in df.itertuples(index=False, name=None)]

def test_fetch_stock_data():
    stock_data = fetch_stock_data("AAPL",1)
    print(stock_data)


conn = psycopg2.connect(database="tsdb",
                        host="urje56javi.s0p1cle568.tsdb.cloud.timescale.com",
                        user="tsdbadmin",
                        password="yE8-7cZrSy0O!5",
                        port=35132)

cursor = conn.cursor()

SQL = "INSERT INTO stocks_data(time, symbol, price_open, price_close, price_low, price_high, trading_volume) VALUES(%s,%s,%s,%s,%s,%s,%s);"
COLUMNS = ('time', 'symbol', 'price_open', 'price_close', 'price_low', 'price_high', 'trading_volume')


for symbol in symbols[13:]:
    print(symbol)

    # time range is last three month
    time_range = range(1,4)

    for month in time_range:

        stock_datas = fetch_stock_data(symbol, month)
        
        # for stock_data in stock_datas:
            # try:
            #     cursor.execute(SQL,stock_data)
            # except (Exception, psycopg2.Error) as error:
            #         print(error.pgerror)

        mgr = CopyManager(conn, 'stocks_data', COLUMNS)

        mgr.copy(stock_datas)

        conn.commit()