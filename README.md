# Hybrid SQL-NoSQL Message Management System

## Project Overview
This project, the Hybrid SQL-NoSQL Message Management System, is a robust application designed to seamlessly interact with both MySQL and MongoDB databases. It integrates a Python-based backend with Docker containerization for MySQL (for account management), MongoDB (for a range of user post operations), alongside Apache Airflow (for efficient workflow management of system logs). The system allows users to create accounts, login, publidh messages, and perform various database operations with an intuitive command-line interface. It's equipped with user-friendly menus and detailed logging functionalities, enhancing both user experience and system monitoring. The application features comprehensive CRUD (Create, Read, Update, Delete) functionality in both MySQL and MongoDB environments, providing versatile data manipulation capabilities across both SQL and NoSQL database systems.

## Key Features Include:
* Command-Line Interface (CLI): An easy-to-use command interface that makes navigating and operating the system straightforward for all users.
* CRUD Functionality: Provides complete Create, Read, Update, and Delete options for both MySQL and MongoDB databases.
* MySQL for User Account Management: Offers strong tools to create and manage user accounts efficiently.
* MongoDB for Message Posting: Users can post and manage their messages. The system also handles the upload and download of various file types including text documents, images, music, and videos (*When the system detects a file in the './Uploads' folder, it prompts the user to confirm if they wish to upload the file. If the user opts to upload the file, it is then uploaded and subsequently removed from the './Uploads' folder. Similarly, during a post search, if a file is associated with any of the posts, the user receives a prompt asking if they want to download the file. In this scenario, the downloaded file is saved to the './Downloads' directory*).
* Enhanced Logging: Equipped with detailed logging features, which include user login activity recorded in '.logs/user_login.csv'. These records are then systematically compiled into '.logs/login_history.xlsx' every hour(done by the Python logging module). Additionally, on an hourly basis, all data from '.logs/user_login.csv' is  transferred to the 'logs' table within the 'crud_app' database in MySQL. Post transfer, the '.logs/user_login.csv' file is cleared to maintain efficiency and organization.


## Prerequisites
- **Python Compatibility**: Developed and tested with **Python 3.12.0**. Compatibility with other versions may vary.


## Initial Setup (First-time Run)
#### To set up the project environment for the first time, follow these steps:
1. Clone the repository: `git clone [repository URL]`
2. Navigate to the project directory: `cd [project directory]`
3. To ensure proper isolation of project dependencies, it is recommended to create and activate a virtual environment before running this app. Follow these steps:
* Create a new virtual environment: `python -m venv venv`
* Activate the virtual environment: `venv\Scripts\activate` on Windows or `source venv/bin/activate` on Linux/macOS
4. Install the required dependencies: `pip install -r requirements.txt`
5. Run `docker-compose up -d` in terminal to download and start the containers.
6. Run `python setup_mysql.py` to set up MySQL.
7. Run `python setup_airflow.py` to set up Apache Airflow.

#### To schedule Airflow logging:

- Navigate to `http://localhost:8080/`.
- Login with `admin:password`.
- Start the `csv_to_sql_dag` DAG to enable logging.


## Regular Usage (Subsequent Runs)
#### For day-to-day operation of the system, execute the following:

- Start Docker containers (if not running) by running `docker-compose up -d` from the project's directory in terminal.
- Run `python app.py` to start the application.



## Security Note:
Please be aware that for simplicity in development and testing, this project uses default passwords for database and Apache Airflow GUI access. These are not secure and should be changed before any production or public deployment. Always use strong, unique passwords in production environments to ensure security.
