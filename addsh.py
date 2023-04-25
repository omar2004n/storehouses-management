from tkinter import *
from tkinter import messagebox
import sqlite3 as sq
import os

os.system("cls")

class add_shouse:
    def __init__(self, master: Tk):
        self.root = master
        self.root.geometry("700x500")
        self.root.title("New Storehouse")
        


        Label(self.root, text="Storehouse ID").grid(row=0, column=0,padx=90,pady=40)
        Label(self.root, text="Name").grid(row=1, column=0,pady=40)
        Label(self.root, text="Address").grid(row=2, column=0,pady=40)
        Label(self.root, text="Supervisor").grid(row=3, column=0,pady=40)
        

        self.shouse_id = Entry(self.root)
        self.shouse_name = Entry(self.root)
        self.address = Entry(self.root)
        self.sup=Entry(self.root)

        self.shouse_id.grid(row=0, column=1,padx=20)
        self.shouse_name.grid(row=1, column=1)
        self.address.grid(row=2, column=1)
        self.sup.grid(row=3,column=1)

        Button(self.root, text="Submit", command=self.submit).grid(row=4, column=0, columnspan=2)

    def submit(self):
        con =sq.connect("database.db")
        cur=con.cursor()
        shouse_id = (self.shouse_id.get()).upper()
        shouse_name =(self.shouse_name.get()).upper()
        address = (self.address.get()).upper()
        sup=(self.sup.get()).upper()
        try:
            cur.execute("INSERT INTO storehouse VALUES(?,?,?,?)"
                        ,[shouse_id,shouse_name,address,sup])
            print("SUCCESS")
            con.commit()
            self.root.withdraw()
            messagebox.showinfo('SUCCESS','Item added successfully !')
            
        except:
            messagebox.showerror('FAILED','Something went wrong !')
            print("DATABASE ERROR !")
        con.close()



        



#a =add_shouse(Tk())
#a.root.mainloop()