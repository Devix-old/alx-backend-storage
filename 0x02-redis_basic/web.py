#!/usr/bin/env python3
"""
Caching request module
"""
import redis
import requests
from functools import wraps
from typing import Callable


def get_page(fn: Callable) -> Callable:
    """Decorator to cache HTTP responses and track request counts."""
    
    @wraps(fn)
    def wrapper(url: str) -> str:
        """Handle caching and counting for HTTP requests."""
        client = redis.Redis()
        
        # Increment the count of how many times this URL has been accessed
        cache_key = f'count:{url}'
        client.incr(cache_key)
        
        # Check if the response is cached
        cached_response = client.get(url)
        if cached_response:
            return cached_response.decode('utf-8')
        
        # If not cached, make the HTTP request
        response = fn(url)
        
        # Cache the response with an expiration time of 10 seconds
        client.setex(url, 10, response)
        return response
    
    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """Fetch the content of a URL."""
    response = requests.get(url)
    return response.text
