import logging
import os
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
    if os.path.exists(PATH_TO_XLSX):
        print('The file exists!')
    else:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        column_names = ['Username', 'Year', 'Month', 'Day', 'Hour', 'Count']
        sheet.append(column_names)

        with open(PATH_TO_CSV, 'r', newline='', encoding='utf-8') as file:
            csv_data = list(csv.reader(file))

        counts_per_hour = Counter()
        for username, timestamp in csv_data:
            dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            hour_slice = dt.strftime('%Y-%m-%d %H')
            counts_per_hour[(username, hour_slice)] += 1

        for (username, hour_slice), count in counts_per_hour.items():
            date_part, hour_part = hour_slice.split(' ')
            year, month, day = date_part.split('-')
            row = [username, int(year), int(month), int(day), int(hour_part), count]
            sheet.append(row)

        workbook.save(PATH_TO_XLSX)

