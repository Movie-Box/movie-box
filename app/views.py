from app import app, db
from flask import render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegisterForm, EmptyForm
from app.models import User, Bookmark
import requests
from werkzeug.urls import url_parse


@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.cli.command('refresh')
def refresh():
    db.drop_all()
    db.create_all()
    u1 = User(username='sameer', email='sameer@sameer.com', password_hash='pbkdf2:sha256:260000$uIx3mtrVJqZ5mU23$172a5ef2813b592e4c78addfda6ddd13738850c825c8d5c6ebdabf390fd3a290', admin=True )
    u2 = User(username='Test@123', email='test@test.com', password_hash='pbkdf2:sha256:260000$VxQC6VwnTWuP95VG$acb886564f48b687303010c74ea7ca9800b6e529df41b9653ee5a4822df4cde4' )
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()
    print('Refresh Sucessful')


@app.get("/")
@app.post("/")
def index():
    movie = 'https://api.themoviedb.org/3/search/movie?api_key=6759ed5eeb52690e2718450fa55c04f4&query={}'
    tv = 'https://api.themoviedb.org/3/search/tv?api_key=6759ed5eeb52690e2718450fa55c04f4&query={}'
    form = EmptyForm()
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
                return render_template('search.html', movies=movie_json['results'], form=form)
        elif option == 'tv':
            response = requests.get(tv.format(query))
            tv_json = response.json()
            status_code = response.status_code
            success = response.ok
            if status_code == 422:
                flash('Beep Boop! Search Is Empty')
                return redirect(url_for('index'))
            else:
                return render_template('search.html',  tvs=tv_json['results'], form=form)
    return render_template('index.html', title='Home')

@app.get("/trending")
@app.post("/trending")
def trending():
    form = EmptyForm()
    url = 'https://api.themoviedb.org/3/trending/all/week?api_key=6759ed5eeb52690e2718450fa55c04f4'
    response = requests.get(url)
    trending = response.json()
    return render_template('trending.html', title='Browse Trending Movies and Tv Shows', trends=trending['results'], media_type=trending['results'], form=form)

@app.get('/movie')
@app.post('/movie')
def popular_movie():
    form = EmptyForm()
    url = 'https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=6759ed5eeb52690e2718450fa55c04f4&page=1'
    response = requests.get(url)
    movie_json = response.json()
    return render_template('popular_movie.html', title='Browse Popular Movies', movies=movie_json['results'], form=form)

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

@app.get('/tv')
@app.post('/tv')
def popular_tv():
    form = EmptyForm()
    url = 'https://api.themoviedb.org/3/tv/popular?api_key=6759ed5eeb52690e2718450fa55c04f4&language=en-US&page=1'
    response = requests.get(url)
    popular_tv = response.json()
    return render_template('popular_tv.html', title='Browse Popular TV Shows', tvs=popular_tv['results'], form=form)

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
    return render_template('about.html', title='About')

@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js'), 200, {'Content-Type': 'text/javascript'}


@app.get("/login")
@app.post("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Email or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Login into your account', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# 3rd party Login



@app.get("/register")
@app.post("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered user!')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Sign up for a new account', form=form)

@app.get('/bookmark/<media_id>/<media_type>/<media_name>/<user_id>')
@app.post('/bookmark/<media_id>/<media_type>/<media_name>/<user_id>')
@login_required
def bookmark(media_id, media_type, media_name, user_id):
    form = EmptyForm()
    if form.validate_on_submit():
        media_id = Bookmark.query.filter_by(media_id=media_id).first()
        if media_id is None:
            bookmark = Bookmark(media_id=media_id, media_type=media_type, title=media_name, user_id=user_id)
            db.session.add(bookmark)
            db.session.commit()
            flash('Bookmark Added')
            return redirect(url_for('user_bookmarks'))
        else:
            flash('Already Bookmarked')
            return redirect(url_for('user_bookmarks'))
        
@app.post('/remove/<id>')
@login_required
def remove(id):
    bookmark = Bookmark.query.get_or_404(id)
    db.session.delete(bookmark)
    db.session.commit()
    flash('Bookmark Removed')
    return redirect(request.referrer)
        

@app.get("/my_bookmarks")
@app.post("/my_bookmarks")
@login_required
def user_bookmarks():
    form = EmptyForm()
    bookmarks = Bookmark.query.filter_by(user=current_user).order_by(Bookmark.timestamp.desc())
    return render_template('user/user_bookmarks.html', title='My Bookamrks', bookmarks=bookmarks, form=form)
