import os
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
import datetime
from flask_ckeditor import CKEditor
from forms import MorseForm
from morse import morse_to_english, english_to_morse

app = Flask(__name__)
ckeditor = CKEditor(app)

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

@app.route('/projects/Morse-Converter', methods=['GET', 'POST'])
def morse_converter():
    form = MorseForm()
    if form.validate_on_submit():
        if form.convert_morse.data:
            form.morse.data = english_to_morse(form.english.data)
        elif form.convert_english.data:
            form.english.data = morse_to_english(form.morse.data)
    else:
        form.morse.data = "Enter morse here..."
        form.english.data = "Enter english here..."
    github_proj_link = 'Text_To_Morse'
    return render_template('project-page.html', form=form, github_link=github_proj_link)

@app.route('/projects/tic_tac_toe')
def tic_tac_toe():
    return render_template("project-page.html")

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

@app.route('/redirect/github/<github>')
def gh_rep_redirect(github):
    return redirect(f'http://www.github.com/ek209/{github}')

if __name__ == "__main__":
    app.run(debug=True, port=5000)