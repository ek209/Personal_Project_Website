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
    return render_template('projects.html')

@app.route('/redirect/linkedin')
def linkedin_redirect():
    my_linkedin = 'https://www.linkedin.com/in/erik-kjell-649875208/'
    return redirect(my_linkedin)

@app.route('/redirect/github')
def github_redirect():
    my_github = 'https://github.com/ek209'
    return redirect(my_github)

@app.route('/redirect/indeed')
def indeed_redirect():
    my_indeed = ''
    return redirect(my_indeed)

if __name__ == "__main__":
    app.run(debug=True, port=5000)