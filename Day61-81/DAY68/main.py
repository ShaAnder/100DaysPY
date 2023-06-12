### --- IMPORTS --- ###

from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

import random

### --- APP SETUP --- ###

app = Flask(__name__)

app.config['SECRET_KEY'] = 'AYOISTHISA...SECRETKEY?'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#we want to configure a folder here to grab files
app.config["FILES"] = "/files"

### --- DB --- ###

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
#Line below only required once, when creating DB. 
# db.create_all()

### --- LOGIN MANAGER --- ### 

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with app.app_context():
        return db.session.get(entity=User, ident=user_id)

### --- ROUTES --- ###

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    
    if request.method == "POST":

        #we create a new user object here
        user = User()
        #get our credentials here, we add the name and email straight to the object but not pw
        user.email = request.form.get('email')
        user.name = request.form.get('name')
        password = request.form.get('password')

        #now we check if the user is already registered, by querying the email
        if User.query.filter_by(email=user.email).first():
            #if already exists flash messages
            #we use a flash messages html file extended into other html to do this
            flash(f"User {user.email} already exists!")
            flash("Log in instead.")
            #take us to login
            return render_template("login.html")
        
        #if not duplicate well first go and salt the password
        user.password = generate_password_hash(
            password, 
            method="pbkdf2:sha256", 
            #random integer so not the same for every pw
            salt_length=random.randint(16,32)
            )
        
        #add the user
        db.session.add(user)
        db.session.commit()
        
        #login the user
        login_user(user)
        #flash login message
        flash('Logged in successfully.')
        #redirect to secret stuff
        return redirect(url_for('secrets', username=user.name))
    return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        print(email, password)

        find_user = User.query.filter_by(email=email).first()
        print(find_user.email)
        if find_user.email == email:
            #check password
            if check_password_hash(pwhash=find_user.password, password=password):
                login_user(find_user)
                print(find_user.name)
                return redirect(url_for('secrets', username=find_user.name))
            else:
                #incorrect login try again
                flash(f"Password is incorrect!")
                return render_template("login.html")
        else:
            flash(f"Email Incorrect Or Not Found")
            return render_template("login.html")   
    return render_template("login.html")

@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    """Opens The File for downloading"""
    try:
        #try to find the file, it's in static, and we use path not filename
        return send_from_directory('static', path="files/cheat_sheet.pdf", as_attachment=True)
    except FileNotFoundError:
        #if no file abort code throw 404
        abort(404)


if __name__ == "__main__":
    app.run(debug=True)
