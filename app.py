from flask import Flask, request
from flask.templating import render_template
import requests

app = Flask(__name__)

api_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

@app.get('/')
@app.post('/')
def index():
    if request.method == 'POST':
        url = 'https://api.themoviedb.org/3/search/movie?api_key=api_key&query={}'
        query = request.form.get('search')
        response = requests.get(url.format(query))
        search_movie_json = response.json()
        image = requests.get('https://image.tmdb.org/t/p/w1280')
        return render_template('index.html', search_movies=search_movie_json['results'], image=image, query=query)
    elif request.method == 'GET':
        movie = requests.get('https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=api_key&page=1')
        movie_json = movie.json()
        image = requests.get('https://image.tmdb.org/t/p/w1280')
        return render_template('index.html', title='Trending', movies=movie_json['results'], image=image)
    return render_template('index.html')

@app.get("/<movie_id>/<movie_name>")
@app.post("/<movie_id>/<movie_name>")
def movie_detail(movie_id, movie_name):
    url ='https://api.themoviedb.org/3/movie/{}?api_key=api_key&language=en-US'
    response = requests.get(url.format(movie_id))
    movie_detail = response.json()
    image = requests.get('https://image.tmdb.org/t/p/w1280')
    return render_template('movie-detail.html', title=movie_name, movie=movie_detail, types=movie_detail['genres'], image=image)


app.run(debug=True)