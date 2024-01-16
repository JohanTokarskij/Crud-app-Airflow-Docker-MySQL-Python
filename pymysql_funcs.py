import pymysql
import bcrypt
from getpass import getpass


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
        print("Connection to MySQL is successful")
        return connection
    except pymysql.Error as e:
        print(f'Error connecting to MySQL: {e}')
        return None


def create_user(db_connection):
    try:
        first_name = get_input('Enter first name (or type "exit" to cancel): ')
        if first_name is None:
            return

        last_name = get_input('Enter last name (or type "exit" to cancel): ')
        if last_name is None:
            return

        address = get_input('Enter your address (or type "exit" to cancel): ')
        if address is None:
            return

        phone_number = get_input(
            'Enter phone number (or type "exit" to cancel): ', is_phone=True)
        if phone_number is None:
            return

        username = get_unique_username(db_connection)
        if username is None:
            return

        password = get_password()
        if password is None:
            return

        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())

        print(f"""\nSummary:
              First name: {first_name}
              Last name: {last_name}
              Address: {address}
              Phone number: {phone_number}
              Username: {username}""")

        confirm_creation = get_input(
            '\nProceed with creating a user? (y/n): ', is_confirm=True)
        if confirm_creation is None or confirm_creation.lower() != 'y':
            print('User creation canceled. No new user has been added.')
            return

        with db_connection.cursor() as cursor:
            insert_query = """
                INSERT INTO users (first_name, last_name, username, password, address, phone_number)
                VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_query, (first_name, last_name,
                           username, hashed_password, address, phone_number))
            db_connection.commit()
            print('User created successfully.')

    except pymysql.Error as e:
        print(f'Database error occurred: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')


def get_input(prompt, is_phone=False, is_confirm=False):
    while True:
        user_input = input(prompt)
        if user_input.lower() == 'exit':
            print('User creation cancelled.')
            return None
        elif not user_input:
            print('This field cannot be left blank. Please enter a value.')
            continue
        elif is_phone and not user_input.isdigit():
            print('Invalid phone number. Please enter only digits.')
        elif is_confirm and user_input.lower() not in ['y', 'n']:
            print('Please enter "y" for yes or "n" for no.')
        else:
            return user_input


def get_unique_username(db_connection):
    while True:
        username = get_input('Enter username (or type "exit" to cancel): ')

        try:
            with db_connection.cursor() as cursor:
                cursor.execute(
                    'SELECT COUNT(*) FROM users WHERE username=%s', (username,))
                result = cursor.fetchone()

                if result['COUNT(*)'] > 0:
                    print(
                        'This username already exists. Please enter a different username.')
                else:
                    return username
        except pymysql.Error as e:
            print(f'Database error occurred: {e}')
            return None


def get_password():
    while True:
        password = getpass('Enter new password (or type "exit" to cancel): ')
        if password == 'exit':
            print('User creation cancelled.')
            return None
        confirm_password = getpass(
            'Re-enter new password (or type "exit" to cancel): ')
        if confirm_password == 'exit':
            print('User creation cancelled.')
            return None
        if password == confirm_password:
            return password
        else:
            print('Passwords do not match.')


def login(db_connection):
    username = input(
        "Enter your username (or type 'exit' to cancel): ").strip()
    if username.lower() == 'exit':
        print("Login cancelled.")
        return None

    password = getpass("Enter your password (or type 'exit' to cancel): ")
    if password.lower() == 'exit':
        print("Login cancelled.")
        return None

    try:
        with db_connection.cursor() as cursor:
            cursor.execute(
                "SELECT password FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()

            if result:
                hashed_password = result['password']

                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    print("Login successful!")
                    return username
                else:
                    print("Incorrect password.")
            else:
                print("Username not found.")
    except pymysql.Error as e:
        print(f"Database error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return None
