from flask import Flask, jsonify
from flask_sockets import Sockets
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from converter import Converter
from json import JSONEncoder


import time

app = Flask(__name__)
sockets = Sockets(app)

encoder = JSONEncoder()


@app.route('/')
def index():
    return "This is index page from flask app."

@sockets.route('/time')
def get_time(ws):
    count = 0
    while not ws.closed:
        ws.send(time.ctime())
        time.sleep(1)
        count += 1
        if count == 10:
            ws.close()

# Conversion progress
PROGRESS = []

@app.route('/convert/<filename>')
def convert(filename):
    c = Converter()

    conv = c.convert(f'./static/{filename}.mp4', f'./static/{filename}.mkv', {
    'format': 'mkv',
    'audio': {
        'codec': 'mp3',
        'samplerate': 11025,
        'channels': 2
    },
    'video': {
        'codec': 'h264',
        'width': 480,
        'height': 360,
        'fps': 30
    }})


    global PROGRESS
    PROGRESS.append({"filename": filename, "progress": 0})

    for percent in conv:
        for item in PROGRESS:
            if item['filename'] == filename:
                item['progress'] = percent



@sockets.route('/progress')
def convert_progress(ws):

    if not ws.closed:
        while True:
            files = [file for file in PROGRESS if file['progress'] != 100]
            if not files:
                break

            data = encoder.encode(PROGRESS)
            ws.send(data)
            time.sleep(2)
        
        

if __name__ == "__main__":
    server = WSGIServer('0.0.0.0', app, handler_class=WebSocketHandler)
    server.serve_forever()