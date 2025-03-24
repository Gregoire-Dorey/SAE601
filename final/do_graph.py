import matplotlib.pyplot as plt
import database as db

db_return = db.select_latency("mt_latence")

for i in range(len(db_return)):
    x = db_return[i][1]
    print(x)


