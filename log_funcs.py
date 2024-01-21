import logging
import openpyxl
import csv
from collections import Counter
from datetime import datetime

PATH_TO_CSV = './logs/user_login.csv'
PATH_TO_XLSX = './logs/login_history.xlsx'


def log_user_login(username):
    logging.info(f'{username}')
    write_to_excel()


def write_to_excel():
        try:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            column_names = ['Year', 'Month', 'Day', 'Hour', 'Username', 'Count']
            sheet.append(column_names)

            with open(PATH_TO_CSV, 'r', newline='', encoding='utf-8') as file:
                csv_data = list(csv.reader(file))

            counts_per_hour = Counter()
            for username, timestamp in csv_data:
                dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                timestamp_slice = dt.strftime('%Y-%m-%d %H')
                counts_per_hour[(username, timestamp_slice)] += 1

            for (username, timestamp_slice), count in counts_per_hour.items():
                date_part, hour_part = timestamp_slice.split(' ')
                year, month, day = date_part.split('-')
                row = [int(year), int(month), int(day), f'{int(hour_part)}:00 - {int(hour_part)}:59', username, count]
                sheet.append(row)

            workbook.save(PATH_TO_XLSX)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


