# -*- coding: utf-8 -*-
import sqlite3, os

#Функция для конвертации цифровых данных (изображений) в бинарные
def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

#Функция для конвертации BLOB-данных в нужный формат и записать готовые файлы на диск
def write_to_file(data, filename):
    # Преобразование двоичных данных в нужный формат
    with open(filename, 'wb') as file:
        file.write(data)
    return filename

################ Вставка изображений в таблицу ################
def insert_blob(emp_id, name, photo):
    try:
        sqlite_connection = sqlite3.connect('Base.db')#Установить SQLite-соединение с базой данных из Python
        cursor = sqlite_connection.cursor()#Создать объект cursor из объекта соединения

        #cursor.execute("DROP TABLE pathname")
        cursor.execute("""CREATE TABLE IF NOT EXISTS pathname (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL, 
        photo BLOB NOT NULL
        )""")

        print("Подключен к SQLite")
        #Создать INSERT-запрос. На этом этапе нужно знать названия таблицы и колонки, в которую будет выполняться вставка
        sqlite_insert_blob_query = """INSERT INTO pathname
                                  (id, name, photo) VALUES (?, ?, ?)"""
        emp_photo = convert_to_binary_data(photo)
        #resume = convert_to_binary_data(resume_file)
        # Преобразование данных в формат кортежа
        data_tuple = (emp_id, name, emp_photo)
        cursor.execute(sqlite_insert_blob_query, data_tuple)#Выполнить INSERT-запрос с помощью cursor.execute();
        sqlite_connection.commit()#После успешного завершения операции закоммитить сохранения в базу данных
        print("Изображение успешно вставлено как BLOB в таблицу")
        cursor.close()#Закрыть объект cursor и соединение
        #Перехватить любые SQL-исключения
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


################ Получение изображения, сохраненных в виде BLOB ################
def read_blob_data(emp_id):
    #idemp=emp_id
    try:
        sqlite_connection = sqlite3.connect('Base.db')#Установить SQLite-соединение с базой данных из Python
        #sqlite_connection.row_factory=sqlite3.Row
        cursor = sqlite_connection.cursor()#Создать объект cursor из объекта соединения
        #Создать SELECT-запрос для получения BLOB-колонок из таблицы
        sql_fetch_blob_query = """SELECT * from pathname where id = ?"""
        cursor.execute(sql_fetch_blob_query, (emp_id,))
        record = cursor.fetchall()#Использовать cursor.fetchall() для получения всех строк и перебора по ним
        for row in record:
            name = row[1]
            photo = row[2]
            photo_path = os.path.join("tmpBd", name)

            # os.remove("tmpBd/tmp.png")
            # cursor.execute("SELECT photo FROM pathname WHERE id > 0 LIMIT 100")
            # img=cursor.fetchone()['photo']
            # whriteAva("tmpBd/tmp.png",img)
            return write_to_file(photo, photo_path)
        cursor.close()#Закрыть объект cursor и соединение

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()

# def whriteAva(filepath,img):
#     try:
#         with open(filepath, "wb") as f:
#             f.write(img)
#             #return filepath
#     except IOError as e:
#         print(e)
