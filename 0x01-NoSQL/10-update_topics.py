#!/usr/bin/env python3
"""Update mongo"""


def update_topics(mongo_collection, name, topics):
    """change all topics of a school document based on the name"""
    return mongo_collection.update_one(
        {'name': name}, {'$set': {'topics': topics}}
    )
