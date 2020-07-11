from flask import Flask, jsonify
from json import dumps

app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    data = request.get_json()
    dumped = dumps(data)
    if dumped['type'] == 'url_verification':
        return jsonify({'challenge': dumped['challenge']}), 200
