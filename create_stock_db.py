import psycopg2

conn = psycopg2.connect(database="tsdb",
                        host="urje56javi.s0p1cle568.tsdb.cloud.timescale.com",
                        user="tsdbadmin",
                        password="yE8-7cZrSy0O!5",
                        port=35132)

cursor = conn.cursor()

stocksdata_table = """ CREATE TABLE stocks_data (
                                "time" timestamptz NOT NULL,
                                symbol text NULL,
                                price_open double precision NULL,
                                price_close double precision NULL,
                                price_low double precision NULL,
                                price_high double precision NULL,
                                trading_volume int NULL
                    );"""
stocksdata_hypertable = "SELECT create_hypertable('stocks_data', 'time');"
cursor.execute(stocksdata_table)
cursor.execute(stocksdata_hypertable)
conn.commit()
print("Hypertable create successfully!")
cursor.close()