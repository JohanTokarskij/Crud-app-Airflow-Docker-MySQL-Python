from pymysql_funcs import establish_mysql_connection
from pymongo_funcs import establish_mongodb_connection
from menus import main_menu
from helper_funcs import clear_screen
import logging
from time import sleep


logging.basicConfig(
    filename='logs/user_login.csv',
    level=logging.INFO,
    format='%(message)s,%(asctime)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def main():
    mysql_connection = None
    mongodb_connection = None

    try:
        mysql_connection = establish_mysql_connection()
        mongodb_connection, posts = establish_mongodb_connection()
        clear_screen(0)
        if mysql_connection and mongodb_connection:
            main_menu(mysql_connection, posts)

    except KeyboardInterrupt:
        print("\nApplication is terminated by user. Exiting application.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        if mysql_connection:
            try:
                mysql_connection.close()
                print('MySQL connection has been terminated.')
                sleep(0.75)
            except Exception as e:
                print(f"Error closing MySQL connection: {e}")
        
        if mongodb_connection:
            try:
                mongodb_connection.close()
                print('MongoDB connection has been terminated.')
            except Exception as e:
                print(f"Error closing MongoDB connection: {e}")
        clear_screen(1)


if __name__ == '__main__':
    main()
