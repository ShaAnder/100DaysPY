### --- IMPORTS --- ###

from flask import Flask, render_template

#### --- APP SETUP --- ###

app = Flask(__name__)

### --- FUNCS --- ###

@app.route('/')
def home():
    return render_template('index.html')

### --- MAIN --- ###

if __name__ == "__main__":
    app.run(debug=True)