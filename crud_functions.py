from functions import *

def create_new_list():
    list_name = input("Enter a name for the new list: ") + '.json'
    os.makedirs(BASE_DIR, exist_ok=True)
    if not os.path.exists(os.path.join(BASE_DIR, list_name)):
        with open(os.path.join(BASE_DIR, list_name), 'w') as file:
            json.dump([], file)
        print(f"List '{list_name}' created successfully.")
        time.sleep(2)
        clear_screen(100)
    else:
        print("List already exists.")
        time.sleep(2)
        clear_screen(100)

def read_list():
    lists = os.listdir(BASE_DIR) if os.path.exists(BASE_DIR) else []
    while_read = True
    while while_read:
        selected_option = view_lists(lists)
        if selected_option == len(lists) + 1:
            while_read = False
        elif 1 <= selected_option <= len(lists):
            file_name = lists[selected_option - 1]
            if file_name:
                key = prompt_password()
                tasks = load_tasks(file_name)
                try:
                    tasks = [decrypt_message(task, key) for task in tasks]
                except Exception as e:
                    print("Incorrect password or corrupted data.")
                    time.sleep(2)
                    clear_screen(100)
                    continue
                clear_screen(100)
                selected_task = view_tasks_select(tasks, "Current tasks:")
                if selected_task == len(tasks) + 1:
                    clear_screen(100)
                else:
                    print("Invalid selection.")
                    time.sleep(2)
                    clear_screen(100)
            else:
                print("Invalid selection.")
                time.sleep(2)
                clear_screen(100)

def update_list():
    lists = os.listdir(BASE_DIR) if os.path.exists(BASE_DIR) else []
    while_update = True
    while while_update:
        selected_option = view_lists(lists)
        if selected_option == len(lists) + 1:
            while_update = False
        elif 1 <= selected_option <= len(lists):
            list_name = lists[selected_option - 1]
            while_list = True
            while while_list:
                clear_screen(100)
                menu_option = menu(f'{list_name} list', 3, ['Add task.', 'Update task.', 'Delete task.'])
                if menu_option == 4:
                    while_list = False
                    clear_screen(100)
                else:
                    key = prompt_password()
                    tasks = load_tasks(list_name)
                    try:
                        tasks = [decrypt_message(task, key) for task in tasks]
                    except Exception as e:
                        print("Incorrect password or corrupted data.")
                        time.sleep(2)
                        clear_screen(100)
                        continue
                    if menu_option == 1:
                        clear_screen(100)
                        task = input("Enter a new task: ")
                        tasks.append(task)
                        encrypted_tasks = [encrypt_message(task, key) for task in tasks]
                        save_tasks(list_name, encrypted_tasks)
                        clear_screen(100)
                        print(f"Task: '{task}' added successfully to '{list_name}'.")
                        input(f'Press Enter to return to the {(list_name).upper()} menu...')
                        clear_screen(100)
                    elif menu_option == 2:
                        clear_screen(100)
                        while_update_task = True
                        while while_update_task:
                            selected_task = view_tasks_select(tasks, 'Enter the number of the task you would like to update:')
                            if selected_task == len(tasks) + 1:
                                while_update_task = False
                            elif 1 <= selected_task <= len(tasks):
                                new_val = input("Enter the new task: ")
                                tasks[selected_task - 1] = new_val
                                encrypted_tasks = [encrypt_message(task, key) for task in tasks]
                                save_tasks(list_name, encrypted_tasks)
                                clear_screen(100)
                                selected_task = view_tasks_select(tasks, "Current tasks:")
                                if selected_task == len(tasks) + 1:
                                    clear_screen(100)
                                else:
                                    print("Invalid selection.")
                                    time.sleep(2)
                                    clear_screen(100)
                            else:
                                print("Invalid selection.")
                                time.sleep(2)
                                clear_screen(100)
                    elif menu_option == 3:
                        clear_screen(100)
                        selected_task = view_tasks_select(tasks, "Enter the number of the task you would like to delete:")
                        if selected_task <= len(tasks):
                            tasks.pop(selected_task - 1)
                            encrypted_tasks = [encrypt_message(task, key) for task in tasks]
                            save_tasks(list_name, encrypted_tasks)
                            clear_screen(100)
                            selected_task_up = view_tasks_select(tasks, "Updated tasks:")
                            if selected_task_up == len(tasks) + 1:
                                clear_screen(100)
                            else:
                                print("Invalid selection.")
                                time.sleep(2)
                                clear_screen(100)
                    else:
                        print("Invalid selection.")
                        time.sleep(2)
                        clear_screen(100)
        else:
            print("List does not exist.")
            time.sleep(2)
            clear_screen(100)


def delete_list():
    list_name = input("Please enter the name of the list you would like to delete: ") + '.json'
    if os.path.exists(os.path.join(BASE_DIR, list_name)):
        os.remove(os.path.join(BASE_DIR, list_name))
        print(f"List {list_name} deleted successfully.")
        time.sleep(2)
        clear_screen(100)
    else:
        print(f"'{list_name}' list does not exist.")
        time.sleep(2)
        clear_screen(100)