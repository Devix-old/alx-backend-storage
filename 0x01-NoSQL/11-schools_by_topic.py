#!/usr/bin/env python3
"""Module to interact with MongoDB collections."""


def schools_by_topic(mongo_collection, topic):
    """Return a list of schools that have a specific topic."""
    return list(mongo_collection.find({"topics": topic}))
