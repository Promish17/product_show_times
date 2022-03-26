from flask_login import UserMixin
from extensions import db

# creating User object
class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    booking = db.relationship("BookingModel", lazy='dynamic')

    def json(self):
        return {'username': self.username, 'booking': [booking.json() for booking in self.user_booking.all()]}

