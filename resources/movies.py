from flask_restful import Resource

from models.movies import BookingModel, MovieModel

class Movie(Resource):

    def get(self):
        return MovieModel.query.all()

    def post(self):

        import imdb
        ia = imdb.IMDb()
        top_movies = ia.get_top250_movies()

        try:
            for i in range(25):
                movie = top_movies[i]['title']
                print(movie)
                item = MovieModel(movie)
                item.save_to_db()
        except:
            return {"message" : "An error occurred while inserting item."}, 500

        return item.json(), 201


class MovieList(Resource):
    def get(self):
        return {'movies': [movie.json() for movie in MovieModel.query.all()]}

class Bookings(Resource):
    def get(self):
        return {'bookings': [booking.json() for booking in BookingModel.query.all()]}