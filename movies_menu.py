import random
import movie_storage_sql as storage
import data_fetcher
import website_generator

def press_enter():
    """last part of almost every function... stops the prompt until user presses enter"""
    print()
    input("Press enter to continue")
    menu()


def menu(user_name):
    """printing the menu and call the enter_choice-function"""
    print(f"\nWelcome back, {user_name}!\n")
    print("1.  List movies")
    print("2.  Add movie")
    print("3.  Delete movie")
    print("4.  Update movie")
    print("5.  Stats")
    print("6.  Random movie")
    print("7.  Search movie")
    print("8.  Movies sorted by rating")
    print("9.  Movies sorted by year")
    print("10. Filter movies")
    print("11. Generate website")
    print("0.  Exit")
    print()
    enter_choice()


def enter_choice():
    """prompt and calls the specific function"""

    def exit_program():
        """exits the program with a goodbye message"""
        print("\nThank you for using My Movies Database. Goodbye!")
        exit()

    # Dispatch table: maps menu choices to functions
    menu_actions = {
        0: exit_program,
        1: command_list_movies,
        2: command_add_movie,
        3: command_delete_movie,
        4: command_update_movie,
        5: stats,
        6: random_movie,
        7: search_movie,
        8: sorted_by_rating,
        9: sorted_by_year,
        10: filter_movies,
        11: website_generator.generate_website
    }

    while True:
        try:
            choice = int(input("Enter choice (0-10): "))
            if choice in menu_actions:
                menu_actions[choice]()
                break  # Exit loop after executing choice (exit() will terminate before this)
            else:
                print(
                    "Invalid choice. Please enter a number between 0 and 11.")
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 11.")


def enter_rating():
    """returns the rating of the movie after checking the validity of the input"""
    while True:
        try:
            rating = float(input("Enter new movie rating (0-10): "))
            if 0 <= rating <= 10:
                return rating
            else:
                print("Invalid rating")
        except ValueError:
            print("Invalid rating")


def enter_year():
    """returns the year of the movie after checking the validity of the input"""
    while True:
        try:
            year = int(input("Enter new movie year: "))
            if 1800 <= year <= 2100:
                return year
            else:
                print(
                    "Invalid year. Please enter a year between 1800 and 2100.")
        except ValueError:
            print("Invalid input. Please enter a valid year (e.g., 2024).")


def enter_title(prompt="Enter movie name: "):
    """returns a valid movie title (non-empty string)"""
    while True:
        title = input(prompt).strip()
        if title:
            return title
        else:
            print("Movie title cannot be empty. Please try again.")


def command_list_movies():
    """Retrieve and display all movies from the database"""
    movies = storage.list_movies()
    print(f"\n{len(movies)} movies in total")
    for title, info in movies.items():
        print(f"{title} ({info['year']}): {info['rating']}")
    press_enter()


def command_add_movie():
    """adds a new movie with rating to the database"""
    movies = storage.list_movies()

    title = enter_title("Enter new movie name: ")
    if title in movies:
        print(f'The movie "{title}" is already in the database')
    else:
        data_dict = data_fetcher.fetch_data(title)
        needed_data = data_fetcher.get_needed_data_from_dict(data_dict)
        if needed_data["Error"] is None:
            new_title = needed_data["Title"]
            try:
                year = int(needed_data["Year"])
            except:
                year = 0
            try:
                rating = float(needed_data["imdbRating"])
            except:
                rating = 0
            poster_url = needed_data["Poster"]
            storage.add_movie(new_title, year, rating, poster_url)
            # print(f"\nMovie {title} successfully added\n")
        else:
            print(needed_data["Error"])
    press_enter()


def command_delete_movie():
    """delete a movie from the database"""
    movies = storage.list_movies()
    title = enter_title("Enter movie name to delete: ")
    if title in movies:
        storage.delete_movie(title)
        # print(f"Movie {title} successfully deleted")
    else:
        print(f"Movie {title} doesn't exist")
    press_enter()


def command_update_movie():
    """update the rating of a movie in the database"""
    movies = storage.list_movies()

    title = enter_title("Enter movie name: ")
    if title in movies:
        rating = enter_rating()
        storage.update_movie(title, rating)
        # print(f"Movie {title} successfully updated")
    else:
        print(f"Movie {title} doesn't exist!")
    press_enter()


def average_rating():
    """returns the average rating of all movies in the database"""
    movies = storage.list_movies()
    if len(movies) == 0:
        return 0
    without_rating = 0
    total = 0
    for info in movies.values():
        if info['rating'] != 0:
            total += info['rating']
        else:
            without_rating += 1
    if (len(movies) - without_rating) == 0:
        return 0
    else:
        return total / (len(movies) - without_rating)


def more_then_one(rating):
    """returns a dictionary with movie-name and rating for all movies with a specific rating"""
    movies = storage.list_movies()
    movies_dict = {}
    for title, info in movies.items():
        if info['rating'] == rating:
            movies_dict[title] = info['rating']
    return movies_dict


def is_empty():
    """checks if the database is empty"""
    movies = storage.list_movies()
    return len(movies) == 0


def best_movie():
    """returns the name with rating of the best rated movie from the database"""
    if is_empty():
        return {"EMPTY DATABASE": 0}

    movies = storage.list_movies()
    best_rating = 0
    for title, info in movies.items():
        if info['rating'] != 0 and info['rating'] > best_rating:
            best_rating = info['rating']

    best_movies = more_then_one(best_rating)
    return best_movies


def worst_movie():
    """returns the name with rating of the worst rated movie from the database"""
    if is_empty():
        return {"EMPTY DATABASE": 0}

    movies = storage.list_movies()
    worst_rating = 10
    for title, info in movies.items():
        if info['rating'] != 0 and info['rating'] < worst_rating:
            worst_rating = info['rating']

    worst_movies = more_then_one(worst_rating)
    return worst_movies


def median_rating():
    """returns the movie with the middle score of the database, if its a even number of movies it returns the average of the two middle score movies"""
    if is_empty():
        return 0

    movies = storage.list_movies()
    rating_list = []
    without_rating = 0
    for info in movies.values():
        if info['rating'] != 0:
            rating_list.append(info['rating'])
        else:
            without_rating += 1
    rating_list.sort()
    if (len(movies) - without_rating) <= 2:
        return 0
    elif (len(movies) - without_rating) % 2 == 0:
        return (
                rating_list[len(rating_list) // 2 - 1] + rating_list[
            len(rating_list) // 2]
        ) / 2
    else:
        return rating_list[len(rating_list) // 2]


def stats():
    """lists some stats about the database"""
    print()
    print(f"Average rating: {average_rating():.1f}")
    print(f"Median rating: {median_rating():.1f}")
    best = best_movie()
    for name, rating in best.items():
        print(f"Best movie: {name}, {rating}")
    worst = worst_movie()
    for name, rating in worst.items():
        print(f"Worst movie: {name}, {rating}")
    press_enter()


def random_movie():
    """print a random movie with rating from the database"""
    if is_empty():
        print("\nEMPTY DATABASE")
        press_enter()
    else:
        movies = storage.list_movies()
        random_title = random.choice(list(movies.keys()))
        movie_info = movies[random_title]
        print(
            f"\nYour movie for tonight: {random_title} ({movie_info['year']}), it's rated {movie_info['rating']}"
        )
        press_enter()


def search_movie():
    """search option for a film or films in the database"""
    movies = storage.list_movies()

    search_term = input("Enter part of movie name: ").strip()
    if not search_term:
        print("Search term cannot be empty.")
    else:
        search_term_lower = search_term.lower()
        print()
        found = False
        for title, info in movies.items():
            if search_term_lower in title.lower():
                print(f"{title} ({info['year']}): {info['rating']}")
                found = True
        if not found:
            print(f"No movies found matching '{search_term}'.")
    press_enter()


def sorted_by_rating():
    """prints all films from the database, sorted by rating."""
    movies = storage.list_movies()

    print()
    sorted_list = sorted(movies.items(), key=lambda x: x[1]['rating'],
                         reverse=True)
    for title, info in sorted_list:
        print(f"{title} ({info['year']}): {info['rating']}")
    press_enter()


def sorted_by_year():
    """prints all films from the database, sorted by year."""
    movies = storage.list_movies()

    # Ask user for sort order
    while True:
        order = input(
            "Do you want to see the newest movies first? (y/n): ").strip().lower()
        if order in ['y', 'yes']:
            reverse_order = True
            break
        elif order in ['n', 'no']:
            reverse_order = False
            break
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

    print()
    sorted_list = sorted(movies.items(), key=lambda x: x[1]['year'],
                         reverse=reverse_order)
    for title, info in sorted_list:
        print(f"{title} ({info['year']}): {info['rating']}")
    press_enter()


def filter_movies():
    """filters movies based on minimum rating, start year, and end year"""
    movies = storage.list_movies()

    print("\nFilter Movies")
    print("(Leave any field blank to skip that filter)")
    print()

    # Get minimum rating (optional)
    min_rating = None
    while True:
        rating_input = input(
            "Enter minimum rating (leave blank for no minimum rating): ").strip()
        if rating_input == "":
            break
        try:
            min_rating = float(rating_input)
            if 0 <= min_rating <= 10:
                break
            else:
                print("Rating must be between 0 and 10.")
        except ValueError:
            print("Invalid rating. Please enter a number or leave blank.")

    # Get start year (optional)
    start_year = None
    while True:
        year_input = input(
            "Enter start year (leave blank for no start year): ").strip()
        if year_input == "":
            break
        try:
            start_year = int(year_input)
            if 1800 <= start_year <= 2100:
                break
            else:
                print("Year must be between 1800 and 2100.")
        except ValueError:
            print("Invalid year. Please enter a number or leave blank.")

    # Get end year (optional)
    end_year = None
    while True:
        year_input = input(
            "Enter end year (leave blank for no end year): ").strip()
        if year_input == "":
            break
        try:
            end_year = int(year_input)
            if 1800 <= end_year <= 2100:
                break
            else:
                print("Year must be between 1800 and 2100.")
        except ValueError:
            print("Invalid year. Please enter a number or leave blank.")

    # Filter movies based on criteria
    filtered_movies = {}
    for title, info in movies.items():
        # Check minimum rating
        if min_rating is not None and info['rating'] < min_rating:
            continue

        # Check start year
        if start_year is not None and info['year'] < start_year:
            continue

        # Check end year
        if end_year is not None and info['year'] > end_year:
            continue

        # Movie passes all filters
        filtered_movies[title] = info

    # Display results
    print("\nFiltered Movies:")
    if filtered_movies:
        for title, info in filtered_movies.items():
            print(f"{title} ({info['year']}): {info['rating']}")
        print(f"\nTotal: {len(filtered_movies)} movie(s) found")
    else:
        print("No movies match the specified criteria.")

    press_enter()