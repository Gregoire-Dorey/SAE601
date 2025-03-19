import sqlite3
def insert_in_base(sw_name,latency):
    conn = sqlite3.connect("./utils/db-test.db")
    curs = conn.cursor()
    curs.execute("INSERT INTO latence (name,latence) VALUES (?,?)",(sw_name,latency))
    conn.commit()
    conn.close()

def select_latency():
    conn = sqlite3.connect("./utils/db-test.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, latence FROM latence")
    data = cursor.fetchall()
    conn.close()
    return data

print(select_latency())