# -*- coding: utf-8 -*-
import sqlite3
import tkinter.messagebox as mb
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter import *
import main1
import bdmain
import comparison
import checkImgBd



def butClickLoad(event):#выбрать фото
    filepath = filedialog.askopenfilename()
    if filepath != "":
        some_string = filepath
        checkStr = some_string[some_string.rfind('.'):len(some_string)]
        if checkStr != ".jpg" and checkStr != ".jpeg" and checkStr != ".png":
            msg = "Неверный формат изображения"
            mb.showerror("Ошибка.", msg)
        else:
            conn = sqlite3.connect('Base.db')
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM pathname")
            result = cursor.fetchone()
            final = result[0]
            for i in range(1,final):
                if comparison.compare_faces(filepath, bdmain.read_blob_data(i)):
                    checkImgBd.vivod(filepath,0,255,0)
                    break
                if i+1==final:
                    checkImgBd.vivod(filepath,0,0,255)
                    #checkImgBd.vivod("tmp/opencv_frame_0.png", 0, 0, 255)
                    flag=messagebox.askquestion("Confirm","Добавить в БД?")
                    rnd=1
                    if(flag=='yes'):
                        bdmain.insert_blob(None,filepath,filepath)
                        rnd+=1
                    break
    else:
        msg = "Вы не выбрали фото."
        mb.showerror("Ошибка.", msg)

def butMakeImg(event):
    main1.main()

def butChuceImg(event):
    filepath = filedialog.askopenfilename()
    if filepath != "":
        some_string = filepath
        checkStr = some_string[some_string.rfind('.'):len(some_string)]
        if checkStr != ".jpg" and checkStr != ".jpeg" and checkStr != ".png":
            msg = "Неверный формат изображения"
            mb.showerror("Ошибка.", msg)
        else:
            bdmain.insert_blob(None,filepath,filepath)
    else:
        msg = "Вы не выбрали фото."
        mb.showerror("Ошибка.", msg)

root = Tk()
root.state('zoomed')
root.title("Распознаватель")
root.geometry("562x495")
root.minsize(562, 495)
root.iconbitmap(default="D:\PythonProject\projectHackathon\magnifier-1_icon-icons.com_56924.ico")


canvas = Canvas(width=250, height=200)
canvas.pack(anchor=CENTER, expand=1)

canvas.create_text(130, 50, font="Plexiglas 22", text="CODICE EFFUSIO", fill="#004D40")

canvas.create_text(50, 73, font="Plexiglas 14", anchor=NW, text="Ионин Дмитрий\nСавчук Богдан\nГоловко Олег\nВладимиров Алексей\nВасиленко Ольга\nЗиновьев Владислав", fill="#004D40")


style = ttk.Style()#
style.configure('my.TButton', font=('Plexiglas', 10))

btn = ttk.Button(text="Сделать фото", style='my.TButton')
btn.pack()
btn.place(relx=0.05, rely=0.95, anchor=W, width=150, height=45)
btn.size()

btn1 = ttk.Button(text="Выбрать фото", style='my.TButton')
btn1.pack()
btn1.place(relx=0.50, rely=0.95, anchor=CENTER, width=150, height=45)

btn2 = ttk.Button(text="Загрузка фото в БД", style='my.TButton')
btn2.pack()
btn2.place(relx=0.95, rely=0.95, anchor=E, width=150, height=45)



btn1.bind("<Button-1>", butClickLoad)
btn.bind("<Button-1>",butMakeImg)
btn2.bind("<Button-1>",butChuceImg)



root.mainloop()