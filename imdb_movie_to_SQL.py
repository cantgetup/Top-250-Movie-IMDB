import mysql.connector
from mysql.connector import Error
import numpy as np
import pandas as pd

imdb_movies = pd.read_csv('imdb_movies.csv')
imdb_movies['movie_id'] = range(1,251) 

# create connection
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

pw = '????'
connection = create_server_connection("localhost", "root", pw)

# create database
def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

create_database_query = 'CREATE DATABASE imdb_movie'
create_database(connection, create_database_query)

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

        
# connect to imdb_TVshow database
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


create_imdb_table = """
CREATE TABLE imdb_movie (
  movie_id INT PRIMARY KEY,
  title VARCHAR(128) NOT NULL,
  link VARCHAR(128) NOT NULL,
  director VARCHAR(128) NOT NULL,
  writer VARCHAR(128) NOT NULL,
  star VARCHAR(128) NOT NULL,
  genre VARCHAR(128) NOT NULL,
  rating float(2,1) NOT NULL
  );
 """

db = 'imdb_movie'

connection = create_db_connection("localhost", "root", pw, db) # Connect to the Database
execute_query(connection, create_imdb_table) # Execute our defined query

# insert data into imdb_tvshow

for idx, line in imdb_movies.iterrows():

    insert_imdb_table=f"""
    INSERT INTO imdb_movie VALUES
    (
    "{line['movie_id']}",
    "{line['Title']}",
    "{line['url']}",
    "{line['Director']}",
    "{line['Writer']}",
    "{line['Star']}",
    "{line['Genre']}",
    {line['Rating']}
    );
    """
    execute_query(connection, insert_imdb_table) # Execute our defined query
