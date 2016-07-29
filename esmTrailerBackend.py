from flask import Flask
from flask import request
from flask import jsonify
from threading import Thread
import time
import requests
from flask_cors import CORS, cross_origin
import logging


panelTemp = 0
boxTemp = 0
warning = ''
message = ''
battery = ''
app = Flask(__name__)
CORS(app)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Shutdown the server internally
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/')
def hello():
    resp = {
            'panelTemp':panelTemp,
            'boxTemp':boxTemp,
            'battery':battery,
            'message':message,
            'warning':warning,
            }
    return jsonify(**resp)

# Handle the shutdown request
@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

# Handle starting and interfacing
def start():
    app.run(host='127.0.0.1', port=8000)
def startThread():
    thread = Thread(target=start)
    thread.start()
def stop():
    r = requests.post('http://localhost:8000/shutdown')
if __name__ == '__main__':
    startThread()
