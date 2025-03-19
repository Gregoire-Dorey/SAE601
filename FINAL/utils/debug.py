import sqlite3

conn = sqlite3.connect("db-test.db")
cursor = conn.cursor()
try:
    cursor.execute("SELECT * FROM latence;")
    print(cursor.fetchall())
except sqlite3.OperationalError as e:
    print("Error:", e)
conn.close()
