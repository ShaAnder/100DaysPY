### --- IMPORTS --- ###

#for our server
from flask import Flask, render_template, request

#for getting blog posts
import requests

#for sending email
import sys
sys.path.append("G:/100DaysPY/toolkit")
from email_sender import SendMail

#finally this for getting our envs
from dotenv import load_dotenv
import os

#### --- APP SETUP --- ###

app = Flask(__name__)

### --- ENVS / VARS --- ###

#loadsenvs
load_dotenv()
#we want this for our email sending later, always gmail as that's receiving email
SMTP = "smtp.gmail.com"
email_to = os.getenv('EMAIL_T')
passw = os.getenv("PW")

### --- BLOG REQUEST --- ###

#we want our blog info 
blog_url = "https://api.npoint.io/c4a2e2ea0b2b2cfed61f"
response = requests.get(blog_url)
all_posts = response.json()

### --- FUNCS --- ###

#we create two routes here that do the same thing, one for loading flask and the other for 
#if the user decides to click the home button
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', posts = all_posts)

#route for our about 
@app.route('/about')
def about():
    return render_template('about.html')

#route for our blog posts
@app.route('/post/<int:id_num>')
def get_blog_post(id_num):
    return render_template("post.html", blogs=all_posts, ID=id_num)

#we want to get the information from the form and email it to the 
#user IF it's a post request if not it will default to contact.html
@app.route('/contact', methods =["GET", "POST"])
def contact():
    if request.method == "POST":
        """Takes the information from the contact page, prints it and returns a message sent function"""
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        message = request.form['message']
        #if len of any of these are 0 (we don't want people to spam )
        if name and email and phone and subject and message != "":
            #we initialize email sender class
            mail_send = SendMail(SMTP, email, passw, email_to, message, subject)
        else:
            return render_template("contact.html", heading = "Message Not Sent! Please Check Fields")
        return render_template("contact.html", heading = "Your Message Has Been Sent Successfully!")
    return render_template("contact.html", heading = "Contact Me!")

### --- MAIN --- ###

if __name__ == "__main__":
    app.run(debug=True)