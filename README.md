# Hybrid SQL-NoSQL Message Management System

## Description
This project, the Multi-Database Message Management System, is a robust application designed to seamlessly interact with both MySQL and MongoDB databases. It integrates a Python-based backend with Docker containerization for MySQL and MongoDB, alongside Apache Airflow for workflow management. The system allows users to create accounts, login, post messages, and perform various database operations with an intuitive command-line interface. It's equipped with user-friendly menus and detailed logging functionalities, enhancing both user experience and system monitoring. Importantly, the application features comprehensive CRUD (Create, Read, Update, Delete) functionality in both MySQL and MongoDB environments, providing versatile data manipulation capabilities across both SQL and NoSQL database systems.


## Prerequisites
- **Python Compatibility**: Developed and tested with **Python 3.12.0**. Compatibility with other versions may vary.
- **Dependencies**: Ensure all packages listed in `requirements.txt` are installed.


## Initial Setup (First-time Run)
#### To set up the project environment for the first time, follow these steps:

- Run `docker-compose up -d` in terminal to download and start the containers.
- Run `python setup_mysql.py` to set up MySQL.
- Run `python setup_airflow.py` to set up Apache Airflow.

#### To schedule Airflow logging:

- Navigate to `http://localhost:8080/`.
- Login with `admin:password`.
- Start the `csv_to_sql_dag` DAG to enable logging.


## Regular Usage (Subsequent Runs)
#### For day-to-day operation of the system, execute the following:

- Start Docker containers (if not running) by running `docker-compose up -d` in terminal.
- Run `python app.py` to start the application.


## Security Note:
Please be aware that for simplicity in development and testing, this project uses default passwords for database and Apache Airflow GUI access. These are not secure and should be changed before any production or public deployment. Always use strong, unique passwords in production environments to ensure security.
