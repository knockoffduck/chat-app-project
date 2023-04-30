from application import app
from flask import render_template, request, url_for, redirect

@app.route('/')
@app.route('/homepage')
def index():
    return render_template('homepage.html')

@app.route('/login')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # perform login validation here
        return redirect('/chat')
    else:
        return render_template('login.html')
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # retrieve form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        country = request.form['country']

        # do any validation or processing here

        # redirect to a new page after successful signup
        return redirect('/chat')

    # render the signup form for GET requests
    return render_template('signup.html')

@app.route('/chat')
def submit():
    # if request.method == 'POST':
    #     message = request.form.get("message")
    #     return render_template("chat.html", message=message)
    # else:
    return render_template("chat.html")
