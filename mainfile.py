from tkinter import *
import subprocess 
import mysql.connector as mysql
import tkinter.messagebox as MessageBox
from PIL import Image, ImageDraw, ImageTk

def center_window(w=300, h=200):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)    
    y = (hs/3) - (h/3)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

root = Tk()
center_window(500,500)
root.title("Take Attendance")
root.configure(bg='#fdba9a')


canvas = Canvas(root,width=500,height=500)
image = ImageTk.PhotoImage(Image.open("wood1.jpg"))

canvas.create_image(0,0,anchor=NW,image=image)
canvas.pack()


username = StringVar()
password = StringVar()

def addfaculty():
    root.destroy()
    subprocess.call(["python","registerFaculty.py"])


def login():
    uname = username.get()
    passw = password.get()
    if(uname=="" or passw==""):
        MessageBox.showinfo("Insert Status","All fields are required!")
    else:
        con = mysql.connect(host="localhost",user="root",password="",database="test")
        custor = con.cursor()
        custor.execute('select * from faculty_info where username = %s and password = %s',(uname,passw))
        rows = custor.fetchall()
        if rows:
            con.close()
            root.destroy()
            subprocess.call(["python","adminPanel.py"])
        else:
            MessageBox.showinfo("Login Status","Faculty not found!")
            

label_0 = Label(root, text="Admin Panel",width=20,font=("bold", 30),fg='#42240c')
label_0.place(x=15,y=53)


label_1 = Label(root, text="Username",width=17,font=("bold", 10))
label_1.place(x=80,y=150)

entry_1 = Entry(root,textvariable=username)
entry_1.place(x=280,y=150)

label_2 = Label(root, text="Password",width=17,font=("bold", 10))
label_2.place(x=80,y=200)

entry_2 = Entry(root,textvariable=password,show="*")
entry_2.place(x=280,y=200)


Button(root, text='Login',width=20,bg='brown',fg='white',command=login).place(x=180,y=280)

Button(root, text='Add Faculty',width=20,bg='brown',fg='white',command=addfaculty).place(x=180,y=340)

root.mainloop()