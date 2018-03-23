from flask import Flask, jsonify, request, current_app
import threading
import time
import json


app = Flask(__name__)
lock = threading.Lock()
d = dict()
d['data'] = {}


def update_thread():
    global d
    while True:
        with lock:
            d['update_time'] = d.get('update_time', 0) + 1
        time.sleep(1.0)


@app.route('/clear', methods=['GET'])
def clear():
    global d
    with lock:
        with open('data.json', 'w') as outfile:
            json.dump({}, outfile)
            d['data'] = {}
            return jsonify(d)


@app.route('/get', methods=['GET'])
def get():
    with lock:
        with open('data.json') as json_file:
            d['data'] = json.load(json_file)
            return jsonify(d)


@app.route('/get/<key>', methods=['GET'])
def get_key(key):
    with lock:
        with open('data.json') as json_file:
            d['data'] = json.load(json_file)
            return jsonify(d['data'].get(key, {}))


@app.route('/set/<key>', methods=['POST'])
def set_key(key):
    global d
    with lock:
        with open('data.json') as json_file:
            d['data'] = json.load(json_file)
            d['data'][key] = d['data'].get(key, {})
            d['data'][key]['value'] = request.args.get('value') or 'N/A'
            d['data'][key]['time'] = time.time()
            with open('data.json', 'w') as outfile:
                json.dump(d['data'], outfile)
            return jsonify(d)

if __name__ == '__main__':
    threading.Thread(target=update_thread).start()
    app.run(host='0.0.0.0', port=8080, threaded=True)
