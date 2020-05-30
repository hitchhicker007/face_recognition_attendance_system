from tkinter import *
import subprocess 
import mysql.connector as mysql
from PIL import Image, ImageDraw, ImageTk

def center_window(w=300, h=200):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)    
    y = (hs/3) - (h/3)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


def addstudent():
    root.destroy()
    subprocess.call(["python","AddStudentWithGUI.py"])

def takeattendance():
    root.destroy()
    subprocess.call(["python","takeAttendanceGUI.py"])

def updatestudent():
    root.destroy()
    subprocess.call(["python","updateStudent.py"])

def logout():
    root.destroy()
    subprocess.call(["python","mainfile.py"])
    

root = Tk()
center_window(500,500)
root.title("Take Attendance")


canvas = Canvas(root,width=500,height=500)
image = ImageTk.PhotoImage(Image.open("wood1.jpg"))

canvas.create_image(0,0,anchor=NW,image=image)
canvas.pack()


label_0 = Label(root, text="Admin Panel",width=20,font=("bold", 20))
label_0.place(x=90,y=20)


Button(root, text='Add Student',width=20,height=7,bg='brown',fg='white',command=addstudent).place(x=80,y=110)

Button(root, text='take Attendance',width=20,height=7,bg='brown',fg='white',command=takeattendance).place(x=280,y=110)

Button(root, text='update student details',width=20,height=7,bg='brown',fg='white',command=updatestudent).place(x=80,y=270)

Button(root, text='Logout',width=20,height=7,bg='brown',fg='white',command=logout).place(x=280,y=270)

root.mainloop()
