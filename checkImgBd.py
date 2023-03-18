# -*- coding: utf-8 -*-
import cv2


def vivod(img, b, g, r):
    image = cv2.imread(img)
    # width = int(image.shape[1] // 4)
    # height = int(image.shape[0] // 4)
    # dsize = (width, height)
    # image = cv2.resize(image, dsize)

    face_cascade = cv2.CascadeClassifier("Face.xml")

    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(img_gray, 1.12, 19)

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (b, g, r), 2)

    cv2.imshow("Result", image)