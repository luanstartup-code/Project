#!/usr/bin/env python3
"""
🎬 CineAI - Super Minimal Test
Versão mínima absoluta para identificar problema
"""

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# CORS
CORS(app, origins=['*'])

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Working!'
    })

@app.route('/')
def home():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("🚀 Super minimal Flask test...")
    app.run(host='0.0.0.0', port=5000, debug=True)