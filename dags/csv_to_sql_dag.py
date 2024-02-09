from datetime import datetime, timedelta
import mysql.connector
import os
import csv
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


PATH_TO_CSV = './logs/user_login.csv'
PATH_TO_XLSX = './logs/login_history.xlsx'

def csv_to_sql():
    try:
        if os.path.exists(PATH_TO_CSV):
            with open(PATH_TO_CSV, 'r', newline='', encoding='utf-8') as file:
                csv_data = list(csv.reader(file))

            with mysql.connector.connect(
                    user='root',
                    password='password',
                    host='mysql',
                    port=3306,
                    database='crud_app') as connection:
                with connection.cursor() as cursor:
                    for row in csv_data:
                        cursor.execute("""
                            SELECT COUNT(*)
                            FROM logs
                            WHERE username = %s AND timestamp = %s
                        """, (row[0], row[1]))

                        result = cursor.fetchone()
                        if result[0] == 0:
                            try:
                                insert_query = """
                                    INSERT INTO logs (username, timestamp) VALUES (%s, %s)
                                """
                                cursor.execute(insert_query, (row[0], row[1]))
                            except mysql.connector.Error as e:
                                print(f'Error inserting data: {e}')
                                connection.rollback()
                        else:
                            print(f'Duplicate record found: {row[0], row[1]}, skipping insertion.')

                    connection.commit()
                    print('Data inserted successfully!')

        else:
            print('Not exists.')
    except mysql.connector.Error as e:
        print(f'\nError connecting to MySQL: {e}')
        return None
    
def empty_csv():
    try:
        if os.path.exists(PATH_TO_CSV):
            open(PATH_TO_CSV, 'w').close() 
            print('CSV file emptied.')
        else:
            print('CSV file does not exist.')
    except Exception as e:
        print(f'Error emptying CSV file: {e}')


default_args = {
    'owner': 'Johan Tokarskij',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1, 12, 0),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'csv_to_sql_dag',
    default_args=default_args,
    description='This hourly DAG transfers user login logs from a CSV to a MySQL database.',
    schedule_interval=timedelta(hours=1),
    catchup=False,
    max_active_runs=1
)

csv_to_sql_task = PythonOperator(
    task_id='csv_to_sql',
    python_callable=csv_to_sql,
    dag=dag
)

empty_csv_task = PythonOperator(
    task_id='empty_csv',
    python_callable=empty_csv,
    dag=dag
)


csv_to_sql_task >> empty_csv_task