from tkinter import *
from tkinter import messagebox,ttk
import sqlite3 as sq
import os

os.system("cls")

class add_prod:
    def __init__(self, master: Tk):
       
        self.root = master
        self.root.geometry("800x500")
        self.root.title("New product")
        
        
        Label(self.root, text="Product ID").grid(row=0, column=0,padx=90,pady=40)
        Label(self.root, text="Product Name").grid(row=1, column=0,pady=40)
        Label(self.root, text="Category").grid(row=2, column=0,pady=40)
        Label(self.root, text="Price").grid(row=3, column=0,pady=40)

        self.prod_id = ttk.Entry(self.root)
        self.prod_name = ttk.Entry(self.root)
        self.categoryd=ttk.Combobox(self.root)
        self.price = ttk.Entry(self.root  )

        self.prod_id.grid(row=0, column=1,padx=20)
        self.prod_name.grid(row=1, column=1)
        self.categoryd.grid(row=2,column=1)
        self.price.grid(row=3, column=1)
        self.load_categ()
        Button(self.root, text="Submit", command=self.submit).grid(row=4, column=0, columnspan=2)
    
    def load_categ(self):
        con =sq.connect("database.db")
        cur=con.cursor()
        cur.execute("SELECT cName FROM category")
        self.categoryd['values']=cur.fetchall()
        con.close()
    def submit(self):
        con =sq.connect("database.db")
        cur=con.cursor()
        prod_id = (self.prod_id.get()).upper()
        prod_name = (self.prod_name.get()).upper()
        category = (self.categoryd.get()).upper()
        price = float(self.price.get())
        try:
            cur.execute("INSERT INTO product VALUES(?,?,?,?)"
                        ,[prod_id,prod_name,category,price])
            print("SUCCESS")
            con.commit()
            self.root.withdraw()
            messagebox.showinfo('SUCCESS','Item added successfully !')
            cur.execute("SELECT cName FROM category")
            dt=cur.fetchall()
            if (category,) not in dt and category!='':
                cur.execute("INSERT INTO category VALUES(?)",[category])
                print(dt)
                print(1000)
                con.commit()
                
        except:
            messagebox.showerror('FAILED','Something went wrong !')
            print("DATABASE ERROR !")
        con.close()



        



#a =add_prod(Tk())
#a.root.mainloop()