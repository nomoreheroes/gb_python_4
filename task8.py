from tkinter import *
from tkinter import ttk
import sqlite3 as sq

conn = None

def save_contact(name, phone,root, frame,id=None):
    global conn
    try:
        cur = conn.cursor()
        if id is None:
            cur.execute("INSERT INTO phones (name,phone) VALUES ('{0}',{1})".format(name,phone))
        else:
            cur.execute("UPDATE phones SET name='{0}', phone={1} WHERE id={2}".format(name,phone,id))
        conn.commit()
        refresh_phones_list(frame,"")
    except sq.Error as e:
        print (e)
    root.destroy()

def clear_frame(frame):
    for widgets in frame.winfo_children():
      widgets.destroy()

def refresh_phones_list(frame,query):
    clear_frame(frame)
    if query == "":
        contacts = get_initial_contacts()
    else:
        contacts = []
        q = "SELECT * FROM phones WHERE name LIKE '{0}%' OR phone LIKE '{0}%'".format(query)
        print(q)
        cur = conn.execute(q)
        for row in cur:
            contacts.append({"id":row[0],"name":row[1],"phone":row[2]})
    if len(contacts) > 0:
        for i, contact in enumerate(contacts):
            print(contact)
            ttk.Label(frame,text="{0} ({1})".format(contact["phone"],contact["name"])).grid(column=0, row=i)
            ttk.Button(frame,text="Редактировать",command=lambda contact=contact.copy(): edit_contact(frame,contact)).grid(column=1,row=i)
            ttk.Button(frame,text="Удалить",command=lambda contact=contact.copy(): del_contact(frame,contact)).grid(column=2,row=i)
    else:
        ttk.Label(frame, text="Нет контактов в справочнике").grid(column=0, row=0)


def get_initial_contacts():
    global conn
    rs = []
    if conn is None:
        conn = sq.connect('phones.db')  
    tables = conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='phones'")
    if [row[0] for row in tables][0] == 0:
        conn.execute("CREATE TABLE phones  (ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT NOT NULL, PHONE INT NOT NULL)")
        return rs
    cur = conn.execute("SELECT * FROM phones LIMIT 10")
    for row in cur:
        rs.append({"id":row[0],"name":row[1],"phone":row[2]})
    return rs


def edit_contact(frame,contact=None):
    root = Tk()
    frm = ttk.Frame(root, padding=10, height=200)
    frm.grid()
    ttk.Label(frm, text="Номер телефона").pack()
    e1 = ttk.Entry(frm, width=30)
    e1.pack()
    ttk.Label(frm, text="Имя").pack()
    e2 = ttk.Entry(frm, width=30,)
    e2.pack()
    ttk.Button(frm, text="Сохранить", command=lambda: save_contact(e2.get(),e1.get(),root, frame,id=contact["id"])).pack()
    if contact is not None:
        if "name" in contact and "phone" in contact:
            e1.delete(0, END)
            e1.insert(0, contact["phone"])
            e2.delete(0, END)
            e2.insert(0, contact["name"])
    root.mainloop()

def del_contact(frame, contact):
    global conn
    if contact is not None and "id" in contact:
        conn.execute("DELETE FROM phones WHERE id={0}".format(contact["id"]))
    refresh_phones_list(frame,"")                       

def search(frame,e):
    value = e.widget.get()
    refresh_phones_list(frame,value)

def create_window():
    root = Tk()
    frm = ttk.Frame(root, padding=10, height=200)
    frm.grid()
    ttk.Label(frm, text="Введите либо номер телефона либо имя контакта").pack()
    e = ttk.Entry(frm, width=30)
    e.pack()
    w = ttk.LabelFrame(frm, width="100",text="Список контактов (первые десять)")
    w.pack(fill="both", expand="yes")
    e.bind("<KeyRelease>",lambda e: search(w,e))
    contacts = get_initial_contacts()
    if len(contacts) > 0:
        for i, contact in enumerate(contacts):
            print (contact)
            ttk.Label(w,text="{0} ({1})".format(contact["phone"],contact["name"])).grid(column=0, row=i)
            ttk.Button(w,text="Редактировать",command=lambda contact=contact.copy(): edit_contact(w,contact)).grid(column=1,row=i)
            ttk.Button(w,text="Удалить",command=lambda contact=contact.copy(): del_contact(w,contact)).grid(column=2,row=i)
    else:
        ttk.Label(w, text="Нет контактов в справочнике").grid(column=0, row=0)
    ttk.Button(frm,text="Добавить новый контакт",command=lambda: edit_contact(w)).pack()
    ttk.Button(frm, text="Quit", command=root.destroy).pack()
    root.mainloop()

create_window()