from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///data/movies.db"

# Create the engine
engine = create_engine(DB_URL) # , echo=True

# Create the users table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
    """))
    connection.commit()

def list_user():
    """Retrieve all user from database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM users"))
        users = result.fetchall()
    return users

def add_user(name):
    """Add a new user to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO users (name) VALUES (:name)"),
                               {"name": name})
            connection.commit()
            print(f"User '{name}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def create_new_user():
    """create a new user for the database"""
    users_in_db = list_user()
    users = []
    for user in users_in_db:
        users.append(user[1])
    while True:
        name = input("Enter new user name (at least 3 characters): ").strip()
        if name not in users and len(name) >= 3:
            add_user(name)
            break
        else:
            print(f'The name "{name}" is already in the database or your name is to short, try again')


def get_users_list():
    users = []
    users_in_db = list_user()
    for user in users_in_db:
        users.append(user[1])
    return users


def main():
    #create_new_user()
    print(get_users_list())

if __name__ == "__main__":
    main()