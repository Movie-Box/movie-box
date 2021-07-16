from app import app, db, mail
from flask import render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from app import email
from app.forms import LoginForm, RegisterForm, EmptyForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User, Bookmark, OAuth
import requests
from werkzeug.urls import url_parse
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer import oauth_authorized
from sqlalchemy.orm.exc import NoResultFound
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from app.email import send_password_reset_email, email_verification
from app.utils import is_admin



google_bp = make_google_blueprint(scope=["profile", "email"], client_id='463516744667-5jqhnjdue26u4k99q44nbtr7dh5gbnc8.apps.googleusercontent.com', client_secret='eesXntMy1cL0VYBoSGKzsPVw')
app.register_blueprint(google_bp,  url_prefix="/google_login")

google_bp.storage = SQLAlchemyStorage(OAuth, db.session)

@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.cli.command('refresh')
def refresh():
    db.drop_all()
    db.create_all()
    u1 = User(username='Sameer Joshi', email='sameerjoshicr7@gmail.com', password_hash='pbkdf2:sha256:260000$a4ZBNBsuCBJtsKr7$853636ac11c4a2261eee9ed43a28382ad01952cff8411961a4d1e795908ff66f', admin=True, email_confirmed=True )
    db.session.add(u1)
    db.session.commit()
    print('Data Added')

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


# Start Auth

@app.get("/login")
@app.post("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Email or password')
            return redirect(url_for('login'))
        if user.email_confirmed == False:
            flash('Please Confirm Your Email To Continue')
            return redirect(request.referrer)
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Login into your account', form=form)

@app.get('/reset_password_request')
@app.post('/reset_password_request')
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)

@app.get('/reset_password/<token>')
@app.post('/reset_password/<token>')
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_password_reset_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('auth/reset_password.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# 3rd party Login
@google_bp.route("/google")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    account_info = google.get("/oauth2/v1/userinfo")
    account = account_info.json()
    return redirect(url_for('index'))

@oauth_authorized.connect_via(google_bp)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with Google.")
        return False
    
    account_info = blueprint.session.get('/oauth2/v3/userinfo')
    if not account_info.ok:
        msg = "Failed to fetch user info from Google."
        flash(msg, category="error")
        return redirect(url_for('login'))
    google_info = account_info.json()
    
    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=blueprint.name
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider=blueprint.name,
            token=token,
        )
    if oauth.user:
        login_user(oauth.user)
        flash("🔥Successfully signed in with Google.🔥")
    
    else:
        user = User(
            # Remember that `email` can be None, if the user declines
            # to publish their email address on GitHub!
            email=google_info["email"],
            # picture=google_info["picture"],
            username=google_info["given_name"]
        )
        user_email = User.query.filter_by(email=email)
        if user_email:
            flash('Do you Want to Crash The Server? The Email Already Exist!')
            return redirect(request.referrer)
        oauth.user = user
        db.session.add_all([user, oauth])
        db.session.commit()
        login_user(user)
        flash("Successfully signed in with Google.")
    return False

# End 3rd Party

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
        email_verification(user)
        flash('Please check your inbox to confirm your email address 📨')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Sign up for a new account', form=form)


@app.get('/confirm_email/<token>')
@app.post('/confirm_email/<token>')
def confirm_email(token):
    user = User.verify_email_token(token)
    if user.email_confirmed:
        flash('Account already confirmed. Please login.')
    else:
        user.email_confirmed = True
        db.session.add(user)
        db.session.commit()
        flash('Email Confirmed')
    return redirect(url_for('index'))

# End Auth


@app.post('/bookmark/<media_id>/<media_type>/<media_name>/<user_id>')
@login_required
def bookmark(media_id, media_type, media_name, user_id):
    form = EmptyForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            media_id = Bookmark.query.filter_by(media_id=media_id).first()
            if media_id is None:
                bookmark = Bookmark(media_id=media_id, media_type=media_type, title=media_name, user_id=user_id)
                db.session.add(bookmark)
                db.session.commit()
                flash('Bookmark Added')
                return redirect(url_for('user_bookmarks'))
            else:
                flash('Already Bookmarked')
                return redirect(request.referrer)
        else:
            flash('Login To Bookmark')
            return redirect(url_for('login'))
        
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

# Admin
@app.route("/setting")
@login_required
@is_admin
def setting():
    users = User.query.all()
    return render_template('admin/settings.html', title='Settings', users=users)

@app.route("/account/<username>")
@login_required
@is_admin
def account(username):
    account_info = User.query.filter_by(username=username)
    return render_template('user/account.html', title=current_user.username, user=account_info)

# End Admin

# Errors
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
# End Errors

