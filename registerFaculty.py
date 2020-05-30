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


canvas = Canvas(root,width=500,height=500)
image = ImageTk.PhotoImage(Image.open("wood1.jpg"))

canvas.create_image(0,0,anchor=NW,image=image)
canvas.place(x=0,y=0)


username = StringVar()
password = StringVar()
fullname = StringVar()

def back():
    root.destroy()
    subprocess.call(["python","mainfile.py"])


def register():
    uname = username.get()
    passwd = password.get()
    fname = fullname.get()
    subs = []
    sems = []
    str1=""
    str2=""

    if os:
        oss =  os.get()
        subs.append(oss)
    if pps:
        ppss =  pps.get()
        subs.append(ppss)
    if os:
        dbmss =  dbms.get()
        subs.append(dbmss)
    if os:
        oops =  oop.get()
        subs.append(oops)
    for subject in subs:
        str1=str1+" "+subject
    if sem1:
        semester = sem1.get()
        sems.append(semester)
    if sem2:
        semester = sem2.get()
        sems.append(semester)
    if sem3:
        semester = sem3.get()
        sems.append(semester)
    if sem4:
        semester = sem4.get()
        sems.append(semester)
    if sem5:
        semester = sem5.get()
        sems.append(semester)
    if sem6:
        semester = sem6.get()
        sems.append(semester)
    if sem7:
        semester = sem7.get()
        sems.append(semester)
    if sem8:
        semester = sem8.get()
        sems.append(semester)
    for s in sems:
        str2=str2+" "+s

    
    if(uname=="" or passwd=="" or fname=="" or str1=="" or str2==""):
        MessageBox.showinfo("Insert Status","All fields are required!")
    else:
        con = mysql.connect(host="localhost",user="root",password="",database="test")
        custor = con.cursor()
        custor.execute('insert into faculty_info values("",%s,%s,%s,%s,%s)',(fname,uname,passwd,str2,str1))

        custor.execute("commit")
        con.close()
        MessageBox.showinfo("Register Status","Faculty added successfully!!")
        root.destroy()
        subprocess.call(["python","mainfile.py"])


    
label_0 = Label(root, text="Add Faculty",width=20,font=("bold", 20))
label_0.place(x=90,y=53)

label_1 = Label(root, text="Fullname",width=17,font=("bold", 10))
label_1.place(x=80,y=130)

entry_1 = Entry(root,textvariable=fullname)
entry_1.place(x=280,y=130)

label_2 = Label(root, text="Username",width=17,font=("bold", 10))
label_2.place(x=80,y=180)

entry_2 = Entry(root,textvariable=username)
entry_2.place(x=280,y=180)

label_3 = Label(root, text="Password",width=17,font=("bold", 10))
label_3.place(x=80,y=230)

entry_3 = Entry(root,textvariable=password)
entry_3.place(x=280,y=230)

label_4 = Label(root, text="SEM",width=17,font=("bold", 10))
label_4.place(x=80,y=280)


sem =  Menubutton ( root, text="Select SEM", relief=RAISED ,width=18)
sem.grid()
sem.menu  =  Menu ( sem, tearoff = 0 )
sem["menu"]  =  sem.menu 

sem1 = StringVar()
sem2 = StringVar()
sem3 = StringVar()
sem4 = StringVar()
sem5 = StringVar()
sem6 = StringVar()
sem7 = StringVar()
sem8 = StringVar()

sem.menu.add_radiobutton ( label="1", variable=sem1)
sem.menu.add_radiobutton ( label="2", variable=sem2)
sem.menu.add_radiobutton ( label="3", variable=sem3)
sem.menu.add_radiobutton ( label="4", variable=sem4)
sem.menu.add_radiobutton ( label="5", variable=sem5)
sem.menu.add_radiobutton ( label="6", variable=sem6)
sem.menu.add_radiobutton ( label="7", variable=sem7)
sem.menu.add_radiobutton ( label="8", variable=sem8)

sem.place(x=280,y=280)


label_5 = Label(root, text="Subjects",width=17,font=("bold", 10))
label_5.place(x=80,y=330)

sub =  Menubutton ( root, text="Select Subjects", relief=RAISED , width=18)
sub.grid()
sub.menu  =  Menu ( sub, tearoff = 0 )
sub["menu"]  =  sub.menu 

os = StringVar()
dbms = StringVar()
pps = StringVar()
oop = StringVar()

sub.menu.add_radiobutton ( label="OS", variable=os)
sub.menu.add_radiobutton ( label="DBMS", variable=dbms)
sub.menu.add_radiobutton ( label="PPS", variable=pps)
sub.menu.add_radiobutton ( label="OOP", variable=oop)

sub.place(x=280,y=330)


Button(root, text='Add',width=20,bg='brown',fg='white',command=register).place(x=180,y=400)
Button(root, text='Back',width=20,bg='brown',fg='white',command=back).place(x=180,y=450)


root.mainloop()