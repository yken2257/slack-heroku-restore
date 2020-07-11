import os
from flask import Flask, jsonify, request
#from json import dumps


app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    data = request.get_json()
    #dumped = dumps(data)
    #print(dumped)
    #print(type(data))
    if data['type'] == 'url_verification':
        return jsonify({'challenge': data['challenge']}), 200
    else:
        return jsonify({'test':'test'}), 200


@app.route('/test')
def greed():
    return 'Hello, World!\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
