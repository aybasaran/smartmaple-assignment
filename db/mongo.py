from pymongo import MongoClient


def GET_MONGO_CLIENT():
    """
    Returns a MongoClient object.

    Returns:
        MongoClient: A MongoClient object.
    """

    return MongoClient("mongodb://localhost:27017/")


def save_book(book, collection_name) -> bool:
    """

    Saves the book to the database.

    Args:
        book (dict): The book to save.
        collection_name (str): The name of the collection to save the book to.

    Returns:
        bool: True if the book is saved successfully, False otherwise.
    """
    try:
        client = GET_MONGO_CLIENT()
        db = client["smartmaple"]
        collection = db[collection_name]
        collection.insert_one(book)
        client.close()
        return True
    except Exception as e:
        print(e)
        return False
