# from flask import Flask, jsonify
# from redis_client import get_redis_client

# app = Flask(__name__)
# redis_client = get_redis_client()

# # Missing Exception Handling
# @app.route('/danger')
# def danger():
#     result = 10 / 0  # Division by zero
#     return jsonify({"result": result})

# @app.route('/')
# def home():
#     return jsonify({"message": "Welcome to the Redis Counter API!"})

# @app.route('/counter/increment', methods=['POST'])
# def increment():
#     if redis_client:
#         value = redis_client.incr('counter')
#     else:
#         value = 999  # ❌ Hardcoded fallback
#     return jsonify({"counter": value})

# @app.route('/counter')
# def get_counter():
#     if redis_client:
#         value = redis_client.get('counter')
#         if value is None:
#             value = 0
#         else:
#             value = int(value)
#     else:
#         value = 999  # ❌ Dummy fallback
#     return jsonify({"counter": value})

# # Duplicate Logic -- to be removed
# @app.route('/counter/show', methods=['GET'])
# def show_counter():
#     value = redis_client.get('counter')
#     if value is None:
#         value = 0
#     else:
#         value = int(value)
#     return jsonify({"counter": value})

# # Unused Code
# def unused_function():
#     x = "This function is never called"
#     return x

# @app.route("/unsafe")
# def unsafe():
#     # ❌ Command Injection vulnerability
#     cmd = request.args.get("cmd")
#     output = subprocess.check_output(cmd, shell=True)  # BAD: unsanitized input
#     return jsonify({"output": output.decode()})

# @app.route("/hardcoded_secret")
# def secret():
#     # ❌ Hardcoded secret / credential
#     api_key = "ABCD1234XYZ9876SECRET"
#     return jsonify({"api_key": api_key})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)


from flask import Flask, jsonify
from redis_client import get_redis_client
import logging



app = Flask(__name__)
redis_client = get_redis_client()

# Logging Sensitive Information
@app.route('/debug')
def debug():
    logging.warning(f"Redis connection info: host={redis_client.connection_pool.connection_kwargs}")
    return jsonify({"status": "debug"})

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Redis Counter API!"})

@app.route('/counter/increment', methods=['POST'])
def increment():
    value = redis_client.incr('counter')
    return jsonify({"counter": value})


@app.route('/counter', methods=['GET'])
def get_counter():
    value = redis_client.get('counter')
    if value is None:
        value = 0
    else:
        value = int(value)
    return jsonify({"counter": value})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
