import requests
from flask import Flask, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top-10-movies-website.db"
db.init_app(app)

MOVIE_URL = "https://api.themoviedb.org/3/search/movie"

MOVIE_DB_API_KEY = "2fc57cb38859b5b026fd021e80d2073e"

class Movie(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String, unique=True)
  year = db.Column(db.String)
  description = db.Column(db.String)
  rating = db.Column(db.Integer)
  ranking = db.Column(db.Integer)
  review = db.Column(db.String)
  img_url = db.Column(db.String)


with app.app_context():
  db.create_all()

new_movie = Movie(
    title="Phone Booth",
    year=2002,
    description=
    "Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
    rating=7.3,
    ranking=10,
    review="My favourite character was the caller.",
    img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg")
second_movie = Movie(
    title="Avatar The Way of Water",
    year=2022,
    description=
    "Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
    rating=7.3,
    ranking=9,
    review="I liked the water.",
    img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg")

# with app.app_context():
#   db.session.add(second_movie)
#   db.session.commit()


class MovieForm(FlaskForm):
  rating = StringField('Your Rating', validators=[DataRequired()])
  review = StringField("Your Review")
  submit = SubmitField('Done')


class AddMovieForm(FlaskForm):
  title = StringField('Movie Title', validators=[DataRequired()])
  submit = SubmitField('Add Movie')


@app.route("/")
def home():
  result = db.session.execute(db.select(Movie))
  all_movies = result.scalars()
  return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def edit():
  form = MovieForm()
  movie_id = request.args.get('id')
  movie = db.get_or_404(Movie, movie_id)
  if form.validate_on_submit():
    movie.rating = float(form.rating.data)
    movie.review = form.review.data
    db.session.commit()
    return redirect(url_for('home'))
  return render_template("edit.html", movie=movie, form=form)


@app.route("/delete")
def delete():
  movie_id = request.args.get('id')
  movie = db.get_or_404(Movie, movie_id)
  db.session.delete(movie)
  db.session.commit()
  return redirect(url_for('home'))


@app.route("/add", methods=["GET", "POST"])
def add():
  form = AddMovieForm()
  if form.validate_on_submit():
    movie_to_find = form.title.data
    response = requests.get(MOVIE_URL,
                            params={"api_key": MOVIE_DB_API_KEY,
                                    "query": movie_to_find}
                           )
    data = response.json()['results']
    return render_template('select.html', options=data)
  return render_template("add.html", form=form)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
