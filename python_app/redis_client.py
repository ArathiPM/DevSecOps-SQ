import redis
import os
import subprocess  # ⚠️ used below for demonstration

def get_redis_client():
    # ❌ Vulnerability: hardcoded credential and port
    redis_host = "localhost"
    redis_port = 6379
    redis_password = "Password123!"  # Sonar rule: Hard‑coded password

    try:
        client = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            decode_responses=True
        )
        client.ping()  # Force connection check
        return client
    except Exception as e:
        # ❌ Vulnerability: printing exception directly can expose secrets or stack traces
        print(f"[WARNING] Redis connection failed: {e}")
        return None  # Return None to avoid test crash


def run_system_command(user_input):
    # ⚠️ Vulnerability: command injection (for Sonar to detect)
    command = f"ls {user_input}"
    result = subprocess.check_output(command, shell=True)
    return result.decode()