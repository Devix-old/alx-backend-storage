#!/usr/bin/env python3
import redis
import uuid
from typing import Union, Optional
"""Redis module"""


class Cache:
    """Cache class"""
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        id = uuid.uuid4()
        self._redis.set(str(id), data)
        return str(id)
    

    def get(self, key: str, fn: Optional[callable] = None) -> any:
        r = self._redis
        data = r.get(key)
        if (fn is str):
            return self.get_str(data)
        if (fn is int):
            return(int(data))
        if (callable(fn)):
            return data.decode('utf-8')
        else:
            return data
    def get_str(self, data: bytes) -> str:
        return 	data.decode('utf-8')
    def get_int(self, data: bytes) -> int:
        return int(data)
        
            
cache = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn=fn) == value
