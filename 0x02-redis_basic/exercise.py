#!/usr/bin/env python3
"""Redis-based caching module with call counting."""
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


def replay(func: Callable) -> None:
   """Replay function to display the history of calls."""
   r = redis.Redis()
   calls = r.get(func.__qualname__).decode('utf-8')
   inputs = [input.decode('utf-8') for input in
             r.lrange(f'{func.__qualname__}:inputs', 0, -1)]
   outputs = [output.decode('utf-8') for output in
              r.lrange(f'{func.__qualname__}:outputs', 0, -1)]
   print(f'{func.__qualname__} was called {calls} times:')
   for input, output in zip(inputs, outputs):
       print(f'{func.__qualname__}(*{input}) -> {output}')


def count_calls(method: callable) -> callable:
    """Decorator to count calls to a method."""
    @wraps(method)
    def wrapper(self: any, *args, **kwds) -> str:
        """wrapper"""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store inputs and ouputs of a method"""
    @wraps(method)
    def wrapper(self: any, *args) -> str:
        """wrapper"""
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        output = method(self, *args)
        self._redis.rpush(f"{method.__qualname__}:outputs", output)
        return output
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
