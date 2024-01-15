import pymysql
from pymysql_funcs import create_user


def initial_menu(db_connection):
    while True:
        print("\nMenu:")
        print("1. Create User")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            create_user(db_connection)
        elif choice == '2':
            username = login(db_connection)
            if username:
                authenticated_menu(db_connection, username)
        elif choice == '3':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")
