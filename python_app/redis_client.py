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
