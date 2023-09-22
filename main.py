import os
from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_bootstrap import Bootstrap5
import datetime
from flask_ckeditor import CKEditor
from forms import MorseForm, WatermarkForm
from morse import morse_to_english, english_to_morse
from watermark import Watermark
from matplotlib import image
import matplotlib
matplotlib.use('Agg')
from PIL import Image
import numpy as np
import io
import base64
from dashboard import create_dashboard
from redfin_api import redfin_api_home
import urllib

#TODO Use sql alchemy instead of psycopg2 for db connections, works but not officially supported
#TODO Clear up morse variables, gets confusing to distinguish

app = Flask(__name__)
app.register_blueprint(redfin_api_home, url_prefix='/redfin_api')
app = create_dashboard(app)
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

@app.route('/dashboard') 
def render_dashboard():
    return redirect('/rf_dashboard')

@app.route('/projects/redfin_scraper')
def redfin_scraper():
    git_hub_proj_link = 'Redfin_Scraper'
    return render_template("redfin_project.html", github=git_hub_proj_link)

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/projects/Image-Watermarker', methods=['POST', 'GET'])
def image_watermarker():
    form = WatermarkForm()
    if request.method == "POST": 
        text_list=['watermark_text', 'img_to_mark', 'font_size', 'font_name', 'add_space']
        if all([text in request.json for text in text_list]):
            img = np.array(Image.open(urllib.request.urlopen(request.json['img_to_mark'])))
            watermarker = Watermark(int(request.json['font_size']),
                            request.json['font_name'],
                            request.json['watermark_text'])
            if request.json['add_space'] == 'Yes':
                watermarker.add_space()
            new_img_arr = watermarker.make_watermark(img)
            new_img = Image.fromarray(new_img_arr.astype('uint8'))
            file_object = io.BytesIO()
            new_img.save(file_object, 'PNG')
            file_object.seek(0)
            base64img = "data:image/png;base64,"+base64.b64encode(file_object.getvalue()).decode('ascii')
            return {'watermark_img' : base64img}
        else: 
            return {'watermark_img' : ''}
    return render_template('image_watermarker.html', form=form)

@app.route('/projects/Morse-Converter', methods=['GET', 'POST'])
def morse_converter():
    form = MorseForm()
    if request.method == "POST":
        if request.json['english'] != None:
            return {"translation" : english_to_morse(request.json['english'])}
        elif request.json['morse'] != None:
            return {"translation" : morse_to_english(request.json['morse'])}
        else:
            return {} 
    else:
        form.morse.data = "Enter morse here..."
        form.english.data = "Enter english here..."
    github_proj_link = 'Text_To_Morse'
    return render_template('morse.html', form=form, github_link=github_proj_link)

@app.route('/projects/tic_tac_toe')
def tic_tac_toe():
    return render_template("WIP")

@app.route('/redirect/linkedin')
def linkedin_redirect():
    my_linkedin = 'https://www.linkedin.com/in/erik-kjell-649875208/'
    return redirect(my_linkedin)

@app.route('/redirect/github')
def github_redirect_ppw():
    my_github = 'https://github.com/ek209/Personal_Project_Website'
    return redirect(my_github)

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
    app.run()