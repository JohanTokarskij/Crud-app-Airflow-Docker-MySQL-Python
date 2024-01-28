import os
from time import sleep

## HELPER FUNCTIONS #
def clear_screen(sleep_value=0.75):
        sleep(sleep_value)
        os.system('cls' if os.name == 'nt' else 'clear')

def wait_for_keypress(sleep_value=0):
    while True:
        input('\nPress "Enter" to continue...')
        clear_screen(sleep_value)
        break
