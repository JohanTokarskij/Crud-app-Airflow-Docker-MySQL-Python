from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
import os
import base64
from time import sleep
from helper_funcs import wait_for_keypress

UPLOAD_FOLDER = os.path.join('.','Uploads')
DOWNLOAD_FOLDER = os.path.join('.', 'Downloads')

# MongoDB Database Connection #
def establish_mongodb_connection():
    try:
        client = MongoClient('mongodb://mongoadmin:mongopassword@localhost:27017')

        client.server_info()

        db = client['posts_db']
        posts = db['posts']

        print('Connection to MongoDB is successful')
        sleep(0.5)
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
        title = input('Enter the title of your post or leave blank to cancel: ' + '\n> ')
        if title == '' :
            print('\nAction cancelled.')
            sleep(0.75)
            return None
        
        message = input('Enter your message or leave blank to cancel: ' + '\n> ')
        if message == '' :
            print('\nAction cancelled.')
            sleep(0.75)
            return None
        

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        files = os.listdir(UPLOAD_FOLDER)

        file_data = None
        if files:
            file_name = files[0]
            while True:
                to_upload = input(f'Found "{file_name}" in Uploads. Upload and remove it? (y/n): ' + '\n> ')
                if to_upload.lower() == 'y':
                    file_path = os.path.join(UPLOAD_FOLDER, file_name)

                    with open(file_path, 'rb') as file:
                        file_content = file.read()
                        encoded_content = base64.b64encode(file_content).decode('utf-8')

                    file_data = {
                        'base64': encoded_content,
                        'name': os.path.splitext(file_name)[0],
                        'extension': os.path.splitext(file_name)[1]
                    }

                    os.remove(file_path)
                    break
                if to_upload.lower() == 'n':
                    break
                else:
                    print('Please choose "y" and "n"!\n')
                

        post_document = {
            'username': username,
            'title': title,
            'message': message,
            'file': file_data
        }

        posts.insert_one(post_document)

        print('\nPost created successfully.')
        sleep(0.75)
    except FileNotFoundError:
        print('\nFile not found in the upload directory.')
        wait_for_keypress()
    except OSError as e:
        print(f'\nAn OS error occurred: {e}')
        wait_for_keypress()
    except PyMongoError as e:
        print(f'\nDatabase error occurred: {e}')
        wait_for_keypress()
    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}')
        wait_for_keypress()

# Authenticated Menu: 2.Search Messages #
def search_messages(posts):
    try:
        search_query = input('\nEnter a keyword in the title or leave blank to cancel: ' + '\n> ')

        if search_query == '':
            print('\nAction cancelled.')
            sleep(0.75)
            return None

        cursor = posts.find({
            'title': {'$regex': search_query, '$options': 'i'}
        })

        print(f'\nSearch results for "{search_query}":')
        
        results = list(cursor)
        if len(results) == 0:
            print(f'No results were found for "{search_query}".')
            wait_for_keypress()
            return

        ask_for_download = False
        for post in results:
            print(f'Username: {post["username"]}')
            print(f'Title: {post["title"]}')
            print(f'Message: {post["message"]}')

            if 'file' in post and post["file"] is not None:
                ask_for_download = True
                print(f'File Name: {post["file"].get("name", "N/A")}{post["file"].get("extension", "N/A")}\n')
            else:
                print('File: None\n')
            print("---------------------------------------------------")
        
        if ask_for_download:
            to_download = input('Files found in post. Download them (y/n)?: ' + '\n> ')
            if to_download.lower() == 'y':
                if not os.path.exists(DOWNLOAD_FOLDER):
                    os.makedirs(DOWNLOAD_FOLDER)
                for post in results:
                    if 'file' in post and post["file"] is not None:
                        file_info = post['file']
                        file_name = file_info.get("name", "N/A")
                        file_extension = file_info.get("extension", "N/A")
                        file_path = os.path.join(DOWNLOAD_FOLDER, f'{file_name}{file_extension}')
                        
                        print(f"Downloading file: {file_path}")
                        
                        if 'base64' in file_info:
                            file_data = base64.b64decode(file_info['base64'])
                            with open(file_path, 'wb') as file:
                                file.write(file_data)
                        else:
                            print(f"Error downloading {file_name}{file_extension}")
        wait_for_keypress()
    except PyMongoError as e:
        print(f'\nDatabase error occurred: {e}')
        wait_for_keypress()
    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}')
        wait_for_keypress()

# Authenticated Menu: 3.View Message Statistics #
def view_message_statistics(posts):
    try:
        search_query = input('\nEnter username to view post count or leave blank to cancel: ' + '\n> ')

        if search_query == '':
            print('\nAction cancelled.')
            sleep(0.75)
            return None

        result = posts.count_documents({
            'username': search_query
        })

        print(f'\nUser "{search_query}" has posted {result} times.')
        wait_for_keypress()
    except PyMongoError as e:
        print(f'\nDatabase error occurred: {e}')
        wait_for_keypress()
    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}')
        wait_for_keypress()

    

