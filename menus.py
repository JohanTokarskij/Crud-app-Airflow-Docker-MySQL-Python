import questionary
from time import sleep
from pymysql_funcs import create_user, login, update_user_details, delete_account
from pymongo_funcs import post_message, search_messages, view_message_statistics
from helper_funcs import clear_screen


def initial_menu(db_connection, mongodb_connection):
    while True:
        print('\n' + '*' * 40)
        print('MAIN MENU'.center(40))
        print('*' * 40)        

        choice = questionary.select(
            "Enter your choice:",
            choices=[
                "1. Create User",
                "2. Login",
                "3. Exit"
            ], qmark='').ask()

        if choice == "1. Create User":
            create_user(db_connection)
        elif choice == "2. Login":
            username = login(db_connection)
            if username:
                should_exit = authenticated_menu(db_connection, mongodb_connection, username)
                if should_exit:
                    break
        elif choice == "3. Exit":
            print('\nExiting the application.')
            sleep(0.75)
            break
        elif choice is None:
            clear_screen()
            break

def authenticated_menu(db_connection, posts, username):
    while True:
        print('\n' + '*' * 40)
        print('AUTHENTICATED MENU'.center(40))
        print('*' * 40)

        print(f'\nWelcome back, {username}!\n')

        choice = questionary.select(
            "Enter your choice:",
            choices=[
                "1. Post a Message",
                "2. Search Messages",
                "3. View Message Statistics",
                "4. Update User Details",
                "5. Delete account",
                "6. Logout"
            ], qmark='').ask()

        if choice == "1. Post a Message":
            post_message(posts, username)
        elif choice == "2. Search Messages":
            search_messages(posts)
        elif choice == "3. View Message Statistics":
            view_message_statistics(posts)
        elif choice == "4. Update User Details":
            update_user_details(db_connection, username)
        elif choice == "5. Delete account":
            delete_account(db_connection, username)
            break
        elif choice == "6. Logout":
            print('\nLogging out.')
            clear_screen()
            break
        elif choice is None:
            clear_screen()
            return True