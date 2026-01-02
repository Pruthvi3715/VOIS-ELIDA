import os
import joblib
import time
from functools import wraps

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

memory = joblib.Memory(CACHE_DIR, verbose=0)

def cache_data(expire_seconds=3600):
    """
    Decorator to cache function results for a specific duration.
    Note: joblib doesn't support expiration natively in a simple way, 
    but for this MVP, persistent disk caching is sufficient to survive restarts
    and prevent immediate re-fetches.
    """
    def decorator(func):
        cached_func = memory.cache(func)
        return cached_func
    return decorator

def clear_cache():
    memory.clear()
    print("Cache cleared.")
