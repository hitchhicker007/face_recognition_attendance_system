from tkinter import *
import os
import time
import cv2
import face_recognition
import glob
from pathlib import Path
from PIL import Image, ImageDraw, ImageTk
import csv
from datetime import datetime
import subprocess
import tkinter.messagebox as MessageBox
import mysql.connector as mysql

#database connection
con = mysql.connect(host="localhost",user="root",password="",database="test")
custor = con.cursor()

def writecsv(path,array,sem,field,classname): #function for writing csv file
    with open(path+'/session.csv','a',newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(["Enrollment","Full Name","Date","Time"])
        for i in array:
            custor.execute('select * from students_info where enrollment = '+i+'')
            temp = custor.fetchall()
            writer.writerow([i,temp[0][1]+" "+temp[0][2],datetime.today().strftime('%Y-%m-%d'),time.strftime('%H-%M-%S')])
            custor.execute('insert into present_students values("",%s,%s,%s,%s,%s,%s,%s)',(i,str(temp[0][1]+' '+temp[0][2]),str(datetime.today().strftime('%Y-%m-%d')),str(time.strftime('%H-%M-%S')),str(sem),str(classname),str(field)))
            custor.execute('commit')
    csvFile.close()     

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
canvas.pack()


c = StringVar()
d = StringVar()
e = StringVar()
    
def back():
    root.destroy()
    subprocess.call(["python","adminPanel.py"])


def takeattendance():
    sem = c.get()
    field = d.get()
    class_name = e.get()

    if(sem=="select your SEM" or field=="select your Branch" or class_name=="select your Class"):
        MessageBox.showinfo("Insert Status","Please select all fields!")
    else:
        #capture images
        cap = cv2.VideoCapture('http://192.168.0.100:8080/video')
        i=0
        current_time = time.strftime('%H.%M.%S')
        current_date = datetime.today().strftime('%Y.%m.%d')
        ts = current_time + '_' + current_date
        attendance_path = str('attendance/sem-'+sem+'/'+field+'/class-'+class_name+'/'+ts)   #path for saving images
        if not os.path.exists(attendance_path):
            os.makedirs(attendance_path)                # making directories if not exist 
        while i<5:
            ret,frame = cap.read()
            cv2.imwrite(attendance_path+'/'+str(current_date)+'_'+str(current_time)+'_'+str(i)+'.jpg',frame)
            time.sleep(1)
            i=i+1
        cap.release()
        print("\n#################image captured######################")

        path=Path('images/sem-'+sem+'/'+field+'/class-'+class_name+'/')   #path of students details

        images=[]
        names=[]
        enrolls=[]

        for imagepath in path.glob("*.jpg"):
            img = face_recognition.load_image_file(str(imagepath))
            img_encode = face_recognition.face_encodings(img)[0]
            images.append(img_encode)
            filename=str(imagepath).split("\\")[-1]
            imname=filename.split('.')[-2]
            name = imname.split('_')[-2]
            names.append(name)
            enrol = imname.split('_')[-3]
            enrolls.append(enrol)


        path2 = Path(attendance_path)  

        j=0
        test_imgs =[]
        pil_imgs =[]
        draws = []
        face_locs = []
        present_student = []

        for classimg in path2.glob("*.jpg"):    #scanning images which is taken above

            test_img = face_recognition.load_image_file(str(classimg))
            face_loc = face_recognition.face_locations(test_img)
            face_locs.append(face_loc)
            face_encodes= face_recognition.face_encodings(test_img,face_loc)
            test_imgs.append(face_encodes)
            
            pil_img = Image.fromarray(test_img)
            pil_imgs.append(pil_img)

            draw = ImageDraw.Draw(pil_img)
            draws.append(draw)

        for test_img,pil_img,draw,face_loc in zip(test_imgs,pil_imgs,draws,face_locs):

            resultpath = str('result/sem-'+sem+'/'+field+'/class-'+class_name+'/'+ts)
            if not os.path.exists(resultpath):
                os.makedirs(resultpath)
                
            for (top,right,bottom,left),face_encode in zip(face_loc,test_img):
                matches = face_recognition.compare_faces(images,face_encode,tolerance=0.5)

                name = "Unknown Person"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = names[first_match_index]
                    enrols = enrolls[first_match_index]

                draw.rectangle(((left,top),(right,bottom)),outline=(0,255,0))

                if enrols!="":
                    present_student.append(enrols)
    
                txt_w, txt_h = draw.textsize(name)
                draw.rectangle(((left,bottom - txt_h - 3),(right,bottom)),fill=(0,255,0),outline=(0,255,0))
                draw.text((left+6,bottom-txt_h-4),name,fill=(0,0,0))
            
            pil_img.save(resultpath+'/'+str(j)+'.jpg')
            j=j+1    

        del draws
        
        final_present_students = []             #list that contains present students
        for stud in present_student:
            if stud not in final_present_students:          
                final_present_students.append(stud)

        writecsv(resultpath,final_present_students,sem,field,class_name) #calling writecsv() function 

        con.close()
        root.destroy()
        subprocess.call(["python","adminPanel.py"])


label_0 = Label(root, text="Take Attendance",width=20,font=("bold", 20))
label_0.place(x=90,y=53)


label_1 = Label(root, text="SEM",width=20,font=("bold", 10))
label_1.place(x=80,y=160)


list1 = ['1','2','3','4','5','6','7','8'];
c=StringVar()
droplist=OptionMenu(root,c, *list1)
droplist.config(width=15)
c.set('select your SEM')
droplist.place(x=280,y=160)



label_2 = Label(root, text="branch",width=20,font=("bold", 10))
label_2.place(x=80,y=210)

list2 = ['CE','IT','EE','ME'];
d=StringVar()
droplist=OptionMenu(root,d, *list2)
droplist.config(width=15)
d.set('select your Branch') 
droplist.place(x=280,y=210)


label_3 = Label(root, text="class",width=20,font=("bold", 10))
label_3.place(x=80,y=260)


list3 = ['A','B','C'];
e=StringVar()
droplist=OptionMenu(root,e, *list3)
droplist.config(width=15)
e.set('select your Class') 
droplist.place(x=280,y=260)

Button(root, text='Take Attendance',width=20,bg='brown',fg='white',command=takeattendance).place(x=180,y=330)

Button(root, text='Back',width=20,bg='brown',fg='white',command=back).place(x=180,y=370)

root.mainloop()