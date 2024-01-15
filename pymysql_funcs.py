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
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Connection to MySQL is successful")
        return connection
    except pymysql.Error as e:
        print(f'Error connecting to MySQL: {e}')
        return None


def create_database_and_table(db_connection):
    try:
        with db_connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS crud_app")
            db_connection.select_db('crud_app')

            create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                username VARCHAR(255) UNIQUE,
                password VARCHAR(255),
                address VARCHAR(255),
                phone_number VARCHAR(255)
            )
            """
            cursor.execute(create_table_query)
        db_connection.commit()
    except pymysql.Error as e:
        print(f"Error while creating database or table: {e}")

def create_user(db_connection):
    try:
        first_name = input('Enter first name: ')
        last_name = input('Enter last name: ')
        address = input('Enter your address: ')

        while True:
            phone_number = input('Enter phone number (or type "exit" to cancel): ')
            if phone_number.lower() == 'exit':
                print('User creation cancelled.')
                return
            elif phone_number.isdigit():
                break
            else:
                print('Invalid phone number. Please enter only digits.')

        while True:
            username = input('Enter username: ')

            try:
                with db_connection.cursor() as cursor:
                    cursor.execute('SELECT COUNT(*) FROM users WHERE username=%s', (username,))
                    result = cursor.fetchone()

                    if result['COUNT(*)'] > 0:
                        print('This username already exists. Please enter a different username.')
                    else:
                        break
            except pymysql.Error as e:
                print(f'Database error occurred: {e}')

        while True:
            password = getpass('Enter new password (or leave blank to cancel): ')
            if password == '':
                print('User creation cancelled.')
                return
            confirm_password = getpass('Re-enter new password: ')
            if password == confirm_password:
                break
            else:
                print('Passwords do not match')
        
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        with db_connection.cursor() as cursor:
            insert_query = """
            INSERT INTO users (first_name, last_name, username, password, address, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s)"""

            cursor.execute(insert_query, (first_name, last_name, username, hashed_password, address, phone_number))
            db_connection.commit()
            print('User created successfully.')
        
    except pymysql.Error as e:
        print(f'Database error occurred: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')
