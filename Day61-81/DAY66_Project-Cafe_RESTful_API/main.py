### --- IMPORTS --- ### 

#we want our flask materials
from flask import Flask, jsonify, render_template, request
#we're getting sql alchemy for the db
from flask_sqlalchemy import SQLAlchemy
#we want to get this for getting a random line in the db
import random

### --- APP & DB SETUP --- ###

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

### --- DB CLASS --- ###

##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

### --- FUNCS --- ###

@app.route("/")
def home():
    return render_template("index.html")
    
## HTTP GET - Read Record

#get is allowed by default, so don't need to add the methods unless we want to post
@app.route("/random")
def get_random_cafe():
    # return random_cafe
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    #using dict comprehension we cut down all the typing of declaring all the info for a json
    #this code here says get the attributes for each item of the cafe in the random cafe
    json_cafe = {item: getattr(random_cafe, item) for item in Cafe.__table__.columns.keys()}
    return jsonify(cafe=json_cafe)

@app.route("/all")
def get_all_cafes():
    cafes = db.session.query(Cafe).all()
    json_all_cafe = []
    for cafe in cafes:
        json_cafe = {item: getattr(cafe, item) for item in Cafe.__table__.columns.keys()}
        json_all_cafe.append(json_cafe)
    return jsonify(cafe=json_all_cafe)

@app.route("/search")
def search_for_cafe():
    pass

# HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record

if __name__ == '__main__':
    app.run(debug=True)
