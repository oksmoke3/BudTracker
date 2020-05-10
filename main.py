import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Notebook as Nb
from tkcalendar import DateEntry
from tkinter import messagebox as ms
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
style.use('fivethirtyeight')


with sqlite3.connect('db.db') as db:
    c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL ,password TEXT NOT NULL);')
c.execute('CREATE TABLE IF NOT EXISTS budget (username TEXT NOT NULL ,amount INT NOT NULL,date TEXT NOT NULL);')
c.execute('CREATE TABLE IF NOT EXISTS expenses (username TEXT NOT NULL ,cost INT NOT NULL,date TEXT NOT NULL,item TEXT NOT NULL);')
db.commit()
db.close()


def LogOut(r1):
	r1.destroy()
	root2 = Tk()
	root2.title("Login")
	main(root2)
	root2.mainloop()

x1=x3=x4=x2=1

#main Class
class main:
	def __init__(self,master):
		
			self.master = master
			self.username = StringVar()
			self.password = StringVar()
			self.n_username = StringVar()
			self.n_password = StringVar()
			self.widgets()

	#Login Function
	def login(self):
		flag=0
		with sqlite3.connect('db.db') as db:
			c = db.cursor()

		find_user = ('SELECT * FROM user WHERE username = ? and password = ?')
		c.execute(find_user,[(self.username.get()),(self.password.get())])
		result = c.fetchall()

		if result:
			flag=1
		else:
			ms.showerror('Oops!','Username Not Found.')

		if flag==1:
			self.master.destroy()
			def Error(a):
				if a==1:
					ms.showerror("ERROR!", "Incorrect Entry. Retry.")
				if a==2:
					ms.showerror("ERROR!", "Insufficient Budget. Add Budget.")

			def AddItem():
				a=item.get()
				b=cal.get()
				c=expense.get()

				with sqlite3.connect('db.db') as db:
					cd = db.cursor()
				f1='Select sum(cost) from expenses where username=?'
				f2='Select sum(amount) from budget where username=?'
				cd.execute(f1,[(self.username.get())])
				Esum = cd.fetchall()
				cd.execute(f2,[(self.username.get())])
				Bsum = cd.fetchall()
				
				if(a==''or c==''):
					Error(1)
					return

				try:
					c=int(c)
				except:
					Error(1)
					return

				try:
					s1=int(Bsum[0][0])
				except:
					s1=0
				
				try:
					s2=int(Esum[0][0])
				except:
					s2=0

				if (s1-s2-c<0):
					Error(2)
					return
				
				with sqlite3.connect('db.db') as db:
					cd = db.cursor()	
				insert = 'INSERT INTO expenses(username,cost,date,item) VALUES(?,?,?,?)'
				cd.execute(insert,[(self.username.get()),c,b,a])
				db.commit()
				ShowData(5,Table,['Item','Date','Expense'])

			def AddAmount():
				a=amt.get()
				b=Bcal.get()

				try:
					a=int(a)
				except:
					Error(1)
					return

				with sqlite3.connect('db.db') as db:
					c = db.cursor()
				insert = 'INSERT INTO budget(username,amount,date) VALUES(?,?,?)'
				c.execute(insert,[(self.username.get()),a,b])
				db.commit()
				ShowData(90,Table1,['Amount','Date'])

			
			def ShowData(t,table,col):
				k=0
				for i in col:
					try:
						table.heading(i,text=i.title())
						table.column(k,anchor ='c')
						k+=1
					except:
						pass
				table.grid(row=4,column=1,padx=t,pady=5,sticky='w')

				if t==90:
					with sqlite3.connect('db.db') as db:
						c = db.cursor()	
					f=('Select * from budget where username=? order by date desc')
					c.execute(f,[(self.username.get())])
					x=c.fetchall()

					table.delete(*table.get_children())
					for data in x:
						d=[data[1],data[2]]
						table.insert('','end',values=d)

					with sqlite3.connect('db.db') as db:
						cd = db.cursor()
					f1='Select sum(amount) from budget where username=?'
					cd.execute(f1,[(self.username.get())])
					Bsum = cd.fetchall()
					try:
						s1=int(Bsum[0][0])
					except:
						s1=0	
					T1=Text(Budget,bg='white',font='TkDefaultFont',height=1,width=25)
					T1.insert(INSERT,"Total Budget:	     "+str(s1))
					T1.grid(row=5, column=1, padx=90 ,pady=5,sticky='w')					

				if t==5:
					with sqlite3.connect('db.db') as db:
						c = db.cursor()	
					f=('Select * from expenses where username=? order by date desc')
					c.execute(f,[(self.username.get())])
					x=c.fetchall()	

					table.delete(*table.get_children())
					for data in x:
						d=[data[3],data[2],data[1]]
						table.insert('','end',values=d)

					with sqlite3.connect('db.db') as db:
						cd = db.cursor()
					f1='Select sum(cost) from expenses where username=?'
					cd.execute(f1,[(self.username.get())])
					Esum = cd.fetchall()
					try:
						s1=int(Esum[0][0])
					except:
						s1=0					
					
					T1=Text(Exp,bg='white',font='TkDefaultFont',height=1,width=25)
					T1.insert(INSERT,"Total Expenses:	 "+str(s1))
					T1.grid(row=5, column=1, padx=200 ,pady=5,sticky='w')
				
			def graph_data():
				leg='Money Spent','Money left'
				amount=0
				cost=0
				with sqlite3.connect('db.db') as db:
					c = db.cursor()
				find = ('SELECT amount FROM budget WHERE username = ?')
				c.execute(find,[(self.username.get())]) 
				for row in c.fetchall():
					amount+=row[0]
				find = ('SELECT cost FROM expenses WHERE username = ?')
				c.execute(find,[(self.username.get())])
				for row in c.fetchall():
					cost+=row[0]
				if cost==0 and amount==0:
					ms.showerror("Error","No budget and expenses entered!")
					return
				sizes=[cost,amount-cost]		
				colors = ['red','gold']
				labels=[cost,amount-cost]
				explode=[0.1,0]
				patches, texts = plt.pie(sizes,explode=explode,colors=colors,labels=labels, shadow=True, startangle=90)
				plt.legend(patches,leg, loc="best")
				plt.axis('equal')
				plt.tight_layout()
				plt.show()
			
			def deleteData(win,col):
				if win==Budget:
					with sqlite3.connect('db.db') as db:
						cd = db.cursor()
					f1='delete from budget where username=?'
					try:
						cd.execute(f1,[self.username.get()])
					except:
						pass
					
					db.commit()
					ShowData(90,Table1,col)
				else:
					with sqlite3.connect('db.db') as db:
						cd = db.cursor()
					f1='delete from expenses where username=?'
					try:
						cd.execute(f1,[self.username.get()])
					except:
						pass
					db.commit()
					
					ShowData(5,Table,col)

			def delete_selected(t,p):				
				select = t.selection()   
				sel=t.set(select)    
				for i in select:  
					t.delete(i)
				if p==1:
					a=sel['Amount']
					b=sel['Date']
					with sqlite3.connect('db.db') as db:
						cd = db.cursor()
					f1='delete from budget where username= ? and amount= ? and date= ?'
					cd.execute(f1,[self.username.get(),a,b])
					db.commit()
					ShowData(90,t,['Amount','Date'])
				if p==2:
					a=sel['Item']
					b=sel['Date']
					c=sel['Expense']
					with sqlite3.connect('db.db') as db:
						cd = db.cursor()
					f1='delete from expenses where username= ? and item= ? and date= ? and cost=?'
					cd.execute(f1,[self.username.get(),a,b,c])
					db.commit()
					ShowData(5,t,['Item','Date','Expense'])
				
			def sort(a,b,table):
				global x1,x2,x3,x4
				with sqlite3.connect('db.db') as db:
					cd = db.cursor()
				if(a==1):
					if(b==1):
						if x1==1:
							f1='Select * from expenses where username=? order by item asc'
							x1=0
							cd.execute(f1,[(self.username.get())])
						else:
							f1='Select * from expenses where username=? order by item desc'
							x1=1
							cd.execute(f1,[(self.username.get())])
					if(b==2):
						if x2==1:
							f1='Select * from expenses where username=? order by date asc'
							x2=0
							cd.execute(f1,[(self.username.get())])
						else:
							f1='Select * from expenses where username=? order by date desc'
							x2=1
							cd.execute(f1,[(self.username.get())])
					if(b==3):
						if x3==1:
							f1='Select * from expenses where username=? order by cost asc'
							x3=0
							cd.execute(f1,[(self.username.get())])
						else:
							f1='Select * from expenses where username=? order by cost desc'
							x3=1
							cd.execute(f1,[(self.username.get())])
					
					x=cd.fetchall()	
					table.delete(*table.get_children())
					for data in x:
						d=[data[3],data[2],data[1]]
						table.insert('','end',values=d)

				if(a==2):
					if(b==1):
						if x4==1:
							f1='Select * from budget where username=? order by amount asc'
							x4=0
							cd.execute(f1,[(self.username.get())])
						else:
							f1='Select * from budget where username=? order by amount desc'
							x4=1
							cd.execute(f1,[(self.username.get())])
					if(b==2):
						if x3==1:
							f1='Select * from budget where username=? order by date asc'
							x3=0
							cd.execute(f1,[(self.username.get())])
						else:
							f1='Select * from budget where username=? order by date desc'
							x3=1
							cd.execute(f1,[(self.username.get())])

					x=cd.fetchall()
					table.delete(*table.get_children())
					for data in x:
						d=[data[1],data[2]]
						table.insert('','end',values=d)
						
			def deleteUser():
				f1='delete from budget where username=?'
				try:
					cd.execute(f1,[(self.username.get())])
				except:
					pass
				f1='delete from expense where username=?'
				try:
					cd.execute(f1,[(self.username.get())])
				except:
					pass
				f1='delete from user where username=?'
				cd.execute(f1,[(self.username.get())])

			root1=Tk()
			root1.title("Let's do this")
			root1.geometry('700x500')
			nb=Nb(root1)

			Budget=Frame(nb,width=500,height=500)
			Exp=Frame(nb,width=500,height=500)
			Graph=Frame(nb,width=500,height=500)

			nb.add(Budget,text="Budget")
			nb.add(Exp,text="Expense")
			nb.add(Graph,text="Graph")
			nb.pack(fill=BOTH,expand=1)

			#--------------- BUDGET-----------------------
			#Amount
			amt=StringVar()
			Amount=Label(Budget,text="Amount")
			Amount.grid(row=0,column=0,padx=5,pady=5)
			AmountEntry=Entry(Budget,textvariable=amt)
			AmountEntry.grid(row=0, column=1, padx=5 ,pady=5,sticky='w')

			#BDate 
			BDate=Label(Budget,text="Date")
			BDate.grid(row=1, column=0, padx=5 ,pady=5)
			Bcal=DateEntry(Budget,width=17,date_pattern='dd/mm/yyyy')
			Bcal.grid(row=1, column=1, padx=5 ,pady=5,sticky='w')

			# Add Amount
			Add=Button(Budget,text="Add Amount",command=AddAmount)
			Add.grid(row=3,column=1,padx=5,pady=5,sticky='w')

			#BTable
			l=['Amount','Date']
			Table1=ttk.Treeview(Budget,selectmode='browse')
			Table1.configure(column=l,show='headings',height=10)
			Table1.heading('Amount',command=lambda: sort(2,1,Table1))
			Table1.heading('Date',command=lambda: sort(2,2,Table1))
			
			#Delete all entries
			DeleteAll=Button(Budget,text="Delete All Entries",command= lambda: deleteData(Budget,l))
			DeleteAll.grid(row=3,column=1,padx=350,pady=5,sticky='w')

			#Delete Selected
			bSel=Button(Budget,text="Delete Selected",command= lambda: delete_selected(Table1,1))
			bSel.grid(row=3,column=1,padx=175,pady=5,sticky='w')

			#Logout
			bLout=Button(Budget,text="Log Out",command=lambda:LogOut(root1))
			bLout.grid(row=7,column=1,padx=265,pady=5,sticky='w')	

			ShowData(90,Table1,l)
			
			#--------------- EXPENSE-----------------------
			#Item 
			item=StringVar()
			Item=Label(Exp,text="Item")
			Item.grid(row=0,column=0,padx=5,pady=5)
			ItemEntry=Entry(Exp,textvariable=item)
			ItemEntry.grid(row=0, column=1, padx=5 ,pady=5,sticky='w')

			#Date 
			Date=Label(Exp,text="Date")
			Date.grid(row=1, column=0, padx=5 ,pady=5)
			cal=DateEntry(Exp,width=17,date_pattern='dd/mm/yyyy')
			cal.grid(row=1, column=1, padx=5 ,pady=5,sticky='w')

			#Expense
			expense=StringVar()
			Expense=Label(Exp,text="Cost")
			Expense.grid(row=2,column=0,padx=5,pady=5)
			ExpenseEntry=Entry(Exp,textvariable=expense)
			ExpenseEntry.grid(row=2, column=1, padx=5 ,pady=5,sticky='w')

			#Add
			Add=Button(Exp,text="Add Item",command=AddItem)
			Add.grid(row=3,column=1,padx=75,pady=5,sticky='w')

			#Table
			l=['Item','Date','Expense']
			Table=ttk.Treeview(Exp,selectmode='browse')
			Table.configure(column=l,show='headings',height=10)
			Table.heading('Item',command=lambda: sort(1,1,Table))
			Table.heading('Date',command=lambda: sort(1,2,Table))
			Table.heading('Expense',command=lambda: sort(1,3,Table))

			#Delete Selected
			eSel=Button(Exp,text="Delete Selected",command= lambda: delete_selected(Table,2))
			eSel.grid(row=3,column=1,padx=270,pady=5,sticky='w')

			#Delete all entries
			EDeleteAll=Button(Exp,text="Delete All Entries",command= lambda: deleteData(Exp,l))
			EDeleteAll.grid(row=3,column=1,padx=450,pady=5,sticky='w')
			
			#Log Out
			ELout=Button(Exp,text="Log Out",command= lambda: LogOut(root1))
			ELout.grid(row=7,column=1,padx=275,pady=5,sticky='w')

			ShowData(5,Table,l)
					
			#----------------------------Graph------------------------------------------------
			gLout=Button(Graph,text="Log Out",command=lambda:LogOut(root1))
			gLout.pack(side=BOTTOM)
			
			get_graph=Button(Graph,text="Graph It!",command=graph_data, height = 5, width = 10)
			get_graph.place(x=300,y=90)

			root1.mainloop()

	
	
			#-------------------------------------------------------------------------------
		
		
	def new_user(self):
			with sqlite3.connect('db.db') as db:
					c = db.cursor()
			if  self.n_username.get()=='':
				ms.showerror('Error!','Please enter a valid username')
				return

			if  self.n_password.get()=='':
				ms.showerror('Error!','Please enter a valid password')
				return

			find_user = ('SELECT * FROM user WHERE username = ?')
			c.execute(find_user,[(self.username.get())])        
			if c.fetchall():
				ms.showerror('Error!','Username Taken Try a Diffrent One.')
			else:
					ms.showinfo('Success!','Account Created!')
					self.log()

			insert = 'INSERT INTO user(username,password) VALUES(?,?)'
			c.execute(insert,[(self.n_username.get()),(self.n_password.get())])
			db.commit()


	def log(self):
			self.username.set('')
			self.password.set('')
			self.crf.pack_forget()
			self.head['text'] = 'LOGIN'
			self.logf.pack()
	def cr(self):
			self.n_username.set('')
			self.n_password.set('')
			self.logf.pack_forget()
			self.head['text'] = 'REGISTER'
			self.crf.pack()
			

	def widgets(self):
			self.head = Label(self.master,text = 'LOGIN',font = ('',35),pady = 10)
			self.head.pack()
			self.logf = Frame(self.master,padx =10,pady = 10)
			Label(self.logf,text = 'Username: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
			Entry(self.logf,textvariable = self.username,bd = 5,font = ('',15)).grid(row=0,column=1)
			Label(self.logf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
			Entry(self.logf,textvariable = self.password,bd = 5,font = ('',15),show = '*').grid(row=1,column=1)
			Button(self.logf,text = ' Login ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.login).grid()
			Button(self.logf,text = ' Create Account ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.cr).grid(row=2,column=1)
			self.logf.pack()
			
			self.crf = Frame(self.master,padx =10,pady = 10)
			Label(self.crf,text = 'Username: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
			Entry(self.crf,textvariable = self.n_username,bd = 5,font = ('',15)).grid(row=0,column=1)
			Label(self.crf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
			Entry(self.crf,textvariable = self.n_password,bd = 5,font = ('',15),show = '*').grid(row=1,column=1)
			Button(self.crf,text = 'Create Account',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.new_user).grid(row=2,column=1)
			Button(self.crf,text = 'Go Back To Login',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.log).grid(row=2)
	

root = Tk()
root.title("Login")
main(root)
root.mainloop()

