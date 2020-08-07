import psycopg2
import datetime

url = "enter url here!"

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies(
    id SERIAL PRIMARY KEY,
    title TEXT,
    release_timestamp REAL
    );"""


CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY
    );"""


CREATE_WATCHLIST_TABLE = """CREATE TABLE IF NOT EXISTS watchlist(
    watcher_name TEXT,
    movie_id INTEGER,
    FOREIGN KEY(watcher_name) REFERENCES users(username),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
    );"""

INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES (%s, %s);"
INSERT_USER = "INSERT INTO users (username) VALUES (%s);"
INSERT_WATCHED_MOVIE = "INSERT INTO watchlist (watcher_name, movie_id) VALUES (%s,%s);"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > %s;"
SELECT_WATCHED_MOVIES = """SELECT movies.title 
FROM movies 
JOIN watchlist 
ON movies.id = watchlist.movie_id 
WHERE watcher_name = %s;"""
DELETE_MOVIE = "DELETE FROM MOVIES WHERE title = %s;"

connection = psycopg2.connect(url)


def create_tables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MOVIES_TABLE)
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_WATCHLIST_TABLE)


def add_movie(title, release_timestamp):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIES, (title, release_timestamp))


def add_user(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (username,))


def get_movies(upcoming = False):
    with connection:
        with connection.cursor() as cursor:
            if upcoming:
                today_timestamp = datetime.datetime.today().timestamp()
                cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp, ))
            else:
                cursor.execute(SELECT_ALL_MOVIES)
            return cursor.fetchall()


def watch_movie(username, movie_id):
    with connection:
        with connection.cursor() as cursor:
            connection.execute(INSERT_WATCHED_MOVIE, (username, movie_id))


def get_watched_movies(username):
    with connection:
        with connection.cursor() as cursor:
            cursor = connection.cursor()
            cursor.execute(SELECT_WATCHED_MOVIES, (username,))
            return cursor.fetchall()


def check_username(username):
    with connection:
        with connection.cursor() as cursor:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM users WHERE username = %s;', (username,))
            return cursor.fetchall()