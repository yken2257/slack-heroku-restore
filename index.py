from flask import Flask, jsonify, request
from json import dumps

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
        return jsonify({'test':'test'}) 200

if __name__ == '__main__':
    app.run()
