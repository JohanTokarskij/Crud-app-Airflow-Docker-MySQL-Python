import subprocess
import time


def run_command_in_compose(service_name, command):
    try:
        compose_command = f'docker-compose exec -T {service_name} /bin/bash -c \"{command}\"'
        subprocess.run(compose_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f'An error occurred: {e}')

def is_container_running(container_name):
    try:
        result = subprocess.run(['docker', 'ps', '--filter', f'name={container_name}', '--format', '{{.Names}}'], stdout=subprocess.PIPE, text=True)
        return container_name in result.stdout
    except subprocess.CalledProcessError:
        return False

def wait_for_containers(container_names, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if all(is_container_running(name) for name in container_names):
            return True
        time.sleep(2) 
    return False


def initialize_airflow():
    # Start the Airflow services
    try:
        subprocess.run(f'docker-compose up -d airflow-webserver airflow-scheduler', shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f'An error occurred: {e}')
        return
    
    # Run the Airflow database upgrade
    run_command_in_compose('airflow-webserver', 'airflow db migrate')

    # Create an admin user
    run_command_in_compose('airflow-webserver', 'airflow users create --username admin --password password --firstname Admin --lastname User --role Admin --email admin@example.com')

    # Upgrade the database for the scheduler
    run_command_in_compose('airflow-scheduler', 'airflow db migrate')

    if wait_for_containers(['airflow-webserver', 'airflow-scheduler']):
        print('Airflow is set up and ready.')
    else:
        print("Error: Airflow containers are not running after setup.")

if __name__ == '__main__':
    initialize_airflow()
