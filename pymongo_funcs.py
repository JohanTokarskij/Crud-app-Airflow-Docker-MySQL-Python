from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
import base64


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


def post_message(posts, username):
    title = input('Enter the title of your post: ')
    message = input('Enter your message: ')

    upload_folder = './Uploads'
    files = os.listdir(upload_folder)

    file_data = None
    if files:
        file_name = files[0]
        to_upload = input(f"Found '{file_name}' in Uploads. Upload and remove it? (y/n): ")
        if to_upload == 'y':
            file_path = os.path.join(upload_folder, file_name)

            with open(file_path, "rb") as file:
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

    print('Post created successfully.')


def search_messages(posts):
    search_query = input('Enter a keyword in the title: ')

    results = posts.find({
        'title': {'$regex': search_query, '$options': 'i'}
    })

    print(f'\nSearch results for "{search_query}":')
    for post in results:
        print(f'Username: {post["username"]}')
        print(f'Title: {post["title"]}')
        print(f'Message: {post["message"]}')

        if 'file' in post and post["file"] is not None:
            print(f'File Name: {post["file"].get("name", "N/A")}{post["file"].get("extension", "N/A")}')
        else:
            print('File: None')

        print("---------------------------------------------------")


def view_message_statistics(posts):
    search_query = input('Enter a username: ')

    result = posts.count_documents({
        'username': search_query
    })

    print(f'User "{search_query}" has posted {result} times.')