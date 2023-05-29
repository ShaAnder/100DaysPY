### --- IMPORTS --- ###

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

### --- APP --- ###

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

### --- ENVS/VARS --- ###

all_books = []

### --- SQlite DB --- ###

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String)
    rating = db.Column(db.Float)

    def __init__(self, title,author, rating):
        self.title = title
        self.author = author
        self.rating = rating

with app.app_context():
    db.create_all()

### --- FUNCS --- ###

@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html', books=all_books)


@app.route('/add', methods=['GET', 'POST'])
def add():
    #we want to take a request and get the data
    if request.method == "POST":
        #then append what's in the form to the list, but we want a list of dicts
        book = Book(
            title=request.form['title'], 
            author=request.form['author'], 
            rating=request.form['rating']
            )    
        db.session.add(book)
        db.session.commit()
        print("Added Book")
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    #if our request is a post (click edit)
    if request.method == "POST":
        #get the book id
        book_id = request.form['id']
        #query the database to edit that id
        book_to_update = Book.query.get(book_id)
        #go to the rating of the book for updating
        book_to_update.rating = request.form['rating']
        #commit the update
        db.session.commit() 
    #get the books id 
    book_id = request.args.get('id')
    #query it to pass through to the edit page
    book_selected = Book.query.get(book_id)
    #return template passing through the selected book
    return render_template("edit.html", book=book_selected)

#we want to delete a record now, seeing as we use a button we're gonna need post req
@app.route('/delete/<num>', methods=["GET", "POST"])
def delete(num):
    #pass in the number of the book when we hit delete fills it in
    book_id = num
    #query that book number
    book_to_delete = Book.query.get(book_id)
    #commit the session
    db.session.delete(book_to_delete)
    db.session.commit()
    #then return home (already on home but just refreshes the page)
    return redirect(url_for('home'))

### --- MAIN --- ###

if __name__ == '__main__':
    app.run(debug=True)

