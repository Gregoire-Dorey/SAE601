from tkinter import *

def launch():
    main = Tk()
    main.title("Lancement des tests")
    main.geometry("450x250")
    main.resizable(False, False)
    bienvenue = Label(main, text="Bienvenue, quel test voulez vous effectuer ?")
    bienvenue.place(x=80, y=10)
    main.mainloop()

launch()