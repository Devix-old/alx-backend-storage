#!/usr/bin/env python3
import redis
import uuid
from typing import Union
"""Redis module"""


class Cache:
    """Cache class"""
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union(str, bytes, int, float)) -> str:
        id = uuid.uuid4()
        self._redis.set(str(id), data)
        return str(id)
