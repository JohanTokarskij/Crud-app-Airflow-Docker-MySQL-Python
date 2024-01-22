from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
import os
import base64


# MongoDB Database Connection #
def establish_mongodb_connection():
    try:
        client = MongoClient('mongodb://mongoadmin:mongopassword@localhost:27017')

        client.server_info()

        db = client['posts_db']
        posts = db['posts']

        print('\nConnection to MongoDB is successful')
        return client, posts
    except ConnectionFailure as e:
        print(f'\nMongoDB connection failed: {e}')
        return None
    except PyMongoError as e:
        print(f'\nAn error occurred with MongoDB: {e}')
        return None


# Authenticated Menu: 1.Post a Message #
def post_message(posts, username):
    try:
        title = input('Enter the title of your post: ')
        message = input('Enter your message: ')

        upload_folder = './Uploads'
        files = os.listdir(upload_folder)

        file_data = None
        if files:
            file_name = files[0]
            to_upload = input(f'Found "{file_name}" in Uploads. Upload and remove it? (y/n): ')
            if to_upload == 'y':
                file_path = os.path.join(upload_folder, file_name)

                with open(file_path, 'rb') as file:
                    file_content = file.read()
                    encoded_content = base64.b64encode(file_content).decode('utf-8')

                file_data = {
                    'base64': encoded_content,
                    'name': os.path.splitext(file_name)[0],
                    'extension': os.path.splitext(file_name)[1]
                }

                os.remove(file_path)

        post_document = {
            'username': username,
            'title': title,
            'message': message,
            'file': file_data
        }

        posts.insert_one(post_document)

        print('\nPost created successfully.')
    except FileNotFoundError:
        print('\nFile not found in the upload directory.')
    except OSError as e:
        print(f'\nAn OS error occurred: {e}')
    except PyMongoError as e:
        print(f'\nDatabase error occurred: {e}')
    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}')

# Authenticated Menu: 2.Search Messages #
def search_messages(posts):
    try:
        search_query = input('Enter a keyword in the title: ')

        cursor = posts.find({
            'title': {'$regex': search_query, '$options': 'i'}
        })

        print(f'\nSearch results for "{search_query}":')
        
        results = list(cursor)
        if len(results) == 0:
            print(f'No results were found for "{search_query}".')
            return

        for post in results:
            print(f'Username: {post["username"]}')
            print(f'Title: {post["title"]}')
            print(f'Message: {post["message"]}')

            if 'file' in post and post["file"] is not None:
                print(f'File Name: {post["file"].get("name", "N/A")}{post["file"].get("extension", "N/A")}')
            else:
                print('File: None')

            print("---------------------------------------------------")
    except PyMongoError as e:
        print(f'\nDatabase error occurred: {e}')
    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}')

# Authenticated Menu: 3.View Message Statistics #
def view_message_statistics(posts):
    try:
        search_query = input('Enter username to view post count: ')

        result = posts.count_documents({
            'username': search_query
        })

        print(f'\nUser "{search_query}" has posted {result} times.')
    except PyMongoError as e:
        print(f'\nDatabase error occurred: {e}')
    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}')