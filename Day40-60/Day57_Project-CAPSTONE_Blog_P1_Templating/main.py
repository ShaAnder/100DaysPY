### --- IMPORTS --- ###

from flask import Flask, render_template
from datetime import datetime
import requests

#### --- APP SETUP --- ###

app = Flask(__name__)

### --- BLOG REQUEST --- ###

blog_url = "https://api.npoint.io/c4a2e2ea0b2b2cfed61f"
response = requests.get(blog_url)
all_posts = response.json()

### --- FUNCS --- ###

@app.route('/')
def get_blog():
    return render_template("index.html", posts = all_posts)

@app.route('/post/<int:id_num>')
def get_blog_post(id_num):
    return render_template("post.html", blogs=all_posts, ID=id_num)

### --- MAIN --- ###

if __name__ == "__main__":
    app.run(debug=True)