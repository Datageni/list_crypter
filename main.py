from crud_functions import *

while_main = True

while(while_main):
    clear_screen(100)
    menu_option = menu('encripted lists',4,['Create new list.',"Read list.",'Update list.','Delete list.'])
    try:
        if  menu_option == 5:
            while_main = False
        elif menu_option ==1:
            clear_screen(100)
            create_new_list()
        elif menu_option ==2:
            clear_screen(100)
            read_list()
        elif menu_option ==3:
            clear_screen(100)
            update_list()
        elif menu_option ==4:
            clear_screen(100)
            delete_list()
        else:
            print('Invalid input.')
            time.sleep(2)
    except ValueError:
        print('Invalid input. Please enter a number.')
        time.sleep(2)