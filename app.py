from application import app
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

CORS(app)

#@app.route('/home')
#def home():
#    return 

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(debug = True, host = '0.0.0.0', port = port)