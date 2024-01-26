import os


### HELPER FUNCTIONS ###
def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

def wait_for_keypress():
    while True:
        input('\nPress "Enter" to continue...')
        break
########################