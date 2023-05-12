from flask import Blueprint, render_template

auth = Blueprint("auth", __name__)



@auth.route("/signup")
def signup():
    return "<h1>SignUp</h1>"

    


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        dob = request.form['dob']
        country = request.form['country']
        gender = request.form['gender']

        # Validate password length
        if len(password) < 8:
            return "Password must be at least 8 characters long"

        # Validate year of birth
        current_year = datetime.datetime.now().year
        dob_year = int(dob.split('-')[0])
        if dob_year > current_year or dob_year < (current_year - 100) or dob_year > 2022:
            return "Invalid year of birth"

        # # Create user account
        # user = User(first_name=first_name, last_name=last_name, email=email, password=password, dob=dob, country=country, gender=gender)
        # db.session.add(user)
        # db.session.commit()

        # Send email confirmation
        # ...

        return "User account created successfully"

    return render_template('signup.html')