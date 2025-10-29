from flask import Flask, jsonify, request
from redis_client import get_redis_client
import subprocess  # ⚠️ Potentially dangerous use below

app = Flask(__name__)
redis_client = get_redis_client()

# 🔥 Vulnerability 1: Command Injection
@app.route('/ping')
def ping():
    ip = request.args.get("ip", "127.0.0.1")
    # ⚠️ Dangerous: direct use of user input inside shell=True
    output = subprocess.check_output(f"ping -c 1 {ip}", shell=True)
    return jsonify({"output": output.decode()})

# Missing Exception Handling
@app.route('/danger')
def danger():
    result = 10 / 0  # Division by zero
    return jsonify({"result": result})

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Redis Counter API!"})

@app.route('/counter/increment', methods=['POST'])
def increment():
    if redis_client:
        value = redis_client.incr('counter')
    else:
        value = 999  # ❌ Hardcoded fallback
    return jsonify({"counter": value})

@app.route('/counter')
def get_counter():
    if redis_client:
        value = redis_client.get('counter')
        if value is None:
            value = 0
        else:
            value = int(value)
    else:
        value = 999  # ❌ Dummy fallback
    return jsonify({"counter": value})

# Duplicate Logic -- to be removed
@app.route('/counter/show', methods=['GET'])
def show_counter():
    value = redis_client.get('counter')
    if value is None:
        value = 0
    else:
        value = int(value)
    return jsonify({"counter": value})

# 🔥 Vulnerability 2: Hardcoded secret
API_KEY = "supersecretapikey123"  # ❌ Hardcoded credential

@app.route('/show-key')
def show_key():
    return jsonify({"api_key": API_KEY})

# Unused Code
def unused_function():
    x = "This function is never called"
    return x


@app.route('/debug')
def debug():
    import os
    return jsonify({"env": dict(os.environ)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)