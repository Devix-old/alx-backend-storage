#!/usr/bin/env python3
"""Redis-based caching module with call counting."""
import redis
import uuid
from typing import Union, Optional
from functools import wraps


def count_calls(method: callable) -> callable:
    """Decorator to count calls to a method."""
    @wraps(method)
    def wrapper(self: any, *args, **kwds) -> str:
        """wrapper"""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: callable) -> callable:
    """Decorator to store inputs and ouputs of a method"""
    @wraps(method)
    def wrapper(self: any, arg: Union[str, bytes, int, float]) -> str:
        """wrapper"""
        self._redis.rpush(f"{method.__qualname__}:inputs", str(arg))
        self._redis.rpush(f"{method.__qualname__}:outputs", method(self, str(arg)))
        return method(self, str(arg))
    return wrapper


class Cache:
    """Cache class using Redis."""
    def __init__(self) -> None:
        """Initialize Redis connection and clear the DB."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis and return its ID."""
        id = uuid.uuid4()
        self._redis.set(str(id), data)
        return str(id)

    def get(self, key: str, fn: Optional[callable] = None) -> any:
        """Retrieve data from Redis, optionally converting it."""
        r = self._redis
        data = r.get(key)
        if fn is str:
            return self.get_str(data)
        if fn is int:
            return self.get_int(data)
        if callable(fn):
            return fn(data)
        else:
            return data

    def get_str(self, data: bytes) -> str:
        """Convert bytes to string."""
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """Convert bytes to integer."""
        return int(data)
