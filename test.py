from flask import Flask, render_template, Response, jsonify
import face_recognition
import numpy as np
import mysql.connector
from mysql.connector import Error
import os
import time
from time import gmtime, strftime
from cv2 import cv2 as cv2

def value():
        # copy pictures
        # source = r'C:\project\uploads'
        # destination = r'C:\face_recognition-master\examples\picture'
        # for file in files:
        #   new_path = shutil.copy(f"{source}/{file}", destination)

        # Get a reference to webcam #0 (the default one)
        # video_capture = cv2.VideoCapture(0)
        # New Load picture
    connection = mysql.connector.connect(host='127.0.0.1',
                                         port='8889',
                                         user='root',
                                         password='',
                                         database='data_schema')

    cursor = connection.cursor()

    file_count = 0

    count = "select max(`personid`) from `data`"
    cursor.execute(count)
    file_count = cursor.fetchone()

    known_face_encodings = []
    known_face_names = []

    print_names = []

    i = 1
    for i in range(1, file_count[0] + 1):
        IsNone = False
        name = "select `name` from `data` WHERE `personid` = %s"
        cursor.execute(name, (i,))
        record = cursor.fetchone()
        if record is None:
            continue
        if os.path.isfile(os.getcwd() + ("\\picture\\%s.jpg" % (record[0],))):
            image_path = os.getcwd() + ("\\picture\\%s.jpg" % (record[0],))
        elif os.path.isfile(os.getcwd() + ("\\picture\\%s.png" % (record[0],))):
            image_path = os.getcwd() + ("\\picture\\%s.png" % (record[0],))
        elif os.path.isfile(os.getcwd() + ("\\picture\\%s.jpeg" % (record[0],))):
            image_path = os.getcwd() + ("\\picture\\%s.jpeg" % (record[0],))
        else:
            print("error")
        image = face_recognition.load_image_file(image_path)
        initial_face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(initial_face_encoding)
        known_face_names.append(record[0])

    connection.close()

    # Load a sample picture and learn how to recognize it.

    return known_face_encodings, known_face_names, print_names
