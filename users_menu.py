import user_storage_sql
import movies_menu


def users_menu():
    """printing the menu and call the enter_choice-function"""
    users_in_db = user_storage_sql.get_users_list()
    max_index = len(users_in_db) + 1
    print("Welcome to the Movie App!")
    print("\nSelect a user:")
    for index, user in enumerate(users_in_db, 1):
        print(f"{index}.  {user}")
    print(f"{max_index}.  Create new user")
    print("0.  Exit")
    print()
    enter_choice(max_index, users_in_db)


def enter_choice(max_index, users_in_db):
    """prompt and calls the specific function"""

    def exit_program():
        """exits the program with a goodbye message"""
        print("\nThank you for using My Movies Database. Goodbye!")
        exit()

    # Dispatch table: maps menu choices to functions
    menu_actions = {
        0: exit_program,
        max_index: user_storage_sql.create_new_user
    }

    while True:
        try:
            choice = int(input(f"Enter choice (0-{max_index}): "))
            if choice in menu_actions:
                menu_actions[choice]()
                break  # Exit loop after executing choice (exit() will terminate before this)
            elif 0 < choice < max_index:
                movies_menu.menu(users_in_db[choice - 1])
            else:
                print(
                    f"Invalid choice. Please enter a number between 0 and {max_index}.")
        except ValueError:
            print(f"Invalid input. Please enter a number between 0 and {max_index}.")

def main():
    users_menu()

if __name__ == "__main__":
    main()