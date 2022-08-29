from flask import Flask, render_template, Response
from camera import VideoCamera
from test import value
from cv2 import cv2 as cv2
import random
import socket
import re
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import requests


app = Flask(__name__)

video_stream = VideoCamera()

known_face_encodings, known_face_names, print_names = value()

time_list = []
temperature_list = []
len_name = 0
flage = 0
print_tmp = "0"


def gen(camera):
    global len_name
    global flage
    global print_tmp
    while True:
        frame, flage = camera.get_frame(known_face_encodings, known_face_names, print_names, time_list, flage,
                                        print_tmp)
        if flage == 1:
            temp = requests.get("https://8fc0-114-41-49-229.jp.ngrok.io").text
            temp = temp.split("<p>")[1].split("</p>")[0].split(":")[1]
            print(temp)
            print_tmp= temp
            temperature_list.append(temp)
            flage = 0


        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/data')
def data():
    user_time = zip(time_list, print_names)
    utmp = temperature_list
    return render_template('data.html', user_time=user_time, utmp=utmp)


@app.route('/video_feed')
def video_feed():
    print(type(gen(video_stream)))
    print(gen(video_stream))
    return Response(gen(video_stream), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
