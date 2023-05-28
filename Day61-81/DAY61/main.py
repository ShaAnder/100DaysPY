### --- IMPORTS --- ###

#flask and wtform imports
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap5

### --- CLASS --- ###

#we want to create a form class
class LoginForm(FlaskForm):
    email = StringField("Email", [Length(min=4, max=40), Email()])
    password = PasswordField("Password", [Length(min=8, max=40)])
    submit = SubmitField(label="Log In")

### --- APP --- ###
app = Flask(__name__)
#we want to make an app key to cross reference vs wtf forms secret 
#this will stop people being able to hijack an app
app.secret_key = "ThisIsASecret"
bootstrap = Bootstrap5(app)

### --- ENV/VAR --- ###

admin_email = "admin@gmail.com"
admin_password = "12345678"

### --- FUNCS --- ###

@app.route('/')
def home():
    return render_template('index.html')

#we create our login function we want get and post to get and post our data
@app.route('/login', methods=['GET', 'POST'])
def login():
    #create login form
    login_form = LoginForm()
    #we validate the login and if valid get details
    if login_form.validate_on_submit():
        if login_form.email.data == admin_email and login_form.password.data == admin_password:
            return render_template('success.html')
        else:
            return render_template('denied.html')
    #return the template with the form on it
    return render_template('login.html', form = login_form)

if __name__ == '__main__':
    app.run(debug=True)

