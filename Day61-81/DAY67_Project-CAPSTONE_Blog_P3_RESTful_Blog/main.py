### --- IMPORTS --- ###

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField

from datetime import datetime

### --- APP --- ###

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

### --- DB --- ###

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

### --- CLASSES --- ###

#our blog post SQL db
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

#we're making awtf form to add new posts later
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    #we use a ckeditorfield instead of a stringfield to give the user a degree of editablity 
    #in their post body
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

### --- ROUTE FUNCS --- ###

@app.route('/')
def get_all_posts():
    """Renders all the blog posts on the homepage"""
    #we get all our blog posts
    blog_posts = db.session.query(BlogPost).all()
    #return them into the html for templating
    return render_template("index.html", all_posts=blog_posts)

@app.route("/post/<int:post_id>")
def show_post(post_id):
    """Renders the page with the relevant post in the DB"""
    #go through our posts and find the post number that matches our id
    post = BlogPost.query.filter_by(id=post_id).first()
    #if the number matches the id (error handling)
    if post.id == post_id:
        #return the template with the data fed in for populating
        return render_template("post.html", post=post)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/new_post", methods=["GET", "POST"])
def new_post():
    #we want to make a new form, this passes all our fields and the ckeditor field into the make-post page
    form = CreatePostForm()
    #we add this here and pass it through so that the heading changes based on if it's create  a post or edit a post
    heading = "<h1>New Post</h1>"
    #check and see if the form validates
    if form.validate_on_submit():
        #if so let's make our post, first get the date
        x = datetime.now()
        #then format the date into what we want it to look like, Month Name / DD / YYYY
        post_date = f"{x.strftime('%B')} {x.strftime('%d')}, {x.year}"
        #now let's make our new blog post object
        new_blog_post = BlogPost(
            title=request.form['title'],
            subtitle=request.form['subtitle'],
            author=request.form['author'],
            img_url=request.form['img_url'],
            body=request.form['body'],
            date=post_date
            )
        #then commit the post to the DB
        db.session.add(new_blog_post)
        db.session.commit()
        #return our url for get all posts (hompage)
        return redirect(url_for("get_all_posts"))
    #bring us to the make a post page
    return render_template("make-post.html", form=form, heading=heading)

@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    """Edits The Post"""
    #get our post id
    post = BlogPost.query.filter_by(id=post_id).first()
    #we add this here and pass it through so that the heading changes based on if it's create  a post or edit a post
    heading = "<h1>Edit Post</h1>"
    #we create an edit form that passes through the current db info pre populating the field
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
        )
    #if form is validated by hitting submit update the records
    if edit_form.validate_on_submit():
        #we edit the data into the post and tehn 
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data               
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    #return the template with the data fed in for populating
    return render_template("make-post.html", heading= heading, post=post, form=edit_form)

@app.route("/delete/<post_id>", methods=["GET", "POST"])
def delete_post(post_id):
    requested_post = BlogPost.query.filter_by(id=post_id).first()
        #if it gets the entry
    if requested_post:
        #delete
        db.session.delete(requested_post)
        db.session.commit()
    #we don't render the template instead we redirect so that we don't get stuck on
    #an older version of the page where the post is still displayed even though it's no 
    #no longer in the database
    return redirect(url_for('get_all_posts'))

if __name__ == "__main__":
    app.run(debug=True)

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)