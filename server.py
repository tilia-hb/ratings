"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route('/movies')
def movies():
    return render_template('movies.html')

@app.route('/users')
def users():
    users = User.query.all()




@app.route('/registration',methods = ['GET'])
def registration():
    if request.form:
        return redirect('/registration-confirm')
    else:
        return render_template ('registration-form.html')

@app.route('/registration', methods = ['POST'])
def registration_confirm():

    new_email = request.form.get("email")


    #check if email in Users
    if User.query.filter_by(email=new_email).first():
        return redirect('/registration')
    else:   
        pwd = request.form.get('password')
        user = User(
                # user_id = user_id,
                email = new_email,
                password = pwd
                )
        db.session.add(user)
        db.session.commit()

        # print("user id is: ",user_id)
        print(user)
    return render_template('registration-confirm.html',
                            email=new_email)


@app.route('/login')
def login():
    print("shows the login form")
    return render_template('login.html')

@app.route('/login_confirm', methods = ['GET'])
def login_confirm():
    print("processes the login get request")
    new_email = request.args.get('email')
    pwd = request.args.get('password')

    if User.query.filter_by(email=new_email).first():
        current_user = User.query.filter_by(email=new_email).first()
        user_id = current_user.user_id
        user_pwd = current_user.password
        print("cur_user object is: ",current_user)
        print("cur_user_id is: ",user_id)
        print("cur_user password is: ",user_pwd)
        print("entered passowrd is: ", pwd)
        if user_pwd == pwd:
            session["current_user"] = user_id
            return redirect('/')
        else:
            flash("Login failed")
        return render_template('login.html')
# @app.route('/users/<user_id>')
# def user_page(user_id):
#     user_id = user.
    # return render_template('users.html', users=users)
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
