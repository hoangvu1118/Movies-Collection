import requests
import json
import pandas as pd 
import numpy as np
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

headers = {
        "accept": "application/json",
        'Accept-Language': 'en-US',
        "Authorization": os.getenv('API_KEY')
        }

url_genres = "https://api.themoviedb.org/3/genre/movie/list?language=en"
genre = requests.get(url_genres, headers=headers)

movie_list, vote_list, date, poster = [], [], [], []
for i in range(1,11):
    url = f"https://api.themoviedb.org/3/movie/popular?language=en-US&page={i}"

    

    response = requests.get(url, headers=headers)

    data = response.json()
    movies = data.get('results',[])
    for movie in movies:
        movie_list.append(movie['title'])
        vote_list.append(movie['vote_average'])
        date.append(movie['release_date'])
        poster.append(f"https://image.tmdb.org/t/p/w500{movie['poster_path']}")

data = [poster, movie_list, np.round(vote_list,1), date, [i for i in range(1,201)]]

def Movies_DB():
    connect= sqlite3.connect(f"Movies_Database/Movies.db")
    cur = connect.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Movies (ID, Poster text, Title text, Rating real, Release text)""")
    for id in range(0,len(data[0])):
        values = (data[4][id], data[0][id], data[1][id], data[2][id], data[3][id])
        cur.execute("INSERT INTO Movies (ID, Poster, Title, Rating, Release) VALUES (?,?,?,?,?)", values )
        connect.commit()
    connect.close()
    return None

