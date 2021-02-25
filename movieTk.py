import sqlite3
from tkinter import *

class DB:
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY,name TEXT)"
        )
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM movies")
        rows = self.cur.fetchall()
        return rows

    def insert(self,name):
        self.cur.execute("INSERT INTO movies VALUES (NULL,?)",
                         (name,))
        self.conn.commit()

    def remove(self,id):
        self.cur.execute("DELETE FROM movies WHERE id=?",(id,))
        self.conn.commit()


db = DB('new.db')

def movie_list():
    listbox.delete(0,END)
    for row in db.fetch():
        listbox.insert(END,row)

def add():
    db.insert(movie.get())
    listbox.delete(0,END)
    listbox.insert(END,movie.get())
    movie_list()

def selected(event):
    try:
        global selected_value
        index = listbox.curselection()[0]
        selected_value = listbox.get(index)

        entry.delete(0,END)
        entry.insert(END,selected_value[1])
    except IndexError:
        pass

def delete():
    global selected_value
    db.remove(selected_value[0])
    movie_list()

root = Tk()
root.geometry('500x400')
root.title("Movies")
root.config(bg="#74b9ff")



movie = StringVar()


title_label = Label(root,text="My Movie List",font=('Arial',28),fg="#0984e3",bg="#74b9ff").place(x=50,y=35)
listbox = Listbox(root)
listbox.place(x=50,y=120)
listbox.bind('<<ListboxSelect>>',selected)
entry = Entry(root,textvariable=movie)
entry.place(x=250,y=120)
add_button = Button(root,text="Add",width=10,command=add).place(x=250,y=160)
delete_button = Button(root,text="Delete",width=10,command=delete).place(x=250,y=200)



root.mainloop()