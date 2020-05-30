from tkinter import *
import subprocess
import tkinter.messagebox as MessageBox
import os
import mysql.connector as mysql
from PIL import Image, ImageDraw, ImageTk


def validity():
    enrol = enroll.get()
    con = mysql.connect(host="localhost",user="root",password="",database="test")
    custor = con.cursor()
    custor.execute('select * from students_info')
    temp = custor.fetchall()
    
    for i in temp:
        if str(i[3])==str(enrol):
            return True
    return False


def center_window(w=300, h=200):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)    
    y = (hs/3) - (h/3)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

def rename_img():
    src_old = str("images/sem-"+c.get() + "/"+d.get()+"/class-"+e.get()+"/"+enroll.get()+"_"+firstname.get()+"_"+lastname.get()+".jpg")
    src_new =  str("images/sem-"+c.get() + "/"+d.get()+"/class-"+e.get()+"/"+enroll.get()+"_"+firstname_new.get()+"_"+lastname_new.get()+".jpg")

    os.rename(src_old,src_new)

def back():
    root.destroy()
    subprocess.call(["python","adminPanel.py"])

def fetchdata():
    if  enroll.get() =="":
        MessageBox.showinfo("Error Status","Please Enter Enrollment!") 
    else:
        if validity():
            con = mysql.connect(host="localhost",user="root",password="",database="test")
            custor = con.cursor()
            custor.execute('select * from students_info where enrollment = '""+enroll.get()+'')
            rows = custor.fetchall()
            entry_2.config(state='normal')
            entry_2.insert(0,rows[0][1])
            entry_2.config(state='disabled')

            entry_3.config(state='normal')
            entry_3.insert(0,rows[0][2])
            entry_3.config(state='disabled')

            entry_4.config(state='normal')
            entry_4.insert(0,rows[0][4])
            entry_4.config(state='disabled')
            
            entry_5.config(state='normal')
            entry_5.insert(0,rows[0][5])
            entry_5.config(state='disabled')

            entry_6.config(state='normal')
            entry_6.insert(0,rows[0][6])
            entry_6.config(state='disabled')
            
            entry_2_new.config(state='normal')
            entry_2_new.insert(0,rows[0][1])
            entry_3_new.config(state='normal')
            entry_3_new.insert(0,rows[0][2])

            btn1.config(state='normal')
            con.close()
        else:
            MessageBox.showinfo("Error Status","Enrollment number not found!") 


def update():
    fname = entry_2_new.get()
    lname = entry_3_new.get()
    enr=enroll.get()

    con = mysql.connect(host="localhost",user="root",password="",database="test")
    custor = con.cursor()
    custor.execute('update students_info set first_name=%s, last_name=%s, sem=%s,field=%s,classname=%s where enrollment=%s',(fname,lname,sem,fild,clname,enr))
    custor.execute("commit")
    con.close()   
    rename_img()
    MessageBox.showinfo("Update Status","Student details updated successfully!") 
    entry_1.delete(0,END)
    entry_2.config(state='normal')
    entry_2.delete(0,END)
    entry_3.config(state='normal')
    entry_3.delete(0,END)
    entry_4.config(state='normal')
    entry_4.delete(0,END)
    entry_5.config(state='normal')
    entry_5.delete(0,END)
    entry_6.config(state='normal')
    entry_6.delete(0,END)

    entry_2_new.delete(0,END)
    entry_3_new.delete(0,END) 


root = Tk()
center_window(500,500)
root.title("Admin Panel")


canvas = Canvas(root,width=500,height=500)
image = ImageTk.PhotoImage(Image.open("wood1.jpg"))

canvas.create_image(0,0,anchor=NW,image=image)
canvas.pack()


firstname = StringVar()
lastname = StringVar()
enroll = StringVar()
firstname_new = StringVar()
lastname_new = StringVar()

label_0 = Label(root, text="Update Student Details",width=20,font=("bold", 20))
label_0.place(x=90,y=20)


label_1 = Label(root, text="Enrollment",font=("bold", 10))
label_1.place(x=60,y=100)

entry_1 = Entry(root,textvariable=enroll)
entry_1.place(x=200,y=100)

Button(root, text='Get data',width=10,bg='brown',fg='white',command=fetchdata).place(x=350,y=97)

Label(root,text="Update Value",font=("bold")).place(x=350,y=140)

label_2 = Label(root, text="Firstname",width=15,font=("bold", 10))
label_2.place(x=15,y=180)

entry_2 = Entry(root,textvariable=firstname,state='disabled')
entry_2.place(x=165,y=180)

entry_2_new = Entry(root,textvariable=firstname_new,state='disabled')
entry_2_new.place(x=330,y=180)

label_3 = Label(root, text="Lastname",width=15,font=("bold", 10))
label_3.place(x=15,y=230)

entry_3 = Entry(root,textvariable=lastname,state='disabled')
entry_3.place(x=165,y=230)

entry_3_new = Entry(root,textvariable=lastname_new,state='disabled')
entry_3_new.place(x=330,y=230)

label_4 = Label(root, text="SEM",width=15,font=("bold", 10))
label_4.place(x=15,y=280)

c=StringVar()
entry_4 = Entry(root,textvariable=c,state='disabled')
entry_4.place(x=165,y=280)



label_5 = Label(root, text="Branch",width=15,font=("bold", 10))
label_5.place(x=15,y=330)

d=StringVar()
entry_5=Entry(root,textvariable=d,state='disabled')
entry_5.place(x=165,y=330)


label_6 = Label(root, text="Class",width=15,font=("bold", 10))
label_6.place(x=15,y=380)

e=StringVar()
entry_6=Entry(root,textvariable=e,state='disabled')
entry_6.place(x=165,y=380)


btn1 = Button(root, text='Update',width=20,bg='brown',fg='white',command=update,state='disabled')
btn1.place(x=180,y=430)
Button(root, text='Back',width=20,bg='brown',fg='white',command=back).place(x=180,y=470)


root.mainloop()