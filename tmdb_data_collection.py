import urllib2
import requests
import json
import imdb
import time
import itertools
import wget
import os
import tmdbsimple as tmdb
import numpy as np
import random
#import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# Set here the path where you want the scraped folders to be saved
poster_folder = 'posters_final/'
if poster_folder.split('/')[0] in os.listdir('./'):
    print('Folder already exists')
else:
    os.mkdir('./' + poster_folder)


api_key = '9525307f0cf585295ef748f0434812b6'
# url = 'https://api.themoviedb.org/3/movie/1581?api_key=' + api_key
# data = urllib2.urlopen(url).read()
# # create dictionary from json
# dataDict = json.loads(data)
tmdb.API_KEY = api_key
search = tmdb.Search()


all_movies = tmdb.Movies()
top_movies = all_movies.popular()
top20_movies = top_movies['results']


########
# Create a tmdb genre object!
genres=tmdb.Genres()
# the list() method of the Genres() class returns a listing of all genres in the form of a dictionary.
list_of_genres=genres.list()['genres']
# Create a dictionary to look up genre names from it IDs
genre_id_to_name = {}
for i in range(len(list_of_genres)):
    genre_id = list_of_genres[i]['id']
    genre_name = list_of_genres[i]['name']
    genre_id_to_name[genre_id] = genre_name


########
#print out top 5 movies' titles and genre
########
for i in range(len(top20_movies)):
    mov = top20_movies[i]
    title = mov['title']
    # one movie might have several IDs
    genre_ids = mov['genre_ids']
    genre_names = []
    for id in genre_ids:
        genre_name = genre_id_to_name[id]
        genre_names.append(genre_name)
    # print title, genre_names
    if i==4 :
        break
########


########
# Pull result from the top 50 pages
# It uses python pickle package to organize serialization
# Some of the code below will store the data into python "pickle" files
# so that it can be ready directly from memory, as opposed to being downloaded every time.
# Once done, you should comment out any code which generated an object that was pickled and is no longer needed.
# Comment out this section once the data is saved into pickle file
########
top1000_movies = []
# print('Pulling movie list, just wait...')
# for i in range(1,51):
#     if i%15==0:
#         time.sleep(7)
#     movies_on_this_page = all_movies.popular(page=i)['results']
#     top1000_movies.extend(movies_on_this_page)
# len(top1000_movies)
# f3 = open('movie_list.pck1','wb')
# pickle.dump(top1000_movies,f3)
# f3.close()
# print('Done!')
########
f3=open('movie_list.pck1','rb')
top1000_movies = pickle.load(f3)
f3.close()


# These functions take in a string movie name i.e. like "The Matrix" or "Interstellar"
# What they return is pretty much clear in the name - Poster, ID , Info or genre of the Movie!
def grab_poster_tmdb(movie):
    response = search.movie(query=movie)
    id = response['results'][0]['id']
    movie = tmdb.Movies(id)
    posterp=movie.info()['poster_path']
    title = movie.info()['original_title']
    url='image.tmdb.org/t/p/original'+posterp
    title='_'.join(title.split(' '))
    strcmd='wget -O '+poster_folder+title+'.jpg '+url
    os.system(strcmd)

def get_movie_id_tmdb(movie):
    response = search.movie(query=movie)
    movie_id=response['results'][0]['id']
    return movie_id

def get_movie_info_tmdb(movie):
    response = search.movie(query = movie)
    id = response['results'][0]['id']
    movie = tmdb.Movies(id)
    info = movie.info()

def get_movie_genres_tmdb(movie):
    response = search.movie(query = movie)
    id = response['results'][0]['id']
    movie=tmdb.Movies(id)
    genres = movie.info()['genres']
    return genres

# grab_poster_tmdb("The Matrix")
# print get_movie_id_tmdb("The Matrix")
