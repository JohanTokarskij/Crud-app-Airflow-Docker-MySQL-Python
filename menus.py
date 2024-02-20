import questionary
from time import sleep
from pymysql_funcs import create_user, login, update_user_details, delete_account
from pymongo_funcs import post_message, search_messages, edit_message, delete_message, view_message_statistics
from helper_funcs import clear_screen


def main_menu(mysql_connection, posts):
    while True:
        print('\n' + '*' * 40)
        print('MAIN MENU'.center(40))
        print('*' * 40)

        choice = questionary.select(
            'Enter your choice:',
            choices=[
                'Create user',
                'Login',
                'Exit'
            ], qmark='').ask()

        if choice == 'Create user':
            create_user(mysql_connection)
        elif choice == 'Login':
            username = login(mysql_connection)
            if username:
                should_exit = authenticated_menu(
                    mysql_connection, posts, username)
                if should_exit:
                    break
        elif choice == 'Exit':
            print('\nExiting the application.')
            sleep(0.75)
            break
        elif choice is None:
            clear_screen()
            break


def authenticated_menu(mysql_connection, posts, username):
    while True:
        print('\n' + '*' * 40)
        print('AUTHENTICATED MENU'.center(40))
        print('*' * 40)

        choice = questionary.select(
            'Enter your choice:',
            choices=[
                'Message board',
                'Account management',
                'Logout'
            ], qmark='').ask()

        if choice == 'Message board':
            clear_screen(0)
            result = message_board_menu(posts, username)
            if result == 'should_exit':
                return True
        elif choice == 'Account management':
            clear_screen(0)
            result = account_management_menu(mysql_connection, username)
            if result == 'account_deleted':
                clear_screen(0)
                break
            elif result == 'should_exit':
                return True
        elif choice == 'Logout':
            print('\nLogging out.')
            clear_screen()
            break
        elif choice is None:
            clear_screen()
            return True


def message_board_menu(posts, username):
    while True:
        print('\n' + '*' * 40)
        print('MESSAGE BOARD'.center(40))
        print('*' * 40)

        choice = questionary.select(
            'Enter your choice:',
            choices=[
                'Post a message',
                'Search all messages',
                'Edit own message',
                'Delete own message',
                'View message statistics',
                'Back to authenticated menu'
            ], qmark='').ask()

        if choice == 'Post a message':
            post_message(posts, username)
        elif choice == 'Search all messages':
            search_messages(posts)
        elif choice == 'Edit own message':
            edit_message(posts, username)
        elif choice == 'Delete own message':
            delete_message(posts, username)
        elif choice == 'View message statistics':
            view_message_statistics(posts)
        elif choice == 'Back to authenticated menu':
            clear_screen(0)
            break
        elif choice is None:
            clear_screen()
            return 'should_exit'


def account_management_menu(mysql_connection, username):
    while True:
        print('\n' + '*' * 40)
        print('ACCOUNT MANAGEMENT'.center(40))
        print('*' * 40)

        choice = questionary.select(
            'Acount options:',
            choices=[
                'Update user details',
                'Delete account',
                'Back to authenticated menu'
            ], qmark='').ask()

        if choice == 'Update user details':
            update_user_details(mysql_connection, username)
        elif choice == 'Delete account':
            acount_deleted = delete_account(mysql_connection, username)
            if acount_deleted:
                return 'account_deleted'
        elif choice == 'Back to authenticated menu':
            clear_screen(0)
            break
        elif choice is None:
            clear_screen()
            return 'should_exit'