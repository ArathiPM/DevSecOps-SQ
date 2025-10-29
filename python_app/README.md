# This set of files will show the error on the sonarqube

** CREATING ERRORS"

# Refresh-rate counter (Flask + Redis)

Simple Python Flask app that counts page refreshes and reports the number of hits in the last window (default 60s). It stores timestamps of hits in a Redis sorted set and a total counter key.

Features
- Records each request to `/` as a hit.
- Uses Redis ZSET to store timestamps and compute recent hit counts efficiently.
- Maintains a total counter (key `total_hits`).
- Falls back to an in-memory store if Redis is not available (useful for local testing).

Quick start

1. Install dependencies (recommended in a virtualenv):

```powershell
python -m pip install -r .\requirements.txt
```

2. Run Redis locally (optional). If you don't start Redis the app will use an in-memory fallback.

3. Start the app:

```powershell
# from the repository root
python .\python-app\app.py
```

4. Open http://localhost:5000/ in your browser and refresh to see counts. The page auto-refreshes every 5s.

Environment
- REDIS_URL: Redis connection string (defaults to `redis://localhost:6379/0`).
- PORT: HTTP port (default 5000).
- REFRESH_WINDOW_SECONDS: Window to compute recent hits (default 60).

Examples

Get JSON output (show total and recent hits):

```powershell
curl -H "Accept: application/json" http://localhost:5000/
```

Production notes
- For realistic traffic, configure a real Redis instance and monitor memory usage for the `hits_zset` key.
- You can periodically trim or compact data depending on retention needs. The app already removes entries older than the configured window on every request.