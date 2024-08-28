#!/usr/bin/env python3
import redis
import uuid
"""Redis module"""


class Cache:
    """Cache class"""
    def __init__(self) -> None:
        self._redis = redis.Redis(host='localhost', port=6379)
        self._redis.flushdb()

    def store(self, data) -> str:
        id = uuid.uuid4()
        self._redis.set(str(id), data)
        return str(id)
