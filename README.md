# Hybrid SQL-NoSQL Message Management System

## Project Overview
This project, the Hybrid SQL-NoSQL Message Management System, is a robust platform that functions similarly to a forum. It allows users to create and manage accounts, log in and post messages (with the option to attach files), search through messages, and view message statistics. Utilizing a Python-based backend, the system supports comprehensive account and message management operations, including creation, reading, updating, and deletion (CRUD) across both MySQL and MongoDB databases. With Docker containerization for MySQL handling accounts and logs, MongoDB for user posts, and Apache Airflow orchestrating workflows and log management, this application offers a seamless experience for managing forum-like interactions.

## Key Features Include:
* UI based on Python's `questionary` module, abstracting a technical side of the implementation.
* CRUD Functionality: Provides complete Create, Read, Update, and Delete options for both MySQL and MongoDB databases.
* MySQL is used for creation and managment of user accounts and logs.
* MongoDB for message posting: Users can post and manage their messages. The system also handles the upload and download of various file types including text documents, images, music, and videos (*To upload files, users should place them into the './Uploads' folder in the root directory. Upon doing so, the user is prompted to confirm if they wish to upload the selected file or files. Similarly, when searching for posts, if any post is associated with a file, the user receives a prompt asking if they want to download the file. Downloaded files are then saved to the './Downloads' directory.*).
* Equipped with detailed logging features, which include: user login activity recorded in '.logs/user_login.csv' upon user authorisation, logs aggregation in '.logs/login_history.xlsx' showing hourly aggregation of log in activity per user (done by the Python logging module). Additionally, on an hourly basis, all data from '.logs/user_login.csv' is  transferred to the 'logs' table within the 'crud_app' database in MySQL. Post transfer, the '.logs/user_login.csv' file is cleared to maintain efficiency and organization.


## Prerequisites
- Docker
- Docker Compose
- Python 3.8+


## Initial Setup (First-time Run)
#### To set up the project environment for the first time, follow these steps:
1. Clone the repository: `git clone [repository URL]`
2. Navigate to the project directory: `cd [project directory]`
3. To ensure proper isolation of project dependencies, it is recommended to create and activate a virtual environment before running this app. Follow these steps:
* Create a new virtual environment: `python -m venv venv`
* Activate the virtual environment: `venv\Scripts\activate` on Windows or `source venv/bin/activate` on Linux/macOS
4. Install the required dependencies: `pip install -r requirements.txt`
5. Run `docker-compose up -d` in terminal to pull the necessary Docker images and start the containers. Once the pulling is complete, proceed to the next step.
6. Run `python setup_mysql.py` to set up MySQL. After getting messages that database for "airflow" and "crud_app" are set up and ready proceed to the next step.
7. Run `python setup_airflow.py` to set up Apache Airflow. After getting a message "Command executed successfully on airflow-webserver" and "Command executed successfully on airflow-scheduler" the initial set up is done!

#### To schedule Airflow logging:

- Navigate to `http://localhost:8080/`.
- Login with `admin:password`.
- Start the `csv_to_sql_dag` DAG to enable logging.


## Regular Usage (Subsequent Runs)
#### For day-to-day operation of the system, execute the following:

- Start Docker containers (if not running) by running `docker-compose up -d` from the project's directory in terminal.
- Run `python app.py` to start the application. Follow the on-screen prompts to interact with the application.

#### Accessing the logs
Houly logs are stored in `./logs/user_login.csv`, aggregated logs per hour are available in `./logs/login_history.xlsx`. Database logs are stored in the `logs` table of `crud_app` database. 

The database is accessible via MySQL:

- **Host**: `localhost`
- **Port**: `3306`
- **User**: `root`
- **Password**: `password`


## Security Note:
Please be aware that for simplicity in development and testing, this project uses default passwords for database and Apache Airflow GUI access. These are not secure and should be changed before any production or public deployment. Always use strong, unique passwords in production environments to ensure security.
