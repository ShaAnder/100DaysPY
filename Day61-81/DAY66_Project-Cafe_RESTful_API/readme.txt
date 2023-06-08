### --- PROJECT NAME / DESC --- ###

RESTful API SQL Cafe DB - A small database that uses api calls to view edit add and delete cafe's from a database

### --- PARAMETERS --- ###

Program must be able to access an sql database of cafes
Must be able to route based on various api calls:
    - random
    - search
    - all
    - add
    - edit
    - delete

must be able to manipulate the database in these ways 

### --- HOW IT WORKS --- ###

Using flask and it's in built tools we create a small flask app that when an API call is made routes the user to 
the information based on the call
We largely do this with the use of the flask request import that allows us to take the information we type into postman / the url bar
and feeds that back into the function
Once we have that information we can manipulate it in a variety of ways from finding the corresponding information in the db, to adding new
information or even deleting

```
@app.route("/random")
def get_random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    return jsonify(cafe=random_cafe.to_dict())
```

In this example we get query the list of cafes and using a random route trigger it to search for a random cafe from the list
we then use our in built function to_dict to turn each piece of information into a key:value pair for passing to the jsonify function


```
@app.route("/add", methods=["POST"])
def add_a_cafe():
    new_cafe = Cafe(
        name = request.args.get("name"),
        map_url=request.args.get("map_url"),
        img_url=request.args.get("img_url"),
        location=request.args.get("location"),
        seats=request.args.get("seats"),
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
```

This one utilizes postman the api testing software to send a query to our url with all the parameters filled in
we then use request.args.get to get the information we want and then create a new object for passing into the database

we then also have responses to give the user feedback 


### --- TO DO / FUTURE PLANS --- ###

All in all this was a fun project and a very valuable dive into API calling and RESTful apis, this is something i'll be using when 
going to build the professional website portfolio project.