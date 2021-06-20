from app.models import Movie
from app import app, db
from flask import render_template, redirect, url_for, flash, request
import requests


@app.get("/")
@app.post("/")
def index():
    movie = 'https://api.themoviedb.org/3/search/movie?api_key=6759ed5eeb52690e2718450fa55c04f4&query={}'
    tv = 'https://api.themoviedb.org/3/search/tv?api_key=6759ed5eeb52690e2718450fa55c04f4&query={}'
    if request.method == 'POST':
        query = request.form.get('search')
        option = request.form.get('options')
        if option == 'movie':
            response = requests.get(movie.format(query))
            movie_json = response.json()
            status_code = response.status_code
            success = response.ok
            if status_code == 422:
                flash('Beep Boop! Search Is Empty')
                return redirect(url_for('index'))
            else:
                return render_template('search.html', movies=movie_json['results'])
        elif option == 'tv':
            response = requests.get(tv.format(query))
            tv_json = response.json()
            status_code = response.status_code
            success = response.ok
            if status_code == 422:
                flash('Beep Boop! Search Is Empty')
                return redirect(url_for('index'))
            else:
                return render_template('search.html',  tvs=tv_json['results'])
    return render_template('index.html', title='Home')

@app.route("/trending")
def trending():
    url = 'https://api.themoviedb.org/3/trending/all/week?api_key=6759ed5eeb52690e2718450fa55c04f4'
    response = requests.get(url)
    trending = response.json()
    return render_template('trending.html', title='Trending', trends=trending['results'], media_type=trending['results'])

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
    tv_url = 'https://api.themoviedb.org/3/tv/{}?api_key=6759ed5eeb52690e2718450fa55c04f4&language=en-US'
    similar_tv_url = 'https://api.themoviedb.org/3/tv/{}/similar?api_key=6759ed5eeb52690e2718450fa55c04f4&language=en-US&page=1'
    response = requests.get(tv_url.format(tv_id))
    tv_detail = response.json()
    similar_tv_response = requests.get(similar_tv_url.format(tv_id))
    similar_tv_detail = similar_tv_response.json()
    return render_template('tv_detail.html', title=tv_name, tv=tv_detail, types=tv_detail['genres'], similar_tv=similar_tv_detail['results'])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js'), 200, {'Content-Type': 'text/javascript'}


@app.route("/login")
def login():
    return render_template('auth/login.html')