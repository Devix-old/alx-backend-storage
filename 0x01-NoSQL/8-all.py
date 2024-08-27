from pymongo import MongoClient


""" list all documents in a collection using python"""


def list_all(mongo_collection):
    """
    List all documents in a collection.

    :param mongo_collection: The pymongo collection object
    :return: List of documents in the collection
    """
    return list(mongo_collection.find())
