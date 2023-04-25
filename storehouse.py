import sqlite3 as sq
from datetime import datetime
from tkinter import *
import os
from dbtoexcel import *
from tkinter import ttk,messagebox
from addp import add_prod as ap
from addsh import add_shouse as ash
os.system("cls")
try :
    con =sq.connect("database.db")
    cur=con.cursor()
    cur.executescript("""
CREATE TABLE product(pID TEXT PRIMARY KEY NOT NULL,pName TEXT,category TEXT,price REAL(2));
CREATE TABLE storehouse(hID TEXT PRIMARY KEY NOT NULL,hName TEXT,hAddress TEXT,supervisor TEXT);
CREATE TABLE history(pID TEXT NOT NULL,pName TEXT,hID TEXT NOT NULL,hName TEXT,operation CHAR(1),amount INT,time TEXT);
CREATE TABLE availability(pID TEXT,hID TEXT,num INT);
CREATE TABLE category(cName TEXT);
""")
    con.commit()
    con.close()
except:
    print()

class App:
    def __init__(self,master:Tk):
        self.bgimage=PhotoImage(file="bg.png")
        self.root=master
        self.bg =Label(self.root,image=self.bgimage)
        self.bg.place(x=0,y=0)
        self.root.title("GREEN ZONE Management")
        self.root.iconbitmap("logo.ico")
        self.root.geometry("1500x857")
        self.root.resizable(0,0)

        self.mframe=Frame(self.root,width=200,height=200,bg='')
        self.mframe.pack(side=TOP,padx=600,pady=300)
        self.mframe.pack_propagate(0)

        self.prod =Button(self.mframe,text="Product management",bd=0,command=lambda:self.prod_section())
        self.prod.pack(side=TOP,pady=10)
        self.shouse =Button(self.mframe,text="Storehouse management",bd=0,command=lambda:self.shouse_section())
        self.shouse.pack(side=TOP,pady=10)
        self.history =Button(self.mframe,text="History of products",bd=0,command=lambda:self.init_hist())
        self.history.pack(side=TOP,pady=10)
        self.expbutton = Button(self.mframe,text='Export',bd=0,command=lambda:self.backup())
        self.expbutton.pack(side=TOP,pady=10)
        self.root.protocol("WM_DELETE_WINDOW",self.close)
        self.hide_add_p()
        self.hide_shouse()
        self.rowcont =[]
        

    
    def close(self):
        self.root.destroy()
        self.win.root.destroy()
        self.asho.root.destroy()
    def prod_section(self):
        self.mframe.pack_forget()
        self.pframe=Frame(self.root,width=1500,height=857)
        self.bg.place(x=0,y=0)
        self.pframe.pack_propagate(0)
        self.pframe.pack()
        self.bck=PhotoImage(file="back.png")
        self.back= Button(self.pframe,image=self.bck,bd=0,command=lambda :self.bck_home(self.pframe))
        self.back.place(x=40,y=70)

        
        self.add=PhotoImage(file='add-button.png')
        self.rm= PhotoImage(file='minus-button.png')
        self.ref= PhotoImage(file="reload.png")
        self.refbutton=Button(self.pframe,bd=0,image=self.ref,command=lambda:self.load_info(tree,"product"))
        self.refbutton.place(x=1000,y=160)
        addbutton =Button(self.pframe,image=self.add,bd=0,command=self.show_add_p)
        rmbutton =Button(self.pframe,image=self.rm,bd=0,command=lambda:self.delete_prod(tree))
        addbutton.place(x=1100,y=160)
        rmbutton.place(x=1050,y=160)
        self.edit=PhotoImage(file="pen.png")
        editbutton=Button(self.pframe,image=self.edit,bd=0,command=lambda:self.edit_price(tree,float(editentry.get())))
        editentry=ttk.Entry(self.pframe,width=10)
        editentry.place(x=470,y=164)
        editbutton.place(x=580,y=160)
        Label(self.pframe,text="Modify price :").place(x=350,y=164)
        tree = ttk.Treeview(self.pframe, columns=('pname', 'categ','price'),height=1000)
        tree.heading('#0',text='ID')
        tree.heading('pname',text='Name',anchor='w')
        tree.heading('categ',text='Categorie',anchor='w')
        tree.heading('price',text='Price',anchor='w')
        tree.bind('<Double-Button-1>',self.get_row)
        self.load_info(tree,"product")
        tree.pack(pady=200)
    def edit_price(self,tree:ttk.Treeview,price):
        con =sq.connect("database.db")
        cur =con.cursor()
        a=tree.item(tree.selection()[0])
        cur.execute("UPDATE product SET price=? WHERE pID=?",[price,a['text']])
        con.commit()
        con.close()
        self.load_info(tree,"product")
        
        
    def hide_add_p(self):
        self.win=ap(Tk())
        self.win.load_categ()
        self.win.root.withdraw()
    def show_add_p(self):
         self.win.root.deiconify()
         self.win.root.iconbitmap("logo.ico")
         self.win.load_categ()
         self.win.root.protocol("WM_DELETE_WINDOW",self.hide_add_p())

    def shouse_section(self):
        self.mframe.pack_forget()
        self.sframe=Frame(self.root,width=1500,height=857)
        self.sframe.pack_propagate(0)
        self.sframe.pack()

        self.bck=PhotoImage(file="back.png")
        self.back= Button(self.sframe,image=self.bck,bd=0,command=lambda :self.bck_home(self.sframe))
        self.back.place(x=40,y=70)

        self.ref= PhotoImage(file="reload.png")
        self.refbutton=Button(self.sframe,bd=0,image=self.ref,command=lambda:self.load_info(tree,'storehouse'))
        self.refbutton.place(x=1000,y=110)
        self.add=PhotoImage(file='add-button.png')
        self.rm= PhotoImage(file='minus-button.png')
        addbutton =Button(self.sframe,image=self.add,bd=0,command=self.show_ash)
        rmbutton =Button(self.sframe,image=self.rm,bd=0,command=lambda:self.delete_sh(tree))
        addbutton.place(x=1100,y=110)
        rmbutton.place(x=1050,y=110)

        tree=ttk.Treeview(self.sframe,columns=('name','address','sup'))
        tree.heading('#0',text='ID')
        tree.heading('name',text='Name')
        tree.heading('address',text='Address')
        tree.heading('sup',text='Supervisor')
        self.load_info(tree,'storehouse')
        tree.bind('<Double-Button-1>',self.sh_access)
        tree.pack(pady=150)
    def hide_shouse(self):
        self.asho= ash(Tk())
        self.asho.root.withdraw()
    def show_ash(self):
         self.asho.root.deiconify()
         self.asho.root.iconbitmap("logo.ico")
         self.root.update_idletasks()
         self.asho.root.protocol("WM_DELETE_WINDOW",self.hide_shouse())


    def availability(self,shouse:list):
        self.sframe.pack_forget()
        self.avframe=Frame(self.root,width=1500,height=857)
        self.avframe.pack_propagate(0)
        self.avframe.pack()

        self.bck=PhotoImage(file="back.png")
        self.back= Button(self.avframe,image=self.bck,bd=0,command=lambda :self.bck_home(self.avframe))
        self.back.place(x=40,y=70)

        self.ref= PhotoImage(file="reload.png")
        self.refbutton=Button(self.avframe,bd=0,image=self.ref,command=lambda:self.load_hsc(tree))
        self.refbutton.place(x=1000,y=110)
        self.add=PhotoImage(file='add-button.png')
        self.rm= PhotoImage(file='minus-button.png')
        self.edit=PhotoImage(file='pen.png')
        addbutton =Button(self.avframe,image=self.add,bd=0,command=lambda:self.assign_prod(shouse[0],tree))
        rmbutton =Button(self.avframe,image=self.rm,bd=0,command=lambda:self.delete_assign(tree))
        editbutton=Button(self.avframe,image=self.edit,bd=0,command=lambda:self.edit_num(tree,int(editentry.get())))
        editentry=ttk.Entry(self.avframe)
        editentry.place(x=820,y=404)
        addbutton.place(x=1100,y=110)
        rmbutton.place(x=1050,y=110)
        editbutton.place(x=1050,y=400)

        self.get_prod()
        self.com=ttk.Combobox(self.avframe,state='readonly')
        self.com['values']= self.get_prod()
        self.com.place(x=800,y=115)
        


        tree=ttk.Treeview(self.avframe,columns=('name','category','price','num','sh'))
        tree.heading('#0',text='pID')
        tree.heading('name',text='Name')
        tree.heading('category',text='Category')
        tree.heading('price',text='Price')
        tree.heading('num',text='Quantity')
        tree.heading('sh',text='Storehouse')
        self.load_hsc(tree)
        tree.bind('<Double-Button-1>',)
        tree.pack(pady=150)
    def init_hist(self):
        self.mframe.pack_forget()
        self.ihframe=Frame(self.root,width=1500,height=857)
        self.ihframe.pack_propagate(0)
        self.ihframe.pack()

        self.bck=PhotoImage(file="back.png")
        self.back= Button(self.ihframe,image=self.bck,bd=0,command=lambda :self.bck_home(self.ihframe))
        self.back.place(x=40,y=70)

        self.ref= PhotoImage(file="reload.png")
        self.refbutton=Button(self.ihframe,bd=0,image=self.ref,command=lambda:self.load_info(tree,'storehouse'))
        self.refbutton.place(x=1000,y=110)
        self.add=PhotoImage(file='add-button.png')
        self.rm= PhotoImage(file='minus-button.png')
        

        tree=ttk.Treeview(self.ihframe,columns=('name','address','sup'))
        tree.heading('#0',text='ID')
        tree.heading('name',text='Name')
        tree.heading('address',text='Address')
        tree.heading('sup',text='Supervisor')
        self.load_info(tree,'storehouse')
        tree.bind('<Double-Button-1>',self.shh_access)
        tree.pack(pady=150)
    def hist_section(self):
        self.ihframe.pack_forget()
        self.hframe=Frame(self.root,width=1500,height=857)
        self.hframe.pack_propagate(0)
        self.hframe.pack()
        
        
        self.expbt =PhotoImage(file="export.png")
        self.exbttn =Button(self.hframe,bd=0,image =self.expbt,command=lambda:hist_excel(self.rowcont[0]))
        self.exbttn.place(x=1400,y=110)
        self.bck=PhotoImage(file="back.png")
        self.back= Button(self.hframe,image=self.bck,bd=0,command=lambda :self.bck_home(self.hframe))
        self.back.place(x=40,y=70)

        self.ref= PhotoImage(file="reload.png")
        self.refbutton=Button(self.hframe,bd=0,image=self.ref,command=lambda:self.load_history(tree))
        self.refbutton.place(x=1350,y=110)
        tree =ttk.Treeview(self.hframe,columns=('pname','hid','shouse','operation','amount','time'),height=900)
        tree.heading('#0',text='pID')
        tree.heading('pname',text='Product')
        tree.heading('hid',text='hsID')
        tree.heading('shouse',text='Store House')
        tree.heading('operation',text='Operation')
        tree.heading('amount',text='Amount')
        tree.heading('time',text='Time')
        self.load_history(tree)       
        tree.pack(pady=150)

    def get_row(self,event):
        rw=event.widget.selection()[0]
        a=event.widget.item(rw)
        a['values'].insert(0,(event.widget.item(rw)['text']))
        self.rowcont=a['values']
        return a['values']

    def sh_access(self,event):
        self.get_row(event) 
        if(self.sframe.winfo_manager() is not None):
             self.availability(self.rowcont)   
    def shh_access(self,event):
        self.get_row(event) 
        if(self.ihframe.winfo_manager() is not None):
             self.hist_section()   

    def bck_home(self,frame:Frame):
        frame.destroy()
        #self.__init__(self.root)
        self.mframe.pack(side=TOP,padx=600,pady=300)


    def load_info(self,tree:ttk.Treeview,table:str):
        con =sq.connect("database.db")
        cur =con.cursor()
        tree.delete(*tree.get_children())
        cur.execute("SELECT * FROM "+str(table))
        info = cur.fetchall()
        for i in info:
     
            tree.insert('','end',text=i[0],values=i[1:])
        con.close()

    def load_hsc(self,tree:ttk.Treeview):
        con =sq.connect("database.db")
        cur =con.cursor()
        tree.delete(*tree.get_children())
        cur.execute("""SELECT p.pID,p.pName,p.category,p.price,av.num,s.hName
         FROM product as p JOIN availability as av ON p.pID=av.pID 
         JOIN storehouse as s ON s.hID=av.hID WHERE av.hID=?""",[self.rowcont[0]])
        info = cur.fetchall()
        for i in info:
            tree.insert('','end',text=i[0],values=i[1:])
        con.close()
    def delete_prod(self,tree:ttk.Treeview):
        con =sq.connect("database.db")
        cur =con.cursor()
        a=tree.item(tree.selection()[0])
        try:
            cur.execute("""DELETE FROM product WHERE pID=? ;""",[a['text']])
            con.commit()
            cur.execute("""DELETE FROM availability WHERE pID=?""",[a['text']])
            con.commit()
            messagebox.showinfo("PRODUCT_DELETION",("Product ",a['values'][0]," has been deleted successfully !"))
        except:
            messagebox.showerror("",("UNABLE TO DELETE product ",a['values']))
        self.load_info(tree,"product")
        con.close()
        
    def delete_sh(self,tree:ttk.Treeview):
        con =sq.connect("database.db")
        cur =con.cursor()
        a=tree.item(tree.selection()[0])
        try:
            cur.execute("""DELETE FROM storehouse WHERE hID=? ;""",[a['text']])
            con.commit()
            cur.execute("""DELETE FROM availability WHERE hID=?""",[a['text']])
            con.commit()
            messagebox.showinfo("PRODUCT_DELETION",("Storehouse ",a['values'][0]," has been deleted successfully !"))
        except:
            messagebox.showerror("",("UNABLE TO DELETE storehouse ",a['values']))
        self.load_info(tree,"storehouse")
        con.close()

    def get_prod(self):
        con =sq.connect("database.db")
        cur =con.cursor()
        cur.execute("SELECT pID,pName FROM product;")
        a=cur.fetchall()
        for i in a:
            a[a.index(i)]=i[0]+"|"+i[1]
        con.close()
        return a
    def ret_prod(self,n:str):
        a=""
        for i in range(len(n)):
            if n[i]=='|':
                break;
            a+=n[i]
        return a
        
    def assign_prod(self,shouse:str,tree:ttk.Treeview):
        con =sq.connect("database.db")
        cur =con.cursor()
        prod=self.ret_prod((self.com.get()))
        cur.execute("SELECT hID FROM availability WHERE pID=?",[prod])

        check =cur.fetchall()
        if (shouse,) in check:
            
                print("Item already exist")
                return
        cur.execute("INSERT INTO availability VALUES(?,?,0)",[prod,shouse])
        con.commit()
        con.close()
        self.load_hsc(tree)
    def delete_assign(self,tree:ttk.Treeview):
        con =sq.connect("database.db")
        cur =con.cursor()
        a=tree.item(tree.selection()[0])
        
        cur.execute("""DELETE FROM availability WHERE pID=? AND hID=?;""",[a['text'],self.rowcont[0]])
        con.commit()
        messagebox.showinfo("PRODUCT_DELETION",("Product ",a['values'][0]," has been deleted successfully !"))
        
        self.load_hsc(tree)
        con.close()
    def edit_num(self,tree:ttk.Treeview,num:int):
         con =sq.connect("database.db")
         cur =con.cursor()
         a=tree.item(tree.selection()[0])
         cur.execute("SELECT num FROM availability WHERE pID=? AND hID=?",[a['text'],self.rowcont[0]])
         prevnum=cur.fetchall()[0][0]
         if(num>0):
             op='d'
         elif (num<0):
             op='w'
         prevnum+=num
         current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
         cur.execute("SELECT pName FROM product WHERE pID=?",[a['text']])
         name=cur.fetchall()
         cur.execute("UPDATE availability SET num=? WHERE pID=? AND hID=?;",[prevnum,a['text'],self.rowcont[0]])
         con.commit()
         cur.execute("INSERT INTO history VALUES(?,?,?,?,?,?,?)",[a['text'],name[0][0],self.rowcont[0],self.rowcont[1],op,num,current_time])
         con.commit()
         self.load_hsc(tree)
         con.close()
    def load_history(self,tree:ttk.Treeview):
        con =sq.connect("database.db")
        cur =con.cursor()
        tree.delete(*tree.get_children())
        a=self.rowcont
        cur.execute("SELECT * FROM history WHERE hID=? ORDER BY time DESC",[a[0]])
        a= cur.fetchall()
        for i in a:
            i=list(i)
            if i[4]=='w':
                i[4]='Withdraw'
            elif i[4]=='d':
                i[4]="Deposit"
            tree.insert('','end',text=i[0],values=i[1:])
        con.close()
    def backup(self):
        try:
            os.mkdir("backup")
        except:
            print()
        os.system(r'copy .\\database.db .\\backup\\database.db')
        export_db()
        

        
    


a =App(Tk())
a.root.mainloop()