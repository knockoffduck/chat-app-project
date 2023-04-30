from application import app
from flask import render_template, request, url_for

@app.route('/')
@app.route('/homepage')
def index():
    return render_template('hompage.html')
app.route('Logup')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # perform login validation here
        return redirect('/Chat')
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
        return redirect('/Chat')

    # render the signup form for GET requests
    return render_template('signup.html')
@app.route('/Chat')
def submit():
    message = request.form.get("message")
    return render_template("chat.html", message=message)

#@app.route('')
# @app.route('/button')
# def button():
#     return render_template('button.html', title = "Button")
