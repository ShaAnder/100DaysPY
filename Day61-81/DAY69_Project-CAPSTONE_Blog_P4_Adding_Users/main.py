### --- UPLOADS --- ### 

from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from flask_gravatar import Gravatar

from functools import wraps

import random

### --- APP --- ###

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

### --- DB --- ###

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    #--- DB RELATIONSHIPS --- #

    #creating  relational databases for the blogpost and comment tables
    #this line here creates effectively a new column in the tables for the relevant vars
    posts = db.relationship("BlogPost", back_populates="author")
    comments = db.relationship("Comment", back_populates="comment_author")

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    #Creating a foreignkey, we point that foreign key to the tablename of User
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #Create a reference to the user object, it back populates the posts property in user class
    author = db.relationship("User", back_populates="posts")
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    #--- Parent Relationship ---#

    comments = relationship("Comment", back_populates="parent_post")

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    #Creating a foreignkey, we point that foreign key to the tablename of User
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #Create a reference to the user object, it back populates the comments property in user class
    comment_author = db.relationship("User", back_populates="comments")
    
    #--- Child Relationship ---#

    #were creating child relationships for the post id, post
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")
    #not a child relationship just for table neatness putting this last
    text = db.Column(db.Text, nullable=False)

#use this once to make db, the comment out, if db needs to be made again delete instance and reuse
with app.app_context():
    db.create_all()

### --- LOGIN --- ### 

#we want to create the login manager to handle login stuff
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    with app.app_context():
        return db.session.get(entity=User, ident=user_id)
    
### --- GRAVITAR --- ### 

#
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)
    
### --- DECORATORS --- ### 

#we create an admin only decorator
#will check if current user is 1 if not won't allow func execution
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

### --- ROUTES --- ###

@app.route('/')
#get all the posts
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)

@app.route('/register', methods=["GET", "POST"])
def register():
    #we want a registration form
    form = RegisterForm()
    #we want to make a post request
    if request.method == "POST":    
        #create a user database
        user = User()
        #get our credentials here, we add the name and email straight to the object but not pw
        user.email = request.form.get('email')
        user.name = request.form.get('name')
        password = request.form.get('password')

        #now we check if the user is already registered, by querying the email
        if User.query.filter_by(email=user.email).first():
            #if already exists flash messages
            #we use a flash messages html file extended into other html to do this
            flash(f"Email {user.email} already exists! Log in instead.")
            #take us to login
            return redirect(url_for('login'))
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
        return redirect(url_for('get_all_posts'))
    return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Logs The User In """
    form = LoginForm()
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        find_user = User.query.filter_by(email=email).first()
        if find_user.email == email:
            #check password
            if check_password_hash(pwhash=find_user.password, password=password):
                login_user(find_user)
                return redirect(url_for('get_all_posts'))
            else:
                #incorrect login try again
                flash(f"Password is incorrect!")
                return render_template("login.html")
        else:
            flash(f"Email Incorrect Or Not Found")
            return render_template("login.html")   
    return render_template("login.html", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))

@app.route("/post/<int:post_id>", methods = ["GET", "POST"])
def show_post(post_id):
    comment_form = CommentForm()
    requested_post = BlogPost.query.get(post_id)

    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))
        
        new_comment = Comment(
            text = comment_form.comment.data,
            comment_author = current_user,
            parent_post = requested_post,
            )
        db.session.add(new_comment)
        db.session.commit()

    return render_template("post.html", post=requested_post, form=comment_form, current_user=current_user)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")

@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)

@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)

@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

if __name__ == "__main__":
    app.run(debug=True)

