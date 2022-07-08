import psycopg2

conn = psycopg2.connect(database="tsdb",
                        host="urje56javi.s0p1cle568.tsdb.cloud.timescale.com",
                        user="tsdbadmin",
                        password="yE8-7cZrSy0O!5",
                        port=35132)

cursor = conn.cursor()

cursor.execute("SELECT drop_chunks('stocks_data', INTERVAL '1 SECOND');")
conn.commit()
print("Delete successfully!")
cursor.close()