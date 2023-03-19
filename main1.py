# -*- coding: utf-8 -*-
import sqlite3
import tkinter.messagebox as mb
from tkinter import messagebox
import cv2
import os
import bdmain
# пути прописываем вручную, path_s - откуда, path_d - куда
import checkImgBd
import comparison


# пути прописываем вручную, path_s - откуда, path_d - куда
def import_img():
    path_s = r'D:/PythonProject/projectHackathon/'
    path_d = r'D:/PythonProject/projectHackathon/tmp/'
    for file in os.listdir(path_s):
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
            os.replace(path_s + file, path_d + file)
rnd=0
#img_counter = 0
def main():

    msg = "Нажмите пробел для фотоснимка, \'q\' для закрытия.."
    mb.showerror("Инфо.", msg)

    face_cascade_db = cv2.CascadeClassifier("Face.xml")
    cap=cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade_db.detectMultiScale(img_gray, 1.1, 19)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h),(255,0,0),2 )
        cv2.imshow('vas zametili', img)
        ret, frame = cap.read()
        if not ret:
            #print("failed to grab frame")
            break
        k = cv2.waitKey(1)
        if k % 256 == 81 or k % 256 == 113 or k % 256 == 201 or k % 256 == 233:
            # й или q  pressed
            # print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_0.png"
            cv2.imwrite(img_name, frame)
            #img_counter += 1
    cap.release()
    cv2.destroyAllWindows()
    import_img()

    conn = sqlite3.connect('Base.db')
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM pathname")
    result = cursor.fetchone()
    final = result[0]

    for i in range(1, final):
        if comparison.compare_faces("tmp/opencv_frame_0.png", bdmain.read_blob_data(i)):
            checkImgBd.vivod("tmp/opencv_frame_0.png", 0, 255, 0)
            break
        if i + 1 == final:
            checkImgBd.vivod("tmp/opencv_frame_0.png", 0, 0, 255)
            flag=messagebox.askquestion("Confirm","Добавить в БД?")
            global rnd
            if(flag=='yes'):
                bdmain.insert_blob(None,"tmp/opencv_frame_"+str(rnd)+".png","tmp/opencv_frame_0.png")
                rnd+=1
            break
    path = os.path.join("tmp", "opencv_frame_0.png")
    os.remove(path)