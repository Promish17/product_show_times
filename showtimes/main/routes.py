import datetime
from flask import Blueprint, render_template, request
from resources.choices import theater_choices, movie_timings, movie_centers, city_choices
from resources.movies import Movie

from models.movies import MovieModel, BookingModel
from models.user import UserModel
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    movie = Movie()
    movies = movie.get()
    if not movies:
        movie.post()

    movie_list = movie.get()
    return render_template('index.html', movies=movie_list)

@main.route('/view')
@login_required
def profile():
    movies = BookingModel.query.filter(BookingModel.username==current_user.username)
    return render_template('view.html', movies=movies)

@main.route('/add')
def add():

    context = {
        'movie_name' : [movie.json()['name'] for movie in MovieModel.query.all()],
        'theater_choices' : theater_choices,
        'movie_timings' : movie_timings,
        'movie_centers' : movie_centers,
        'city_choices' : city_choices,
    }

    return render_template('add.html', **context)

@main.route('/add', methods=['GET', 'POST'])
def add_post():
    username = current_user.username
    movie_name = request.form.get('movie_name')
    theater_choices = request.form.get('theater_choices')
    movie_timings = request.form.get('movie_timings')
    movie_centers = request.form.get('movie_centers')
    city_choices = request.form.get('city_choices')
    booking_time = datetime.datetime.now()

    booking = BookingModel(username=username, movie_name=movie_name, theater_choices=theater_choices,
                        movie_timings=movie_timings, movie_centers=movie_centers,
                        city_choices=city_choices, booking_time=booking_time)

    booking.save_to_db()

    return render_template('response.html')

@main.route('/view')
def view():
    movies = BookingModel.query.all()
    return render_template('view.html', movies=movies)