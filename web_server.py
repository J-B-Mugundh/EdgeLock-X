from flask import Flask, send_from_directory, request, jsonify
import requests

app = Flask(__name__)

TEE_SERVER_URL = 'http://localhost:6000/secure'  # URL of the TEE server

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/secure', methods=['POST'])
def secure():
    response = requests.post(TEE_SERVER_URL, json=request.json)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5000)
