import sqlite3
import datetime as dt


def insert_in_base(sw_name,latency,table):
    if type(sw_name)!=str:
        sw_name = str(sw_name)
    if type(latency)!=str:
        latency = str(latency)
    if type(table)!=str:
        table = str(table)
    date = dt.datetime.now()
    date = date.strftime("%d/%m/%Y-%H:%M:%S")
    conn = sqlite3.connect("db-metrics.db")
    curs = conn.cursor()
    curs.execute(f"INSERT INTO {table} (switch_name,latence,date) VALUES (?,?,?);",(sw_name,latency,date))
    conn.commit()
    conn.close()

def select_latency(table):
    conn = sqlite3.connect("db-metrics.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT switch_name, latence FROM {table};")
    data = cursor.fetchall()
    conn.close()
    return data


#print(select_latency())