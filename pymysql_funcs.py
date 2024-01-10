import pymysql


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
