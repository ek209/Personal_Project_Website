import os
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('PERSON_SITE_SECRET_KEY')
Bootstrap5(app)


@app.context_processor
def time_processor():
    return dict(todays_date_data=datetime.date.today())

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about_me():
    return 'In progress'

@app.route('/projects')
def projects():
    return 'WIP'

if __name__ == "__main__":
    app.run(debug=True, port=5000)