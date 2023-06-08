### --- IMPORTS --- ### 

#we want our flask materials
from flask import Flask, jsonify, render_template, request
#we're getting sql alchemy for the db
from flask_sqlalchemy import SQLAlchemy
#we want to get this for getting a random line in the db
import random

### --- VARS --- ###

API_KEY = "TopSecretAPIKey"


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

    def to_dict(self):
        """Returns the elements of the object as key value pairs"""
    # use dictionary comprehension, Key(column name): Value(attribute in the column name) for the column in the table
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
        #we use this for later as some of our data comes back as a list of objects and we want to convert that into a dict
        #tldr this method goes through the list object, extracts the info converts it into a key value pair and saves it into a dict

### --- FUNCS --- ###

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/random")
def get_random_cafe():
    """Gets A Random Cafe"""
    #Get our data
    cafes = db.session.query(Cafe).all()
    #Get a random cafe
    random_cafe = random.choice(cafes)
    #return the cafe as a dict
    return jsonify(cafe=random_cafe.to_dict())

@app.route("/all")
def get_all_cafes():
    """Gets All The Cafe's In The DB"""
    #we query all the cafes
    cafes = db.session.query(Cafe).all()
    #then using our to_dict method, as well as list comprehension, convert the returned data into
    #a dict and then append it to a list
    return jsonify(cafes= [cafe.to_dict() for cafe in cafes])

@app.route("/search")
def search_for_cafe():
    """Allows You To Search For A Cafe"""
    #we want to request the location arg for our cafes
    location = request.args.get("location").title()
    #we query the cafe DB and filter by all the locations
    requested_cafes = Cafe.query.filter_by(location=location).all()
    #if there are cafes in the list
    if requested_cafes:
        #and here we put our to dict method into action. We convert each entry in the cafe to a dict using
        #the method and do this for all the cafes, then return them as a json'd dict appended to the cafes list
        return jsonify(cafes = [cafe.to_dict() for cafe in requested_cafes])
    return jsonify(error={"Sorry there are no cafes in that location"})

@app.route("/add", methods=["POST"])
def add_a_cafe():
    """Adds A New Cafe"""
    #we're adding a new cafe, we take the request args from the POST request from postman
    #then we feed them into the new Cafe Object
    new_cafe = Cafe(
        name = request.args.get("name"),
        map_url=request.args.get("map_url"),
        img_url=request.args.get("img_url"),
        location=request.args.get("location"),
        seats=request.args.get("seats"),
        #these 4 are booleans so we want a true false statement
        has_toilet=bool(request.args.get("toilet")),
        has_wifi=bool(request.args.get("wifi")),
        has_sockets=bool(request.args.get("sockets")),
        can_take_calls=bool(request.args.get("calls")),
        coffee_price=request.args.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    if new_cafe:
        return jsonify(response = {"success": "Successfully added new cafe"})
    return jsonify(response = {"failure": "New cafe could note be added"})

#we want to update coffee prices with a patch request
@app.route("/update-price/<cafe_id>", methods = ["GET","POST","PATCH"])
def update(cafe_id):
    """Updates The Cafe Listing"""
    #get our cafe, we filter by the id, the user will get this via the get request (we can also change it to name later)
    requested_cafe = Cafe.query.filter_by(id=cafe_id).first()
    #setup a conditional to make sure we don't try and add to a non existent cafe
    if requested_cafe is not None:
        #get the new price request from postman
        new_price = request.args.get("new_price")
        #then change the price
        requested_cafe.coffee_price = f"£{new_price}"
        #commit the session
        db.session.commit()
        #return info
        return jsonify(response={"success": "Successfully updated the price."}), 200
    return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404

#we want to delete records of closed cafes will be using the test cafe i made in step 6
@app.route("/report-closed/<cafe_id>", methods = ["GET","DELETE"])
def delete_cafe(cafe_id):
    """Deletes a closed cafe"""
    api = request.args.get("api-key")
    #we have this for testing (this is to test and ensure that if the api key IS present code works)
    #we do this because the request is coming from postman and not our browser and will always fail if we try 
    #refresh our code and not send from the postman app
    # api = "TopSecretAPIKey"
    if api == "TopSecretAPIKey":
        #get the first entry with our id
        requested_cafe = Cafe.query.filter_by(id=cafe_id).first()
        #if it gets the entry
        if requested_cafe:
            #delete
            db.session.delete(requested_cafe)
            db.session.commit()
    #-------------- if / else response handling --------- #
            return jsonify(response={"success": "Successfully removed the cafe from the database."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found."}), 404
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure your api_key is correct."}), 403


if __name__ == '__main__':
    app.run(debug=True)
