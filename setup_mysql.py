import pymysql


def initiate_databases_and_tables():
    try:    
        with pymysql.connect(user='root',
                             password='password',
                             host='localhost',
                             port=3306,
                             cursorclass=pymysql.cursors.DictCursor) as connect:
            with connect.cursor() as cursor:
                # Creating a database for Airflow
                cursor.execute('CREATE DATABASE IF NOT EXISTS airflow')

                # Creating a database and tables for crud_app
                cursor.execute("CREATE DATABASE IF NOT EXISTS crud_app")
                connect.select_db('crud_app')

                create_users_table_query = """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    first_name VARCHAR(100),
                    last_name VARCHAR(100),
                    username VARCHAR(100) UNIQUE,
                    password VARCHAR(1000),
                    address VARCHAR(255),
                    phone_number VARCHAR(20)
                );
                """
                cursor.execute(create_users_table_query)
                
                create_logs_table = """
                CREATE TABLE IF NOT EXISTS logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(100),
                    timestamp DATETIME,
                    UNIQUE (username, timestamp)
                ) COMMENT = 'This table records the timestamps of user logins';"""
                cursor.execute(create_logs_table)
            connect.commit()
        print('Database "airflow" is set up and ready.')
        print('Database "crud_app" with necessary tables is set up and ready.')
    except pymysql.Error as e:
        print(f'An error has occured: {e}')


if __name__ == '__main__':
    initiate_databases_and_tables()
