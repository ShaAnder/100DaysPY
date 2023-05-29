### --- IMPORTS --- ###

#flask stuff
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
#forms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired

#requests and envs
import requests
import os
from dotenv import load_dotenv

### --- ENV AND VAR --- ###

#we're going to make requests, so get our envs here
load_dotenv()
api_key = os.getenv('API')
api_read_token = os.getenv('READ')

### --- APP --- ###

#make our db
db = SQLAlchemy()
app = Flask(__name__)
#we set it to make a movies collection under specified name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///top-10-movies-collection.db'
#to deal with track errors
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#key for crsf validation
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
#initiate app and our bootstrap 5 
Bootstrap(app)
db.init_app(app)

### --- SQL CLASS --- ###

#we want to make a class for our db, with everything we're going to need 
#header wise, this is to get the information abck later in our code
class MovieList(db.Model):   
    id= db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String, unique=True, nullable=False)
    year= db.Column(db.Integer)
    description= db.Column(db.String)
    rating= db.Column(db.Float)
    ranking= db.Column(db.Integer)
    review= db.Column(db.String)
    img_url= db.Column(db.String)

#build our db
with app.app_context():
    db.create_all()

### --- FORM CLASS --- ###

#we need a flask form to accept edits, so we build it here
class RateMovieForm(FlaskForm):   
    rating = FloatField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your Review")
    submit = SubmitField(label = 'Submit')

#another flask form this time for accepting an add movie suggestion
class AddMovie(FlaskForm):   
    add_movie = StringField("Type A Movie Here")
    submit = SubmitField(label = 'Submit')

### --- FUNCS --- ###

#route us to home and feed in whatever is in the db, to populate the movie cards
@app.route('/')
def home():
    #for the final part of the project we want to sort our movies by ranking, using order_by
    all_movies = MovieList.query.order_by(MovieList.rating).all()

    #we're also going to loop through the list and rank them from bottom to top
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    #also commit it to the db so it won't need to be loaded every time
    db.session.commit()
    #bring us to index with our movies
    return render_template('index.html', movies=all_movies)

#now we make an edit page to ensure we can edit our ratings and reviews as needed
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    #make a new form
    form = RateMovieForm()
    #get the movie id, so that the edit button knows to take us to the correct movie
    movie_id = int(request.args.get("id"))
    print(movie_id)
    #query it to pass through to the edit page
    movie_selected = MovieList.query.get(movie_id)
    #if our form validates on click
    if form.validate_on_submit() and movie_selected:
        #get our form and review rating and put them in the db
        movie_selected.rating = float(form.rating.data)
        movie_selected.review = form.review.data
        db.session.commit()
        #load home
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie_selected, form=form)

@app.route('/add', methods=["GET", "POST"])
def add():
    #make our form
    name_form = AddMovie()
    
    if name_form.validate_on_submit():
        #get our movie data back
        name_of_movie = name_form.add_movie.data
        print(name_of_movie)
        #make our request
        url = "https://api.themoviedb.org/3/search/movie?include_adult=true&language=en-US&page=1"
        #send out our data
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_read_token}"
                }
        params = {
            "api_key": api_key,
            "query": {name_of_movie},
                }
        #we want to get our request data and parse it, in the html file we will 
        #get the specific data we're after
        response = requests.get(url, headers=headers, params=params)
        movie_data = response.json()['results']
        #load the select html with all the movie data on it
        return render_template("select.html", movies=movie_data)

    return render_template('add.html', form=name_form)

@app.route('/select')
def select():
    #now we need to be able to select the movie and get details 
    #firstly we get the id of the movie, based on the list we grabbed
    movie_id=request.args.get('id')
    #if we get an id send this in another request to the movie db
    if movie_id:
        movie_url=f'https://api.themoviedb.org/3/movie/{movie_id}'
        #this time the data we are getting back is the EXACT movie we want
        response =requests.get(movie_url, params={'api_key':api_key})
        data= response .json()
        #create a new movie entry
        new_movie= MovieList(
            #get the stuff we want for it from our movie response
            title= data['title'],
            #split the string to remove dashes
            year= data['release_date'].split('-')[0],
            description= data['overview'],
            #we want to get the poster image so we add the data for the movie into a movie poster path
            img_url= f'https://image.tmdb.org/t/p/w500/{data["poster_path"]}'
        )
        #add movie to the list
        db.session.add(new_movie)
        db.session.commit()
        #go back to edit so we can add a rating and review
        return redirect(url_for('edit',id=new_movie.id))

@app.route('/delete/<int:num>', methods=["GET", "POST"])
def delete(num):
    #unlike edit we get the movie id to delete from the url 
    #hotbar, we then pass it through like normal for deletion
    movie_id = num
    #query that movie number
    movie_to_delete = MovieList.query.get(movie_id)
    #commit the session
    db.session.delete(movie_to_delete)
    db.session.commit()
    #then return home (already on home but just refreshes the page)
    return redirect(url_for('home'))

# ### --- MAIN --- ###

if __name__ == '__main__':
    app.run(debug=True)
