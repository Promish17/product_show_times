from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_login import LoginManager

from main.routes import main
from extensions import db

from security import authenticate, identity

from resources.user import UserRegister
from resources.movies import Movie, MovieList, Bookings

app = Flask(__name__)

@app.before_first_request
def create_tables():
    db.create_all()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret_key_goes_here"

api = Api(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from models.user import UserModel

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return UserModel.query.get(int(user_id))

jwt = JWT(app, authenticate, identity)  # /auth

# blueprint for auth routes in our app
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
app.register_blueprint(main)

api.add_resource(UserRegister, '/register')
api.add_resource(Movie, '/movies')
api.add_resource(MovieList, '/movies')
api.add_resource(Bookings, '/booking')

db.init_app(app)
app.run(port=5000, debug=True)
