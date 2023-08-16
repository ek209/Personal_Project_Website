import os
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('PERSON_SITE_SECRET_KEY')
Bootstrap5(app)

@app.route('/')
def get_all_posts():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)