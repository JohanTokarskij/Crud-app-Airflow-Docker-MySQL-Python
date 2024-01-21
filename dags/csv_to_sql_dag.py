
from datetime import datetime, timedelta
import pymysql
import os
import csv
#from airflow import DAG
#from airflow.operators.python_operator import PythonOperator


PATH_TO_CSV = './logs/user_login.csv'

def csv_to_sql():
    try:
        if os.path.exists(PATH_TO_CSV):
            with open(PATH_TO_CSV, 'r', newline='', encoding='utf-8') as file:
                csv_data = list(csv.reader(file))
            print(csv_data)
            with pymysql.connect(
                user='root',
                password='password',
                host='localhost',
                port=3306,
                database='crud_app') as connection:
                with connection.cursor() as cursor:
                    print('Connection OK!')

            
        else:
            print('Not exists.')
    except pymysql.Error as e:
        print(f'\nError connecting to MySQL: {e}')
        return None

csv_to_sql()

