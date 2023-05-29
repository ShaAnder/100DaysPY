### --- IMPORTS --- ###

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, URL
import csv

### --- APP --- ###

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

### --- FORM CLASS --- ###

class CafeForm(FlaskForm):
    
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField('Location', validators=[DataRequired(), URL()])
    open_time = StringField('Opening Time', validators=[DataRequired()])
    close_time = StringField('Closing Time', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating 0-5', validators=[DataRequired()], 
        choices=[("✘", "✘"), ("☕", "☕"), ("☕☕", "☕☕"), ("☕☕☕", "☕☕☕"), ("☕☕☕☕", "☕☕☕☕"),("☕☕☕☕☕", "☕☕☕☕☕")])
    wifi_rating = SelectField('Wifi Rating 0-5', validators=[DataRequired()], 
        choices=[("✘", "✘"), ("💪", "💪"), ("💪💪", "💪💪"), ("💪💪💪", "💪💪💪"), ("💪💪💪💪", "💪💪💪💪"),("💪💪💪💪", "💪💪💪💪💪")])
    power_rating = SelectField('Power Rating 0-5', validators=[DataRequired()], 
        choices=[("✘", "✘"), ("🔌", "🔌"), ("🔌🔌", "🔌🔌"), ("🔌🔌🔌", "🔌🔌🔌"), ("🔌🔌🔌🔌", "🔌🔌🔌🔌"),("🔌🔌🔌🔌🔌", "🔌🔌🔌🔌🔌")])
    
    submit = SubmitField('Submit')


### --- FUNCS --- ###

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        new_data = form.data
        new_row = [value for (key,value) in new_data.items() if not key in ['submit','csrf_token']]
        with open('cafe-data.csv',mode='a', newline='', encoding="utf8") as csv_file:
            wr = csv.writer(csv_file)
            wr.writerow(new_row)
    return render_template('add.html', form=form)

@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)

### --- MAIN --- ###

if __name__ == '__main__':
    app.run(debug=True)
