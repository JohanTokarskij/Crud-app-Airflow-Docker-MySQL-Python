from time import sleep
import os
import base64
import questionary
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from helper_funcs import wait_for_keypress, clear_screen

UPLOAD_FOLDER = os.path.join('.', 'Uploads')
DOWNLOAD_FOLDER = os.path.join('.', 'Downloads')

# MongoDB Database Connection #
def establish_mongodb_connection():
    try:
        client = MongoClient(
            'mongodb://mongoadmin:mongopassword@localhost:27017')

        client.server_info()

        db = client['posts_db']
        posts = db['posts']

        print('Connection to MongoDB is successful')
        sleep(0.5)

        return client, posts
    except ConnectionFailure as e:
        print(f"\nMongoDB connection failed: {e}")
        return None
    except PyMongoError as e:
        print(f"\nAn error occurred with MongoDB: {e}")
        return None


# MESSAGE BOARD: Post a Message #
def post_message(posts, username):
    try:
        title = input(
            'Enter the title of your post or leave blank to cancel: ' + '\n> ')
        if title == '':
            print('\nAction cancelled.')
            clear_screen()
            return None

        message = input(
            'Enter your message or leave blank to cancel: ' + '\n> ')
        if message == '':
            print('\nAction cancelled.')
            clear_screen()
            return None

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        upload_folder_content = os.listdir(UPLOAD_FOLDER)

        file_data = None
        file_data_list = []
        if upload_folder_content:
            chosen_files_to_upload = questionary.checkbox(
                f"{len(upload_folder_content)} files found in {UPLOAD_FOLDER}. Select files to upload:",
                choices=upload_folder_content, qmark='').ask()
            if chosen_files_to_upload:
                for file_name in chosen_files_to_upload:
                    file_path = os.path.join(UPLOAD_FOLDER, file_name)

                    with open(file_path, 'rb') as file:
                        file_content = file.read()
                        encoded_content = base64.b64encode(file_content).decode('utf-8')

                    file_data = {
                        'base64': encoded_content,
                        'name': os.path.splitext(file_name)[0],
                        'extension': os.path.splitext(file_name)[1]
                    }

                    file_data_list.append(file_data)

        post_document = {
            'username': username,
            'title': title,
            'message': message,
            'files': file_data_list
        }

        posts.insert_one(post_document)
        print('\nPost created successfully.')
        clear_screen()
    except FileNotFoundError:
        print('\nFile not found in the upload directory.')
        wait_for_keypress()
    except OSError as e:
        print(f"\nAn OS error occurred: {e}")
        wait_for_keypress()
    except PyMongoError as e:
        print(f"\nDatabase error occurred: {e}")
        wait_for_keypress()
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        wait_for_keypress()


# MESSAGE BOARD: Search Messages #
def search_messages(posts):
    try:
        search_query = input(
            '\nEnter a keyword in the title or leave blank to cancel: ' + '\n> ')

        if search_query == '':
            print('\nAction cancelled.')
            clear_screen()
            return None

        cursor = posts.find({
            'title': {'$regex': search_query, '$options': 'i'}
        })

        print(f"\nSearch results for '{search_query}':")

        results = list(cursor)
        if len(results) == 0:
            print(f"No results were found for '{search_query}'.")
            wait_for_keypress()
            return

        # Pagination setup
        page_size = 5 
        page_count = len(results) // page_size + (1 if len(results) % page_size > 0 else 0)
        current_page = 0

        total_posts = len(results)

        while current_page < page_count:
            clear_screen(0)
            print(f"\nPage {current_page + 1} of {page_count} (Total posts: {total_posts})\n")
            start_index = current_page * page_size
            end_index = start_index + page_size
            for index, post in enumerate(results[start_index:end_index], start=start_index + 1):
                print(f"Post #{index}")
                print(f"Username: {post['username']}\nTitle: {post['title']}\nMessage: {post['message']}")
                if 'files' in post and post['files']:
                    print('Files available for download:')
                    for file in post['files']:
                        print(f'- {file.get("name", "N/A")}{file.get("extension", "N/A")}')
                    if questionary.confirm('Download files from this post?', qmark='').ask():
                        download_files(post['files'])
                print("---------------------------------------------------")

            current_page += 1
            if current_page < page_count and not questionary.confirm('See next page?', qmark='').ask():
                break
        print('No more messages to display.')
        wait_for_keypress()
    except PyMongoError as e:
        print(f"\nDatabase error occurred: {e}")
        wait_for_keypress()
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        wait_for_keypress()


# MESSAGE BOARD: Update a Message #
def edit_message(posts, username):
    try:
        search_query = input(
            '\nEnter a keyword in the title or leave blank to cancel: ' + '\n> ')

        if search_query == '':
            print('\nAction cancelled.')
            clear_screen()
            return None

        cursor = posts.find({
            'username': username,
            'title': {'$regex': search_query, '$options': 'i'}
        })

        results = list(cursor)
        
        if len(results) == 0:
            print('\nNo messages found.')
            wait_for_keypress()
            return
        
        choices = [f"{index + 1}. {message['title']}: {message['message']}" for index, message in enumerate(results)]
        selection = questionary.select(
            'Select a message to edit:',
            choices=choices, qmark=''
        ).ask()

        if not selection:
            print('\nAction cancelled.')
            clear_screen()
            return
        
        selected_index = int(selection.split('.')[0]) - 1
        selected_post = results[selected_index]

        new_title = input(f"\nCurrent title: '{selected_post['title']}'\nEnter new title (press Enter to keep current): ")
        if new_title.strip() == '':
            new_title = selected_post['title']

        new_message = input(f"\nCurrent message: '{selected_post['message']}'\nEnter new message (press Enter to keep current): ")
        if new_message.strip() == '':
            new_message = selected_post['message']

        update_data = {'title': new_title,
                       'message': new_message}

        posts.update_one({'_id': selected_post['_id']}, {'$set': update_data})
        print('\nMessage updated successfully.')

        clear_screen() 
    except PyMongoError as e:
        print(f"\nDatabase error occurred: {e}")
        wait_for_keypress()
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        wait_for_keypress()


# MESSAGE BOARD: Delete a Message #
def delete_message(posts, username):
    try:
        search_query = input(
            '\nEnter a keyword in the title or leave blank to cancel: ' + '\n> ')

        if search_query == '':
            print('\nAction cancelled.')
            clear_screen()
            return None
        
        cursor = posts.find({
            'username': username,
            'title': {'$regex': search_query, '$options': 'i'}
        })

        results = list(cursor)
        if len(results) == 0:
            print('\nNo messages found.')
            wait_for_keypress()
            return
        choices = [f"{index + 1}. {message['title']}: {message['message']}" for index, message in enumerate(results)]
        selection = questionary.select(
            'Select a message to delete:',
            choices=choices, qmark=''
        ).ask()

        if not selection:
            print('\nAction cancelled.')
            clear_screen()
            return
        
        selected_index = int(selection.split('.')[0]) - 1
        selected_post = results[selected_index]

        confirm_deletion = questionary.confirm(f"Are you sure you want to delete this message:\n {selected_post['title']} - {selected_post['message']}?", default=False).ask()
        if confirm_deletion:
            posts.delete_one({'_id': selected_post['_id']})
            print('\nMessage deleted successfully.')
        else:
            print('\nDeletion cancelled')
        
        clear_screen()
    except PyMongoError as e:
        print(f"\nDatabase error occurred: {e}")
        wait_for_keypress()
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        wait_for_keypress()


# MESSAGE BOARD: View Message Statistics #
def view_message_statistics(posts):
    try:
        search_query = input(
            '\nEnter username to view post count or leave blank to cancel: ' + '\n> ')

        if search_query == '':
            print('\nAction cancelled.')
            clear_screen()
            return None

        result = posts.count_documents({
            'username': search_query
        })
        print(f"\nUser '{search_query}' has posted {result} times.")
        wait_for_keypress()
    except PyMongoError as e:
        print(f"\nDatabase error occurred: {e}")
        wait_for_keypress()
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        wait_for_keypress()


# Helper functions #
def download_files(files):
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
    
    for file in files:
        file_path = os.path.join(DOWNLOAD_FOLDER, f"{file['name']}{file['extension']}")
        print(f"Downloading file: {file_path}")
        file_data = base64.b64decode(file['base64'])
        with open(file_path, 'wb') as f:
            f.write(file_data)