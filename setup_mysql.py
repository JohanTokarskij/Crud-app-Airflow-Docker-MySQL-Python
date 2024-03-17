import pymysql
import time


def initiate_databases_and_tables(retries=5):
    for attempt in range(retries):
        try:
            print(f'Initializing databases and tables, Attempt: {attempt + 1}')
            with pymysql.connect(user='root',
                                password='password',
                                host='localhost',
                                port=3306,
                                cursorclass=pymysql.cursors.DictCursor) as connect:
                with connect.cursor() as cursor:
                    # Creating a database and admin account for Airflow
                    cursor.execute('CREATE DATABASE IF NOT EXISTS airflow')
                    cursor.execute('CREATE USER "admin" IDENTIFIED BY "password"')
                    cursor.execute('GRANT ALL PRIVILEGES ON airflow_db.* TO "admin"')

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
            print('Initialization of MySQL is complete.')
            return
        except pymysql.Error as e:
            print(f"Attempt {attempt + 1}: An error occurred: {e}")
            time.sleep(3)

    print(f"Failed to set up databases after {retries} attempts. Please check the MySQL connection and try again.")

if __name__ == '__main__':
    initiate_databases_and_tables()
