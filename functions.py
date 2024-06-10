import os
import json
import time
import base64
from dotenv import load_dotenv, find_dotenv
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from getpass import getpass



dotenv_path = find_dotenv('config.env')
print(f"Loading environment variables from: {dotenv_path}")
load_dotenv(dotenv_path)

env_salt = os.getenv("SALT")
env_password = os.getenv('PASSWORD')
BASE_DIR = os.getenv('BASE_DIR')

print(f"Loaded password: {env_password}")


def derive_key(password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=env_salt.encode(),
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

KEY = derive_key(env_password)

def encrypt_message(message, key):
    fernet = Fernet(key)
    return fernet.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message.encode()).decode()

def load_tasks(list_name):
    try:
        with open(os.path.join(BASE_DIR, list_name), 'r') as file:
            encrypted_tasks = json.load(file)
            return encrypted_tasks
    except FileNotFoundError:
        return []

def save_tasks(list_name, tasks):
    with open(os.path.join(BASE_DIR, list_name), 'w') as file:
        json.dump(tasks, file)

def view_lists(lists):
    if not lists:
        print("No lists available. Please create a new list.")
        input("Press Enter to return to the menu...")
        clear_screen(100)
    options = []
    for _, list_file in enumerate(lists, start=1):
        options.append(list_file)
    selected_option = menu("Available lists:", len(lists), options)
    return selected_option

def view_tasks_select(tasks, context):
    if not tasks:
        print("No tasks found.")
    else:
        options = []
        for _, task in enumerate(tasks, start=1):
            options.append(task)
        selected_option = menu(f'Tasks:', len(tasks), options, context)
        return selected_option

def clear_screen(n):
    for _ in range(n):
        print(" ")

def menu(title, num_options, options_array, context='Please select one of the options:'):
    while True:
        title_length = len(title)
        context_length = len(context)
        side_length = int((context_length - (title_length + 2)) / 2)
        if side_length % 2 == 0:
            side_char = '-' * (side_length)
            header = f'{side_char} {(title).upper()} {side_char}'
            total_char = '-' * (context_length)
        else:
            side_char = '-' * (side_length)
            header = f'{side_char} {(title).upper()} {side_char}'
            total_char = '-' * (context_length)
        print(header)
        print(context)
        print(total_char)
        for i in range(num_options):
            print(f'{i+1}) {options_array[i]}')
        exit_option = f'{num_options+1}) Exit.'
        print(exit_option)
        print(total_char)
        try:
            menu_option = int(input('Option: '))
            return menu_option
        except ValueError:
            print('Please enter a valid integer')
            time.sleep(2)
            clear_screen(100)

def prompt_password():
    password = getpass("Enter password to access the tasks: ")
    return derive_key(password)