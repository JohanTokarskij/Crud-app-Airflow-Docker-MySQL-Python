from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def establish_mongobd_connection():
    try:
        client = MongoClient('mongodb://mongoadmin:mongopassword@localhost:27017')
        db = client['posts_db']
        posts = db['posts']
        print('Connection to MongoDB is successful')
        return client, posts
    except ConnectionFailure as e:
        print(f'MongoDB connection failed: {e}')
        return None

