import pymysql


def initiate_databases_and_tables():
    try:
        with pymysql.connect(user='root',
                             password='password',
                             host='localhost',
                             port=3306,
                             cursorclass=pymysql.cursors.DictCursor) as connect:
            with connect.cursor() as cursor:
                cursor.execute('CREATE DATABASE IF NOT EXISTS airflow')
                cursor.execute("CREATE DATABASE IF NOT EXISTS crud_app")
                connect.select_db('crud_app')

                create_table_query = """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    first_name VARCHAR(255),
                    last_name VARCHAR(255),
                    username VARCHAR(255) UNIQUE,
                    password VARCHAR(255),
                    address VARCHAR(255),
                    phone_number INT(255)
                )
                """
                cursor.execute(create_table_query)
            connect.commit()
        print('Database "airflow" is set up and ready.')
        print('Database "crud_app" with table "users" is set up and ready.')
    except pymysql.Error as e:
        print(f'An error has occured: {e}')


if __name__ == '__main__':
    initiate_databases_and_tables()
