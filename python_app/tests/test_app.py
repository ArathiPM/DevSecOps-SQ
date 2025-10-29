# import pytest
# from app import app, redis_client
# import sys, os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     return app.test_client()

# def test_home(client):
#     response = client.get('/')
#     assert response.status_code == 200

import pytest
import json
from unittest.mock import MagicMock, patch
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

# ---- Test Home Route ----
def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Welcome to the Redis Counter API!"

# ---- Test /counter when no value exists ----
@patch('app.redis_client')
def test_get_counter_none(mock_redis, client):
    mock_redis.get.return_value = None
    response = client.get('/counter')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["counter"] == 0

# ---- Test /counter when value exists ----
@patch('app.redis_client')
def test_get_counter_existing(mock_redis, client):
    mock_redis.get.return_value = b'5'
    response = client.get('/counter')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["counter"] == 5

# ---- Test /counter/increment ----
@patch('app.redis_client')
def test_increment_counter(mock_redis, client):
    mock_redis.incr.return_value = 6
    response = client.post('/counter/increment')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["counter"] == 6
    mock_redis.incr.assert_called_with('counter')

# ---- Test /debug route ----
@patch('app.redis_client')
def test_debug_route(mock_redis, client, caplog):
    mock_redis.connection_pool.connection_kwargs = {"host": "localhost", "port": 6379}
    response = client.get('/debug')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "debug"
    assert any("Redis connection info" in message for message in caplog.messages)
