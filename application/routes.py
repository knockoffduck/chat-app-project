from application import app
from flask import render_template, request, url_for

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

#@app.route('')
# @app.route('/button')
# def button():
#     return render_template('button.html', title = "Button")
