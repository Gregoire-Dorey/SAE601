import sqlite3
def insert_in_base(sw_name,latency,table):
    conn = sqlite3.connect("./db-test.db")
    curs = conn.cursor()
    curs.execute(f"INSERT INTO {table} (switch_name,latence) VALUES (?,?);",(sw_name,latency))
    conn.commit()
    conn.close()

def select_latency(table):
    conn = sqlite3.connect("./db-test.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT name, latence FROM {table};")
    data = cursor.fetchall()
    conn.close()
    return data


#print(select_latency())