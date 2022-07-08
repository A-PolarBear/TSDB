import plotly.express as px
import plotly.offline
from IPython.display import HTML
import plotly.graph_objects as go
import pandas as pd
import psycopg2

conn = psycopg2.connect(database="tsdb",
                        host="urje56javi.s0p1cle568.tsdb.cloud.timescale.com",
                        user="tsdbadmin",
                        password="yE8-7cZrSy0O!5",
                        port=35132)

def query1(conn):
    query1 = """
        SELECT time_bucket('{bucket}', time) AS bucket,
        last(price_close, time) AS last_closing_price
        FROM stocks_data
        WHERE symbol = '{symbol}'
        GROUP BY bucket
        ORDER BY bucket
    """.format(bucket="1 day", symbol="TSLA")

    df = pd.read_sql(query1, conn)
    fig = px.line(df, x='bucket', y='last_closing_price',title="Tesla's daily stock price over last three months")
    HTML(fig.to_html())
    # fig.show()
    plotly.offline.plot(fig)

def query2(conn):
    query = """
    SELECT time_bucket('{bucket}', time) AS bucket, 
    FIRST(price_open, time) AS price_open, 
    LAST(price_close, time) AS price_close,
    MAX(price_high) AS price_high,
    MIN(price_low) AS price_low
    FROM stocks_data
    WHERE symbol = '{symbol}' AND date(time) = date('{date}') 
    GROUP BY bucket
""".format(bucket="15 min", symbol="GOOG", date="2022-07-05")
    df = pd.read_sql(query, conn)
    fig = go.Figure(data=[go.Candlestick(x=df['bucket'],
                   open=df['price_open'],
                   high=df['price_high'],
                   low=df['price_low'],
                   close=df['price_close'],)])
    fig.update_layout(title="15-min candlestick chart of Google, 2022-07-05")
    plotly.offline.plot(fig)

query2(conn)