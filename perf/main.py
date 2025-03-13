from tkinter import *
from tkinter import ttk
import latence as ltc
import graph as grph
import database as db

def latency():
    latency_win = Tk()
    latency_win.title("Mesure de la latence")
    latency_win.geometry("700x300")
    latency_win.resizable(False,False)
    progressbar = ttk.Progressbar(latency_win, orient=HORIZONTAL, length=400)
    progressbar.place(x=150, y=150)
    def lat_launch():
        ltc.latence(str(sw.get()),str(ip.get()),latency_win,progressbar)
    button = Button(latency_win, text="Lancer la mesure", width=15, command=lat_launch)
    button.place(x=20, y=200)
    label = Label(latency_win, text="Quel cible voulez vous atteindre", fg="gray")
    label.place(x=5, y=2)
    ip = Entry(latency_win, width=40)
    ip.pack(pady=10)
    label = Label(latency_win, text="Quel est le nom du switch", fg="gray")
    label.place(x=5, y=60)
    sw = Entry(latency_win, width=40)
    sw.pack(pady=20)



def launch():
    main = Tk()
    main.title("Lancement des tests")
    main.geometry("450x250")
    main.resizable(False, False)
    bienvenue = Label(main, text="Bienvenue, quel test voulez vous effectuer ?")
    bienvenue.place(x=80, y=10)
    button = Button(main, text="Latence", width=10, command=latency)
    button.place(x=85, y=75)
    main.mainloop()

#launch()
grph.bargraph(db.select_latency(),"Latence en fonctionement normal","Nom des switch","Latence (en ms)")
ltc.latence("charge_9200","192.168.111.175")