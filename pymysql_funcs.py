import pymysql
import bcrypt
from getpass import getpass
from log_funcs import log_user_login
from helper_funcs import clear_screen, wait_for_keypress
from time import sleep


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
            clear_screen()

    except pymysql.Error as e:
        print(f'\nDatabase error occurred: {e}')
        wait_for_keypress()
    except Exception as e:
        print(f'\nAn error occurred: {e}')
        wait_for_keypress()


# Menu: 2.Login #
def login(db_connection):
    try:
        username = input(
            'Enter your username (type "exit" to cancel): ' + '\n> ').strip()
        if username.lower() == 'exit':
            print('\nLogin cancelled.')
            clear_screen()
            return None

        password = getpass('Enter your password (type "exit" to cancel): ' + '\n> ')
        if password.lower() == 'exit':
            print('\nLogin cancelled.')
            clear_screen()
            return None

        if verify_password(db_connection, username, password):
            log_user_login(username)
            print('\nLogin successful!')
            clear_screen()
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
            clear_screen()

    except pymysql.Error as e:
        print(f'\nDatabase error occurred: {e}')
        wait_for_keypress()
    except Exception as e:
        print(f'\nAn error occurred: {e}')
        wait_for_keypress()

# Authenticated Menu: Delete Account #
def delete_account(db_connection, username):
    current_password = getpass('Enter your current password: ')
    if not verify_password(db_connection, username, current_password):
        return
    try:
        user_choice = input('Are you sure you want to delete your user account (y/n)?')
        if user_choice == 'n':
            print('\nAction cancelled.')
            clear_screen()
            return
        
        with db_connection.cursor() as cursor:
            delete_query = """
                            DELETE FROM users
                            WHERE username = %s
                            """
            cursor.execute(delete_query, (username,))
            db_connection.commit()
        
        print('The account has been deleted.')
        clear_screen()
    except pymysql.Error as e:
        print(f'\nDatabase error occurred: {e}')
        wait_for_keypress()
    except Exception as e:
        print(f'\nAn error occurred: {e}')
        wait_for_keypress()

# Helper functions #
def get_user_info(db_connection, is_create=True):
    try:
        first_name = get_input('first name ')
        if first_name is None:
            return None

        last_name = get_input('last name')
        if last_name is None:
            return None

        address = get_input('address')
        if address is None:
            return None

        phone_number = get_input('phone number', is_phone=True)
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

        action = 'create' if is_create else 'update'
        print(f"""\nSummary:
              First name: {first_name}
              Last name: {last_name}
              Address: {address}
              Phone number: {phone_number}
              Username: {username if username else '[Not Changed]'}""")

        confirm = get_input(f'"y" to {action} an account. ', is_confirm=True)
        if confirm is None or confirm.lower() != 'y':
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
        user_input = input(f'Enter {prompt} (type "exit" to cancel): ' + '\n> ')
        if user_input.lower() == 'exit':
            print('\nAction cancelled.')
            clear_screen()
            return None
        elif not user_input:
            print('This field cannot be left blank. Please enter a value.\n')
            continue
        elif is_phone and not user_input.isdigit():
            print('Invalid phone number. Please enter only digits.\n')
            continue
        elif is_confirm and user_input.lower() not in ['y', 'exit']:
            print('Please enter "y" for yes or "exit" for cancel the operation.\n')
            continue
        elif is_username and not user_input.isalnum():
            print('Invalid username. Please use only letters and numbers.\n')
            continue
        else:
            return user_input



def get_unique_username(db_connection):
    while True:
        username = get_input('username', is_username=True)

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
            clear_screen()
            return None
        confirm_password = getpass(
            'Re-enter new password (type "exit" to cancel): '+ '\n> ')
        if confirm_password.lower() == 'exit':
            print('\nUser creation cancelled.')
            clear_screen()
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
                clear_screen()
                return False
            hashed_password = result['password']
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return True
            else:
                print('\nIncorrect password.')
                clear_screen()
                return False
      
    except pymysql.Error as e:
        print(f'\nDatabase error occurred: {e}')
        wait_for_keypress()
        return False
    except Exception as e:
        print(f'\nAn error occurred: {e}')
        wait_for_keypress()
        return False






