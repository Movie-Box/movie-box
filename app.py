from flask import Flask, request, flash
from flask.helpers import url_for
from flask.templating import render_template
import requests
from werkzeug.utils import redirect

app = Flask(__name__)

app.config['SECRET_KEY'] = 'TtNqvoYQX@6Fjr&@GT5pW!brWFSZ'

@app.get('/')
@app.post('/')
def index():
    if request.method == 'POST':
        url = 'https://api.themoviedb.org/3/search/movie?api_key=6759ed5eeb52690e2718450fa55c04f4&query={}'
        query = request.form.get('search')
        response = requests.get(url.format(query))
        search_movie_json = response.json()
        status_code =  response.status_code
        success = response.ok
        if success:
            return render_template('index.html', search_movies=search_movie_json['results'], query=query, success=success)
        elif status_code == 422:
            msg = 'Search is Empty'
            return redirect(url_for('index', msg=msg))
    elif request.method == 'GET':
        movie = requests.get('https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=6759ed5eeb52690e2718450fa55c04f4&page=1')
        movie_json = movie.json()
        success = movie.ok
        return render_template('index.html', title='Trending', movies=movie_json['results'], success=success)
    return render_template('index.html')

@app.get("/<movie_id>/<movie_name>")
@app.post("/<movie_id>/<movie_name>")
def movie_detail(movie_id, movie_name):
    movie_url ='https://api.themoviedb.org/3/movie/{}?api_key=6759ed5eeb52690e2718450fa55c04f4&language=en-US'
    similar_movie_url = 'https://api.themoviedb.org/3/movie/{}/similar?api_key=6759ed5eeb52690e2718450fa55c04f4&language=en-US&page=1'
    response = requests.get(movie_url.format(movie_id))
    movie_detail = response.json()
    similar_movie_response = requests.get(similar_movie_url.format(movie_id))
    similar_movie_detail = similar_movie_response.json()
    return render_template('movie-detail.html', title=movie_name, movie=movie_detail, types=movie_detail['genres'], similar_movie=similar_movie_detail['results'])
