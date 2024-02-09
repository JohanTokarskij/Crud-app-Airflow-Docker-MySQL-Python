import os
from time import sleep
import questionary

## HELPER FUNCTIONS #
def clear_screen(sleep_value=0.75):
        sleep(sleep_value)
        os.system('cls' if os.name == 'nt' else 'clear')

def wait_for_keypress(sleep_value=0):
    while True:
        questionary.press_any_key_to_continue().ask()
        clear_screen(sleep_value)
        break
