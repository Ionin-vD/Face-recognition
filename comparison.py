# -*- coding: utf-8 -*-
import cv2
def compare_faces(image1, image2):
    # Загрузить изображения и преобразовать их в оттенки серого
    img1 = cv2.imread(image1)
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.imread(image2)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Создать объект класса CascadeClassifier для распознавания лиц
    face_cascade = cv2.CascadeClassifier('Face.xml')

    # Найти лица на изображениях
    faces1 = face_cascade.detectMultiScale(img1_gray, scaleFactor=1.12, minNeighbors=19)
    # 19 min neib влады и олечки совпадают+10 и димы совпадают
    faces2 = face_cascade.detectMultiScale(img2_gray, scaleFactor=1.12, minNeighbors=19)

    # Проверить количество найденных лиц
    if len(faces1) != len(faces2):
        return False

    # Сравнить координаты найденных лиц
    for (x1, y1, w1, h1), (x2, y2, w2, h2) in zip(faces1, faces2):
        if x1 != x2 or y1 != y2 or w1 != w2 or h1 != h2:
            return False

    return True
