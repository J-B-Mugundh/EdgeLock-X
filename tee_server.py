from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Key and IV for AES encryption/decryption
KEY = base64.b64decode(os.getenv('AES_KEY'))  # 32 bytes for AES-256
IV = base64.b64decode(os.getenv('AES_IV'))    # 16 bytes for AES

def encrypt_aes256(data):
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_aes256(encrypted_data):
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(base64.b64decode(encrypted_data)) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    return unpadder.update(decrypted_data) + unpadder.finalize()

def authenticate_face(encrypted_data):
    decrypted_data = decrypt_aes256(encrypted_data).decode('utf-8')
    if decrypted_data == 'face_detected':
        return 'Face authenticated successfully'
    return 'Face authentication failed'

@app.route('/secure', methods=['POST'])
def secure():
    action = request.json['action']
    encrypted_data = request.json['data']
    
    try:
        result = authenticate_face(encrypted_data)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=6000)
