from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)
LOG_FILE = 'logs.txt'  
log_dir = os.path.dirname(LOG_FILE)
if log_dir:
    os.makedirs(log_dir, exist_ok=True)

@app.route('/api/logs/', methods=['POST'])
def log_access():
    data = request.get_json()

    required_fields = {'short_code', 'accessed_at', 'ip', 'user_agent'}
    if not data or not required_fields.issubset(data.keys()):
        return jsonify({"error": "Missing required log fields."}), 400

    log_entry = f"[{data['accessed_at']}] {data['ip']} accessed {data['short_code']} using {data['user_agent']}\n"

    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)

    return jsonify({"message": "Log recorded"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
