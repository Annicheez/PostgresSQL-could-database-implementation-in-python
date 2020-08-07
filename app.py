import datetime
import SqlDatabase as database

menu = """"Please select one of the following options:
1) Add new movie
2) View upcoming movies
3) View all movies
4) Watch a movie
5) View watched movies
6) Create New User
7) Exit

Your selection: """
welcome = "Welcome to the watchlist app!"


def prompt_add_movie():
    title = input('Movie title: ')
    release_date_timestamp = datetime.datetime.strptime(input('Release date (dd-mm-yyyy): '), '%d-%m-%Y').timestamp()
    
    database.add_movie(title, release_date_timestamp)


def print_movie_list(heading, movies):
    print(f'-- {heading} movies --')
    for movie in movies:
        movie_date = datetime.datetime.fromtimestamp(movie[2])
        human_date = movie_date.strftime('%b %d %Y')
        print(f'{movie[0]}: {movie[1]} <on {human_date}>')

    print('---- \n')


def print_watched_movie_list(username, movies):
    print(f'--- {username}\'s watched movies')
    for movie in movies:
        print(f'{movie}')
    print("--- \n")


def prompt_watch_movie():
    username =  input('Who watched the movie?: ')
    movie_id = input('Movie ID:?')
    database.watch_movie(username, movie_id)


def prompt_show_watched_movies():
    username = database.check_username(input('username: '))
    if username:
        movies = database.get_watched_movies(username[0][0])
        if movies:
            print_watched_movie_list(username[0][0], movies)
        else:
            print(f'{username[0][0]} has watched no movies yet')
    else:
        print('No such user exists')


print(welcome)
database.create_tables()

user_input = 0

while user_input != '7':
    print(menu)
    user_input = input('Please enter your selection: ')
    if user_input == '1':
        prompt_add_movie()
    elif user_input == '2':
        movies = database.get_movies(True)
        print_movie_list('UPCOMING', movies)
    elif user_input == '3':
        movies = database.get_movies()
        print_movie_list('ALL', movies)
    elif user_input == '4':
        prompt_watch_movie()
    elif user_input == '5':
        prompt_show_watched_movies()
    elif user_input == '6':
        username = input('Please enter your desired username: ')
        database.add_user(username)
    else:
        print('Invalid input, please try again!')

