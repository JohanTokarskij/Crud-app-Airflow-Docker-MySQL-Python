from pymysql_funcs import create_user, login, update_user_details
from pymongo_funcs import post_message, search_messages, view_message_statistics
from setup_funcs import clear_screen,wait_for_keypress
from time import sleep


def initial_menu(db_connection, mongodb_connection):
    while True:
        clear_screen()
        print('\n' + '*' * 40)
        print('MAIN MENU'.center(40))
        print('*' * 40)
        
        print('\n1. Create User')
        print('2. Login')
        print('3. Exit')
        
        print('\n' + '*' * 40 + '\n')

        choice = input('Enter your choice (1-3): ')

        if choice == '1':
            create_user(db_connection)
        elif choice == '2':
            username = login(db_connection)
            if username:
                authenticated_menu(db_connection, mongodb_connection, username)
        elif choice == '3':
            print('\nExiting the application.')
            sleep(0.75)
            clear_screen()
            break
        else:
            print('\nInvalid choice. Please try again.')
            sleep(0.5)

def authenticated_menu(db_connection, posts, username):
    while True:
        clear_screen()
        print('\n' + '*' * 40)
        print('AUTHENTICATED MENU'.center(40))
        print('*' * 40)

        print(f'\nWelcome back, {username}!')

        print('\n1. Post a Message')
        print('2. Search Messages')
        print('3. View Message Statistics')
        print('4. Update User Details')
        print('5. Logout')

        print('\n' + '*' * 40 + '\n')

        choice = input('Enter your choice (1-5): ')

        if choice == '1':
            post_message(posts, username)
        elif choice == '2':
            search_messages(posts)
        elif choice == '3':
            view_message_statistics(posts)
        elif choice == '4':
            update_user_details(db_connection, username)
        elif choice == '5':
            print('\nLogging out.')
            sleep(0.75)
            break
        else:
            print('\nInvalid choice. Please try again.')

