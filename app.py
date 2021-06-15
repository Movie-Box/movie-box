from flask import Flask, request, flash
from flask.helpers import url_for
from flask.templating import render_template
import requests
from werkzeug.utils import redirect
from werkzeug.wrappers import response

app = Flask(__name__)

app.config['SECRET_KEY'] = 'TtNqvoYQX@6Fjr&@GT5pW!brWFSZ'

# @app.route("/test")
# def test():
#     movie = 'https://api.themoviedb.org/3/movie/popular?api_key=6759ed5eeb52690e2718450fa55c04f4&language=en-US&page=1'
#     movie_response = requests.get(movie)
#     movie_json = movie_response.json()
#     return render_template('test.html', movies=movie_json['results'])

@app.route("/")
def index():
    movie = 'https://api.themoviedb.org/3/movie/popular?api_key=6759ed5eeb52690e2718450fa55c04f4&language=en-US&page=1'
    tv = 'https://api.themoviedb.org/3/tv/popular?api_key=6759ed5eeb52690e2718450fa55c04f4&language=en-US&page=1'
    movie_response = requests.get(movie)
    tv_response = requests.get(tv)
    movie_json = movie_response.json()
    tv_json = tv_response.json()
    
    return render_template('index.html', title='Home', movies=movie_json['results'], tvs=tv_json['results'] )

@app.route('/movie')
def popular_movie():
    url = 'https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=6759ed5eeb52690e2718450fa55c04f4&page=1'
    response = requests.get(url)
    movie_json = response.json()
    return render_template('popular_movie.html', title='Popular Movie', movies=movie_json['results'])

@app.get("/movie/<movie_id>/<movie_name>")
@app.post("/movie/<movie_id>/<movie_name>")
def movie_detail(movie_id, movie_name):
    movie_url ='https://api.themoviedb.org/3/movie/{}?api_key=6759ed5eeb52690e2718450fa55c04f4&language=en-US'
    similar_movie_url = 'https://api.themoviedb.org/3/movie/{}/similar?api_key=6759ed5eeb52690e2718450fa55c04f4&language=en-US&page=1'
    response = requests.get(movie_url.format(movie_id))
    movie_detail = response.json()
    similar_movie_response = requests.get(similar_movie_url.format(movie_id))
    similar_movie_detail = similar_movie_response.json()
    return render_template('movie-detail.html', title=movie_name, movie=movie_detail, types=movie_detail['genres'], similar_movie=similar_movie_detail['results'])

@app.route('/tv')
def popular_tv():
    url = 'https://api.themoviedb.org/3/tv/popular?api_key=6759ed5eeb52690e2718450fa55c04f4&language=en-US&page=1'
    response = requests.get(url)
    popular_tv = response.json()
    return render_template('popular_tv.html', title='Popular TV Shows', tvs=popular_tv['results'])

@app.route("/tv/<tv_id>/<tv_name>/")
def tv_detail(tv_id, tv_name):
    url = 'https://api.themoviedb.org/3/tv/{}?api_key=6759ed5eeb52690e2718450fa55c04f4&language=en-US'
    response = requests.get(url.format(tv_id))
    tv_detail = response.json()
    return render_template('tv_detail.html', title=tv_name, tv=tv_detail, types=tv_detail['genres'])

