from pymysql_funcs import create_user, login, update_user_details
from pymongo_funcs import post_message, search_messages, view_message_statistics
import os
import platform

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def initial_menu(db_connection, mongodb_connection):
    while True:
        print("\n\nMenu:")
        print("1. Create User")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            create_user(db_connection)
        elif choice == '2':
            username = login(db_connection)
            if username:
                authenticated_menu(db_connection, mongodb_connection, username)
        elif choice == '3':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

def authenticated_menu(db_connection, posts, username):
    print(f'\nWelcome back, {username}!')
    while True:
        print("\nAuthenticated Menu:")
        print("1. Post a Message")
        print("2. Search Messages")
        print("3. View My Message Statistics")
        print("4. Update User Details")
        print("5. Logout")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            post_message(posts, username)
        elif choice == '2':
            search_messages(posts)
        elif choice == '3':
            view_message_statistics(posts)
        elif choice == '4':
            update_user_details(db_connection, username)
        elif choice == '5':
            print("Logging out.")
            break
        else:
            print("Invalid choice. Please try again.")


