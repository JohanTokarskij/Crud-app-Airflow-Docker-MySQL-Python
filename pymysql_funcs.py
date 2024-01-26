import pymysql
import bcrypt
from getpass import getpass
from time import sleep
from log_funcs import log_user_login
from helper_funcs import clear_screen, wait_for_keypress


# MySQL Database Connection #
def establish_mysql_connection():
    try:
        connection = pymysql.connect(
            user='root',
            password='password',
            host='localhost',
            port=3306,
            database='crud_app',
            cursorclass=pymysql.cursors.DictCursor
        )
        print('Connection to MySQL is successful')
        sleep(0.5)
        return connection
    except pymysql.Error as e:
        print(f'\nError connecting to MySQL: {e}')
        wait_for_keypress()
        return None


# Menu: 1.Create User #
def create_user(db_connection):
    try:
        clear_screen()
        print('\n' + '*' * 40)
        print('Menu: 1.CREATE USER'.center(40))
        print('*' * 40)
        user_info = get_user_info(db_connection)
        if user_info is None:
            return

        first_name, last_name, address, phone_number, username, hashed_password = user_info

        with db_connection.cursor() as cursor:
            insert_query = """
                INSERT INTO users (first_name, last_name, username, password, address, phone_number)
                VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_query, (first_name, last_name,
                           username, hashed_password, address, phone_number))
            db_connection.commit()
            print('\nUser created successfully.')
            sleep(0.75)

    except pymysql.Error as e:
        print(f'\nDatabase error occurred: {e}')
        wait_for_keypress()
    except Exception as e:
        print(f'\nAn error occurred: {e}')
        wait_for_keypress()


# Menu: 2.Login #
def login(db_connection):
    try:
        """ clear_screen()
        print('\n' + '*' * 40)
        print('Menu: 2.LOGIN'.center(40))
        print('*' * 40) """
        username = input(
            'Enter your username (type "exit" to cancel): ' + '\n> ').strip()
        if username.lower() == 'exit':
            print('\nLogin cancelled.')
            sleep(0.75)
            return None

        password = getpass('Enter your password (type "exit" to cancel): ' + '\n> ')
        if password.lower() == 'exit':
            print('\nLogin cancelled.')
            sleep(0.75)
            return None

        if verify_password(db_connection, username, password):
            print('\nLogin successful!')
            sleep(0.75)
            log_user_login(username)
            return username
        else:
            return None
    except pymysql.Error  as e:
        print(f'\nDatabase error occurred: {e}')
        wait_for_keypress()
        return None
    except Exception as e:
        print(f'\nAn unexpected error occurred: {e}')
        wait_for_keypress()
        return None
    

# Authenticated Menu: Update User Details #
def update_user_details(db_connection, username):
    current_password = getpass('Enter your current password: ')
    if not verify_password(db_connection, username, current_password):
        return
    try:
        user_info = get_user_info(db_connection, is_create=False)
        if user_info is None:
            return

        first_name, last_name, address, phone_number, _, hashed_password = user_info

        with db_connection.cursor() as cursor:
            update_query = """UPDATE users SET first_name=%s, last_name=%s, password=%s, address=%s, phone_number=%s
                            WHERE username=%s"""
            cursor.execute(update_query, (first_name, last_name, hashed_password, address, phone_number, username))
            db_connection.commit()
            print('\nUser details updated successfully.')

    except pymysql.Error as e:
        print(f'\nDatabase error occurred: {e}')
        wait_for_keypress()
    except Exception as e:
        print(f'\nAn error occurred: {e}')
        wait_for_keypress()

# Helper functions #
def get_user_info(db_connection, is_create=True):
    try:
        first_name = get_input('Enter first name (type "exit" to cancel): ')
        if first_name is None:
            return None

        last_name = get_input('Enter last name (type "exit" to cancel): ')
        if last_name is None:
            return None

        address = get_input('Enter your address (type "exit" to cancel): ')
        if address is None:
            return None

        phone_number = get_input('Enter phone number (type "exit" to cancel): ', is_phone=True)
        if phone_number is None:
            return None

        username=None
        if is_create:
            username = get_unique_username(db_connection)
            if username is None:
                return None

        password = get_password()
        if password is None:
            return None

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        action = 'creating' if is_create else 'updating'
        print(f"""\nSummary:
              First name: {first_name}
              Last name: {last_name}
              Address: {address}
              Phone number: {phone_number}
              Username: {username if username else '[Not Changed]'}""")

        confirm = get_input(f'\nProceed with {action} a user? (y/n): ', is_confirm=True)
        if confirm is None or confirm.lower() != 'y':
            print(f'\nUser {action} canceled.')
            sleep(0.75)
            return None

        return first_name, last_name, address, phone_number, username, hashed_password

    except pymysql.Error as e:
        print(f'\nDatabase error occurred: {e}')
        wait_for_keypress()
    except Exception as e:
        print(f'\nAn error occurred: {e}')
        wait_for_keypress()


def get_input(prompt, is_phone=False, is_confirm=False, is_username=False):
    while True:
        user_input = input(prompt + '\n> ')
        if user_input.lower() == 'exit':
            print('\nUser creation cancelled.')
            sleep(0.75)
            return None
        elif not user_input:
            print('This field cannot be left blank. Please enter a value.\n')
            continue
        elif is_phone and not user_input.isdigit():
            print('Invalid phone number. Please enter only digits.\n')
            continue
        elif is_confirm and user_input.lower() not in ['y', 'n']:
            print('Please enter "y" for yes or "n" for no.\n')
            continue
        elif is_username and not user_input.isalnum():
            print('Invalid username. Please use only letters and numbers.\n')
            continue
        else:
            return user_input



def get_unique_username(db_connection):
    while True:
        username = get_input('Enter username (type "exit" to cancel): ', is_username=True)

        try:
            with db_connection.cursor() as cursor:
                cursor.execute(
                    'SELECT COUNT(*) FROM users WHERE username=%s', (username,))
                result = cursor.fetchone()

                if result['COUNT(*)'] > 0:
                    print('This username already exists. Please enter a different username.\n')
                else:
                    return username
        except pymysql.Error as e:
            print(f'\nDatabase error occurred: {e}')
            wait_for_keypress()
        except Exception as e:
            print(f'\nAn error occurred: {e}')
            wait_for_keypress()


def get_password():
    while True:
        password = getpass('Enter new password (type "exit" to cancel): '+ '\n> ')
        if password.lower() == 'exit':
            print('\nUser creation cancelled.')
            sleep(0.75)
            return None
        confirm_password = getpass(
            'Re-enter new password (type "exit" to cancel): '+ '\n> ')
        if confirm_password.lower() == 'exit':
            print('\nUser creation cancelled.')
            sleep(0.75)
            return None
        if password == confirm_password:
            return password
        else:
            print('Passwords do not match.\n')


def verify_password(db_connection, username, password):
    try:
        with db_connection.cursor() as cursor:
            cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()

            if not result:
                print('\nUsername not found.')
                sleep(0.75)
                return False
            hashed_password = result['password']
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return True
            else:
                print('\nIncorrect password.')
                sleep(0.75)
                return False
      
    except pymysql.Error as e:
        print(f'\nDatabase error occurred: {e}')
        wait_for_keypress()
        return False
    except Exception as e:
        print(f'\nAn error occurred: {e}')
        wait_for_keypress()
        return False






