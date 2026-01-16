import movie_storage_sql as storage
import movies_menu

HTML_TEMPLATE = "index_template.html"


def get_html():
    """ Loads the html-template and returns it as a string """
    with open(HTML_TEMPLATE, "r") as fileobj:
        return fileobj.read()


def save_html(html_string, file_name):
    """ Saves the generated HTML-file """
    with open(file_name, "w") as fileobj:
        fileobj.write(html_string)


def get_string(movies):
    """ Returns the movie-data as a string """
    print(f"Number of movies: {len(movies)}")
    if movies is None:
        return None
    output = ""
    for title, info in movies.items():
        output += serialize_movie(title, info)
    return output


def serialize_movie(title, info):
    """ Serialize the movie-data and returns a string """
    output = ""
    output += '<li>\n'
    output += f'<div class="movie">\n'
    try:
        output += f'<img class="movie-poster" src="{info["poster_url"]}" title> <br/>\n'
    except KeyError:
        pass
    try:
        output += f'<div class="movie-title">{title}</div><br/>\n'
    except KeyError:
        pass
    try:
        output += f'<div class="movie-year">{info["year"]}</div><br/>\n'
    except KeyError:
        pass
    output += '</div>\n'
    output += '</li>\n'
    return output


def generate_website(user_name):
    file_name = f"{user_name}.html"
    movies = storage.list_movies(user_name)
    movies_string = get_string(movies)
    site_title = f"{user_name}'s Moviedatabase"
    html_template = get_html()
    html_output = html_template.replace("__TEMPLATE_TITLE__", site_title)
    html_output = html_output.replace("__TEMPLATE_MOVIE_GRID__", movies_string)
    save_html(html_output, file_name)
    print("Website was generated successfully.")
    movies_menu.press_enter(user_name)