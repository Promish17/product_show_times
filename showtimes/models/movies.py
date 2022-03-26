import json
import datetime
from sqlalchemy import ForeignKey
from extensions import db
from models.user import UserModel

from flask_login import current_user

class MovieModel(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class BookingModel(db.Model):
    __tablename__ = 'bookings'

    # structure of booking table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey('users.username'))
    movie_name = db.Column(db.String(50), nullable=False)
    theater_choices = db.Column(db.String(50), nullable=False)
    movie_timings = db.Column(db.String(50), nullable=False)
    movie_centers = db.Column(db.String(50), nullable=False)
    city_choices = db.Column(db.String(50), nullable=False)
    booking_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    user = db.relationship('UserModel')

    def __init__(self, username, movie_name, theater_choices, movie_timings, 
                    movie_centers, city_choices, booking_time):
        self.username = username
        self.movie_name = movie_name
        self.theater_choices = theater_choices
        self.movie_timings = movie_timings
        self.movie_centers = movie_centers
        self.city_choices = city_choices
        self.booking_time = booking_time

    def json(self):
        data = {'username': current_user.username, 'movie_name': self.movie_name,
                    'theater_choices': self.theater_choices, 'movie_timings': self.movie_timings,
                    'movie_centers': self.movie_centers, 'city_choices': self.city_choices,
                    'booking_time': self.booking_time}
        def myconverter(book_t):
            if isinstance(book_t, datetime.datetime):
                return book_t.__str__()
        return json.dumps(data, default = myconverter)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()