from tkinter import *
import os
import cv2
import numpy
from PIL import Image, ImageDraw, ImageTk
import mysql.connector as mysql
import tkinter.messagebox as Messagebox
import subprocess
import tkinter.messagebox as MessageBox

con = mysql.connect(host="localhost",user="root",password="",database="test")
custor = con.cursor()

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
root.title("Registration Form")


canvas = Canvas(root,width=500,height=500)
image = ImageTk.PhotoImage(Image.open("wood1.jpg"))

canvas.create_image(0,0,anchor=NW,image=image)
canvas.pack()


FirstName = StringVar()
LastName = StringVar()
Enrollment = StringVar()
c = IntVar()
d = StringVar()
e = StringVar()

def back():
    con.close()
    root.destroy()
    subprocess.call(["python","adminPanel.py"])

def validity():
    enrol = Enrollment.get()
    custor.execute('select * from students_info')
    temp = custor.fetchall()
    
    for i in temp:
        if str(i[3])==str(enrol):
            return False
    return True

def register():
    fname = FirstName.get()
    lname = LastName.get()
    enrol = Enrollment.get()
    sem = c.get()
    fild = d.get()
    classname = e.get()

    if(fname=="" or lname=="" or enrol=="" or sem=="select your SEM" or fild=="select your Branch" or classname=="select your Class"):
        MessageBox.showinfo("Insert Status","All fields are required!")
    else:
        if validity():  

            path = str('./images/sem-'+str(sem)+'/'+fild+'/class-'+classname)
            if not os.path.exists(path):
                os.makedirs(path)
            
            cap = cv2.VideoCapture(0)
            while True:  
                ret,frame = cap.read()
                cv2.imshow('window',frame)
                k = cv2.waitKey(30) & 0xff
                if k == 27:
                    cv2.imwrite(path+'/'+str(enrol)+'_'+fname+'_'+lname+'.jpg',frame) # press 'ESC' to quit
                    break
            cap.release()
            cv2.destroyAllWindows()
            MessageBox.showinfo("Register Status","Student added successfully!!")
            entry_1.delete(0,END)
            entry_2.delete(0,END)
            entry_3.delete(0,END)
            c.set('select your SEM')    
            d.set('select your Branch') 
            e.set('select your Class') 
            custor.execute('insert into students_info values("",%s,%s,%s,%s,%s,%s)',(fname,lname,enrol,sem,fild,classname))
            custor.execute("commit")
        else:
            MessageBox.showinfo("Insert Status","Enrollment already exists!")


label_0 = Label(root, text="Registration form",width=20,font=("bold", 20))
label_0.place(x=90,y=53)


label_1 = Label(root, text="First Name",width=15,font=("bold", 10))
label_1.place(x=80,y=130)

entry_1 = Entry(root,textvariable=FirstName)
entry_1.place(x=280,y=130)

label_2 = Label(root, text="Last Name",width=15,font=("bold", 10))
label_2.place(x=80,y=180)

entry_2 = Entry(root,textvariable=LastName)
entry_2.place(x=280,y=180)

label_3 = Label(root, text="Enrollment",width=15,font=("bold", 10))
label_3.place(x=80,y=230)

entry_3 = Entry(root,textvariable=Enrollment)
entry_3.place(x=280,y=230)

label_4 = Label(root, text="SEM",width=15,font=("bold", 10))
label_4.place(x=80,y=280)

list1 = ['1','2','3','4','5','6','7','8'];
c=StringVar()
droplist=OptionMenu(root,c, *list1)
droplist.config(width=15)
c.set('select your SEM') 
droplist.place(x=280,y=280)


label_4 = Label(root, text="Branch",width=15,font=("bold", 10))
label_4.place(x=80,y=330)

list2 = ['CE','IT','EE','ME'];
d=StringVar()
droplist=OptionMenu(root,d, *list2)
droplist.config(width=15)
d.set('select your Branch') 
droplist.place(x=280,y=330)


label_5 = Label(root, text="Class",width=15,font=("bold", 10))
label_5.place(x=80,y=380)

list3 = ['A','B','C'];
e=StringVar()
droplist=OptionMenu(root,e, *list3)
droplist.config(width=15)
e.set('select your Class') 
droplist.place(x=280,y=380)


Button(root, text='Submit',width=20,bg='brown',fg='white',command=register).place(x=180,y=430)
Button(root, text='Back',width=20,bg='brown',fg='white',command=back).place(x=180,y=470)

root.mainloop()

