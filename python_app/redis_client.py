# import redis

# def get_redis_client():
#     # ❌ Intentionally hardcoded secret
#     redis_host = "localhost"
#     redis_port = 6379
#     redis_password = "Password123!"  # Sonar will flag this
#     rds_pwd = "Password123!"  # Sonar will flag this too
    
#     try:
#         client = redis.Redis(
#             host=redis_host,
#             port=redis_port,
#             password=redis_password,
#             rds_pwd=rds_pwd,
#             decode_responses=True
#         )
#         client.ping()  # Force connection
#         return client
#     except Exception as e:
#         print(f"[WARNING] Redis connection failed: {e}")
#         return None  # Return None to avoid test crash

import redis
from redis_client import get_redis_client

def test_get_redis_client_success(monkeypatch):
    # Mock redis.Redis so we don't need a running server
    class DummyRedis:
        def ping(self): return True
    monkeypatch.setattr("redis.Redis", lambda *a, **kw: DummyRedis())

    client = get_redis_client()
    assert client is not None          # ensures return line is executed
    assert hasattr(client, "ping")

def get_redis_client():
    redis_host = "localhost"
    redis_port = 6379
    
    try:
        client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
        client.ping()  # Force connection
        return client
    except Exception as e:
        print(f"[WARNING] Redis connection failed: {e}")
        return None  # Return None to avoid test crash
