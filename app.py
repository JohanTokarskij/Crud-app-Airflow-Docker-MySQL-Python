from pymysql_funcs import establish_mysql_connection
from pymongo_funcs import establish_mongobd_connection
from menus import initial_menu

def main():
    try:
        mysql_connection = establish_mysql_connection()
        mongodb_connection, posts = establish_mongobd_connection()
        if mysql_connection and mongodb_connection:
            initial_menu(mysql_connection, posts)
    except:
        pass
    finally:
        if mysql_connection:
            mysql_connection.close()
            print('MySQL connection has been terminated.')
        if mongodb_connection:
            mongodb_connection.close()
            print('MongoDB connection has been terminated.')


if __name__ == '__main__':
    main()
        