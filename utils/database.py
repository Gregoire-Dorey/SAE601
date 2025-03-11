import sqlite3
def insert_in_base(sw_name,latency):
    conn = sqlite3.connect("db-metrics.db")
    curs = conn.cursor()
    curs.execute("INSERT INTO latence (name,latency) VALUES (?,?)",(sw_name,latency))
    conn.commit()
    conn.close()